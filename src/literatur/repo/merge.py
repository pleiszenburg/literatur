# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/merge.py: merge changes to repo

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

from ..const import (
	FILE_DB_CURRENT,
	FILE_DB_JOURNAL,
	FILE_DB_MASTER,
	KEY_JOURNAL,
	KEY_MASTER,
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES?
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def merge_at_root_path(root_path, target, mode = 'mp'):

	if target == KEY_JOURNAL:
		merge_a, merge_b = FILE_DB_CURRENT + '.' + mode, FILE_DB_JOURNAL + '.' + mode
	elif target == KEY_MASTER:
		merge_a, merge_b = FILE_DB_JOURNAL + '.' + mode, FILE_DB_MASTER + '.' + mode
	else:
		raise #

	__backup__(merge_b, root_path)
	__copy__(merge_a, merge_b, root_path)


def __backup__(merge_source, working_path):

	# Full path of file which is going into backup
	merge_source_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, merge_source)

	# Run only if there is something to backup
	if os.path.isfile(merge_source_path):

		# Get creation time of file
		ctime = os.path.getmtime(merge_source_path)

		# Form string from creation time
		ctime_string = __datestring__(ctime)

		# Create new file name with creation time
		merge_target = merge_source.replace('.', '_' + ctime_string + '.')

		# Get full path of backup target
		merge_target_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DBBACKUP, merge_target)

		# Copy file for backup
		shutil.copyfile(merge_source_path, merge_target_path)


def __datestring__(ctime):

	# Get time in sec, convert to GMT and time object
	ctime_object = time.gmtime(ctime)

	# Convert time object into string
	ctime_string = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
		ctime_object.tm_year, ctime_object.tm_mon, ctime_object.tm_mday, ctime_object.tm_hour, ctime_object.tm_min, ctime_object.tm_sec
		)

	return ctime_string


def __copy__(merge_source, merge_target, working_path):

	# Get full paths
	merge_source_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, merge_source)
	merge_target_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, merge_target)

	# Only push if source exists
	if os.path.isfile(merge_source_path):

		# If previous merge exists, kill it
		if os.path.isfile(merge_target_path):
			os.remove(merge_target_path)

		# Copy original to target ('copyfile' will overwrite)
		shutil.copyfile(merge_source_path, merge_target_path)
