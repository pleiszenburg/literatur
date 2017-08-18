# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/info.py: Routines related to type and meta info

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
from pprint import pprint as pp
import sys

from .filetypes import (
	get_literatur_type_from_magicinfo,
	get_magicinfo,
	filetypes
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def print_filetype():

	files, nofiles = __get_arg_file_list__()

	for nofile in nofiles:
		pp({
			'filename': nofile,
			'error': 'Not a file.'
			})

	for filename in files:
		magic_info = get_magicinfo(filename)
		type_info = get_literatur_type_from_magicinfo(magic_info)
		pp({
			'filename': filename,
			'type': type_info,
			'magic_info': magic_info
			})


def print_metainfo():

	files, nofiles = __get_arg_file_list__()

	for nofile in nofiles:
		pp({
			'filename': nofile,
			'error': 'Not a file.'
			})

	for filename in files:
		magic_info = get_magicinfo(filename)
		type_info = get_literatur_type_from_magicinfo(magic_info)
		meta_info = None
		if type_info is not None:
			meta_info = filetypes[type_info].get_meta_info(filename)
		pp({
			'filename': filename,
			'type': type_info,
			'magic_info': magic_info,
			'meta_info': meta_info
			})


def __get_arg_file_list__():

	ret_files = []
	ret_else = []

	for argument in sys.argv[1:]:
		if os.path.isfile(argument):
			ret_files.append(argument)
		else:
			ret_else.append(argument)

	return ret_files, ret_else
