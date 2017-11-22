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
import yaml

from ..const import (
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	IGNORE_DIR_LIST,
	IGNORE_FILE_LIST,
	INDEX_TYPES,
	KEY_EXISTS_BOOL,
	KEY_FILE,
	KEY_FILES,
	KEY_GROUPS,
	KEY_ID,
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
	KEY_TAGS,
	KEY_YAML,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP,
	PATH_SUB_REPORTS
	)
from ..entry import (
	compare_entry_lists,
	find_duplicates_in_entry_list,
	generate_entry
	)
from ..parallel import run_routines_on_objects_in_parallel_and_return
from ..parser import ctime_to_datestring


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ERRORS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class repoinitialized_error(Exception):
	pass


class reponotinitialized_error(Exception):
	pass


class tagdoesnotexists_error(Exception):
	pass


class tagexists_error(Exception):
	pass


class taginsuse_error(Exception):
	pass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class repository_class():


	def __init__(self):

		# Init all index related lists and dicts
		self.__init_index__()

		# Init paths and repo status
		self.__init_paths__()


	def commit(self):

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		self.__update_index_on_files__()
		self.__update_index_dicts_from_lists__(index_key_list = [KEY_FILES])
		self.__update_mirror_dicts__()

		self.__store_index__()


	def diff(self):
		""" Diff looks for files, which have been changed (changed, created, moved, deleted).
		It does not care about tags and groups.
		"""

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		old_entries_list = self.index_list_dict[KEY_FILES]
		new_entries_light_list = self.__generate_light_index_and_return__()

		# Compare old list vs new list and return result
		return compare_entry_lists(old_entries_list, new_entries_light_list)


	def dump(self, path = None, mode = KEY_JSON):

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		self.__store_index__(path = path, mode = mode) #


	def find_duplicates(self):
		""" find_duplicates looks for identical files.
		Multiples of tags and groups are not yet being looked for.
		"""

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		return find_duplicates_in_entry_list(self.index_list_dict[KEY_FILES])


	def get_file_metainfo(self, filename):

		if self.initialized_bool:

			# TODO look for changed or moved files, too (i.e. return change reports)
			# Requires index dicts by hash

			if not self.index_loaded_bool:
				self.__load_index__()

			abs_path = os.path.abspath(os.path.join(self.current_path, filename))
			if abs_path in self.filemirror_dict_byabspath.keys():
				return self.index_dict_byid_dict[KEY_FILES][self.filemirror_dict_byabspath[abs_path]]

		entry = generate_entry(
			self, filepath_tuple = (self.current_path, filename)
			)
		for routine_name in [
			'update_file_existence',
			'update_file_info',
			'update_file_hash',
			'update_file_magic',
			'update_file_type'
			]:
			getattr(entry, routine_name)()

		return entry


	def get_stats(self):

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		magic_list = [entry.p_dict[KEY_MAGIC] for entry in self.index_list_dict[KEY_FILES]]
		mime_list = [entry.p_dict[KEY_MIME] for entry in self.index_list_dict[KEY_FILES]]

		magic_dict = Counter(magic_list)
		mime_dict = Counter(mime_list)

		return {
			KEY_MAGIC: OrderedDict(sorted(magic_dict.items(), key = lambda t: t[1])),
			KEY_MIME: OrderedDict(sorted(mime_dict.items(), key = lambda t: t[1]))
			}


	def get_tag_name_list(self, used_only = False, unused_only = False):

		if not used_only and not unused_only:
			return list(self.tagmirror_dict_bytagname.keys())

		tag_name_list = []

		for tag_id in self.index_dict_byid_dict[KEY_TAGS].keys():

			tag_use = self.__is_tag_in_use__(tag_id)
			tag_name = self.index_dict_byid_dict[KEY_TAGS][tag_id].p_dict[KEY_NAME]

			if tag_use and used_only:
				tag_name_list.append(tag_name)

			if not tag_use and unused_only:
				tag_name_list.append(tag_name)

		return tag_name_list


	def init(self):

		if self.initialized_bool:
			raise repoinitialized_error()

		current_repository = os.path.join(self.root_path, PATH_REPO)
		os.makedirs(current_repository)
		for fld in [PATH_SUB_DB, PATH_SUB_DBBACKUP, PATH_SUB_REPORTS]:
			os.makedirs(os.path.join(current_repository, fld))
		self.initialized_bool = True

		self.index_loaded_bool = True
		self.__store_index__()


	def merge(self, branch_name, mode = KEY_MP):

		if branch_name == KEY_JOURNAL:
			merge_a, merge_b = FILE_DB_CURRENT + '.' + mode, FILE_DB_JOURNAL + '.' + mode
		elif branch_name == KEY_MASTER:
			merge_a, merge_b = FILE_DB_JOURNAL + '.' + mode, FILE_DB_MASTER + '.' + mode
		else:
			raise #

		self.__backup_index_file__(merge_b)
		self.__copy_index_file__(merge_a, merge_b)


	def tag(self,
		tag_name,
		target_filename_list = [], target_group_list = [], target_tag_list = [],
		remove_flag = False
		):

		pass


	def tags_modify(self, create_tag_names_list = [], delete_tag_names_list = [], force_delete = False):
		""" Creates and deletes lists of tags
		"""

		if not self.initialized_bool:
			raise reponotinitialized_error()

		if not self.index_loaded_bool:
			self.__load_index__()

		tags_donotexist_list = []
		tags_exist_list = []
		tags_inuse_list = []

		# Create path
		for tag_name in create_tag_names_list:
			try:
				self.__tag_create__(tag_name)
			except tagexists_error:
				tags_exist_list.append(tag_name)

		# Delete path
		for tag_name in delete_tag_names_list:
			try:
				self.__tag_delete__(tag_name, force_delete = force_delete)
			except tagdoesnotexists_error:
				tags_donotexist_list.append(tag_name)
			except taginsuse_error:
				tags_inuse_list.append(tag_name)

		self.__update_index_dicts_from_lists__(index_key_list = INDEX_TYPES)
		self.__update_mirror_dicts__()

		self.__store_index__()

		return tags_donotexist_list, tags_exist_list, tags_inuse_list


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
		entries_list = [generate_entry(
			self, file_dict = item
			) for item in files_dict_list]

		# Run index helper
		for entry in entries_list:
			entry.generate_id()

		# Restore old CWD
		os.chdir(self.current_path)

		return entries_list


	def __init_index__(self):

		# Index dicts by ID ({ID: entry, ...})
		self.index_dict_byid_dict = {}
		# Index dicts by tag ({TAG_ID: {ENTRY_ID: entry, ...}, ...}); tags to entries are tagged with!
		self.index_dict_bytagid_dict = {}
		# Index lists ([entry, ...])
		self.index_list_dict = {}

		# Seting up index dicts and lists ...
		for index_key in INDEX_TYPES:
			self.index_dict_byid_dict.update({index_key: {}})
			self.index_dict_bytagid_dict.update({index_key: {}})
			self.index_list_dict.update({index_key: []})

		# Mirror of tags by name {TAG_NAME: tag_entry, ...}
		self.tagmirror_dict_bytagname = {}
		# Mirror of files by ABSPATH {FULLABSPATH: file_entry, ...}
		self.filemirror_dict_byabspath = {}

		# Have index dicts been loaded?
		self.index_loaded_bool = False


	def __init_paths__(self):

		# Store CWD
		self.current_path = os.getcwd()

		# Find repo root
		try:
			self.root_path = self.__find_root_path__(self.current_path)
			self.initialized_bool = True
		except: # TODO only on special error in find_root_path
			self.root_path = self.current_path
			self.initialized_bool = False

		# Relative path between CWD and repo root
		self.current_relative_path = os.path.relpath(self.root_path, self.current_path)


	def __is_tag_in_use__(self, tag_id):

		tag_used_bool = False
		for index_type in INDEX_TYPES:
			tag_used_bool |= bool(self.index_dict_bytagid_dict[index_type][tag_id])

		return tag_used_bool


	def __load_index__(self, mode = KEY_MP, force_reload = False):

		if not self.index_loaded_bool or force_reload:

			f = open(os.path.join(
				self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode
				), 'rb')

			if mode == KEY_PKL:
				import_dict = pickle.load(f)
			elif mode == KEY_MP:
				import_dict = msgpack.unpackb(f.read(), encoding = 'utf-8')
			elif mode == KEY_JSON:
				import_dict = json.load(f)
			else:
				f.close()
				raise # TODO

			self.index_loaded_bool = True
			f.close()

			for index_key in INDEX_TYPES:
				self.index_list_dict[index_key].clear()
				self.index_list_dict[index_key] += [generate_entry(
					self, storage_dict = entry_dict
					) for entry_dict in import_dict[index_key]]
			self.__update_index_dicts_from_lists__(index_key_list = INDEX_TYPES)
			self.__update_mirror_dicts__()

		else:

			raise # TODO


	def __store_index__(self, path = None, mode = KEY_MP, force_store = False):

		export_dict = {}
		for index_key in INDEX_TYPES:
			export_dict.update({index_key: [
				entry.export_storage_dict() for entry in self.index_list_dict[index_key]
				]})

		if self.index_loaded_bool or force_store:

			if path in [None, '']:
				path = os.path.join(
					self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode
					)

			if mode == KEY_PKL:
				f = open(path, 'wb+')
				pickle.dump(export_dict, f, -1)
			elif mode == KEY_MP:
				f = open(path, 'wb+')
				msg_pack = msgpack.packb(export_dict, use_bin_type = True)
				f.write(msg_pack)
			elif mode == KEY_JSON:
				f = open(path, 'w+')
				json.dump(export_dict, f, indent = '\t', sort_keys = True)
			elif mode == KEY_YAML:
				if hasattr(yaml, 'CDumper'):
					dumper = yaml.CDumper
				else:
					dumper = yaml.Dumper
				f = open(path, 'w+')
				yaml.dump(export_dict, f, Dumper = dumper, default_flow_style = False)
			else:
				raise # TODO

			f.close()

		else:

			raise # TODO


	def __tag_create__(self, tag_name):

		# Raise an error if tag exists
		if tag_name in self.tagmirror_dict_bytagname.keys():
			raise tagexists_error()

		# Generate new tag entry
		new_tag_entry = generate_entry(self, tag_dict = {KEY_NAME: tag_name})
		# Give the tag an ID
		new_tag_entry.generate_id()
		# Append tag to list of tags
		self.index_list_dict[KEY_TAGS].append(new_tag_entry)


	def __tag_delete__(self, tag_name, force_delete = False):

		# Raise an error if the tag does not exist
		if tag_name not in self.tagmirror_dict_bytagname.keys():
			raise tagdoesnotexists_error()

		# Get tag entry
		tag_entry = self.index_dict_byid_dict[KEY_TAGS][self.tagmirror_dict_bytagname[tag_name]]
		# Get tag id
		tag_id = tag_entry.p_dict[KEY_ID]

		# Is tag in use?
		tag_used_bool = self.__is_tag_in_use__(tag_id)

		# Raise an error if the tag is in use and the delete is not forced
		if tag_used_bool and not force_delete:
			raise taginsuse_error()

		# Remove the tag from all entries if the tag is in use and delete forced
		if tag_used_bool and force_delete:
			for index_type in INDEX_TYPES:
				for entry in self.index_dict_bytagid_dict[index_type][tag_id].values():
					entry.p_dict[KEY_TAGS].pop(tag_id)

		# Actually delete tag
		tag_entry_index = self.index_list_dict[KEY_TAGS].index(tag_entry)
		del self.index_list_dict[KEY_TAGS][tag_entry_index]


	def __update_index_on_files__(self):

		uc_list, rw_list, _, nw_list, ch_list, mv_list = self.diff()

		# Set CWD to root
		os.chdir(self.root_path)

		# Update file information on new entries
		updated_entries_list = run_routines_on_objects_in_parallel_and_return(
			rw_list + ch_list + mv_list,
			['merge_p_dict']
			)

		# Clear the index
		self.index_list_dict[KEY_FILES].clear()
		# Rebuild index
		self.index_list_dict[KEY_FILES] += uc_list + nw_list + updated_entries_list

		# Restore old CWD
		os.chdir(self.current_path)


	def __update_index_dicts_from_lists__(self, index_key_list = []):

		tag_id_list = [
			tag_entry.p_dict[KEY_ID] for tag_entry in self.index_list_dict[KEY_TAGS]
			]

		for index_key in index_key_list:

			# Clear [file, group, tag] by ID index
			self.index_dict_byid_dict[index_key].clear()
			# Rebuild the index dict
			self.index_dict_byid_dict[index_key].update({
				entry.p_dict[KEY_ID]: entry for entry in self.index_list_dict[index_key]
				})

			# Clear [file, group, tag] by TAG_NAME index
			self.index_dict_bytagid_dict[index_key].clear()
			# First, generate a dict of empty dicts
			self.index_dict_bytagid_dict[index_key].update(
				{tag_id: {} for tag_id in tag_id_list}
				)
			# Build tag dicts
			for entry in self.index_list_dict[index_key]:
				for entry_tag_id in entry.p_dict[KEY_TAGS].keys():
					self.index_dict_bytagid_dict[index_key][entry_tag_id][entry.p_dict[KEY_ID]] = entry


	def __update_mirror_dicts__(self):

		self.tagmirror_dict_bytagname = {
			entry.p_dict[KEY_NAME]: entry.p_dict[KEY_ID] for entry in self.index_list_dict[KEY_TAGS]
			}
		self.filemirror_dict_byabspath = {
			os.path.abspath(os.path.join(
				self.root_path, entry.p_dict[KEY_PATH], entry.p_dict[KEY_NAME]
				)): entry.p_dict[KEY_ID] for entry in self.index_list_dict[KEY_FILES]
			}
