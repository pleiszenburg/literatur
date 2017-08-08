#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *
from lw_file import *
from lw_storage import *
from lw_index import *
from lw_report import *

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
# DIFF, REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Diff base vs new index
diff_base_rm, diff_base_new, diff_base_mv, diff_base_changed = lit_diff_lists(lit_list_full_base, lit_list_full_new)

# Diff old vs new index
diff_old_rm, diff_old_new, diff_old_mv, diff_old_changed = lit_diff_lists(lit_list_full_old, lit_list_full_new)

# Store diffs
lit_write_pprint(diff_old_rm, lit_working_path + lit_path_subfolder_db + lit_path_report_old_pprint_rm)
lit_write_pprint(diff_old_new, lit_working_path + lit_path_subfolder_db + lit_path_report_old_pprint_new)
lit_write_pprint(diff_old_mv, lit_working_path + lit_path_subfolder_db + lit_path_report_old_pprint_mv)
lit_write_pprint(diff_old_changed, lit_working_path + lit_path_subfolder_db + lit_path_report_old_pprint_changed)
lit_write_pprint(diff_base_rm, lit_working_path + lit_path_subfolder_db + lit_path_report_base_pprint_rm)
lit_write_pprint(diff_base_new, lit_working_path + lit_path_subfolder_db + lit_path_report_base_pprint_new)
lit_write_pprint(diff_base_mv, lit_working_path + lit_path_subfolder_db + lit_path_report_base_pprint_mv)
lit_write_pprint(diff_base_changed, lit_working_path + lit_path_subfolder_db + lit_path_report_base_pprint_changed)

# Generate email text with new entries
diff_old_mail_new = report_mail_newfiles(diff_old_new)
diff_base_mail_new = report_mail_newfiles(diff_base_new)

# Store mail reports
lit_write_plaintext(diff_old_mail_new, lit_working_path + lit_path_subfolder_db + lit_path_report_old_mail_new)
lit_write_plaintext(diff_base_mail_new, lit_working_path + lit_path_subfolder_db + lit_path_report_base_mail_new)

