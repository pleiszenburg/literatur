# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/__init__.py: Repository management

	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/literatur/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from functools import partial
import hashlib
import multiprocessing
import os
from pathlib import PurePath
import pickle
from pprint import pformat as pf
from pprint import pprint as pp
import sys

import tqdm

from ..file import (
	get_file_info,
	get_file_hash
	)
from ..const import (
	FILE_DB_CURRENT,
	IGNORE_DIR_LIST,
	IGNORE_FILE_LIST,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS,
	STATUS_UC,
	STATUS_RM,
	STATUS_NW,
	STATUS_CH,
	STATUS_MV
	)

NUM_CORES = multiprocessing.cpu_count()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def find_root_dir():

	current_path = os.getcwd()

	# Landed directly in root?
	if os.path.isdir(os.path.join(current_path, PATH_REPO)):
		return current_path

	while True:

		# Go one up
		new_path = os.path.abspath(os.path.join(current_path, '..'))
		# Can't go futher up
		if new_path == current_path:
			break
		# Set path
		current_path = new_path

		# Check for repo folder
		if os.path.isdir(os.path.join(current_path, PATH_REPO)):
			return current_path

	# Nothing found
	raise # TODO


def find_root_dir_with_message():

	try:
		return find_root_dir()
	except:
		print('You are no in a literature repository.')
		sys.exit()


def script_init():

	# Am I in existing repo?
	try:
		root_dir = find_root_dir()
		print('You already are in an existing literature repository.')
		raise # TODO
	except:
		pass

	# Create folders for repo meta data
	current_path = os.getcwd()
	current_repository = os.path.join(current_path, PATH_REPO)
	os.makedirs(current_repository)
	for fld in [PATH_SUB_DB, PATH_SUB_DBBACKUP, PATH_SUB_REPORTS]:
		os.makedirs(os.path.join(current_repository, fld))

	# Init empty database
	__store_index__([], current_path)

	# # Build initial index of paths and filenames
	# repo_filepathtuple_list = __get_recursive_filepathtuple_list__(current_path)
	#
	# # Get filesystem info for all files
	# repo_indexdict_list = __get_file_info_parallel__(repo_filepathtuple_list)
	#
	# # Hash all files
	# repo_indexdict_list = __get_file_hash_parallel__(repo_indexdict_list)
	#
	# # Store index
	# __store_index__(repo_indexdict_list, current_path)


def script_diff():

	root_dir = find_root_dir_with_message()
	old_entries_list = __load_index__(root_dir)
	os.chdir(root_dir)

	# Build new index of paths and filenames
	new_filepathtuple_list = __get_recursive_filepathtuple_list__(root_dir)
	# Convert index into list of entries
	new_entries_list = [__convert_filepathtuple_to_entry__(item) for item in new_filepathtuple_list]
	# Get filesystem info for all entires
	new_entries_list = __get_entry_info_on_list__(new_entries_list)
	# Generate ID fields
	new_entries_list = __add_id_field_on_list__(new_entries_list)

	# Compare old list vs new list
	uc_list, rm_list, nw_list, ch_list, mv_list = __compare_entry_lists__(old_entries_list, new_entries_list)

	pp({
		'rm': rm_list,
		'nw': nw_list,
		'ch': ch_list,
		'uc': uc_list,
		'mv': mv_list
		})


def __add_id_field_on_entry__(entry):

	entry.update({'id': __get_entry_id__(entry)})
	return entry


