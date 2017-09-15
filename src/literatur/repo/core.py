# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/core.py: Defines a click-compatible repository class

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
import shutil

import msgpack

from .entry import (
	add_switched_to_entry,
	compare_entry_lists,
	convert_filepathtuple_to_entry,
	find_duplicates_in_entry_list,
	merge_entry_file_info
	)
from .fs import get_recursive_filepathtuple_list

from ..const import (
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	KEY_JSON,
	KEY_JOURNAL,
	KEY_MASTER,
	KEY_MP,
	KEY_PKL,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS
	)
from ..parallel import run_in_parallel_with_return
from ..parser import ctime_to_datestring


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class repository_class():


	current_path = ''
	current_relative_path = ''
	root_path = ''
	initialized_bool = False

	index_dict_list = []
	index_loaded_bool = False


	def __init__(self):

		self.current_path = os.getcwd()

		try:
			self.root_path = self.__find_root_path__(self.current_path)
			self.initialized_bool = True
		except: # TODO only on special error in find_root_path
			self.root_path = self.current_path
			self.initialized_bool = False

		self.current_relative_path = os.path.relpath(self.root_path, self.current_path)


	def commit(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()

			self.index_dict_list = self.__update_index_and_return__()

			self.__store_index__()

		else:

			raise # TODO


	def diff(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()
			old_entries_list = self.index_dict_list
			new_entries_list = self.__generate_index_and_return__()

			# Compare old list vs new list and return result
			return compare_entry_lists(old_entries_list, new_entries_list)

		else:

			raise # TODO


	def dump(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()

			self.__store_index__(mode = KEY_JSON)

		else:

			raise # TODO


	def find_duplicates(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()

			return find_duplicates_in_entry_list(self.index_dict_list)

		else:

			raise # TODO


	def init(self):

		if not self.initialized_bool:

			current_repository = os.path.join(self.root_path, PATH_REPO)
			os.makedirs(current_repository)
			for fld in [PATH_SUB_DB, PATH_SUB_DBBACKUP, PATH_SUB_REPORTS]:
				os.makedirs(os.path.join(current_repository, fld))
			self.initialized_bool = True

			self.index_loaded_bool = True
			self.__store_index__()

		else:

			raise # TODO


	def merge(self, branch_name, mode = KEY_MP):

		if branch_name == KEY_JOURNAL:
			merge_a, merge_b = FILE_DB_CURRENT + '.' + mode, FILE_DB_JOURNAL + '.' + mode
		elif branch_name == KEY_MASTER:
			merge_a, merge_b = FILE_DB_JOURNAL + '.' + mode, FILE_DB_MASTER + '.' + mode
		else:
			raise #

		self.__backup_index_file__(merge_b)
		self.__copy_index_file__(merge_a, merge_b)


	def __copy_index_file__(self, merge_source, merge_target):

		# Get full paths
		merge_source_path = os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, merge_source)
		merge_target_path = os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, merge_target)

		# Only push if source exists
		if os.path.isfile(merge_source_path):

			# If previous merge exists, kill it
			if os.path.isfile(merge_target_path):
				os.remove(merge_target_path)

			# Copy original to target ('copyfile' will overwrite)
			shutil.copyfile(merge_source_path, merge_target_path)


	def __backup_index_file__(self, merge_source):

		# Full path of file which is going into backup
		merge_source_path = os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, merge_source)

		# Run only if there is something to backup
		if os.path.isfile(merge_source_path):

			# Get creation time of file
			ctime = os.path.getmtime(merge_source_path)

			# Form string from creation time
			ctime_string = ctime_to_datestring(ctime)

			# Create new file name with creation time
			merge_target = merge_source.replace('.', '_' + ctime_string + '.')

			# Get full path of backup target
			merge_target_path = os.path.join(self.root_path, PATH_REPO, PATH_SUB_DBBACKUP, merge_target)

			# Copy file for backup
			shutil.copyfile(merge_source_path, merge_target_path)


	def __find_root_path__(self, current_path):

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


	def __generate_index_and_return__(self):

		# Set CWD to root
		os.chdir(self.root_path)

		# Build new index of paths and filenames
		filepathtuple_list = get_recursive_filepathtuple_list(self.root_path)
		# Convert index into list of entries
		entries_dict_list = [convert_filepathtuple_to_entry(item) for item in filepathtuple_list]

		# Run index helper in parallel
		entries_dict_list = run_in_parallel_with_return(
			add_switched_to_entry,
			entries_dict_list,
			add_return = True
			)

		# Restore old CWD
		os.chdir(self.current_path)

		return entries_dict_list


	def __load_index__(self, mode = KEY_MP, force_reload = False):

		if not self.index_loaded_bool or force_reload:

			if mode == KEY_PKL:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
				self.index_dict_list = pickle.load(f)
				f.close()
				self.index_loaded_bool = True
			elif mode == KEY_MP:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
				msg_pack = f.read()
				f.close()
				self.index_dict_list = msgpack.unpackb(msg_pack, encoding = 'utf-8')
				self.index_loaded_bool = True
			elif mode == KEY_JSON:
				print('load_index from JSON not supported')
				raise # TODO
			else:
				raise # TODO

		else:

			raise # TODO


	def __store_index__(self, mode = KEY_MP, force_store = False):

		if self.index_loaded_bool or force_store:

			if mode == KEY_PKL:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
				pickle.dump(self.index_dict_list, f, -1)
				f.close()
			elif mode == KEY_MP:
				msg_pack = msgpack.packb(self.index_dict_list, use_bin_type = True)
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
				f.write(msg_pack)
				f.close()
			elif mode == KEY_JSON:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_REPORTS, FILE_DB_CURRENT + '.' + mode), 'w+')
				pp(self.index_dict_list, stream = f)
				f.close()
			else:
				raise # TODO

		else:

			raise # TODO


	def __update_index_and_return__(self):

		uc_list, rw_list, rm_list, nw_list, ch_list, mv_list = self.diff()

		# Set CWD to root
		os.chdir(self.root_path)

		# Update file information on new entries
		updated_entries_list = run_in_parallel_with_return(
			merge_entry_file_info,
			uc_list + rw_list + rm_list + nw_list + ch_list + mv_list,
			add_return = True
			)

		# Restore old CWD
		os.chdir(self.current_path)

		return updated_entries_list
