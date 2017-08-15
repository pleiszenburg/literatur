# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/stat.py: Test routines for statistics and indexing

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

from collections import OrderedDict
import os
from pathlib import PurePath
from pprint import pprint as pp

import magic


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def print_stats():

	ignore_dir_list = [
		'.l',
		'.git'
		]
	ignore_file_list = [
		'desktop.ini',
		'.directory'
		]

	magic_dict = {}
	mime_dict = {}

	for path, dir_list, file_list in os.walk('.'):
		for filename in file_list:

			# ignore a bunch of folders
			path_list = PurePath(path).parts
			if any(item in ignore_dir_list for item in path_list):
				continue

			# ignore a bunch of files
			if filename in ignore_file_list:
				continue

			file_path = os.path.join(path, filename)

			file_magic = magic.from_file(file_path)
			file_mime = magic.from_file(file_path, mime = True)

			if file_magic in magic_dict.keys():
				magic_dict[file_magic] += 1
			else:
				magic_dict[file_magic] = 1

			if file_mime in mime_dict.keys():
				mime_dict[file_mime] += 1
			else:
				mime_dict[file_mime] = 1

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))
