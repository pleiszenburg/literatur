# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/const.py: Constants, keys, default parameter

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
# STATIC STRINGS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

PATH_SUB_DB = 'db'
PATH_SUB_DBBACKUP = 'db/backup'
PATH_SUB_REPORTS = 'reports'

PATH_REPO = '.l'

IGNORE_DIR_LIST = [
	PATH_REPO,
	'.git'
	]
IGNORE_FILE_LIST = [
	'desktop.ini',
	'.directory'
	]

KEY_CURRENT = 'current'
KEY_JOURNAL = 'journal'
KEY_MASTER = 'master'

FILE_DB_CURRENT = 'index_%s.pkl' % KEY_CURRENT # stage 1
FILE_DB_JOURNAL = 'index_%s.pkl' % KEY_JOURNAL # stage 2
FILE_DB_MASTER = 'index_%s.pkl' % KEY_MASTER # stage 3

STATUS_UC = 0
STATUS_RM = 1
STATUS_NW = 2
STATUS_CH = 3
STATUS_MV = 4
STATUS_RW = 5

REPORT_MAX_LINES = 1000
