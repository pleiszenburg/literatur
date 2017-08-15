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

from collections import (
	Counter,
	OrderedDict
	)
from joblib import (
	Parallel,
	delayed
	)
import multiprocessing
import os
from pathlib import PurePath
from pprint import pprint as pp

import magic


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def print_stats():

	file_path_list = __get_file_path_list__('.')

	num_cores = multiprocessing.cpu_count()

	magic_list = Parallel(n_jobs = num_cores)(delayed(magic.from_file)(item) for item in file_path_list)
	mime_list = Parallel(n_jobs = num_cores)(delayed(magic.from_file)(item, mime = True) for item in file_path_list)

	magic_dict = Counter(magic_list)
	mime_dict = Counter(mime_list)

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))


def __get_file_path_list__(working_path):

	ignore_dir_list = [
		'.l',
		'.git'
		]
	ignore_file_list = [
		'desktop.ini',
		'.directory'
		]

	file_path_list = []

	for path, dir_list, file_list in os.walk(working_path):
		for filename in file_list:

			# ignore a bunch of folders
			path_list = PurePath(path).parts
			if any(item in ignore_dir_list for item in path_list):
				continue

			# ignore a bunch of files
			if filename in ignore_file_list:
				continue

			file_path_list.append(os.path.join(path, filename))

	return file_path_list
