# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/__init__.py: Repository management

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

import multiprocessing
import os
from pathlib import PurePath
import pickle
from pprint import pformat as pf
import sys

import tqdm

from ..file import (
	get_file_info,
	get_file_hash
	)
from ..const import (
	FILE_DB_CURRENT,
	IGNORE_DIR_LIST,
	IGNORE_FILE_LIST,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS
	)

NUM_CORES = multiprocessing.cpu_count()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def find_root_dir():

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


def find_root_dir_with_message():

	try:
		return find_root_dir()
	except:
		print('You are no in a literature repository.')
		sys.exit()


def script_init():

	# Am I in existing repo?
	try:
		root_dir = find_root_dir()
		print('You already are in an existing literature repository.')
		raise # TODO
	except:
		pass

	# Create folders for repo meta data
	current_path = os.getcwd()
	current_repository = os.path.join(current_path, PATH_REPO)
	os.makedirs(current_repository)
	for fld in [PATH_SUB_DB, PATH_SUB_DBBACKUP, PATH_SUB_REPORTS]:
		os.makedirs(os.path.join(current_repository, fld))

	# Init empty database
	__store_index__([], current_path)

	# Build initial index of paths and filenames
	repo_filepathtuple_list = __get_recursive_filepathtuple_list__(current_path)

	# Get filesystem info for all files
	repo_indexdict_list = __get_file_info_parallel__(repo_filepathtuple_list)

	# Hash all files
	repo_indexdict_list = __get_file_hash_parallel__(repo_indexdict_list)

	# Store index
	__store_index__(repo_indexdict_list, current_path)


def script_diff():

	pass


def __add_hash_to_file_dict__(file_dict):

	file_dict['hash'] = get_file_hash((file_dict['path'], file_dict['filename']))
	return file_dict


def __get_file_hash_parallel__(in_indexdict_list):

	file_count = len(in_indexdict_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		out_indexdict_list = list(tqdm.tqdm(p.imap(__add_hash_to_file_dict__, in_indexdict_list), total = file_count))

	return out_indexdict_list


def __get_file_info_parallel__(filepathtuple_list):

	file_count = len(filepathtuple_list)

	with multiprocessing.Pool(processes = NUM_CORES) as p:
		indexdict_list = list(tqdm.tqdm(p.imap(get_file_info, filepathtuple_list), total = file_count))

	return indexdict_list


def __get_recursive_filepathtuple_list__(in_path):

	filepathtuple_list = []

	for path, dir_list, file_list in os.walk(in_path):
		for filename in file_list:

			# ignore a bunch of folders
			path_list = PurePath(path).parts
			if any(item in IGNORE_DIR_LIST for item in path_list):
				continue

			# ignore a bunch of files
			if filename in IGNORE_FILE_LIST:
				continue

			filepathtuple_list.append((os.path.relpath(path, in_path), filename))

	return filepathtuple_list


def __store_index__(indexdict_list, root_dir):

	f = open(os.path.join(root_dir, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT), 'wb+')
	pickle.dump(indexdict_list, f, -1)
	f.close()
