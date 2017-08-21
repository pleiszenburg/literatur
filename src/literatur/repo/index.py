# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/scripts.py: Repository index routines

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
import os
from pprint import pprint as pp

from .entry import (
	add_switched_to_entry,
	compare_entry_lists,
	convert_filepathtuple_to_entry,
	merge_entry_file_info
	)
from .fs import get_recursive_filepathtuple_list
from .storage import load_index
from ..parallel import (
	add_return_to_func,
	run_in_parallel_with_return
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def create_index_from_path(
	root_dir,
	switch_dict = {}
	):

	# Store current CWD
	old_cwd = os.getcwd()
	# Set CWD to root
	os.chdir(root_dir)

	# Build new index of paths and filenames
	filepathtuple_list = get_recursive_filepathtuple_list(root_dir)
	# Convert index into list of entries
	entries_list = [convert_filepathtuple_to_entry(item) for item in filepathtuple_list]

	# Run index helper in parallel
	entries_list = run_in_parallel_with_return(
		add_switched_to_entry,
		entries_list,
		add_return = True
		)

	# Restore old CWD
	os.chdir(old_cwd)

	return entries_list


def update_index(root_dir):

	# Store current CWD
	old_cwd = os.getcwd()
	# Set CWD to root
	os.chdir(root_dir)

	# Load old index
	old_entries_list = load_index(root_dir)
	# Create new index, least number of parameters
	new_entries_list = create_index_from_path(root_dir)

	# Compare old list vs new list
	uc_list, rm_list, nw_list, ch_list, mv_list = compare_entry_lists(old_entries_list, new_entries_list)

	# Run index helper in parallel
	nw_list = run_in_parallel_with_return(
		partial(add_switched_to_entry, switch_list = ['all']),
		nw_list,
		add_return = True
		)

	# Update file information on new entries
	updated_entries_list = run_in_parallel_with_return(
		merge_entry_file_info,
		ch_list + mv_list,
		add_return = True
		)

	# Restore old CWD
	os.chdir(old_cwd)

	return uc_list + nw_list + updated_entries_list
