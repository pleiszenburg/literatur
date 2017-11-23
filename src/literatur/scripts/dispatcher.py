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
from pprint import pformat as pf

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
	MSG_DEBUG_CANFORCEDELETE,
	MSG_DEBUG_FILEUNKNOWN,
	MSG_DEBUG_GROUPDOESNOTEXIST,
	MSG_DEBUG_INREPOSITORY,
	MSG_DEBUG_NOREPOSITORY,
	MSG_DEBUG_STATUS,
	MSG_DEBUG_TAGDOESNOTEXIST,
	MSG_DEBUG_TAGEXISTS,
	MSG_DEBUG_TAGINUSE,
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
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def diff(repo):
	"""Show uncommited changes
	"""

	if repo.initialized_bool:
		__print_diff__(*(repo.diff()))
	else:
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@click.option(
	'--mode', '-m',
	type = click.Choice([KEY_JSON, KEY_MP, KEY_PKL, KEY_YAML]),
	default = KEY_JSON,
	help = 'Export data format, defaults to JSON if not provided'
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
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def duplicates(repo):
	"""Find duplicate entries in repository
	"""

	if repo.initialized_bool:
		__print_duplicates__(repo.find_duplicates())
	else:
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@click.argument(
	'filenames',
	nargs = -1,
	type = click.Path(exists = True)
	)
@pass_repository_decorator
def file(repo, filenames):
	"""Get meta information on file(s)
	"""

	for filename in filenames:
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
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@pass_repository_decorator
def init(repo):
	"""Create a literature repository
	"""

	if not repo.initialized_bool:
		repo.init()
	else:
		click.echo(MSG_DEBUG_INREPOSITORY % repo.root_path)


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
		click.echo(MSG_DEBUG_NOREPOSITORY)


@script_entry.command()
@click.option(
	'--untag', '-u',
	is_flag = True,
	help = 'Removes tag from target(s)'
	)
@click.option(
	'--group-target', '-g',
	nargs = 1,
	type = str,
	multiple = True,
	help = 'Defines a group as a target'
	)
@click.option(
	'--tag-target', '-t',
	nargs = 1,
	type = str,
	multiple = True,
	help = 'Defines a(nother) tag as a target'
	)
@click.argument(
	'tag',
	nargs = 1,
	type = str
	)
@click.argument(
	'filename',
	type = click.Path(exists = True),
	nargs = -1
	)
@pass_repository_decorator
def tag(repo, untag, group_target, tag_target, tag, filename):
	"""Tags files & groups or removes tags from them
	"""

	if not repo.initialized_bool:
		click.echo(MSG_DEBUG_NOREPOSITORY)
		return

	file_not_found_list, group_not_found_list, tag_not_found_list = repo.tag(
		tag,
		target_filename_list = list(filename),
		target_group_list = list(group_target),
		target_tag_list = list(tag_target),
		remove_flag = untag
		)

	for file_not_found in file_not_found_list:
		click.echo('"%s": %s' % (file_not_found, MSG_DEBUG_FILEUNKNOWN))
	for group_not_found in group_not_found_list:
		click.echo('"%s": %s' % (group_not_found, MSG_DEBUG_GROUPDOESNOTEXIST))
	for tag_not_found in tag_not_found_list:
		click.echo('"%s": %s' % (tag_not_found, MSG_DEBUG_TAGDOESNOTEXIST))


@script_entry.command()
@click.option(
	'--create', '-c',
	nargs = 1,
	type = str,
	multiple = True,
	help = 'Creates a new tag'
	)
@click.option(
	'--delete', '-d',
	nargs = 1,
	type = str,
	multiple = True,
	help = 'Deletes a tag'
	)
@click.option(
	'--force-delete', '-f',
	is_flag = True,
	help = 'Forces delete of tags in use'
	)
@click.option(
	'--ls', '-l',
	is_flag = True,
	help = 'Lists tags'
	)
@click.option(
	'--ls-used', '-u',
	is_flag = True,
	help = 'Lists used tags'
	)
@click.option(
	'--ls-unused', '-x',
	is_flag = True,
	help = 'Lists unused tags'
	)
@pass_repository_decorator
def tagm(repo, create, delete, force_delete, ls, ls_used, ls_unused):
	"""Manages tags
	"""

	if repo.initialized_bool:

		tags_donotexist_list, tags_exist_list, tags_inuse_list = repo.tags_modify(
			create_tag_names_list = list(create),
			delete_tag_names_list = list(delete),
			force_delete = force_delete
			)

		for tag_name in tags_exist_list:
			click.echo('"%s": %s' % (tag_name, MSG_DEBUG_TAGEXISTS))
		for tag_name in tags_donotexist_list:
			click.echo('"%s": %s' % (tag_name, MSG_DEBUG_TAGDOESNOTEXIST))
		for tag_name in tags_inuse_list:
			click.echo('"%s": %s (%s)' % (tag_name, MSG_DEBUG_TAGINUSE, MSG_DEBUG_CANFORCEDELETE))

		if ls or ls_used or ls_unused:
			tag_list = repo.get_tag_name_list(used_only = ls_used, unused_only = ls_unused)
			tag_list.sort()
			for tag_name in tag_list:
				click.echo(tag_name)

	else:
		click.echo(MSG_DEBUG_NOREPOSITORY)


def __print_diff__(uc_list, rw_list, rm_list, nw_list, ch_list, mv_list):

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_UC], uc_list),
		(MSG_DEBUG_STATUS[STATUS_RW], rw_list)
		]:
		if len(rp_list) > 0:
			click.echo('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_NW], nw_list),
		(MSG_DEBUG_STATUS[STATUS_RM], rm_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				click.echo('%s: "%s"' % (rp_message, os.path.join(entry.p_dict[KEY_PATH], entry.p_dict[KEY_NAME])))
		else:
			click.echo('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))

	for rp_message, rp_list in [
		(MSG_DEBUG_STATUS[STATUS_MV], mv_list),
		(MSG_DEBUG_STATUS[STATUS_CH], ch_list)
		]:
		if len(rp_list) <= REPORT_MAX_LINES:
			for entry in rp_list:
				for rp_line in entry.report:
					click.echo(rp_line)
		else:
			click.echo('%s: [%d %s]' % (rp_message, len(rp_list), KEY_FILES))


def __print_duplicates__(duplicates_list):

	click.echo(pf(duplicates_list))


def __print_file_metainfo__(metainfo_dict):

	click.echo(pf(metainfo_dict))


def __print_stats__(stats_dict):

	for key in stats_dict.keys():
		print(key)
		click.echo(pf(stats_dict[key]))
