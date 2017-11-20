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

from collections import (
	Counter,
	OrderedDict
	)
import json
import os
import pickle
from pprint import pprint as pp
import shutil

import msgpack

from ..const import (
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	IGNORE_DIR_LIST,
	IGNORE_FILE_LIST,
	KEY_EXISTS_BOOL,
	KEY_FILE,
	KEY_INODE,
	KEY_JSON,
	KEY_JOURNAL,
	KEY_MAGIC,
	KEY_MASTER,
	KEY_META,
	KEY_MIME,
	KEY_MODE,
	KEY_MP,
	KEY_MTIME,
	KEY_NAME,
	KEY_PATH,
	KEY_PKL,
	KEY_SIZE,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS
	)
from ..entry import (
	compare_entry_lists,
	entry_class,
	find_duplicates_in_entry_list
	)
from ..parallel import run_routines_on_objects_in_parallel_and_return
from ..parser import ctime_to_datestring


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class repository_class():


	def __init__(self):

		# Set defauls
		self.current_relative_path = ''
		self.root_path = ''
		self.initialized_bool = False
		self.index_list = []
		self.index_loaded_bool = False

		self.current_path = os.getcwd()

		try:
			self.root_path = self.__find_root_path__(self.current_path)
			self.initialized_bool = True
		except: # TODO only on special error in find_root_path
			self.root_path = self.current_path
			self.initialized_bool = False

		# Tell entry class about root_path
		entry_class.root_path = self.root_path

		self.current_relative_path = os.path.relpath(self.root_path, self.current_path)


	def commit(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()

			self.index_list = self.__update_index_and_return__()

			self.__store_index__()

		else:

			raise # TODO


	def diff(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()
			old_entries_list = self.index_list
			new_entries_light_list = self.__generate_light_index_and_return__()

			# Compare old list vs new list and return result
			return compare_entry_lists(old_entries_list, new_entries_light_list)

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

			return find_duplicates_in_entry_list(self.index_list)

		else:

			raise # TODO


	def get_file_metainfo(self, filename):

		# TODO check if it is already in DB etc ...
		# TODO move code into entry class (as type "temp entry" if it is not in repo yet)

		entry = entry_class(
			filepath_tuple = (self.current_path, filename)
			)
		for routine_name in [
			'update_file_existence',
			'update_file_info',
			'update_file_id',
			'update_file_hash',
			'update_file_magic',
			'update_file_type'
			]:
			getattr(entry, routine_name)()

		return entry


	def get_stats(self):

		if self.initialized_bool:

			if not self.index_loaded_bool:
				self.__load_index__()

			magic_list = [entry.f_dict[KEY_MAGIC] for entry in self.index_list]
			mime_list = [entry.f_dict[KEY_MIME] for entry in self.index_list]

			magic_dict = Counter(magic_list)
			mime_dict = Counter(mime_list)

			return {
				KEY_MAGIC: OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])),
				KEY_MIME: OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1]))
				}

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


	def __get_recursive_inventory_list__(self, scan_root_path, files_dict_list):

		relative_path = os.path.relpath(scan_root_path, self.root_path)

		# Scan below current working directory and generate an iterator
		for item in os.scandir(scan_root_path):

			if item.is_file():

				# Append to list of file is not ignored
				if item.name not in IGNORE_FILE_LIST:
					item_stat = item.stat()
					files_dict_list.append({
						KEY_EXISTS_BOOL: True,
						KEY_INODE: item_stat.st_ino,
						KEY_MODE: item_stat.st_mode,
						KEY_MTIME: item_stat.st_mtime_ns,
						KEY_NAME: item.name,
						KEY_PATH: relative_path,
						KEY_SIZE: item_stat.st_size
						})

			elif item.is_dir():

				# Dive deeper if directory is not ignored
				if item.name not in IGNORE_DIR_LIST:
					self.__get_recursive_inventory_list__(item.path, files_dict_list)

			elif item.is_symlink():

				print('ERROR: Symlinks not supported, %s' % item.path)

			else:

				raise # TODO


	def __generate_light_index_and_return__(self):

		# Set CWD to root
		os.chdir(self.root_path)

		# Build new index of paths and filenames
		files_dict_list = []
		self.__get_recursive_inventory_list__(self.root_path, files_dict_list)

		# Convert index into list of entries
		entries_list = [entry_class(
			file_dict = item
			) for item in files_dict_list]

		# Run index helper
		for entry in entries_list:
			entry.update_file_id()

		# Restore old CWD
		os.chdir(self.current_path)

		return entries_list


	def __load_index__(self, mode = KEY_MP, force_reload = False):

		if not self.index_loaded_bool or force_reload:

			if mode == KEY_PKL:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
				import_list = pickle.load(f)
				f.close()
				self.index_loaded_bool = True
			elif mode == KEY_MP:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'rb')
				msg_pack = f.read()
				f.close()
				import_list = msgpack.unpackb(msg_pack, encoding = 'utf-8')
				self.index_loaded_bool = True
			elif mode == KEY_JSON:
				print('load_index from JSON not supported')
				raise # TODO
			else:
				raise # TODO

			if self.index_loaded_bool:

				self.index_list = [entry_class(
					file_dict = entry_dict[KEY_FILE],
					meta_dict = entry_dict[KEY_META]
					) for entry_dict in import_list]

		else:

			raise # TODO


	def __store_index__(self, mode = KEY_MP, force_store = False):

		export_list = [{
			KEY_FILE: entry.f_dict,
			KEY_META: entry.m_dict
			} for entry in self.index_list]

		if self.index_loaded_bool or force_store:

			if mode == KEY_PKL:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
				pickle.dump(export_list, f, -1)
				f.close()
			elif mode == KEY_MP:
				msg_pack = msgpack.packb(export_list, use_bin_type = True)
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode), 'wb+')
				f.write(msg_pack)
				f.close()
			elif mode == KEY_JSON:
				f = open(os.path.join(self.root_path, PATH_REPO, PATH_SUB_REPORTS, FILE_DB_CURRENT + '.' + mode), 'w+')
				json.dump(export_list, f, indent = '\t', sort_keys = True)
				f.close()
			else:
				raise # TODO

		else:

			raise # TODO


	def __update_index_and_return__(self):

		uc_list, rw_list, _, nw_list, ch_list, mv_list = self.diff()

		# Set CWD to root
		os.chdir(self.root_path)

		# Update file information on new entries
		updated_entries_list = run_routines_on_objects_in_parallel_and_return(
			uc_list + rw_list + nw_list + ch_list + mv_list,
			['merge_file_dict']
			)

		# Restore old CWD
		os.chdir(self.current_path)

		return updated_entries_list
