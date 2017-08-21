# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/entry.py: Manipulating repository entries

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

import datetime
from functools import partial
import hashlib
import os
from pprint import pprint as pp

import humanize

from ..file import (
	get_file_info,
	get_file_hash
	)
from ..filetypes import (
	get_literatur_type_from_magicinfo,
	get_magicinfo,
	get_mimetype
	)
from ..const import (
	STATUS_UC,
	STATUS_RM,
	STATUS_NW,
	STATUS_CH,
	STATUS_MV,
	STATUS_RW
	)
from ..parallel import run_in_parallel_with_return


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def add_change_report_to_entry(entry):

	entry_status = entry['status']
	entry_report = []

	if entry_status == STATUS_MV:

		entry_report.append('Moved: %s to %s' % (
			os.path.join(entry['file']['path'], entry['file']['name']),
			os.path.join(entry['_file']['path'], entry['_file']['name'])
			))

	elif entry_status == STATUS_RW:

		entry_report.append('Rewritten: %s' % (
			os.path.join(entry['_file']['path'], entry['_file']['name'])
			))

	elif entry_status == STATUS_CH:

		size_diff = entry['_file']['size'] - entry['file']['size']
		if size_diff >= 0:
			size_prefix = '+'
		else:
			size_prefix = '-'
		entry_report.append('Changed: %s [%s] %s' % (
			os.path.join(entry['file']['path'], entry['file']['name']),
			size_prefix + humanize.naturalsize(abs(size_diff), gnu = True),
			humanize(
				datetime.datetime.now()
				- datetime.datetime.fromtimestamp(entry['_file']['mtime'] / 1e6)
				)
			))

	elif entry_status in [STATUS_UC, STATUS_RM, STATUS_NW]:
		pass
	else:
		raise # TODO

	entry['report'] = entry_report
	entry.pop('status')


def add_id_to_entry(entry):

	entry['file'].update({'id': get_entry_id(entry)})


def add_info_to_entry(entry):

	entry['file'].update(get_file_info((entry['file']['path'], entry['file']['name'])))


def add_hash_to_entry(entry):

	entry['file'].update({
		'hash': get_file_hash((entry['file']['path'], entry['file']['name']))
		})


def add_magic_to_entry(entry):

	entry['file'].update({
		'magic': get_magicinfo((entry['file']['path'], entry['file']['name'])),
		'mime': get_mimetype((entry['file']['path'], entry['file']['name']))
		})


def add_switched_to_entry(entry, switch_list = []):

	routines_dict = {
		'hash': add_hash_to_entry,
		'magic': add_magic_to_entry,
		'type': add_type_to_entry
		}

	if 'all' not in switch_list:
		keys = switch_list
	else:
		keys = list(routines_dict.keys())

	if 'info' not in entry['file'].keys():
		add_info_to_entry(entry)
	if 'id' not in entry['file'].keys():
		add_id_to_entry(entry)

	for key in keys:
		if key not in entry['file'].keys():
			routines_dict[key](entry)


def add_type_to_entry(entry):

	if 'magic' in entry['file'].keys():
		magic_info = entry['file']['magic']
	else:
		magic_info = get_magicinfo((entry['file']['path'], entry['file']['name']))

	entry['file'].update({
		'type': get_literatur_type_from_magicinfo(magic_info)
		})


