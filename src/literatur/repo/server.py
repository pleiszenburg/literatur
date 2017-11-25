# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/server.py: Defines a server-side repository class

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

import atexit
from collections import (
	Counter,
	OrderedDict
	)
import os
import pickle
from pprint import pprint as pp
import random
import shutil

from .storage import (
	load_data,
	store_data
	)

from ..const import (
	DEFAULT_INDEX_FORMAT,
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	ID_HASH_LENGTH,
	IGNORE_DIR_LIST,
	IGNORE_FILE_LIST,
	INDEX_TYPES,
	KEY_ADDRESS,
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
	KEY_PORT,
	KEY_PKL,
	KEY_SECRET,
	KEY_SIZE,
	KEY_TAGS,
	KEY_TERMINATE,
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
from ..errors import (
	filename_unrecognized_by_repo_error,
	not_in_repo_error,
	repo_initialized_error,
	tag_does_not_exists_error,
	tag_exists_error,
	tag_in_use_error
	)
from ..rpc import mp_server_class
from ..parallel import run_routines_on_objects_in_parallel_and_return
from ..parser import ctime_to_datestring


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class repository_server_class():


	def __init__(self, root_path, server_p_dict = None, daemon = None):

		# Store root
		self.root_path = root_path

		# Update CWD
		self.set_cwd(self.root_path)

		# Init all index related lists and dicts
		self.__init_index__()

		# Init server component if required
		if server_p_dict is not None and type(server_p_dict) is dict:
			self.__init_server__(server_p_dict, daemon)


	def backup(self, branch_name, mode = KEY_MP):

		# TODO error handling!

		if branch_name == KEY_JOURNAL:
			merge_a, merge_b = FILE_DB_CURRENT + '.' + mode, FILE_DB_JOURNAL + '.' + mode
		elif branch_name == KEY_MASTER:
			merge_a, merge_b = FILE_DB_JOURNAL + '.' + mode, FILE_DB_MASTER + '.' + mode
		else:
			raise #

		self.__backup_index_file__(merge_b)
		self.__copy_index_file__(merge_a, merge_b)


	def diff(self):
		""" Diff looks for files, which have been changed (changed, created, moved, deleted).
		It does not care about tags and groups.
		"""

		if not self.index_loaded_bool:
			self.__load_index__()

		return self.__diff__()


	def dump(self, path = None, mode = KEY_JSON):

		if not self.index_loaded_bool:
			self.__load_index__()

		self.__store_index__(path = path, mode = mode)


	def find_duplicates(self):
		""" find_duplicates looks for identical files.
		Multiples of tags and groups are not yet being looked for.
		"""

		if not self.index_loaded_bool:
			self.__load_index__()

		return find_duplicates_in_entry_list(self.index_list_dict[KEY_FILES])


	def get_file_metainfo(self, filename):

		if not self.index_loaded_bool:
			self.__load_index__()

		try:
			return self.__get_file_entry_by_filename__(filename)
		except filename_unrecognized_by_repo_error:
			pass

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


	def get_free_id(self):

		if not self.index_loaded_bool:
			self.__load_index__()

		while True:
			new_id = ('%0' + str(ID_HASH_LENGTH) + 'x') % random.randrange(16**ID_HASH_LENGTH)
			if new_id not in self.index_id_set:
				self.index_id_set.update(new_id)
				break

		return new_id


	def get_stats(self):

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


	def run_server(blocking = True):

		if blocking:
			self.server.server_forever()
		else:
			self.server.server_forever_in_thread()


	def set_cwd(self, target_path):

		# Store CWD
		self.current_path = target_path

		# Relative path between CWD and repo root
		self.current_relative_path = os.path.relpath(self.root_path, self.current_path)


	def tag(self,
		tag_name,
		target_filename_list = [], target_group_list = [], target_tag_list = [],
		remove_flag = False
		):

		if not self.index_loaded_bool:
			self.__load_index__()

		if tag_name not in self.tagmirror_dict_bytagname.keys():
			self.__tag_create__(tag_name)
			self.__update_mirror_dicts__(only_tags = True)

		tag_id = self.tagmirror_dict_bytagname[tag_name]

		file_not_found_list = []
		group_not_found_list = []
		tag_not_found_list = []

		for target_filename in target_filename_list:
			try:
				target_entry = self.__get_file_entry_by_filename__(target_filename)
			except filename_unrecognized_by_repo_error:
				file_not_found_list.append(target_filename)
				continue
			self.__tag_entry__(target_entry, tag_id, remove_flag = remove_flag)

		for target_tag_name in target_tag_list:
			if target_tag_name not in self.tagmirror_dict_bytagname.keys():
				tag_not_found_list.append(target_tag_name)
				continue
			target_tag_id = self.tagmirror_dict_bytagname[target_tag_name]
			if tag_id == target_tag_id:
				continue
			target_entry = self.index_dict_byid_dict[KEY_TAGS][target_tag_id]
			self.__tag_entry__(target_entry, tag_id, remove_flag = remove_flag)

		# TODO add tagging for groups
		# HACK tell user about untagged groups
		group_not_found_list = target_group_list

		self.__update_index_dicts_from_lists__(index_key_list = INDEX_TYPES)
		self.__store_index__()

		return file_not_found_list, group_not_found_list, tag_not_found_list


	def tags_modify(self, create_tag_names_list = [], delete_tag_names_list = [], force_delete = False):
		""" Creates and deletes lists of tags
		"""

		if not self.index_loaded_bool:
			self.__load_index__()

		tags_donotexist_list = []
		tags_exist_list = []
		tags_inuse_list = []

		# Create path
		for tag_name in create_tag_names_list:
			try:
				self.__tag_create__(tag_name)
			except tag_exists_error:
				tags_exist_list.append(tag_name)

		# Delete path
		for tag_name in delete_tag_names_list:
			try:
				self.__tag_delete__(tag_name, force_delete = force_delete)
			except tag_does_not_exists_error:
				tags_donotexist_list.append(tag_name)
			except tag_in_use_error:
				tags_inuse_list.append(tag_name)

		self.__update_index_dicts_from_lists__(index_key_list = INDEX_TYPES)
		self.__update_mirror_dicts__(only_tags = True)

		self.__store_index__()

		return tags_donotexist_list, tags_exist_list, tags_inuse_list


	def update(self):

		if not self.index_loaded_bool:
			self.__load_index__()

		self.__update_index_on_files__()
		self.__update_index_dicts_from_lists__(index_key_list = [KEY_FILES])
		self.__update_mirror_dicts__()

		self.__store_index__()


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


	def __diff__(self):

		old_entries_list = self.index_list_dict[KEY_FILES]
		new_entries_light_list = self.__generate_light_index_and_return__()

		# Compare old list vs new list and return result
		return compare_entry_lists(old_entries_list, new_entries_light_list)


	def __get_file_entry_by_filename__(self, filename):

		abs_path = os.path.abspath(os.path.join(self.current_path, filename))

		if not (abs_path in self.filemirror_dict_byabspath.keys()):
			raise filename_unrecognized_by_repo_error()

		return self.index_dict_byid_dict[KEY_FILES][self.filemirror_dict_byabspath[abs_path]]


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

		# A set of all currently known IDs
		self.index_id_set = set()

		# Have index dicts been loaded?
		self.index_loaded_bool = False


	def __init_server__(self, server_p_dict, daemon):

		# Store reference to daemon object
		self.daemon = daemon

		# Start MP server
		self.server = mp_server_class(
			(server_p_dict[KEY_ADDRESS], server_p_dict[KEY_PORT]),
			server_p_dict[KEY_SECRET],
			server_p_dict[KEY_TERMINATE]
			)

		# Register functions on server
		for func_name in [
			'backup',
			'diff',
			'dump',
			'find_duplicates',
			'get_file_metainfo',
			'get_free_id',
			'get_stats',
			'get_tag_name_list',
			'run_server',
			'set_cwd',
			'tag',
			'tags_modify',
			'update'
			]:
			self.server.register_function(
				getattr(self, func_name), func_name
				)

		atexit.register(self.__terminate__)


	def __is_tag_in_use__(self, tag_id):

		tag_used_bool = False
		for index_type in INDEX_TYPES:
			tag_used_bool |= bool(self.index_dict_bytagid_dict[index_type][tag_id])

		return tag_used_bool


	def __load_index__(self, mode = DEFAULT_INDEX_FORMAT, force_reload = False):

		if self.index_loaded_bool and not force_reload:
			raise # TODO

		import_dict = load_data(os.path.join(
			self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode
			), mode = mode)

		for index_key in INDEX_TYPES:
			self.index_list_dict[index_key].clear()
			self.index_list_dict[index_key] += [generate_entry(
				self, storage_dict = entry_dict
				) for entry_dict in import_dict[index_key]]
		self.__update_index_dicts_from_lists__(index_key_list = INDEX_TYPES)
		self.__update_mirror_dicts__()


	def __store_index__(self, path = None, mode = DEFAULT_INDEX_FORMAT, force_store = False):

		export_dict = {}
		for index_key in INDEX_TYPES:
			export_dict.update({index_key: [
				entry.export_storage_dict() for entry in self.index_list_dict[index_key]
				]})

		if not (self.index_loaded_bool or force_store):
			raise # TODO

		if path in [None, '']:
			path = os.path.join(
				self.root_path, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT + '.' + mode
				)

		store_data(path, export_dict, mode = mode)


	def __tag_create__(self, tag_name):

		# Raise an error if tag exists
		if tag_name in self.tagmirror_dict_bytagname.keys():
			raise tag_exists_error()

		# Generate new tag entry
		new_tag_entry = generate_entry(self, tag_dict = {KEY_NAME: tag_name})
		# Give the tag an ID
		new_tag_entry.generate_id()
		# Append tag to list of tags
		self.index_list_dict[KEY_TAGS].append(new_tag_entry)


	def __tag_delete__(self, tag_name, force_delete = False):

		# Raise an error if the tag does not exist
		if tag_name not in self.tagmirror_dict_bytagname.keys():
			raise tag_does_not_exists_error()

		# Get tag entry
		tag_entry = self.index_dict_byid_dict[KEY_TAGS][self.tagmirror_dict_bytagname[tag_name]]
		# Get tag id
		tag_id = tag_entry.p_dict[KEY_ID]

		# Is tag in use?
		tag_used_bool = self.__is_tag_in_use__(tag_id)

		# Raise an error if the tag is in use and the delete is not forced
		if tag_used_bool and not force_delete:
			raise tag_in_use_error()

		# Remove the tag from all entries if the tag is in use and delete forced
		if tag_used_bool and force_delete:
			for index_type in INDEX_TYPES:
				for entry in self.index_dict_bytagid_dict[index_type][tag_id].values():
					entry.p_dict[KEY_TAGS].pop(tag_id)

		# Actually delete tag
		tag_entry_index = self.index_list_dict[KEY_TAGS].index(tag_entry)
		del self.index_list_dict[KEY_TAGS][tag_entry_index]


	def __tag_entry__(self, target_entry, tag_id, remove_flag = False):

		if remove_flag:
			if tag_id in target_entry.p_dict[KEY_TAGS].keys():
				target_entry.p_dict[KEY_TAGS].pop(tag_id)
		else:
			if tag_id not in target_entry.p_dict[KEY_TAGS].keys():
				target_entry.p_dict[KEY_TAGS].update({
					tag_id: self.index_dict_byid_dict[KEY_TAGS][tag_id].p_dict[KEY_NAME]
					})


	def __terminate__(self):

		pass


	def __update_index_on_files__(self):

		uc_list, rw_list, _, nw_list, ch_list, mv_list = self.__diff__()

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

		# Keep a list of used indexes
		self.index_id_set.clear()
		for index_key in INDEX_TYPES:
			self.index_id_set.update(self.index_dict_byid_dict[index_key].keys())


	def __update_mirror_dicts__(self, only_tags = False, only_filenames = False):

		if not only_filenames:
			self.tagmirror_dict_bytagname = {
				entry.p_dict[KEY_NAME]: entry.p_dict[KEY_ID] for entry in self.index_list_dict[KEY_TAGS]
				}

		if not only_tags:
			self.filemirror_dict_byabspath = {
				os.path.abspath(os.path.join(
					self.root_path, entry.p_dict[KEY_PATH], entry.p_dict[KEY_NAME]
					)): entry.p_dict[KEY_ID] for entry in self.index_list_dict[KEY_FILES]
				}
