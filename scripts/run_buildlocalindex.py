#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	scripts/run_buildlocalindex.py: Builds an index

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
if dropbox_on:
	from lw_dropbox import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT TO DB
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_working_path = lit_path_local # TODO read path from config

# Build index object from file system
lit_list_full = lit_get_list(lit_working_path)

# Hash files in index
lit_list_full = lit_listpartialupdate_hashsize(lit_list_full, lit_working_path)

# Get dropbox links to files (else: url fields simply remain empty)
if dropbox_on:
	lit_list_full = dropbox_listfullupdate(lit_list_full)

# Store into commited database
lit_create_pickle(lit_list_full, lit_working_path + lit_path_subfolder_db + lit_path_pickle_old)
