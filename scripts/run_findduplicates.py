#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	scripts/run_findduplicates.py: Finds duplicates in repository

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
from lw_storage import *
from lw_index import *
from lw_report import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LOAD
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_working_path = lit_path_local # TODO read path from config

# Load new index
lit_list_full_new = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_new)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# FIND THEM
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Find duplicates
lit_duplicates_key, lit_duplicates_hash = lit_find_duplicates(lit_list_full_new, lit_working_path)

lit_duplicates_key_text = report_debug_duplicates(lit_duplicates_key)
lit_duplicates_hash_text = report_debug_duplicates(lit_duplicates_hash)

print(lit_duplicates_key_text + cnt_n)
print(lit_duplicates_hash_text + cnt_n)
