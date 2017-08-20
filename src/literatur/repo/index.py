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

import os

from .entry import (
	add_id_field_on_list,
	convert_filepathtuple_to_entry,
	get_entry_hash_on_list,
	get_entry_info_on_list
	)
from .fs import get_recursive_filepathtuple_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def create_index_from_path(root_dir, hash_files = False):

	# Store current CWD
	old_cwd = os.getcwd()
	# Set CWD to root
	os.chdir(root_dir)

	# Build new index of paths and filenames
	filepathtuple_list = get_recursive_filepathtuple_list(root_dir)
	# Convert index into list of entries
	entries_list = [convert_filepathtuple_to_entry(item) for item in filepathtuple_list]
	# Get filesystem info for all entires
	entries_list = get_entry_info_on_list(entries_list)
	# Generate ID fields
	entries_list = add_id_field_on_list(entries_list)

	# Hash files (optional)
	if hash_files:
		entries_list = get_entry_hash_on_list(entries_list)

	# Restore old CWD
	os.chdir(old_cwd)

	return entries_list
