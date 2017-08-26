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

def add_change_report_to_entry(entry, entry_status):

	entry_report = []

	if entry_status == STATUS_MV:

		entry_report.append('Moved: "%s" -> "%s"' % (
			os.path.join(entry['file']['path'], entry['file']['name']),
			os.path.join(entry['_file']['path'], entry['_file']['name'])
			))

	elif entry_status == STATUS_RW:

		entry_report.append('Rewritten: "%s"' % (
			os.path.join(entry['_file']['path'], entry['_file']['name'])
			))

	elif entry_status == STATUS_CH:

		size_diff = entry['_file']['size'] - entry['file']['size']
		if size_diff >= 0:
			size_prefix = '+'
		else:
			size_prefix = '-'
		entry_report.append('Changed: "%s" [%s] %s ago' % (
			os.path.join(entry['file']['path'], entry['file']['name']),
			size_prefix + humanize.naturalsize(abs(size_diff), gnu = True),
			humanize.naturaldelta(
				datetime.datetime.now() - datetime.datetime.fromtimestamp(entry['_file']['mtime'] / 1e9)
				)
			))

	elif entry_status in [STATUS_UC, STATUS_RM, STATUS_NW]:
		pass
	else:
		raise # TODO

	entry.update({
		'status': entry_status,
		'report': entry_report
		})


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

	# Find unchanged files
	diff_uc_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, ('id',), STATUS_UC
		)

	# Find moved and renamed files
	diff_mv_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, ('inode', 'mtime', 'size'), STATUS_MV
		)

	# Fetch missing information on b-list entries (hash, magic, mime, type)
	b_entry_list = run_in_parallel_with_return(
		partial(add_switched_to_entry, switch_list = ['all']),
		b_entry_list,
		add_return = True
		)

	# Find files, which have likely been written to a new inode
	diff_rw_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, ('hash', 'name', 'path'), STATUS_RW
		)

	# Find files, where content was changed
	diff_ch_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, ('name', 'path'), STATUS_CH
		)

	# Remaining a-list was likely removed
	diff_rm_list = a_entry_list

	# Remaining b-list was likely added as new
	diff_nw_list = b_entry_list

	return diff_uc_list, diff_rw_list, diff_rm_list, diff_nw_list, diff_ch_list, diff_mv_list


def convert_filepathtuple_to_entry(filepath_tuple):

	return {
		'file': {
			'path': filepath_tuple[0],
			'name': filepath_tuple[1]
			}
		}


def __find_process_diff__(a_entry_list, b_entry_list, key_tuple, status_code):

	def list_to_dict(entry_list, key_tuple):
		return {tuple(entry['file'][key] for key in key_tuple): entry for entry in entry_list}

	def update_entry(a_entry, b_entry, status_code):
		a_entry.update({
			'status': status_code,
			'_file': b_entry['file']
			})
		add_change_report_to_entry(a_entry, status_code)
		return a_entry

	a_entry_dict = list_to_dict(a_entry_list, key_tuple)
	b_entry_dict = list_to_dict(b_entry_list, key_tuple)

	diff_id_set = a_entry_dict.keys() & b_entry_dict.keys()

	a_entry_remaining_set = a_entry_dict.keys() - diff_id_set
	b_entry_remaining_set = b_entry_dict.keys() - diff_id_set

	diff_list = [update_entry(
		a_entry_dict[key], b_entry_dict[key], status_code
		) for key in diff_id_set]

	a_entry_list = [a_entry_dict[key] for key in a_entry_remaining_set]
	b_entry_list = [b_entry_dict[key] for key in b_entry_remaining_set]

	return diff_list, a_entry_list, b_entry_list


def get_entry_id(entry):

	field_key_list = ['name', 'path', 'mode', 'inode', 'size', 'mtime']
	field_value_list = [str(entry['file'][key]) for key in field_key_list]
	field_value_str = ' '.join(field_value_list)

	hash_object = hashlib.sha256(field_value_str.encode())

	return hash_object.hexdigest()


def merge_entry_file_info(entry):

	if '_file' in entry.keys():
		entry['file'].update(entry['_file'])
	for key in ['_file', 'report', 'status']:
		if key in entry.keys():
			entry.pop(key)
