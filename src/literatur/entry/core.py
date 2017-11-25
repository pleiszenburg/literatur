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
	KEY_ENTRYTYPE,
	KEY_EXISTS_BOOL,
	KEY_FILE,
	KEY_ID,
	KEY_GROUP,
	KEY_INODE,
	KEY_HASH,
	KEY_MAGIC,
	KEY_META,
	KEY_MIME,
	KEY_MODE,
	KEY_MTIME,
	KEY_NAME,
	KEY_PATH,
	KEY_PARAM,
	KEY_REPORT,
	KEY_SIZE,
	KEY_STATUS,
	KEY_TAG,
	KEY_TAGS,
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
# FACTORY FUNCTION FOR ENTRIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def generate_entry(
	root_path = None,
	file_dict = None,
	filepath_tuple = None,
	group_dict = None,
	storage_dict = None,
	tag_dict = None
	):

	if storage_dict is not None and type(storage_dict) == dict:
		if storage_dict[KEY_PARAM][KEY_ENTRYTYPE] == KEY_FILE:
			return entry_file_class(storage_dict, root_path)
		elif storage_dict[KEY_PARAM][KEY_ENTRYTYPE] == KEY_GROUP:
			return entry_group_class(storage_dict, root_path)
		elif storage_dict[KEY_PARAM][KEY_ENTRYTYPE] == KEY_TAG:
			return entry_tag_class(storage_dict, root_path)
		else:
			raise # TODO

	if file_dict is not None and type(file_dict) == dict:
		return entry_file_class({KEY_PARAM: file_dict}, root_path)

	if filepath_tuple is not None and type(filepath_tuple) == tuple:
		return entry_file_class({KEY_PARAM: {
			KEY_PATH: filepath_tuple[0],
			KEY_NAME: filepath_tuple[1]
			}}, root_path)

	if group_dict is not None and type(group_dict) == dict:
		return entry_group_class({KEY_PARAM: group_dict}, root_path)

	if tag_dict is not None and type(tag_dict) == dict:
		return entry_tag_class({KEY_PARAM: tag_dict}, root_path)

	raise # TODO


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class __entry_class__():


	def __init__(self, import_dict, root_path):

		self.report = None # Detailes on status
		self.status = None # Changed, moved, ...
		self.id = None

		self.p_dict = {} # Parameter dict
		self.p_ch_dict = {} # Updated parameter dict

		self.m_dict = {} # Meta info dict

		self.root_path = root_path

		self.import_storage_dict(import_dict)

		if KEY_TAGS not in self.p_dict.keys():
			self.p_dict[KEY_TAGS] = {}


	def __repr__(self):

		if self.status is None:
			return pf({
				KEY_ID: self.id,
				KEY_META: self.m_dict,
				KEY_PARAM: self.p_dict
				})
		else:
			merged_p_dict = {key: self.p_dict[key] for key in self.p_dict.keys()}
			merged_p_dict.update(self.p_ch_dict)
			return pf({
				KEY_ID: self.id,
				KEY_META: self.m_dict,
				KEY_PARAM: merged_p_dict,
				KEY_REPORT: self.report,
				KEY_STATUS: '%s (%d)' % (MSG_DEBUG_STATUS[self.status], self.status)
				})


	def export_storage_dict(self):

		if self.id in [None, 0, '']:
			raise # TODO

		return {
			KEY_ID: self.id,
			KEY_PARAM: self.p_dict
			}


	def import_storage_dict(self, import_dict):

		if KEY_ID in import_dict.keys():
			self.id = import_dict[KEY_ID]
		if KEY_PARAM in import_dict.keys():
			self.p_dict.update(import_dict[KEY_PARAM])


	def merge_p_dict(self):

		self.p_dict.update(self.p_ch_dict)
		self.p_ch_dict.clear()
		self.report = None
		self.status = None


	def set_id(self, new_id):

		self.id = new_id


	def update_report(self):

		raise NotImplementedError


