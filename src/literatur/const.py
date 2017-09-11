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
# REPO STORAGE
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

FILE_DB_CURRENT = 'index_%s' % KEY_CURRENT # stage 1
FILE_DB_JOURNAL = 'index_%s' % KEY_JOURNAL # stage 2
FILE_DB_MASTER = 'index_%s' % KEY_MASTER # stage 3


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ENTRY STATUS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

STATUS_UC = 0
STATUS_RM = 1
STATUS_NW = 2
STATUS_CH = 3
STATUS_MV = 4
STATUS_RW = 5


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPORTING
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

REPORT_MAX_LINES = 1000


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# USER I/O
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

DELIMITER_USERINPUT_BLOCK = '#'
DELIMITER_USERINPUT_SERIES = '~'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DEFAULTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

DEFAULT_ANNOTATION = ''
DEFAULT_AUTHOR = 'ANONYMOUS'
DEFAULT_CLASS = 'AA'
DEFAULT_EXTENSION = 'pdf'
DEFAULT_TITLE = 'NOTITLE'
DEFAULT_YEAR_MAX = 2100
DEFAULT_YEAR_MIN = 1000
DEFAULT_YEAR = DEFAULT_YEAR_MIN


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# KEYS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

KEY_ANNOTATION = 'annotation'
KEY_AUTHOR_FIRST = 'author_first'
KEY_AUTHORS_DICT = 'authors_dict'
KEY_AUTHORS_LIST = 'authors_list'
KEY_CLASS = 'class'
KEY_EDITORS_DICT = 'editors_dict'
KEY_EDITORS_LIST = 'editors_list'
KEY_ETAL_BOOL = 'etal'
KEY_EXTENSION = 'extension'
KEY_SERIES_ID = 'series_id'
KEY_SERIES_NAME = 'series_name'
KEY_SERIES_SECTION = 'series_section'
KEY_SERIES_TYPE = 'series_type'
KEY_TITLE = 'title'
KEY_YEAR = 'year'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CLASS_CHAPTER = 'CHAPTER'
CLASS_BOOK = 'BOOK'
CLASS_PROCEEDINGS = 'PROCEEDINGS'
CLASS_JOURNAL = 'JOURNAL'

KNOWN_CLASSES_SP_LIST = [
	CLASS_CHAPTER, CLASS_BOOK, CLASS_PROCEEDINGS, CLASS_JOURNAL
	]
KNOWN_CLASSES_LIST = KNOWN_CLASSES_SP_LIST + [
	'ABSTRACT', 'ABSTRACTS', 'PAPER', 'ANNOUNCEMENT',
	'ARTICLE', 'LETTER', 'MANUAL', 'NOTE', 'PATENT', 'POSTER',
	'PRESENTATION', 'REPORT', 'RESOLUTION', 'SCRIPT', 'THESIS',
	'THESIS-MSC', 'THESIS-BSC', 'THESIS-PHD', 'THESIS-DIPLOMA',
	'WEB', 'PROPOSAL', 'DATASHEET', 'SPEECH', 'SPEC',
	'TUTORIAL', 'STANDARD', 'REVIEW', 'DATA', 'CALL'
	]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# FILENAME HANDLING
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

LETTER_SUB_DICT = {
	"ä":"ae", "Ä":"Ae", "ö":"oe", "Ö":"Oe", "ü":"ue", "Ü":"Ue",
	"é":"e", "É":"E", "è":"e", "È":"E",
	"á":"a", "Á":"A", "à":"a", "À":"A", "Á":"A", "À":"A",
	"ĉ":"c", "Ĉ":"C",
	"ß":"ss", "š":"s",
	"ﬀ":"ff", "ﬁ":"fi", "ﬂ":"fl",
	"í":"i",
	"µ":"u",
	"ñ":"n"
	}
