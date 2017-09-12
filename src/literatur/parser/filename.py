# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/parser/filename.py: Handle metadata in filename format

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

from collections import OrderedDict

from .lib import (
	get_book_from_bookid,
	get_default_metaentry_dict,
	string_to_authors_dict,
	string_to_keywords_list
	)
from .string import clean_str

from ..const import (
	ANNOTATION_LIST,
	DELIMITER_FILENAME_BLOCK,
	DELIMITER_FILENAME_SECTION,
	DELIMITER_FILENAME_SUB,
	FIMENAME_MAXLENGTH_INT,
	FILENAME_SHORTLENGTH_INT,
	KEY_ANNOTATION,
	KEY_AUTHORS_DICT,
	KEY_AUTHOR_FIRST,
	KEY_CLASS,
	KEY_EDITORS_DICT,
	KEY_ETAL_BOOL,
	KEY_KEYWORDS_LIST,
	KEY_MATTER_BOOL,
	KEY_SERIES_ID,
	KEY_SERIES_NAME,
	KEY_SERIES_SECTION,
	KEY_SERIES_TYPE,
	KEY_TITLE,
	KEY_YEAR,
	KNOWN_CLASSES_LIST,
	MATTER_LIST,
	MSG_DEBUG_FILENAMETOOLONG,
	MSG_DEBUG_NOTITLE,
	MSG_DEBUG_RESERVEDTITLE,
	MSG_DEBUG_SHORTTITLE,
	MSG_DEBUG_UNEXPECTEDANNOTATION,
	MSG_DEBUG_UNKNOWNCLASS,
	MSG_DEBUG_UNKNOWNEXTENSION,
	MSG_DEBUG_UNKNWNSERIES,
	MSG_DEBUG_YEARNAN,
	TITLE_LENGTH_MIN_INT
	)
from ..repo import get_series_dict


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def filename_str_to_metaentry_dict(filename_str):

	# Short filename for debugging
	filename_short_str = __short_filename_str_for_log__(filename_str)
	# Debug messages list
	item_msg = []

	def debug_msg(msg_type_str, msg_str):
		item_msg.append('%s: %s (%s)\n' % (
			msg_type_str, msg_str, filename_short_str
			))

	# New meta entry
	metaentry_dict = get_default_metaentry_dict()

	# Check length filename
	if len(filename_str) > FIMENAME_MAXLENGTH_INT:
		debug_msg(MSG_DEBUG_FILENAMETOOLONG, filename_str)

	# Break file name into items
	items = filename_str.split(DELIMITER_FILENAME_BLOCK)

	# 1st item: Class
	metaentry_dict[KEY_CLASS] = items[0]
	if metaentry_dict[KEY_CLASS] not in KNOWN_CLASSES_LIST:
		debug_msg(MSG_DEBUG_UNKNOWNCLASS, metaentry_dict[KEY_CLASS])

	# 2nd item: Year, series, section
	items_block = items[1].split(DELIMITER_FILENAME_SECTION)
	if items_block[0].isdigit():
		metaentry_dict[KEY_YEAR] = int(items_block[0])
	else:
		debug_msg(MSG_DEBUG_YEARNAN, items_block[0])
	if len(items_block) > 1:
		metaentry_dict[KEY_SERIES_ID] = items_block[1]
		(
			metaentry_dict[KEY_SERIES_NAME],
			metaentry_dict[KEY_EDITORS_DICT],
			metaentry_dict[KEY_SERIES_TYPE]
			) = get_book_from_bookid(metaentry_dict[KEY_YEAR], metaentry_dict[KEY_SERIES_ID])
		if metaentry_dict[KEY_SERIES_ID] not in list(get_series_dict().keys()):
			debug_msg(MSG_DEBUG_UNKNWNSERIES, metaentry_dict[KEY_SERIES_ID])
	if len(items_block) > 2:
		metaentry_dict[KEY_SERIES_SECTION] = items_block[2].split(DELIMITER_FILENAME_SUB)

	# 3rd item: Authors
	(
		metaentry_dict[KEY_AUTHOR_FIRST],
		metaentry_dict[KEY_AUTHORS_DICT],
		metaentry_dict[KEY_ETAL_BOOL]
		) = string_to_authors_dict(items[2])

	# 4th item: Title
	if len(items) > 3:
		metaentry_dict[KEY_TITLE] = items[3].replace(DELIMITER_FILENAME_SUB, ' ')
		metaentry_dict[KEY_KEYWORDS_LIST] = string_to_keywords_list(metaentry_dict[KEY_TITLE])
		if (
			len(metaentry_dict[KEY_TITLE]) < TITLE_LENGTH_MIN_INT
			) and (
			metaentry_dict[KEY_TITLE].split(' ')[0] not in MATTER_LIST
			):
			debug_msg(MSG_DEBUG_SHORTTITLE, metaentry_dict[KEY_TITLE])
	# Handle special titles, frontmatters etc
	metaentry_dict[KEY_MATTER_BOOL] = metaentry_dict[KEY_TITLE].split(' ')[0] in MATTER_LIST
	if metaentry_dict[KEY_MATTER_BOOL]:
		debug_msg(MSG_DEBUG_RESERVEDTITLE, metaentry_dict[KEY_TITLE])

	# # Deal with special files, frontmatters etc - TODO remove this section eventually
	# if items[2].split('-')[0] in MATTER_LIST:
	# 	item_title = '[' + items[2].replace('-', ' ') + ']'
	# 	debug_msg(filename_str, item_msg, MSG_DEBUG_RESERVEDTITLE, item_title)
	# 	# item_flag_sp = True
	# # else:
	# 	# item_flag_sp = False

	# 5th item: Annotations (optional)
	if len(items) > 4:
		metaentry_dict[KEY_ANNOTATION] = ' '.join(items[4:])
		if metaentry_dict[KEY_ANNOTATION] not in ANNOTATION_LIST:
			debug_msg(MSG_DEBUG_UNEXPECTEDANNOTATION, metaentry_dict[KEY_ANNOTATION])

	# Build object
	return metaentry_dict, ''.join(item_msg).strip(' \n\t')


