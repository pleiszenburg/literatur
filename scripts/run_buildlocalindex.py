#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

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
