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
from pprint import pprint as pp

import magic

from .repo import __get_recursive_filepathtuple_list__ as get_recursive_filepathtuple_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def print_stats():

	filepathtuple_list = get_recursive_filepathtuple_list('.')
	file_path_list = [os.path.join(*item) for item in filepathtuple_list]

	num_cores = multiprocessing.cpu_count()

	magic_list = Parallel(n_jobs = num_cores)(delayed(magic.from_file)(item) for item in file_path_list)
	mime_list = Parallel(n_jobs = num_cores)(delayed(magic.from_file)(item, mime = True) for item in file_path_list)

	magic_dict = Counter(magic_list)
	mime_dict = Counter(mime_list)

	pp(OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])))
	pp(OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1])))
