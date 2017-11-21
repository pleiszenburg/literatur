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

PATH_REPO = '.lit'

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

FIMENAME_MAXLENGTH_INT = 255 # EXT4 & NTFS
FILENAME_SHORTLENGTH_INT = 80 # For logging ...


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

DELIMITER_FILENAME_BLOCK = '_'
DELIMITER_FILENAME_SECTION = '.'
DELIMITER_FILENAME_SUB = '-'
DELIMITER_USERINPUT_BLOCK = '#'
DELIMITER_USERINPUT_SERIES = '~'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DEFAULTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

DEFAULT_ANNOTATION = ''
DEFAULT_AUTHOR = 'ANONYMOUS'
DEFAULT_CLASS = 'AA'
# DEFAULT_EXTENSION = 'pdf'
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
KEY_CLASS = 'class'
KEY_EDITORS_DICT = 'editors_dict'
KEY_ENTRYTYPE = 'entry_type'
KEY_ETAL_BOOL = 'etal'
KEY_EXISTS_BOOL = 'exists'
KEY_FILE = 'file'
KEY_FILES = 'files'
KEY_GROUP = 'group'
KEY_GROUPS = 'groups'
KEY_HASH = 'hash'
KEY_ID = 'id'
KEY_INFO = 'info'
KEY_INODE = 'inode'
KEY_JSON = 'json'
KEY_KEYWORDS_LIST = 'keywords'
KEY_MAGIC = 'magic'
KEY_MATTER_BOOL = 'matter'
KEY_META = 'meta'
KEY_MIME = 'mime'
KEY_MODE = 'mode'
KEY_MP = 'mp'
KEY_MTIME = 'mtime'
KEY_NAME = 'name'
KEY_PATH = 'path'
KEY_PARAM = 'param'
KEY_PKL = 'pkl'
KEY_REPORT = 'report'
KEY_SERIES_ID = 'series_id'
KEY_SERIES_NAME = 'series_name'
KEY_SERIES_SECTION = 'series_section'
KEY_SERIES_TYPE = 'series_type'
KEY_SIZE = 'size'
KEY_STATUS = 'status'
KEY_TAGS = 'tags'
KEY_TITLE = 'title'
KEY_TYPE = 'type'
# KEY_URL = 'url'
KEY_YEAR = 'year'


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INDEX TYPES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

INDEX_TYPES = [KEY_FILES, KEY_GROUPS, KEY_TAGS]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ENTRY META: CLASSES, AUTHORS, ...
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

AUTHORS_ETAL = 'ETAL'
AUTHORS_EXCLUDE_LIST = [AUTHORS_ETAL, 'plate', 'frontmatter', 'backmatter', 'hires']

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

MATTER_LIST = ['plate', 'frontmatter', 'backmatter']

ANNOTATION_LIST = ['OCR', 'WATERMARKED-DO-NOT-DISTRIBUTE', 'PREPRINT', 'SM', 'SM-PREPRINT']

TITLE_LENGTH_MIN_INT = 12


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MESSAGES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

MSG_DEBUG_FILEALREADYEXISTS = "File already exists."
MSG_DEBUG_FILENAMETOOLONG = 'Filename too long'
MSG_DEBUG_INREPOSITORY = 'You already are in an existing literature repository at "%s".'
MSG_DEBUG_NOREPOSITORY = 'You are no in a literature repository.'
MSG_DEBUG_NOTITLE = 'No title'
MSG_DEBUG_RESERVEDTITLE = 'Reserved special title'
MSG_DEBUG_SHORTTITLE = 'Short title'
MSG_DEBUG_UNEXPECTEDANNOTATION = 'Unexpected annotation'
MSG_DEBUG_UNKNOWNCLASS = 'Unknown class'
MSG_DEBUG_UNKNOWNEXTENSION = 'Unknown extension'
MSG_DEBUG_UNKNWNSERIES = 'Unknown series'
MSG_DEBUG_YEARNAN = 'Year not a number'

MSG_DEBUG_STATUS = {
	STATUS_UC: 'Unchanged',
	STATUS_RM: 'Removed',
	STATUS_NW: 'New',
	STATUS_CH: 'Changed',
	STATUS_MV: 'Moved',
	STATUS_RW: 'Rewritten'
	}


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
