# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/scripts/lib.py: Repository management script entry points

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

from collections import (
	Counter,
	OrderedDict
	)
import os
from pprint import pprint as pp
import sys

from ..const import REPORT_MAX_LINES
from ..repo import (
	add_switched_to_entry,
	init_repo_folders_at_root_path,
	compare_entry_lists,
	convert_filepathtuple_to_entry,
	create_index_from_path,
	find_duplicates_in_entry_list,
	find_root_path_with_message,
	load_index_from_root_path,
	merge_at_root_path,
	store_index_at_root_path,
	update_index_at_root_path
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def script_init():

	try:
		find_root_path_with_message(need_to_find = False)
	except:
		sys.exit()

	# Create folders for repo meta data
	current_path = os.getcwd()

	# Init folders
	init_repo_folders_at_root_path(current_path)

	# Init empty database
	store_index_at_root_path([], current_path)


def script_commit():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	updated_entries_list = update_index_at_root_path(root_dir)

	store_index_at_root_path(updated_entries_list, root_dir)


def script_diff():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	old_entries_list = load_index_from_root_path(root_dir)
	new_entries_list = create_index_from_path(root_dir)

	# Compare old list vs new list
	uc_list, rw_list, rm_list, nw_list, ch_list, mv_list = compare_entry_lists(old_entries_list, new_entries_list)

	for rp_message, rp_list in [
		('Unchanged', uc_list),
		('Rewritten', rw_list)
		]:
		if len(rp_list) > 0:
			print('%s: [%d files]' % (rp_message, len(rp_list)))

	for rp_message, rp_list in [
		('New', nw_list),
		('Removed', rm_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				print('%s: "%s"' % (rp_message, os.path.join(entry['file']['path'], entry['file']['name'])))
		else:
			print('%s: [%d files]' % (rp_message, len(rp_list)))

	for rp_message, rp_list in [
		('Moved', mv_list),
		('Changed', ch_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				for rp_line in entry['report']:
					print(rp_line)
		else:
			print('%s: [%d files]' % (rp_message, len(rp_list)))


def script_dump():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	entries_list = load_index_from_root_path(root_dir)

	store_index_at_root_path(entries_list, root_dir, mode = 'json')


def script_duplicates():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	entries_list = load_index_from_root_path(root_dir)

	duplicates_dict = find_duplicates_in_entry_list(entries_list)

	pp(duplicates_dict)


def script_merge(target = 'journal'):

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	merge_at_root_path(root_dir, target)


def script_metainfo(current_path, file_list):

	meta = []
	for filename in file_list:
		entry = convert_filepathtuple_to_entry((current_path, filename))
		add_switched_to_entry(entry, {'all': True})
		meta.append(entry)

	pp(meta)


def script_stats():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	entries_list = load_index_from_root_path(root_dir)

	magic_list = [entry['file']['magic'] for entry in entries_list]
	mime_list = [entry['file']['mime'] for entry in entries_list]

	magic_dict = Counter(magic_list)
	mime_dict = Counter(mime_list)

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))
