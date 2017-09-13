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

from .hash import get_file_hash

from ..const import (
	KEY_ALL,
	KEY_FILE,
	KEY_FILE_TMP,
	KEY_ID,
	KEY_INFO,
	KEY_INODE,
	KEY_HASH,
	KEY_MAGIC,
	KEY_MIME,
	KEY_MODE,
	KEY_MTIME,
	KEY_NAME,
	KEY_PATH,
	KEY_REPORT,
	KEY_SIZE,
	KEY_STATUS,
	KEY_TYPE
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
			os.path.join(entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME]),
			os.path.join(entry[KEY_FILE_TMP][KEY_PATH], entry[KEY_FILE_TMP][KEY_NAME])
			))

	elif entry_status == STATUS_RW:

		entry_report.append('Rewritten: "%s"' % (
			os.path.join(entry[KEY_FILE_TMP][KEY_PATH], entry[KEY_FILE_TMP][KEY_NAME])
			))

	elif entry_status == STATUS_CH:

		size_diff = entry[KEY_FILE_TMP][KEY_SIZE] - entry[KEY_FILE][KEY_SIZE]
		if size_diff >= 0:
			size_prefix = '+'
		else:
			size_prefix = '-'
		entry_report.append('Changed: "%s" [%s] %s ago' % (
			os.path.join(entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME]),
			size_prefix + humanize.naturalsize(abs(size_diff), gnu = True),
			humanize.naturaldelta(
				datetime.datetime.now() - datetime.datetime.fromtimestamp(entry[KEY_FILE_TMP][KEY_MTIME] / 1e9)
				)
			))

	elif entry_status in [STATUS_UC, STATUS_RM, STATUS_NW]:
		pass
	else:
		raise # TODO

	entry.update({
		KEY_STATUS: entry_status,
		KEY_REPORT: entry_report
		})


def add_id_to_entry(entry):

	entry[KEY_FILE].update({KEY_ID: get_entry_id(entry)})


def add_info_to_entry(entry):

	entry[KEY_FILE].update(get_file_info((entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME])))


def add_hash_to_entry(entry):

	entry[KEY_FILE].update({
		KEY_HASH: get_file_hash((entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME]))
		})


def add_magic_to_entry(entry):

	entry[KEY_FILE].update({
		KEY_MAGIC: get_magicinfo((entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME])),
		KEY_MIME: get_mimetype((entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME]))
		})


def add_switched_to_entry(entry, switch_list = []):

	routines_dict = {
		KEY_HASH: add_hash_to_entry,
		KEY_MAGIC: add_magic_to_entry,
		KEY_TYPE: add_type_to_entry
		}

	if KEY_ALL not in switch_list:
		keys = switch_list
	else:
		keys = list(routines_dict.keys())

	if KEY_INFO not in entry[KEY_FILE].keys():
		add_info_to_entry(entry)
	if KEY_ID not in entry[KEY_FILE].keys():
		add_id_to_entry(entry)

	for key in keys:
		if key not in entry[KEY_FILE].keys():
			routines_dict[key](entry)


def add_type_to_entry(entry):

	if KEY_MAGIC in entry[KEY_FILE].keys():
		magic_info = entry[KEY_FILE][KEY_MAGIC]
	else:
		magic_info = get_magicinfo((entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME]))

	entry[KEY_FILE].update({
		KEY_TYPE: get_literatur_type_from_magicinfo(magic_info)
		})


def compare_entry_lists(a_entry_list, b_entry_list):

	# Find unchanged files
	diff_uc_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, (KEY_ID,), STATUS_UC
		)

	# Find moved and renamed files
	diff_mv_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, (KEY_INODE, KEY_MTIME, KEY_SIZE), STATUS_MV
		)

	# Fetch missing information on b-list entries (hash, magic, mime, type)
	b_entry_list = run_in_parallel_with_return(
		partial(add_switched_to_entry, switch_list = [KEY_ALL]),
		b_entry_list,
		add_return = True
		)

	# Find files, which have likely been written to a new inode
	diff_rw_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, (KEY_HASH, KEY_NAME, KEY_PATH), STATUS_RW
		)

	# Find files, where content was changed
	diff_ch_list, a_entry_list, b_entry_list = __find_process_diff__(
		a_entry_list, b_entry_list, (KEY_NAME, KEY_PATH), STATUS_CH
		)

	# Remaining a-list was likely removed
	diff_rm_list = a_entry_list

	# Remaining b-list was likely added as new
	diff_nw_list = b_entry_list

	return diff_uc_list, diff_rw_list, diff_rm_list, diff_nw_list, diff_ch_list, diff_mv_list


def convert_filepathtuple_to_entry(filepath_tuple):

	return {
		KEY_FILE: {
			KEY_PATH: filepath_tuple[0],
			KEY_NAME: filepath_tuple[1]
			}
		}


def find_duplicates_in_entry_list(entry_list):

	entry_by_hash_dict = {}

	for entry in entry_list:
		hash_str = entry[KEY_FILE][KEY_HASH]
		if hash_str not in entry_by_hash_dict.keys():
			entry_by_hash_dict.update({hash_str: [entry]})
		else:
			entry_by_hash_dict[hash_str].append(entry)

	duplicates_dict = {}

	for hash_str in entry_by_hash_dict.keys():
		if len(entry_by_hash_dict[hash_str]) > 1:
			duplicates_dict.update({hash_str: entry_by_hash_dict[hash_str]})

	return duplicates_dict


def __find_process_diff__(a_entry_list, b_entry_list, key_tuple, status_code):

	def list_to_dict(entry_list, key_tuple):
		return {tuple(entry[KEY_FILE][key] for key in key_tuple): entry for entry in entry_list}

	def update_entry(a_entry, b_entry, status_code):
		a_entry.update({
			KEY_STATUS: status_code,
			KEY_FILE_TMP: b_entry[KEY_FILE]
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

	field_key_list = [KEY_NAME, KEY_PATH, KEY_MODE, KEY_INODE, KEY_SIZE, KEY_MTIME]
	field_value_list = [str(entry[KEY_FILE][key]) for key in field_key_list]
	field_value_str = ' '.join(field_value_list)

	hash_object = hashlib.sha256(field_value_str.encode())

	return hash_object.hexdigest()


def get_file_info(in_path_tuple):

	in_path = os.path.join(*in_path_tuple)
	stat_info = os.stat(in_path)

	return {
		KEY_MODE: stat_info.st_mode,
		KEY_INODE: stat_info.st_ino,
		KEY_SIZE: stat_info.st_size,
		KEY_MTIME: stat_info.st_mtime_ns
		}


def merge_entry_file_info(entry):

	if KEY_FILE_TMP in entry.keys():
		entry[KEY_FILE].update(entry[KEY_FILE_TMP])
	for key in [KEY_FILE_TMP, KEY_REPORT, KEY_STATUS]:
		if key in entry.keys():
			entry.pop(key)
