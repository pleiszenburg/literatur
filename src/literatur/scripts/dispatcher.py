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

from importlib import import_module
import os
from pprint import pprint as pp

import click

from ..const import (
	KEY_FILES,
	KEY_JOURNAL,
	KEY_JSON,
	KEY_MASTER,
	KEY_MP,
	KEY_NAME,
	KEY_PATH,
	KEY_PKL,
	KEY_YAML,
	MSG_DEBUG_INREPOSITORY,
	MSG_DEBUG_NOREPOSITORY,
	MSG_DEBUG_STATUS,
	REPORT_MAX_LINES,
	STATUS_UC,
	STATUS_RM,
	STATUS_NW,
	STATUS_CH,
	STATUS_MV,
	STATUS_RW
	)
from ..repo import repository_class
pass_repository_decorator = click.make_pass_decorator(repository_class, ensure = True)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@click.group()
@click.pass_context
def script_entry(click_context):
	"""LITERATUR

	Literature management with Python, Dropbox and MediaWiki
	"""

	click_context.obj = repository_class()


@script_entry.command()
@pass_repository_decorator
def commit(repo):
	"""Record changes to the repository
	"""

	if repo.initialized_bool:
		repo.commit()
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def diff(repo):
	"""Show uncommited changes
	"""

	if repo.initialized_bool:
		__print_diff__(*(repo.diff()))
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@click.option(
	'--mode', '-m',
	type = click.Choice([KEY_JSON, KEY_MP, KEY_PKL, KEY_YAML]),
	default = KEY_JSON
	)
@click.argument(
	'filename',
	nargs = 1,
	default = ''
	)
@pass_repository_decorator
def dump(repo, mode, filename):
	"""Dump repository database
	"""

	if repo.initialized_bool:
		repo.dump(path = filename, mode = mode)
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def duplicates(repo):
	"""Find duplicate entries in repository
	"""

	if repo.initialized_bool:
		__print_duplicates__(repo.find_duplicates())
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@click.argument(
	'file',
	nargs = -1,
	type = click.Path(exists = True)
	)
@pass_repository_decorator
def file(repo, file):
	"""Get meta information on file(s)
	"""

	# TODO look for file in repo first, then generate new (temp) entry
	for filename in file:
		__print_file_metainfo__(repo.get_file_metainfo(filename))


@script_entry.command()
@click.argument(
	'branch',
	nargs = 1,
	type = click.Choice([KEY_JOURNAL, KEY_MASTER])
	)
@pass_repository_decorator
def merge(repo, branch):
	"""Merge repository changes from current to journal or journal to master
	"""

	if repo.initialized_bool:
		repo.merge(branch)
	else:
		print(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def init(repo):
	"""Create a literature repository
	"""

	if not repo.initialized_bool:
		repo.init()
	else:
		print(MSG_DEBUG_INREPOSITORY % repo.root_path)


@script_entry.command()
@pass_repository_decorator
def rename(repo):
	"""Launch GUI for renaming files
	"""

	guis = import_module('literatur.scripts.guis')
	guis.script_ui_filerename()


@script_entry.command()
@pass_repository_decorator
def stats(repo):
	"""Display repository statistics
	"""

	if repo.initialized_bool:
		__print_stats__(repo.get_stats())
	else:
		print(MSG_DEBUG_NOREPOSITORY)


def __print_diff__(uc_list, rw_list, rm_list, nw_list, ch_list, mv_list):

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_UC], uc_list),
		(MSG_DEBUG_STATUS[STATUS_RW], rw_list)
		]:
		if len(rp_list) > 0:
			print('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_NW], nw_list),
		(MSG_DEBUG_STATUS[STATUS_RM], rm_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				print('%s: "%s"' % (rp_message, os.path.join(entry.p_dict[KEY_PATH], entry.p_dict[KEY_NAME])))
		else:
			print('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_MV], mv_list),
		(MSG_DEBUG_STATUS[STATUS_CH], ch_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				for rp_line in entry.report:
					print(rp_line)
		else:
			print('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))


def __print_duplicates__(duplicates_list):

	pp(duplicates_list)


def __print_file_metainfo__(metainfo_dict):

	pp(metainfo_dict)


def __print_stats__(stats_dict):

	for key in stats_dict.keys():
		print(key)
		pp(stats_dict[key])
