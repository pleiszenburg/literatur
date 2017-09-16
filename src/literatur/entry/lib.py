# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/entry/lib.py: Process and analyse larger quantities of entries

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

from ..const import (
	STATUS_CH,
	STATUS_MV,
	STATUS_NW,
	STATUS_RM,
	STATUS_RW,
	STATUS_UC
	)
from ..parallel import run_routines_on_objects_in_parallel_and_return


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def compare_entry_lists(a_entry_list, b_entry_light_list):

	# Find unchanged files
	diff_uc_list, a_entry_list, b_entry_light_list = __find_process_diff__(
		a_entry_list, b_entry_light_list, (KEY_ID,), STATUS_UC
		)

	# Find moved and renamed files
	diff_mv_list, a_entry_list, b_entry_light_list = __find_process_diff__(
		a_entry_list, b_entry_light_list, (KEY_INODE, KEY_MTIME, KEY_SIZE), STATUS_MV
		)

	# Fetch missing information on b-list entries (hash, magic, mime, type)
	b_entry_list = run_routines_on_objects_in_parallel_and_return(
		b_entry_light_list,
		['update_hash', 'update_magic', 'update_type']
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
