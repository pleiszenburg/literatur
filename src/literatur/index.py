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

from .core.strings import (
	dropbox_on, # TODO move into config
	PATH_ROOT, # TODO move into config
	PATH_SUB_DB,
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
	)
from .core.groups import lit_book_ids
from .core.commit import (
	commit_backup,
	commit_push
	)
from .core.file import (
	lit_get_list,
	lit_listpartialupdate_hashsize
	)
from .core.index import lit_diff_lists
from .core.report import report_mail_newfiles
from .core.storage import (
	lit_create_pickle,
	lit_read_pickle,
	lit_write_plaintext,
	lit_write_pprint
	)

if dropbox_on:
	from .core.dropbox import (
		dropbox_listfullupdate,
		dropbox_listpartialupdate
		)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT TO DB
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def check_sanity():

	list_full = lit_get_list(PATH_ROOT)


def commit_journal():

	commit_backup(FILE_DB_JOURNAL, PATH_ROOT)

	commit_push(FILE_DB_CURRENT, FILE_DB_JOURNAL, PATH_ROOT)


def commit_master():

	commit_backup(FILE_DB_MASTER, PATH_ROOT)

	commit_push(FILE_DB_JOURNAL, FILE_DB_MASTER, PATH_ROOT)


def build_index():

	# Build index object from file system
	list_full = lit_get_list(PATH_ROOT)

	# Hash files in index
	list_full = lit_listpartialupdate_hashsize(list_full, PATH_ROOT)

	# Get dropbox links to files (else: url fields simply remain empty)
	if dropbox_on:
		list_full = dropbox_listfullupdate(list_full)

	# Store into commited database
	lit_create_pickle(
		list_full,
		os.path.join(PATH_ROOT, PATH_SUB_DB, FILE_DB_CURRENT)
		)


def dump_index():

	# Load all index stages and dump them into plain text
	for stage_file in [
		FILE_DB_CURRENT,
		FILE_DB_JOURNAL,
		FILE_DB_MASTER
		]:

		try:
			list_full = lit_read_pickle(os.path.join(PATH_ROOT, PATH_SUB_DB, stage_file))
			lit_write_pprint(
				list_full,
				os.path.join(PATH_ROOT, PATH_SUB_DB, stage_file + '.txt')
				)
		except:
			pass


def rebuild_index():

	# Build new index object from file system
	list_full_new = lit_get_list(PATH_ROOT)

	# Hash files in index
	list_full_new = lit_listpartialupdate_hashsize(list_full_new, PATH_ROOT)

	# Load old index
	list_full_old = lit_read_pickle(os.path.join(PATH_ROOT, PATH_SUB_DB, FILE_DB_CURRENT))

	# Add Dropbox URLs to new index (fetch from Dropbox or local cache)
	if dropbox_on:
		list_full_new = dropbox_listpartialupdate(list_full_old, list_full_new)

	# Store into database journal
	lit_create_pickle(
		list_full_new,
		os.path.join(PATH_ROOT, PATH_SUB_DB, FILE_DB_CURRENT)
		)


def report():

	list_full_dict = {}

	# Load all stages
	for stage_key, stage_file in [
		(KEY_CURRENT, FILE_DB_CURRENT),
		(KEY_JOURNAL, FILE_DB_JOURNAL),
		(KEY_MASTER, FILE_DB_MASTER)
		]:

		try:
			list_full = lit_read_pickle(os.path.join(PATH_ROOT, PATH_SUB_DB, stage_file))
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
				os.path.join(PATH_ROOT, PATH_SUB_DB, stage_file_old + '.diff_' + status_key + '.txt')
				)

		lit_write_plaintext(
			report_mail_newfiles(diff_dict[KEY_NEW]),
			os.path.join(PATH_ROOT, PATH_SUB_DB, stage_file_old + '.mail_' + status_key + '.txt')
			)
