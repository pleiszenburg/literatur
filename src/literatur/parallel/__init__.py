# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/parallel/__init__.py: Parallel computing routines

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

from functools import partial
import multiprocessing

import tqdm

NUM_CORES = multiprocessing.cpu_count()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def add_return_to_func(func_handle):

	return partial(__wrapper_with_return__, func_handle)


def get_optimal_chunksize(items_count):

	chunksize = int(float(items_count) / (float(NUM_CORES) * 100.0))
	if chunksize < 1:
		chunksize = 1

	return chunksize


def run_in_parallel_with_return(func_handle, parameter_list, add_return = False):

	parameter_count = len(parameter_list)

	try:
		func_name = func_handle.__name__
	except:
		func_name = 'partial(%s)' % func_handle.func.__name__
	print('Running: %s' % func_name)

	if add_return:
		func_call = add_return_to_func(func_handle)
	else:
		func_call = func_handle

	with multiprocessing.Pool(processes = NUM_CORES) as p:

		return_list = list(tqdm.tqdm(p.imap_unordered(
			func_call,
			(parameter for parameter in parameter_list),
			get_optimal_chunksize(parameter_count)
			), total = parameter_count))

	return return_list


def __wrapper_with_return__(func_handle, mutable_object, **kw):
	func_handle(mutable_object, **kw)
	return mutable_object
