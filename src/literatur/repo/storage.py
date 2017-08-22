# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/storage.py: Store & load DB files

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

import os
import pickle
from pprint import pprint as pp

import msgpack

from ..const import (
	FILE_DB_CURRENT,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def init_repo_folders_at_root_path(root_dir):

	current_repository = os.path.join(root_dir, PATH_REPO)
	os.makedirs(current_repository)
	for fld in [PATH_SUB_DB, PATH_SUB_DBBACKUP, PATH_SUB_REPORTS]:
		os.makedirs(os.path.join(current_repository, fld))


def find_root_path():

	current_path = os.getcwd()

	# Landed directly in root?
	if os.path.isdir(os.path.join(current_path, PATH_REPO)):
		return current_path

	while True:

		# Go one up
		new_path = os.path.abspath(os.path.join(current_path, '..'))
		# Can't go futher up
		if new_path == current_path:
			break
		# Set path
		current_path = new_path

		# Check for repo folder
		if os.path.isdir(os.path.join(current_path, PATH_REPO)):
			return current_path

	# Nothing found
	raise # TODO


def find_root_path_with_message(need_to_find = True):

	if need_to_find:

		try:
			return find_root_path()
		except:
			print('You are no in a literature repository.')
			raise # TODO

	else:

		try:
			root_dir = find_root_path()
		except:
			pass
		else:
			print('You already are in an existing literature repository at "%s".' % root_dir)
			raise # TODO


def load_index_from_root_path(root_dir, mode = 'mp'):

	if mode == 'pkl':
		f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
		indexdict_list = pickle.load(f)
		f.close()
	elif mode == 'mp':
		f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
		msg_pack = f.read()
		f.close()
		indexdict_list = msgpack.unpackb(msg_pack, encoding='utf-8')
	elif mode == 'json':
		print('load_index from JSON not supported')
		raise # TODO
	else:
		raise # TODO

	return indexdict_list


def store_index_at_root_path(indexdict_list, root_dir, mode = 'mp'):

	if mode == 'pkl':
		f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
		pickle.dump(indexdict_list, f, -1)
		f.close()
	elif mode == 'mp':
		msg_pack = msgpack.packb(indexdict_list, use_bin_type = True)
		f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
		f.write(msg_pack)
		f.close()
	elif mode == 'json':
		f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_REPORTS, FILE_DB_CURRENT + '.' + mode), 'w+')
		pp(indexdict_list, stream = f)
		f.close()
	else:
		raise # TODO
