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

import hashlib
import os

from ..const import (
	KEY_ALL,
	KEY_FILE,
	KEY_FILE_TMP,
	KEY_ID,
	KEY_INFO,
	KEY_INODE,
	KEY_HASH,
	KEY_MAGIC,
	KEY_MIME,
	KEY_MODE,
	KEY_MTIME,
	KEY_NAME,
	KEY_PATH,
	KEY_REPORT,
	KEY_SIZE,
	KEY_STATUS,
	KEY_TYPE
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

	root_path = '' # Root path of repository
	f_dict = {
		KEY_EXISTS_BOOL: False,
		KEY_HASH: '',
		KEY_ID: '',
		KEY_INODE: -1,
		KEY_MAGIC: '',
		KEY_MIME: '',
		KEY_MODE: -1,
		KEY_MTIME: -1
		KEY_NAME: '',
		KEY_PATH: '',
		KEY_SIZE: -1,
		KEY_TYPE: ''
		} # file information
	m_dict = {} # meta information


	def __init__(self, file_dict = None, meta_dict = None, filepath_tuple = None, root_path = None):

		if file_dict is not None and type(file_dict) == dict:
			self.f_dict.update(file_dict)

		if meta_dict is not None and type(meta_dict) == dict:
			self.m_dict.update(meta_dict)

		if filepath_tuple is not None and type(filepath_tuple) == tuple:
			self.f_dict.update({
				KEY_PATH: filepath_tuple[0],
				KEY_NAME: filepath_tuple[1]
				}

		if root_path is not None and type(root_path) == str:
			self.root_path = root_path


	def check_existence_and_return(self):

		if os.path.isfile(os.path.join(self.get_full_path(), self.f_dict[KEY_NAME])):
			return True
		return False


	def get_full_path(self):

		if self.root_path != '':
			return os.path.join(self.root_path, self.f_dict[KEY_PATH])
		return self.f_dict[KEY_PATH]


	def update_existence(self):

		self.f_dict[KEY_EXISTS_BOOL] = self.check_existence_and_return()


	def update_id(self):

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


	def update_hash(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			in_path = os.path.join(self.get_full_path(), self.f_dict[KEY_NAME])
			blocksize = 65536
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


	def update_magic(self):

		if self.f_dict[KEY_EXISTS_BOOL]:

			path = self.get_full_path()
			self.f_dict.update({
				KEY_MAGIC: get_magicinfo((path, self.f_dict[KEY_NAME])),
				KEY_MIME: get_mimetype((path, self.f_dict[KEY_NAME]))
				})

		else:

			raise # TODO


	def update_fileinfo(self):

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


	def update_type(self):

		pass
