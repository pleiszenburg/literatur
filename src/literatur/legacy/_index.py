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

from .legacy.strings import (
	dropbox_on, # TODO move into config
	wiki_on, # TODO move into config
	wiki_url, wiki_user, wiki_pwd, # TODO move into config
	# PATH_ROOT, # TODO move into config
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_REPORTS,
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	KEY_CURRENT,
	KEY_JOURNAL,
	KEY_MASTER,
	KEY_RM,
	KEY_NEW,
	KEY_MV,
	KEY_CHANGED,
	cnt_n,
	wiki_page_indexfull,
	wiki_page_indexbyclass,
	wiki_page_indexbyname,
	wiki_page_indexbykeyword,
	wiki_page_authorrelationship
	)
from .legacy.commit import (
	commit_backup,
	commit_push
	)
from .legacy.file import (
	lit_get_list,
	lit_listpartialupdate_hashsize
	)
from .legacy.index import (
	lit_diff_lists,
	lit_find_duplicates,
	lit_list_organize_by_name,
	lit_list_organize_by_keyword,
	lit_list_organize_by_class,
	lit_list_organize_author_relationship
	)
from .legacy.report import (
	report_debug_duplicates,
	report_mail_newfiles,
	report_wiki_full,
	report_wiki_indexbyclass,
	report_wiki_indexbyname,
	report_wiki_indexbykeyword,
	report_wiki_authorrelationship
	)
from .legacy.repository import (
	find_root_dir,
	find_root_dir_with_message,
	init_dir
	)
from .legacy.storage import (
	lit_create_pickle,
	lit_read_pickle,
	lit_write_plaintext,
	lit_write_pprint
	)
# from .legacy.timing import lw_log

if wiki_on:
	from .legacy.mediawiki import (
		wiki_login,
		wiki_get_edittoken,
		wiki_page_set_cnt,
		wiki_logout
		)
if dropbox_on:
	from .legacy.dropbox import (
		dropbox_listfullupdate,
		dropbox_listpartialupdate
		)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT TO DB
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def check_sanity():

	list_full = lit_get_list(find_root_dir_with_message())


def commit_journal():

	path_root = find_root_dir_with_message()

	commit_backup(FILE_DB_JOURNAL, path_root)

	commit_push(FILE_DB_CURRENT, FILE_DB_JOURNAL, path_root)


def commit_master():

	path_root = find_root_dir_with_message()

	commit_backup(FILE_DB_MASTER, path_root)

	commit_push(FILE_DB_JOURNAL, FILE_DB_MASTER, path_root)


def build_index():

	path_root = find_root_dir_with_message()

	# Build index object from file system
	list_full = lit_get_list(path_root)

	# Hash files in index
	list_full = lit_listpartialupdate_hashsize(list_full, path_root)

	# Get dropbox links to files (else: url fields simply remain empty)
	if dropbox_on:
		list_full = dropbox_listfullupdate(list_full)

	# Store into commited database
	lit_create_pickle(
		list_full,
		os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT)
		)


def dump_index():

	path_root = find_root_dir_with_message()

	# Load all index stages and dump them into plain text
	for stage_file in [
		FILE_DB_CURRENT,
		FILE_DB_JOURNAL,
		FILE_DB_MASTER
		]:

		try:
			list_full = lit_read_pickle(os.path.join(path_root, PATH_REPO, PATH_SUB_DB, stage_file))
			lit_write_pprint(
				list_full,
				os.path.join(path_root, PATH_REPO, PATH_SUB_REPORTS, stage_file + '.txt')
				)
		except:
			pass


def find_duplicates():

	path_root = find_root_dir_with_message()

	# Load current index
	list_full = lit_read_pickle(
		os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT)
		)

	# Find duplicates
	duplicates_key, duplicates_hash = lit_find_duplicates(list_full, path_root)

	# Generate reports
	duplicates_key_text = report_debug_duplicates(duplicates_key)
	duplicates_hash_text = report_debug_duplicates(duplicates_hash)

	# Print them on screen
	print(duplicates_key_text + cnt_n)
	print(duplicates_hash_text + cnt_n)


def init_index():

	try:
		root_dir = find_root_dir()
		print('You are already in a repository located at "%s".' % root_dir)
	except:
		init_dir()
		build_index()
		commit_journal()
		commit_master()


