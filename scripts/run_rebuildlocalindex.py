#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	scripts/run_rebuildlocalindex.py: Updates current index

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

from lw_strings import *
from lw_groups import *
from lw_file import *
from lw_storage import *
from lw_index import *
from lw_report import *
if dropbox_on:
	from lw_dropbox import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REBUILD NEW INDEX, LOAD OLD, DIFF, REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_working_path = lit_path_local # TODO read path from config

# Build new index object from file system
lit_list_full_new = lit_get_list(lit_working_path)

# Hash files in index
lit_list_full_new = lit_listpartialupdate_hashsize(lit_list_full_new, lit_working_path)

# Load old index
lit_list_full_old = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_old)

# Add Dropbox URLs to new index (fetch from Dropbox or local cache)
if dropbox_on:
	lit_list_full_new = dropbox_listpartialupdate(lit_list_full_old, lit_list_full_new)

# Store into database journal
lit_create_pickle(lit_list_full_new, lit_working_path + lit_path_subfolder_db + lit_path_pickle_new)