def compare_entry_lists(a_entry_list, b_entry_list):

	def reduce_by_id_list(entry_list, id_list):
		entry_dict = {entry['file']['id']: entry for entry in entry_list}
		for entry_id in id_list:
			entry_dict.pop(entry_id)
		return [entry_dict[key] for key in entry_dict.keys()]

	def remove_none_from_list(in_list):
		return [value for value in in_list if value is not None]

	def diff_by_func(func_handle, tmp_a_entry_list, tmp_b_entry_list):
		# Find relevant entries
		diff_list = run_in_parallel_with_return(
			partial(func_handle, tmp_a_entry_list),
			tmp_b_entry_list
			)
		# Split the return tuples
		if len(diff_list) > 0:
			a_id_list, b_id_list, diff_list = map(list, zip(*diff_list))
		else:
			a_id_list, b_id_list, diff_list = [], [], []
		# Return result
		return (
			remove_none_from_list(diff_list),
			reduce_by_id_list(tmp_a_entry_list, remove_none_from_list(a_id_list)),
			reduce_by_id_list(tmp_b_entry_list, remove_none_from_list(b_id_list))
			)

	# Find unchanged files
	diff_uc_list, a_entry_list, b_entry_list = find_entry_unchanged_in_list(
		a_entry_list, b_entry_list
		)

	# Find moved and renamed files
	diff_mv_list, a_entry_list, b_entry_list = diff_by_func(
		find_entry_moved_in_list, a_entry_list, b_entry_list
		)

	# Fetch missing information on b-list entries (hash, magic, mime, type)
	b_entry_list = run_in_parallel_with_return(
		partial(add_switched_to_entry, switch_list = ['all']),
		b_entry_list,
		add_return = True
		)

	# Find files, which have likely been written to a new inode
	diff_rw_list, a_entry_list, b_entry_list = diff_by_func(
		find_entry_rewritten_in_list, a_entry_list, b_entry_list
		)

	# Find files, where content was changed
	diff_ch_list, a_entry_list, b_entry_list = diff_by_func(
		find_entry_changed_in_list, a_entry_list, b_entry_list
		)

	# Remaining a-list was likely removed
	diff_rm_list = a_entry_list

	# Remaining b-list was likely added as new
	diff_nw_list = b_entry_list

	return diff_uc_list, diff_rm_list, diff_nw_list, diff_ch_list, (diff_mv_list + diff_rw_list)


def convert_filepathtuple_to_entry(filepath_tuple):

	return {
		'file': {
			'path': filepath_tuple[0],
			'name': filepath_tuple[1]
			}
		}


def find_entry_changed_in_list(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = in_entry['file']['id']

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
				if in_entry_file[match_key] == entry['file'][match_key]:
					match[match_key].append(entry)

	# Old name, old path, file changed
	for name_entry in match['name']:
		for path_entry in match['path']:
			if name_entry['file']['id'] == path_entry['file']['id']:
				entry = name_entry
				entry.update({
					'status': STATUS_CH,
					'_file': in_entry['file']
					})
				add_change_report_to_entry(entry)
				return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def find_entry_moved_in_list(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be missing hashes!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = in_entry['file']['id']

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
				if in_entry_file[match_key] == entry['file'][match_key]:
					match[match_key].append(entry)

	# Size, mtime and inode match, likely moved to new path or renamed
	for size_entry in match['size']:
		for mtime_entry in match['mtime']:
			for inode_entry in match['inode']:
				if size_entry['file']['id'] == mtime_entry['file']['id'] == inode_entry['file']['id']:
					entry = inode_entry
					entry.update({
						'status': STATUS_MV,
						'_file': in_entry['file']
						})
					add_change_report_to_entry(entry)
					return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def find_entry_rewritten_in_list(entry_list, in_entry):
	"""
	`entry_list` is expected to be hashed!
	`in_entry` is expected to be hashed!
	Returns tuple: id of old entry, id of new entry, entry dict with report
	"""

	in_entry_id = in_entry['file']['id']
	in_entry_hash = in_entry['file']['hash']

	# Let's look for the hash
	for entry in entry_list:
		if entry['file']['hash'] == in_entry_hash:
			entry.update({
				'status': STATUS_RW,
				'_file': in_entry['file']
				})
			add_change_report_to_entry(entry)
			return (entry['file']['id'], in_entry_id, entry)

	return (None, None, None)


def find_entry_unchanged_in_list(a_entry_list, b_entry_list):

	a_entry_dict = {entry['file']['id']: entry for entry in a_entry_list}
	b_entry_dict = {entry['file']['id']: entry for entry in b_entry_list}
	unchange_id_set = a_entry_dict.keys() & b_entry_dict.keys()
	a_entry_remaining_set = a_entry_dict.keys() - unchange_id_set
	b_entry_remaining_set = b_entry_dict.keys() - unchange_id_set
	diff_uc_list = [a_entry_dict[key] for key in unchange_id_set]
	a_entry_list = [a_entry_dict[key] for key in a_entry_remaining_set]
	b_entry_list = [b_entry_dict[key] for key in b_entry_remaining_set]

	return diff_uc_list, a_entry_list, b_entry_list


def get_entry_id(entry):

	field_key_list = ['name', 'path', 'mode', 'inode', 'size', 'mtime']
	field_value_list = [str(entry['file'][key]) for key in field_key_list]
	field_value_str = ' '.join(field_value_list)

	hash_object = hashlib.sha256(field_value_str.encode())

	return hash_object.hexdigest()


def merge_entry_file_info(entry):

	new_file = entry['_file']
	old_file = entry['file']

	for key in new_file.keys():
		old_file[key] = new_file[key]

	entry.pop('_file')
