#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	scripts/run_pushwiki.py: Pushes current repository into wiki

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
if wiki_on:
	from lw_mediawiki import *

from lw_timing import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lit_working_path = lit_path_local # TODO read path from config

# Load new index
lit_list_full_new = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_new)
lw_log('lit_list_full_new')

# Reorganize index
lit_list_by_name = lit_list_organize_by_name(lit_list_full_new)
lw_log('lit_list_organize_by_name')
lit_list_by_keyword = lit_list_organize_by_keyword(lit_list_full_new)
lw_log('lit_list_organize_by_keyword')
lit_list_by_class = lit_list_organize_by_class(lit_list_full_new)
lw_log('lit_list_organize_by_class')
lit_list_author_relationship = lit_list_organize_author_relationship(lit_list_full_new)
lw_log('lit_list_organize_author_relationship')

# Generate content
cnt_index_full = report_wiki_full(lit_list_full_new)
lw_log('report_wiki_full')
cnt_index_by_class = report_wiki_indexbyclass(lit_list_by_class)
lw_log('report_wiki_indexbyclass')
cnt_index_by_name = report_wiki_indexbyname(lit_list_by_name)
lw_log('report_wiki_indexbyname')
cnt_index_by_keyword = report_wiki_indexbykeyword(lit_list_by_keyword)
lw_log('report_wiki_indexbykeyword')
cnt_author_relationship = report_wiki_authorrelationship(lit_list_author_relationship)
lw_log('report_wiki_authorrelationship')

# Write content to local files
lit_write_plaintext(cnt_index_full, lit_working_path + lit_path_subfolder_db + lit_path_report_new_wikicnt_indexfull)
lit_write_plaintext(cnt_index_by_class, lit_working_path + lit_path_subfolder_db + lit_path_report_new_wikicnt_indexbyclass)
lit_write_plaintext(cnt_index_by_name, lit_working_path + lit_path_subfolder_db + lit_path_report_new_wikicnt_indexbyname)
lit_write_plaintext(cnt_index_by_keyword, lit_working_path + lit_path_subfolder_db + lit_path_report_new_wikicnt_indexbykeyword)
lit_write_plaintext(cnt_author_relationship, lit_working_path + lit_path_subfolder_db + lit_path_report_new_wikicnt_authorrelationship)

# Wiki kill switch
if wiki_on:

	# Log into wiki and get token
	site = wiki_login(wiki_url, wiki_user, wiki_pwd)
	site_edittoken = wiki_get_edittoken(site)

	# Push content
	if True:
		wiki_page_set_cnt(site, site_edittoken, wiki_page_indexfull, cnt_index_full, '')
		wiki_page_set_cnt(site, site_edittoken, wiki_page_indexbyclass, cnt_index_by_class, '')
		wiki_page_set_cnt(site, site_edittoken, wiki_page_indexbyname, cnt_index_by_name, '')
		wiki_page_set_cnt(site, site_edittoken, wiki_page_indexbykeyword, cnt_index_by_keyword, '')
		wiki_page_set_cnt(site, site_edittoken, wiki_page_authorrelationship, cnt_author_relationship, '')

	# Log out
	wiki_logout(site)
