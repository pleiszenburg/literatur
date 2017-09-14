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
import os # TODO remove?
import sys # TODO remove?

import click

from .guis import script_ui_filerename
from .lib import (
	script_init,
	script_commit,
	script_merge,
	script_diff,
	script_dump,
	script_duplicates,
	script_metainfo,
	script_stats
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
def diff(repo):
	"""Shows uncommited changes.
	"""

	script_diff()


# 	commands_dict = {
# 		'init': (script_init, tuple()),
# 		'commit': (script_commit, tuple()),
# 		'merge_journal': (script_merge, ('journal',)),
# 		'merge_master': (script_merge, ('master',)),
## 		'diff': (script_diff, tuple()),
# 		'dump': (script_dump, tuple()),
# 		'duplicates': (script_duplicates, tuple()),
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
