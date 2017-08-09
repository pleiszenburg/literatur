# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/commit.py: Commit changes to repo

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
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import shutil
import time
import pprint

from .strings import *
from .groups import lit_book_ids


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES?
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def commit_push(c_original, c_target, working_path):

	# If previous commit exists, kill it
	if os.path.isfile(c_target):
		os.remove(c_target)

	# Copy original to target
	shutil.copyfile(
		working_path + lit_path_subfolder_db + c_original,
		working_path + lit_path_subfolder_db + c_target
		)


def commit_backup(commit_file, working_path):

	# Get creation time of file
	ctime = os.path.getmtime(working_path + lit_path_subfolder_db + commit_file)

	# Form string from creation time
	ctime_string = commit_datestring(ctime)

	# Create new file name with creation time
	commit_file_target = commit_file.replace('.', '_' + ctime_string + '.');

	# Copy file for backup
	shutil.copyfile(
		working_path + lit_path_subfolder_db + commit_file,
		working_path + lit_path_subfolder_dbbackup + commit_file_target
		)


def commit_datestring(ctime):

	# Get time in sec, convert to GMT and time object
	ctime_object = time.gmtime(ctime)

	# Convert time object into string
	ctime_string = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
		ctime_object.tm_year, ctime_object.tm_mon, ctime_object.tm_mday, ctime_object.tm_hour, ctime_object.tm_min, ctime_object.tm_sec
		)

	return ctime_string
