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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def entry():

	commands_dict = {
		'init': (script_init, tuple()),
		'commit': (script_commit, tuple()),
		'merge_journal': (script_merge, ('journal',)),
		'merge_master': (script_merge, ('master',)),
		'diff': (script_diff, tuple()),
		'dump': (script_dump, tuple()),
		'duplicates': (script_duplicates, tuple()),
		'meta': (script_metainfo, tuple()),
		'stats': (script_stats, tuple())
		}

	parser = argparse.ArgumentParser(
		prog = 'LITERATUR',
		description = 'Literature management with Python, Dropbox and MediaWiki'
		)
	parser.add_argument(
		dest = 'command',
		nargs = 1,
		action = 'store',
		type = str,
		choices = list(commands_dict.keys())
		)
	args = parser.parse_args()

	cmd_routine, cmd_arguments = commands_dict[args.command[0]]
	cmd_routine(*cmd_arguments)
	# TODO fix input for meta


def __get_arg_file_list__():

	ret_files = []
	ret_else = []

	for argument in sys.argv[1:]:
		if os.path.isfile(argument):
			ret_files.append(argument)
		else:
			ret_else.append(argument)

	return ret_files, ret_else