def __add_id_field_on_list__(in_entry_list):

	entry_count = len(in_entry_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_indexdict_list = list(tqdm.tqdm(p.imap_unordered(
			__add_id_field_on_entry__,
			__entry_iterator__(in_entry_list),
			__get_optimal_chunksize__(entry_count)
			), total = entry_count))

	return out_indexdict_list


def __compare_entry_lists__(a_entry_list, b_entry_list):

	def reduce_by_id_list(entry_list, id_list):
		entry_dict = {entry['file']['id']: entry for entry in entry_list}
		for entry_id in id_list:
			entry_dict.pop(entry_id)
		return [item[key] for key in entry_dict.keys()]

	def remove_none_from_list(in_list):
		return [value for value in in_list if value is not None]

	def diff_by_func(func_handle):
		# Find relevant entries
		b_entry_count = len(b_entry_list)
		func_handle_partial = partial(func_handle, a_entry_list)
		with multiprocessing.Pool(processes = NUM_CORES) as p:
			diff_list = list(tqdm.tqdm(p.imap_unordered(
				func_handle_partial,
				__entry_iterator__(b_entry_list),
				__get_optimal_chunksize__(b_entry_count)
				), total = b_entry_count))
		# Split the return tuples
		a_id_list, b_id_list, diff_list = map(list, zip(*diff_list))
		# Reduce a_entry_list and b_entry_list by removing unchanged entries
		a_entry_list = reduce_by_id_list(a_entry_list, remove_none_from_list(a_id_list))
		b_entry_list = reduce_by_id_list(b_entry_list, remove_none_from_list(b_id_list))
		# Return result
		return remove_none_from_list(diff_list)

	diff_uc_list = diff_by_func(__find_entry_unchanged_in_list__)
	diff_mv_list = diff_by_func(__find_entry_moved_in_list__)
	diff_rw_list = diff_by_func(__find_entry_rewritten_in_list__)
	diff_ch_list = diff_by_func(__find_entry_changed_in_list__)
	diff_rm_list = a_entry_list
	diff_nw_list = b_entry_list

	return diff_uc_list, diff_rm_list, diff_nw_list, diff_ch_list, (diff_mv_list + diff_rw_list)


def __convert_filepathtuple_to_entry__(filepath_tuple):

	return {
		'file': {
			'path': filepath_tuple[0],
			'name': filepath_tuple[1]
			}
		}


def __entry_iterator__(entries_list):

	for entry in entries_list:
		yield entry


def __find_entry_changed_in_list__(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = __get_entry_id__(in_entry)

	# Match all except path and hash
	match = {
		'name': [],
		'path': []
		}
	match_key_list = list(match.keys())
	in_entry_file_key_list = list(in_entry['file'].keys())
	in_entry_file = in_entry['file']

	# Iterate and find the matches
	for entry in entry_list:
		for match_key in match_key_list:
			if match_key in in_entry_file_key_list:
				if in_entry_file[match_key] == entry['file'][match_key]
					match[match_key].append(in_entry)

	# Old name, old path, file changed
	for name_entry in match['name']:
		for path_entry in match['path']:
			if name_entry['file']['id'] == path_entry['file']['id']:
				entry = name_entry
				entry.update({'status': STATUS_CH})
				entry.update({'_file': in_entry['file']})
				entry.update({'report': __get_entry_change_report__(entry)})
				return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def __find_entry_moved_in_list__(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = __get_entry_id__(in_entry)

	# Match all except path and hash
	match = {
		'inode': [],
		'size': [],
		'mtime': [],
		}
	match_key_list = list(match.keys())
	in_entry_file_key_list = list(in_entry['file'].keys())
	in_entry_file = in_entry['file']

	# Iterate and find the matches
	for entry in entry_list:
		for match_key in match_key_list:
			if match_key in in_entry_file_key_list:
				if in_entry_file[match_key] == entry['file'][match_key]
					match[match_key].append(in_entry)

	# Size, mtime and inode match, likely moved to new path or renamed
	for size_entry in match['size']:
		for mtime_entry in match['mtime']:
			for inode_entry in match['inode']:
				if size_entry['file']['id'] == mtime_entry['file']['id'] == inode_entry['file']['id']:
					entry = inode_entry
					entry.update({'status': STATUS_MV})
					entry.update({'_file': in_entry['file']})
					entry.update({'report': __get_entry_change_report__(entry)})
					return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def __find_entry_rewritten_in_list__(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = __get_entry_id__(in_entry)

	# Hash new file
	in_entry['file'].update({
		'hash': get_file_hash((in_entry['file']['path'], in_entry['file']['name']))
		})
	in_entry_hash = in_entry['file']['hash']

	# Let's look for the hash
	for entry in entry_list:
		if entry['file']['hash'] == in_entry_hash:
			entry.update({'status': STATUS_MV})
			entry.update({'_file': in_entry['file']})
			entry.update({'report': __get_entry_change_report__(entry)})
			return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def __find_entry_unchanged_in_list__(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, old entry dict
	"""

	in_entry_id = __get_entry_id__(in_entry)
	for entry in entry_list:
		if entry['file']['id'] == in_entry_id:
			entry.update({'status': STATUS_UC})
			return (in_entry_id, in_entry_id, entry)

	return (None, None, None)


def __get_entry_change_report__(entry):

	return [] # TODO


def __get_entry_hash_on_item__(entry):

	entry['file'].update({
		'hash': get_file_hash((entry['file']['path'], entry['file']['name']))
		})
	return entry


def __get_entry_hash_on_list__(in_entry_list):

	entry_count = len(in_entry_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_indexdict_list = list(tqdm.tqdm(p.imap_unordered(
			__get_entry_hash_on_item__,
			__entry_iterator__(in_entry_list),
			__get_optimal_chunksize__(entry_count)
			), total = entry_count))

	return out_indexdict_list


def __get_entry_id__(entry):

	field_key_list = ['name', 'path', 'mode', 'inode', 'size', 'mtime']
	field_value_list = [str(entry[key]) for key in field_key_list]
	field_value_str = ' '.join(field_value_list)

	hash_object = hashlib.sha256(field_value_str.encode())

	return hash_object.hexdigest()


def __get_entry_info_on_item__(entry):

	entry['file'].update(get_file_info((entry['file']['path'], entry['file']['name'])))
	return entry


def __get_entry_info_on_list__(in_entry_list):

	entry_count = len(in_entry_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_entry_list = list(tqdm.tqdm(p.imap_unordered(
			__get_entry_info_on_item__,
			__entry_iterator__(in_entry_list),
			__get_optimal_chunksize__(entry_count)
			), total = entry_count))

	return out_entry_list


def __get_optimal_chunksize__(items_count):

	chunksize = int(float(items_count) / (float(NUM_CORES) * 3.0))
	if chunksize < 1:
		chunksize = 1

	return chunksize


def __get_recursive_filepathtuple_list__(in_path):

	filepathtuple_list = []

	for path, dir_list, file_list in os.walk(in_path):
		for filename in file_list:

			# ignore a bunch of folders
			path_list = PurePath(path).parts
			if any(item in IGNORE_DIR_LIST for item in path_list):
				continue

			# ignore a bunch of files
			if filename in IGNORE_FILE_LIST:
				continue

			filepathtuple_list.append((os.path.relpath(path, in_path), filename))

	return filepathtuple_list


def __load_index__(root_dir):

	f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT), 'rb')
	indexdict_list = pickle.load(f)
	f.close()

	return indexdict_list


def __store_index__(indexdict_list, root_dir):

	f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT), 'wb+')
	pickle.dump(indexdict_list, f, -1)
	f.close()