def rebuild_index():

	path_root = find_root_dir_with_message()

	# Build new index object from file system
	list_full_new = lit_get_list(path_root)

	# Hash files in index
	list_full_new = lit_listpartialupdate_hashsize(list_full_new, path_root)

	# Load old index
	list_full_old = lit_read_pickle(os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT))

	# Add Dropbox URLs to new index (fetch from Dropbox or local cache)
	if dropbox_on:
		list_full_new = dropbox_listpartialupdate(list_full_old, list_full_new)

	# Store into database journal
	lit_create_pickle(
		list_full_new,
		os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT)
		)


def report():

	path_root = find_root_dir_with_message()

	list_full_dict = {}

	# Load all stages
	for stage_key, stage_file in [
		(KEY_CURRENT, FILE_DB_CURRENT),
		(KEY_JOURNAL, FILE_DB_JOURNAL),
		(KEY_MASTER, FILE_DB_MASTER)
		]:

		try:
			list_full = lit_read_pickle(os.path.join(path_root, PATH_REPO, PATH_SUB_DB, stage_file))
		except:
			list_full = []

		list_full_dict[stage_key] = list_full

	# Diff the pairs
	for stage_file_old, stage_key_old, stage_key_new in [
		(FILE_DB_JOURNAL, KEY_JOURNAL, KEY_CURRENT),
		(FILE_DB_MASTER, KEY_MASTER, KEY_CURRENT)
		]:

		diff_dict = lit_diff_lists(
			list_full_dict[stage_key_old],
			list_full_dict[stage_key_new]
			)

		for status_key in [KEY_MV, KEY_RM, KEY_NEW, KEY_CHANGED]:

			lit_write_pprint(
				diff_dict[status_key],
				os.path.join(path_root, PATH_REPO, PATH_SUB_REPORTS, stage_file_old + '.diff_' + status_key + '.txt')
				)

		lit_write_plaintext(
			report_mail_newfiles(diff_dict[KEY_NEW]),
			os.path.join(path_root, PATH_REPO, PATH_SUB_REPORTS, stage_file_old + '.mail_' + KEY_NEW + '.txt')
			)


def update_wiki():

	path_root = find_root_dir_with_message()

	lit_list_full_new = lit_read_pickle(os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT))
	# lw_log('lit_list_full_new')

	# Reorganize index
	lit_list_by_name = lit_list_organize_by_name(lit_list_full_new)
	# lw_log('lit_list_organize_by_name')
	lit_list_by_keyword = lit_list_organize_by_keyword(lit_list_full_new)
	# lw_log('lit_list_organize_by_keyword')
	lit_list_by_class = lit_list_organize_by_class(lit_list_full_new)
	# lw_log('lit_list_organize_by_class')
	lit_list_author_relationship = lit_list_organize_author_relationship(lit_list_full_new)
	# lw_log('lit_list_organize_author_relationship')

	# Generate content
	cnt_index_full = report_wiki_full(lit_list_full_new)
	# lw_log('report_wiki_full')
	cnt_index_by_class = report_wiki_indexbyclass(lit_list_by_class)
	# lw_log('report_wiki_indexbyclass')
	cnt_index_by_name = report_wiki_indexbyname(lit_list_by_name)
	# lw_log('report_wiki_indexbyname')
	cnt_index_by_keyword = report_wiki_indexbykeyword(lit_list_by_keyword)
	# lw_log('report_wiki_indexbykeyword')
	cnt_author_relationship = report_wiki_authorrelationship(lit_list_author_relationship)
	# lw_log('report_wiki_authorrelationship')

	# Write content to local files
	lit_write_plaintext(
		cnt_index_full,
		os.path.join(
			path_root, PATH_REPO, PATH_SUB_REPORTS,
			'wiki_' + wiki_page_indexfull.replace(' ', '-') + '.txt'
			)
		)
	lit_write_plaintext(
		cnt_index_by_class,
		os.path.join(
			path_root, PATH_REPO, PATH_SUB_REPORTS,
			'wiki_' + wiki_page_indexbyclass.replace(' ', '-') + '.txt'
			)
		)
	lit_write_plaintext(
		cnt_index_by_name,
		os.path.join(
			path_root, PATH_REPO, PATH_SUB_REPORTS,
			'wiki_' + wiki_page_indexbyname.replace(' ', '-') + '.txt'
			)
		)
	lit_write_plaintext(
		cnt_index_by_keyword,
		os.path.join(
			path_root, PATH_REPO, PATH_SUB_REPORTS,
			'wiki_' + wiki_page_indexbykeyword.replace(' ', '-') + '.txt'
			)
		)
	lit_write_plaintext(
		cnt_author_relationship,
		os.path.join(
			path_root, PATH_REPO, PATH_SUB_REPORTS,
			'wiki_' + wiki_page_authorrelationship.replace(' ', '-') + '.txt'
			)
		)

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
