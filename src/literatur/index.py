#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/index.py: (Re-) building the index

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
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

from .core.strings import *
from .core.groups import lit_book_ids
from .core.file import (
	lit_get_list,
	lit_listpartialupdate_hashsize
	)
from .core.storage import (
	lit_create_pickle,
	lit_read_pickle
	)

if dropbox_on:
	from .core.dropbox import (
		dropbox_listfullupdate,
		dropbox_listpartialupdate
		)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT TO DB
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def build_index():

	lit_working_path = lit_path_local # TODO read path from config

	# Build index object from file system
	lit_list_full = lit_get_list(lit_working_path)

	# Hash files in index
	lit_list_full = lit_listpartialupdate_hashsize(lit_list_full, lit_working_path)

	# Get dropbox links to files (else: url fields simply remain empty)
	if dropbox_on:
		lit_list_full = dropbox_listfullupdate(lit_list_full)

	# Store into commited database
	lit_create_pickle(lit_list_full, os.path.join(lit_working_path, lit_path_subfolder_db, lit_path_pickle_old))


def rebuild_index():

	lit_working_path = lit_path_local # TODO read path from config

	# Build new index object from file system
	lit_list_full_new = lit_get_list(lit_working_path)

	# Hash files in index
	lit_list_full_new = lit_listpartialupdate_hashsize(lit_list_full_new, lit_working_path)

	# Load old index
	lit_list_full_old = lit_read_pickle(os.path.join(lit_working_path, lit_path_subfolder_db, lit_path_pickle_old))

	# Add Dropbox URLs to new index (fetch from Dropbox or local cache)
	if dropbox_on:
		lit_list_full_new = dropbox_listpartialupdate(lit_list_full_old, lit_list_full_new)

	# Store into database journal
	lit_create_pickle(lit_list_full_new, os.path.join(lit_working_path, lit_path_subfolder_db, lit_path_pickle_new))
