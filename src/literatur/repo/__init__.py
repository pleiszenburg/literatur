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
	PATH_SUB_REPORTS
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

	# Build new index of paths and filenames
	new_filepathtuple_list = __get_recursive_filepathtuple_list__(root_dir)
	# Convert index into list of entries
	new_entries_list = [__convert_filepathtuple_to_entry__(item) for item in new_filepathtuple_list]
	# Get filesystem info for all entires
	new_entries_list = __get_entry_info_on_list__(new_entries_list)

	pp(new_entries_list)


def __convert_filepathtuple_to_entry__(filepath_tuple):

	return {
		'file': {
			'path': filepath_tuple[0],
			'name': filepath_tuple[1]
			}
		}


def __get_entry_hash_on_item__(entry):

	entry['file'].update({
		'hash': get_file_hash((entry['file']['path'], entry['file']['name']))
		})
	return entry


def __get_entry_hash_on_list__(in_entry_list):

	entry_count = len(in_entry_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_indexdict_list = list(tqdm.tqdm(p.imap(
			__get_entry_hash_on_item__, __entry_iterator__(in_entry_list)
			), total = entry_count))

	return out_indexdict_list


def __get_entry_info_on_item__(entry):

	entry['file'].update(get_file_info((entry['file']['path'], entry['file']['name'])))
	return entry


def __get_entry_info_on_list__(in_entry_list):

	entry_count = len(in_entry_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_entry_list = list(tqdm.tqdm(p.imap(
			__get_entry_info_on_item__, __entry_iterator__(in_entry_list)
			), total = entry_count))

	return out_entry_list


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


def __entry_iterator__(entries_list):

	for entry in entries_list:
		yield entry


def __load_index__(root_dir):

	f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT), 'rb')
	indexdict_list = pickle.load(f)
	f.close()

	return indexdict_list


def __store_index__(indexdict_list, root_dir):

	f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT), 'wb+')
	pickle.dump(indexdict_list, f, -1)
	f.close()