def metaentry_dict_to_filename_str(metaentry_dict):

	# Left of author block: Class, year, book and section
	left_str = metaentry_dict[KEY_CLASS] + DELIMITER_FILENAME_BLOCK + str(metaentry_dict[KEY_YEAR])
	if metaentry_dict[KEY_SERIES_ID] != '':
		left_str += DELIMITER_FILENAME_SECTION + metaentry_dict[KEY_SERIES_ID]
		if len(metaentry_dict[KEY_SERIES_SECTION]) > 0:
			left_str += DELIMITER_FILENAME_SECTION + DELIMITER_FILENAME_SUB.join([str(el) for el in metaentry_dict[KEY_SERIES_SECTION]])
	left_str += DELIMITER_FILENAME_BLOCK

	# Right of author block: Title, annotation, file format
	right_str = DELIMITER_FILENAME_BLOCK + metaentry_dict[KEY_TITLE].replace(' ', DELIMITER_FILENAME_SUB)
	if metaentry_dict[KEY_ANNOTATION] != '':
		right_str += DELIMITER_FILENAME_BLOCK + metaentry_dict[KEY_ANNOTATION].replace(' ', DELIMITER_FILENAME_SUB)

	# Length of filename without author block
	lFile_len = len(left_str) + len(right_str)
	# Length of author block
	lFile_author_len = 0
	# Empty author string
	lFile_Author = ''

	# Iterate over authors
	check_etal = False
	for uu in list(metaentry_dict[lit_id_authors].keys()):
		uu_temp = metaentry_dict[lit_id_authors][uu].replace(" ", "-") + "-"
		if (lFile_len + lFile_author_len + len(uu_temp) + len(lit_authors_etal)) <= lit_filename_maxlength:
			lFile_author_len += len(uu_temp)
			lFile_Author += uu_temp
		else:
			lFile_author_len += len(lit_authors_etal)
			lFile_Author += lit_authors_etal
			check_etal = True
			break
	# ETAL flag from object?
	if not check_etal and metaentry_dict[lit_id_flag_etal]:
		lFile_author_len += len(lit_authors_etal)
		lFile_Author += lit_authors_etal
		check_etal = True

	lFile_Author = lFile_Author.strip('-')

	filename_str = left_str + lFile_Author + right_str

	return filename_str


def __short_filename_str_for_log__(filename_str):

	if len(filename_str) > FILENAME_SHORTLENGTH_INT:
		return filename_str[:(FILENAME_SHORTLENGTH_INT - 10)] + '...' + filename_str[-6:]
	else:
		return filename_str
