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

from ..const import (
	KEY_ALL,
	KEY_FILE,
	KEY_JOURNAL,
	KEY_MAGIC,
	KEY_MIME,
	KEY_NAME,
	KEY_PATH,
	REPORT_MAX_LINES
	)
from ..repo import (
	add_switched_to_entry,
	# init_repo_folders_at_root_path,
	compare_entry_lists,
	convert_filepathtuple_to_entry,
	create_index_from_path,
	find_duplicates_in_entry_list,
	find_root_path_with_message,
	# load_index_from_root_path,
	merge_at_root_path,
	# store_index_at_root_path,
	update_index_at_root_path
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def script_merge(target = KEY_JOURNAL):

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	merge_at_root_path(root_dir, target)


def script_metainfo(current_path, file_list):

	meta = []
	for filename in file_list:
		entry = convert_filepathtuple_to_entry((current_path, filename))
		add_switched_to_entry(entry, {KEY_ALL: True})
		meta.append(entry)

	pp(meta)


def script_stats():

	try:
		root_dir = find_root_path_with_message(need_to_find = True)
	except:
		sys.exit()

	entries_list = load_index_from_root_path(root_dir)

	magic_list = [entry[KEY_FILE][KEY_MAGIC] for entry in entries_list]
	mime_list = [entry[KEY_FILE][KEY_MIME] for entry in entries_list]

	magic_dict = Counter(magic_list)
	mime_dict = Counter(mime_list)

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))
