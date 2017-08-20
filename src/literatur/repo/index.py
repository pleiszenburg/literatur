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

from .entry import (
	convert_filepathtuple_to_entry,
	add_id_to_entry,
	add_info_to_entry,
	add_hash_to_entry,
	add_magic_to_entry,
	add_type_to_entry
	)
from .fs import get_recursive_filepathtuple_list
from ..parallel import run_in_parallel_with_return


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

	# Fill switch_dict with defaults
	for switch in ['hash', 'magic', 'type']:
		if switch not in switch_dict.keys():
			switch_dict[switch] = False

	# Prepare configured index helper
	index_parallel_helper_partial = partial(__index_parallel_helper__, switch_dict)
	# Run index helper in parallel
	entries_list = run_in_parallel_with_return(
		index_parallel_helper_partial,
		entries_list
		)

	# Restore old CWD
	os.chdir(old_cwd)

	return entries_list


def __index_parallel_helper__(
	switch_dict,
	entry
	):

	add_info_to_entry(entry)
	add_id_to_entry(entry)
	if switch_dict['hash']:
		add_hash_to_entry(entry)
	if switch_dict['magic']:
		add_magic_to_entry(entry)
	if switch_dict['type']:
		add_type_to_entry(entry)

	return entry
