# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/filetypes/__loader__.py: loades available filetype plugins

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

from importlib import import_module
import os


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LOADER ROUTINE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_file_types():

	plugin_name_list = __get_list_of_available_types__()
	plugin_dict = {}

	for item in plugin_name_list:
		module = import_module('literatur.filetypes.' + item)
		plugin_dict[item] = module.file_type

	return plugin_dict


def __get_list_of_available_types__():

	ls_list = os.path.dirname(os.path.realpath(__file__))
	candidate_list = os.listdir(ls_list)

	plugin_list = []
	for item in candidate_list:
		if not item.startswith('_') and not item.startswith('.') and item[-3:] == '.py':
			plugin_list.append(item[:-3])

	return plugin_list
