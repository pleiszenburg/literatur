# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/scripts.py: Repository management script entry points

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

from .entry import compare_entry_lists
from .index import (
	create_index_from_path,
	update_index
	)
from .storage import (
	init_repo_folders,
	find_root_dir_with_message,
	load_index,
	store_index
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def script_init():

	try:
		find_root_dir_with_message(need_to_find = False)
	except:
		sys.exit()

	# Create folders for repo meta data
	current_path = os.getcwd()

	# Init folders
	init_repo_folders(current_path)

	# Init empty database
	store_index([], current_path)


def script_diff():

	try:
		root_dir = find_root_dir_with_message(need_to_find = True)
	except:
		sys.exit()

	old_entries_list = load_index(root_dir)
	new_entries_list = create_index_from_path(root_dir)

	# Compare old list vs new list
	uc_list, rm_list, nw_list, ch_list, mv_list = compare_entry_lists(old_entries_list, new_entries_list)

	pp({
		'rm': rm_list,
		'nw': nw_list,
		'ch': ch_list,
		'uc': uc_list,
		'mv': mv_list
		})


def script_filetype():

	pass


def script_metainfo():

	pass


def script_stats():

	try:
		root_dir = find_root_dir_with_message(need_to_find = True)
	except:
		sys.exit()

	entries_list = load_index(root_dir)

	magic_list = [entry['file']['magic'] for entry in entries_list]
	mime_list = [entry['file']['mime'] for entry in entries_list]

	magic_dict = Counter(magic_list)
	mime_dict = Counter(mime_list)

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))


def script_update():

	try:
		root_dir = find_root_dir_with_message(need_to_find = True)
	except:
		sys.exit()

	updated_entries_list = update_index(root_dir)

	store_index(updated_entries_list, root_dir)
