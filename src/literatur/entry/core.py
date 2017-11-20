# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/entry/core.py: Defines an entry class

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

import datetime
import hashlib
import os
from pprint import pformat as pf

import humanize

from ..const import (
	KEY_EXISTS_BOOL,
	KEY_FILE,
	KEY_ID,
	KEY_GROUP,
	# KEY_INFO,
	KEY_INODE,
	KEY_HASH,
	KEY_MAGIC,
	KEY_META,
	KEY_MIME,
	KEY_MODE,
	KEY_MTIME,
	KEY_NAME,
	KEY_PATH,
	KEY_REPORT,
	KEY_SIZE,
	KEY_STATUS,
	KEY_TYPE,
	MSG_DEBUG_STATUS,
	STATUS_CH,
	STATUS_MV,
	STATUS_NW,
	STATUS_RM,
	STATUS_RW,
	STATUS_UC
	)
from ..filetypes import (
	get_literatur_type_from_magicinfo,
	get_magicinfo,
	get_mimetype
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class entry_class():


	# Root path of repository, identical accross all entries
	root_path = None


	def __init__(self,
		file_dict = None,
		filepath_tuple = None,
		group_dict = None,
		meta_dict = None,
		storage_dict = None
		):

		self.id = None # Unique entry ID
		self.type = None # One in {KEY_FILE, KEY_GROUP}
		self.report = None # Detailes on status
		self.status = None # Changed, moved, ...

		self.f_dict = {} # File information
		self.f_ch_dict = {} # Updated file information
		self.g_dict = {} # Group information
		self.m_dict = {} # meta information

		if file_dict is not None and type(file_dict) == dict:
			self.f_dict.update(file_dict)
			self.type = KEY_FILE

		if filepath_tuple is not None and type(filepath_tuple) == tuple:
			self.f_dict.update({
				KEY_PATH: filepath_tuple[0],
				KEY_NAME: filepath_tuple[1]
				})
			self.type = KEY_FILE

		if group_dict is not None and type(group_dict) == dict:
			self.g_dict.update(group_dict)
			self.type = KEY_GROUP

		if meta_dict is not None and type(meta_dict) == dict:
			self.m_dict.update(meta_dict)

		if storage_dict is not None and type(storage_dict) == dict:
			self.import_storage_dict(storage_dict)


	def __repr__(self):

		if self.status is None:
			return pf({
				KEY_FILE: self.f_dict,
				KEY_ID: self.id,
				KEY_META: self.m_dict,
				KEY_TYPE: self.type
				})
		else:
			merged_f_dict = {key: self.f_dict[key] for key in self.f_dict.keys()}
			merged_f_dict.update(self.f_ch_dict)
			return pf({
				KEY_FILE: merged_f_dict,
				KEY_ID: self.id,
				KEY_META: self.m_dict,
				KEY_REPORT: self.report,
				KEY_STATUS: '%s (%d)' % (MSG_DEBUG_STATUS[self.status], self.status),
				KEY_TYPE: self.type
				})


	def check_existence_and_return(self):

		if os.path.isfile(os.path.join(self.get_full_path(), self.f_dict[KEY_NAME])):
			return True
		return False


	def export_storage_dict(self):

		export_dict = {}

		if self.id is not None:
			export_dict.update({KEY_ID: self.id})
		if self.type is not None:
			export_dict.update({KEY_TYPE: self.type})
			if self.type == KEY_FILE:
				export_dict.update({KEY_FILE: self.f_dict})
			elif self.type == KEY_GROUP:
				export_dict.update({KEY_GROUP: self.g_dict})
			else:
				raise # TODO
		else: # TODO remove else section
			if len(self.f_dict.keys()) > 0:
				export_dict.update({
					KEY_TYPE: KEY_FILE,
					KEY_FILE: self.f_dict
					})
			elif len(self.g_dict.keys()) > 0:
				export_dict.update({
					KEY_TYPE: KEY_GROUP,
					KEY_GROUP: self.g_dict
					})

		return export_dict


	def generate_report(self):

		self.report = []

		if self.status == STATUS_MV:

			self.report.append('%s: "%s" -> "%s"' % (
				MSG_DEBUG_STATUS[STATUS_MV],
				os.path.join(self.f_dict[KEY_PATH], self.f_dict[KEY_NAME]),
				os.path.join(self.f_ch_dict[KEY_PATH], self.f_ch_dict[KEY_NAME])
				))

		elif self.status == STATUS_RW:

			self.report.append('%s: "%s"' % (
				MSG_DEBUG_STATUS[STATUS_RW],
				os.path.join(self.f_ch_dict[KEY_PATH], self.f_ch_dict[KEY_NAME])
				))

		elif self.status == STATUS_CH:

			size_diff = self.f_ch_dict[KEY_SIZE] - self.f_dict[KEY_SIZE]
			if size_diff >= 0:
				size_prefix = '+'
			else:
				size_prefix = '-'
			self.report.append('%s: "%s" [%s] %s ago' % (
				MSG_DEBUG_STATUS[STATUS_CH],
				os.path.join(self.f_dict[KEY_PATH], self.f_dict[KEY_NAME]),
				size_prefix + humanize.naturalsize(abs(size_diff), gnu = True),
				humanize.naturaldelta(
					datetime.datetime.now() - datetime.datetime.fromtimestamp(self.f_ch_dict[KEY_MTIME] / 1e9)
					)
				))

		elif self.status in [STATUS_UC, STATUS_RM, STATUS_NW]:

			pass

		else:

			raise # TODO


	def get_full_path(self):

		if self.root_path is not None:
			return os.path.join(self.root_path, self.f_dict[KEY_PATH])
		return self.f_dict[KEY_PATH]


	def import_storage_dict(self, import_dict):

		if KEY_ID in import_dict.keys():
			self.id = import_dict[KEY_ID]
		if KEY_TYPE in import_dict.keys():
			self.type = import_dict[KEY_TYPE]

		if KEY_FILE in import_dict.keys():
			self.f_dict.update(import_dict[KEY_FILE])
			self.type = KEY_FILE
		elif KEY_GROUP in import_dict.keys():
			self.g_dict.update(import_dict[KEY_GROUP])
			self.type = KEY_GROUP
		else:
			raise # TODO

		if KEY_META in import_dict.keys():
			self.m_dict.update(import_dict[KEY_META])


	def merge_file_dict(self):

		self.f_dict.update(self.f_ch_dict)
		self.f_ch_dict = {}
		self.report = None
		self.status = None
		# self.update_file_existence()


	def update_file_existence(self):

		self.f_dict[KEY_EXISTS_BOOL] = self.check_existence_and_return()


	def update_file_id(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			field_key_list = [KEY_NAME, KEY_PATH, KEY_MODE, KEY_INODE, KEY_SIZE, KEY_MTIME]
			field_value_list = [
				str(self.f_dict[key]) for key in field_key_list
				]
			field_value_str = ' '.join(field_value_list)

			hash_object = hashlib.sha256(field_value_str.encode())

			self.f_dict[KEY_ID] = hash_object.hexdigest()

		else:

			raise # TODO


	def update_file_hash(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			in_path = os.path.join(self.get_full_path(), self.f_dict[KEY_NAME])
			blocksize = 8 * 1024 * 1024 # 65536
			hasher = hashlib.sha256()

			f = open(in_path, 'rb')
			buf = f.read(blocksize)
			while len(buf) > 0:
				hasher.update(buf)
				buf = f.read(blocksize)
			f.close()

			self.f_dict[KEY_HASH] = hasher.hexdigest()

		else:

			raise # TODO


	def update_file_magic(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			path = self.get_full_path()
			self.f_dict.update({
				KEY_MAGIC: get_magicinfo((path, self.f_dict[KEY_NAME])),
				KEY_MIME: get_mimetype((path, self.f_dict[KEY_NAME]))
				})

		else:

			raise # TODO


	def update_file_info(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			stat_info = os.stat(os.path.join(self.get_full_path(), self.f_dict[KEY_NAME]))
			self.f_dict.update({
				KEY_MODE: stat_info.st_mode,
				KEY_INODE: stat_info.st_ino,
				KEY_SIZE: stat_info.st_size,
				KEY_MTIME: stat_info.st_mtime_ns
				})

		else:

			raise # TODO


	def update_file_type(self):

		self.f_dict[KEY_TYPE] = get_literatur_type_from_magicinfo(self.f_dict[KEY_MAGIC])
