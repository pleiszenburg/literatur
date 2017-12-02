# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/fs.py: File system indexing related stuff

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

from .storage import store_data

from ..const import (
	FILE_DAEMON_LOG,
	FILE_DB_CURRENT,
	FILE_IGNORE,
	IGNORE_FILE_TEMPLATE,
	INDEX_TYPES,
	DEFAULT_INDEX_FORMAT,
	KEY_INFO,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_LOGS,
	REPO_PATH_LIST
	)
from ..errors import (
	not_in_repo_error,
	repo_initialized_error
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def init_root_path(in_path):

	def __write_file__(file_path, file_cnt):
		f = open(file_path, 'w+')
		f.write(file_cnt)
		f.close()

	try:
		root_path = find_root_path(in_path)
		raise repo_initialized_error()
	except not_in_repo_error:
		pass

	current_repository = os.path.join(in_path, PATH_REPO)
	os.makedirs(current_repository)
	for fld in REPO_PATH_LIST:
		os.makedirs(os.path.join(current_repository, fld))

	__write_file__(
		os.path.join(in_path, PATH_REPO, FILE_IGNORE),
		IGNORE_FILE_TEMPLATE
		)
	__write_file__(
		os.path.join(in_path, PATH_REPO, PATH_SUB_LOGS, FILE_DAEMON_LOG),
		'' # TODO add meta info on repo init date/time
		)

	store_data(os.path.join(
		in_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + DEFAULT_INDEX_FORMAT
		), {index_key: [] for index_key in INDEX_TYPES}, mode = DEFAULT_INDEX_FORMAT)


def find_root_path(in_path):

	# Landed directly in root?
	if os.path.isdir(os.path.join(in_path, PATH_REPO)):
		return in_path

	while True:

		# Go one up
		new_path = os.path.abspath(os.path.join(in_path, '..'))
		# Can't go futher up
		if new_path == in_path:
			break
		# Set path
		in_path = new_path

		# Check for repo folder
		if os.path.isdir(os.path.join(in_path, PATH_REPO)):
			return in_path

	# Nothing found
	raise not_in_repo_error()


def get_file_list(in_path):
	"""Lists all files in `in_path`. Used by rename-ui only.
	TODO: Make ui use repo daemon instead ...
	"""

	out_list = []

	# List all files in folder
	ls_list = os.listdir(in_path)

	# Clean list
	for item in ls_list:
		if os.path.isfile(os.path.join(in_path, item)):
			out_list.append(item)

	# Sort them all
	out_list.sort()

	return out_list