class entry_file_class(__entry_class__):


	def __init__(self, import_dict, root_path):

		super().__init__(import_dict, root_path)
		self.p_dict.update({KEY_ENTRYTYPE: KEY_FILE})


	def get_file_existence(self):

		if os.path.isfile(os.path.join(self.get_file_fullpath(), self.p_dict[KEY_NAME])):
			return True
		return False


	def get_file_fullpath(self):

		if self.root_path is not None:
			return os.path.join(self.root_path, self.p_dict[KEY_PATH])
		return self.p_dict[KEY_PATH]


	def update_file_existence(self):

		self.p_dict[KEY_EXISTS_BOOL] = self.get_file_existence()


	def update_file_hash(self):

		if self.p_dict[KEY_EXISTS_BOOL]:

			in_path = os.path.join(self.get_file_fullpath(), self.p_dict[KEY_NAME])
			blocksize = 8 * 1024 * 1024 # 65536
			hasher = hashlib.sha256()

			f = open(in_path, 'rb')
			buf = f.read(blocksize)
			while len(buf) > 0:
				hasher.update(buf)
				buf = f.read(blocksize)
			f.close()

			self.p_dict[KEY_HASH] = hasher.hexdigest()

		else:

			raise # TODO


	def update_file_info(self):

		if self.p_dict[KEY_EXISTS_BOOL]:

			stat_info = os.stat(os.path.join(self.get_file_fullpath(), self.p_dict[KEY_NAME]))
			self.p_dict.update({
				KEY_MODE: stat_info.st_mode,
				KEY_INODE: stat_info.st_ino,
				KEY_SIZE: stat_info.st_size,
				KEY_MTIME: stat_info.st_mtime_ns
				})

		else:

			raise # TODO


	def update_file_magic(self):

		if self.p_dict[KEY_EXISTS_BOOL]:

			path = self.get_file_fullpath()
			self.p_dict.update({
				KEY_MAGIC: get_magicinfo((path, self.p_dict[KEY_NAME])),
				KEY_MIME: get_mimetype((path, self.p_dict[KEY_NAME]))
				})

		else:

			raise # TODO


	def update_file_type(self):

		self.p_dict[KEY_TYPE] = get_literatur_type_from_magicinfo(self.p_dict[KEY_MAGIC])


	def update_report(self):

		if self.status == STATUS_MV:

			self.report = '%s: "%s" -> "%s"' % (
				MSG_DEBUG_STATUS[STATUS_MV],
				os.path.join(self.p_dict[KEY_PATH], self.p_dict[KEY_NAME]),
				os.path.join(self.p_ch_dict[KEY_PATH], self.p_ch_dict[KEY_NAME])
				)

		elif self.status == STATUS_RW:

			self.report = '%s: "%s"' % (
				MSG_DEBUG_STATUS[STATUS_RW],
				os.path.join(self.p_ch_dict[KEY_PATH], self.p_ch_dict[KEY_NAME])
				)

		elif self.status == STATUS_CH:

			size_diff = self.p_ch_dict[KEY_SIZE] - self.p_dict[KEY_SIZE]
			if size_diff >= 0:
				size_prefix = '+'
			else:
				size_prefix = '-'
			self.report = '%s: "%s" [%s] %s ago' % (
				MSG_DEBUG_STATUS[STATUS_CH],
				os.path.join(self.p_dict[KEY_PATH], self.p_dict[KEY_NAME]),
				size_prefix + humanize.naturalsize(abs(size_diff), gnu = True),
				humanize.naturaldelta(
					datetime.datetime.now() - datetime.datetime.fromtimestamp(self.p_ch_dict[KEY_MTIME] / 1e9)
					)
				)

		elif self.status in [STATUS_UC, STATUS_RM, STATUS_NW]:

			self.report = None

		else:

			raise # TODO


class entry_group_class(__entry_class__):


	def __init__(self, import_dict, root_path = None):

		super().__init__(import_dict, root_path)
		self.p_dict.update({KEY_ENTRYTYPE: KEY_GROUP})


	def update_report(self):

		raise NotImplementedError


class entry_tag_class(__entry_class__):


	def __init__(self, import_dict, root_path = None):

		super().__init__(import_dict, root_path)
		self.p_dict.update({KEY_ENTRYTYPE: KEY_TAG})


	def update_report(self):

		raise NotImplementedError
