# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/scripts/dispatcher.py: Interpreting commands

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
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import argparse
import os
from pprint import pprint as pp
import sys # TODO remove?

import click

from .guis import script_ui_filerename
# from .lib import (
# 	#script_init,
# 	#script_commit,
# 	script_merge,
# 	#script_diff,
# 	script_dump,
# 	script_duplicates,
# 	script_metainfo,
# 	script_stats
# 	)

from ..const import (
	KEY_FILE,
	KEY_JOURNAL,
	KEY_MASTER,
	KEY_NAME,
	KEY_PATH,
	KEY_REPORT,
	MSG_DEBUG_INREPOSITORY,
	MSG_DEBUG_NOREPOSITORY,
	REPORT_MAX_LINES
	)
from ..repo import repository_class
pass_repository_decorator = click.make_pass_decorator(repository_class, ensure = True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@click.group()
@click.pass_context
def entry(click_context):
	"""LITERATUR

	Literature management with Python, Dropbox and MediaWiki
	"""

	click_context.obj = repository_class()


@entry.command()
@pass_repository_decorator
def commit(repo):
	"""Record changes to the repository
	"""

	if repo.initialized_bool:
		repo.commit()
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@entry.command()
@pass_repository_decorator
def diff(repo):
	"""Show uncommited changes
	"""

	if repo.initialized_bool:
		__print_diff__(*(repo.diff()))
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@entry.command()
@pass_repository_decorator
def dump(repo):
	"""Dump repository database
	"""

	if repo.initialized_bool:
		repo.dump()
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@entry.command()
@pass_repository_decorator
def duplicates(repo):
	"""Find duplicate entries in repository
	"""

	if repo.initialized_bool:
		__print_duplicates__(repo.find_duplicates())
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@entry.command()
@click.argument(
	'branch',
	nargs = 1,
	type = click.Choice([KEY_JOURNAL, KEY_MASTER])
	)
@pass_repository_decorator
def merge(repo, branch):
	"""Dumps repository database
	"""

	if repo.initialized_bool:
		repo.merge(branch)
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@entry.command()
@pass_repository_decorator
def init(repo):
	"""Create a literature repository
	"""

	if not repo.initialized_bool:
		repo.init()
	else:
		print(MSG_DEBUG_INREPOSITORY % repo.root_path)


# 	commands_dict = {
## 		'init': (script_init, tuple()),
## 		'commit': (script_commit, tuple()),
## 		'merge_journal': (script_merge, ('journal',)),
## 		'merge_master': (script_merge, ('master',)),
## 		'diff': (script_diff, tuple()),
## 		'dump': (script_dump, tuple()),
## 		'duplicates': (script_duplicates, tuple()),
# 		'meta': (script_metainfo, tuple()),
# 		'stats': (script_stats, tuple()),
# 		'rename': (script_ui_filerename, (sys.argv,))
# 		}
#
#
# def __get_arg_file_list__():
#
# 	ret_files = []
# 	ret_else = []
#
# 	for argument in sys.argv[1:]:
# 		if os.path.isfile(argument):
# 			ret_files.append(argument)
# 		else:
# 			ret_else.append(argument)
#
# 	return ret_files, ret_else


def __print_diff__(uc_list, rw_list, rm_list, nw_list, ch_list, mv_list):

	for rp_message, rp_list in [
		('Unchanged', uc_list),
		('Rewritten', rw_list)
		]:
		if len(rp_list) > 0:
			print('%s: [%d files]' % (rp_message, len(rp_list)))

	for rp_message, rp_list in [
		('New', nw_list),
		('Removed', rm_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				print('%s: "%s"' % (rp_message, os.path.join(entry[KEY_FILE][KEY_PATH], entry[KEY_FILE][KEY_NAME])))
		else:
			print('%s: [%d files]' % (rp_message, len(rp_list)))

	for rp_message, rp_list in [
		('Moved', mv_list),
		('Changed', ch_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				for rp_line in entry[KEY_REPORT]:
					print(rp_line)
		else:
			print('%s: [%d files]' % (rp_message, len(rp_list)))


def __print_duplicates__(duplicates_list):

	pp(duplicates_list)
