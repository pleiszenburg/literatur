# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/commit.py: Commit changes to repo

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
	PATH_REPO,
	PATH_SUB_DB,
	PATH_SUB_DBBACKUP
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES?
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def commit(working_path, target):

	if target == 'journal':
		commit_a, commit_b = FILE_DB_CURRENT, FILE_DB_JOURNAL
	elif target == 'master':
		commit_a, commit_b = FILE_DB_JOURNAL, FILE_DB_MASTER
	else:
		raise #

	__commit_backup__(commit_b, working_path)
	__commit_push__(commit_a, commit_b, working_path)


def __commit_backup__(commit_source, working_path):

	# Full path of file which is going into backup
	commit_source_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, commit_source)

	# Run only if there is something to backup
	if os.path.isfile(commit_source_path):

		# Get creation time of file
		ctime = os.path.getmtime(commit_source_path)

		# Form string from creation time
		ctime_string = __commit_datestring__(ctime)

		# Create new file name with creation time
		commit_target = commit_source.replace('.', '_' + ctime_string + '.')

		# Get full path of backup target
		commit_target_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DBBACKUP, commit_target)

		# Copy file for backup
		shutil.copyfile(commit_source_path, commit_target_path)


def __commit_datestring__(ctime):

	# Get time in sec, convert to GMT and time object
	ctime_object = time.gmtime(ctime)

	# Convert time object into string
	ctime_string = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
		ctime_object.tm_year, ctime_object.tm_mon, ctime_object.tm_mday, ctime_object.tm_hour, ctime_object.tm_min, ctime_object.tm_sec
		)

	return ctime_string


def __commit_push__(commit_source, commit_target, working_path):

	# Get full paths
	commit_source_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, commit_source)
	commit_target_path = os.path.join(working_path, PATH_REPO, PATH_SUB_DB, commit_target)

	# Only push if source exists
	if os.path.isfile(commit_source_path):

		# If previous commit exists, kill it
		if os.path.isfile(commit_target_path):
			os.remove(commit_target_path)

		# Copy original to target ('copyfile' will overwrite)
		shutil.copyfile(commit_source_path, commit_target_path)
