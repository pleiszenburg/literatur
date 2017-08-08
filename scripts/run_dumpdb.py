#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *
from lw_file import *
from lw_storage import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LOAD
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_working_path = lit_path_local # TODO read path from config

# Load base index
lit_list_full_base = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_base)

# Load old index
lit_list_full_old = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_old)

# Load new index
lit_list_full_new = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_new)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DUMP IN PLAIN TEXT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_write_pprint(lit_list_full_base, lit_working_path + lit_path_subfolder_db + lit_path_pickle_base + '.txt')
lit_write_pprint(lit_list_full_old, lit_working_path + lit_path_subfolder_db + lit_path_pickle_old + '.txt')
lit_write_pprint(lit_list_full_new, lit_working_path + lit_path_subfolder_db + lit_path_pickle_new + '.txt')

