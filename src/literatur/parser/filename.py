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
	authors_dict_to_string,
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
	if len(filename_str) > FILENAME_SHORTLENGTH_INT:
		filename_short_str = filename_str[:(FILENAME_SHORTLENGTH_INT - 10)] + '...' + filename_str[-6:]
	else:
		filename_short_str = filename_str

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

	# 5th item: Annotations (optional)
	if len(items) > 4:
		metaentry_dict[KEY_ANNOTATION] = ' '.join(items[4:])
		if metaentry_dict[KEY_ANNOTATION] not in ANNOTATION_LIST:
			debug_msg(MSG_DEBUG_UNEXPECTEDANNOTATION, metaentry_dict[KEY_ANNOTATION])

	# Build object
	return metaentry_dict, ''.join(item_msg).strip(' \n\t')


def follows_filename_convention_guess(filename_str):
	"""
	Try *quick* guess: Is this a filename following the convention?
	"""

	items = filename_str.split(DELIMITER_FILENAME_BLOCK)

	if len(items) > 2:
		if items[0] in KNOWN_CLASSES_LIST:
			if len(items[1]) > 3:
				if items[1][:4].isdigit():
					return True

	return False


def metaentry_dict_to_filename_str(metaentry_dict):

	# Left of author block: Class, year, book and section
	left_list = [metaentry_dict[KEY_CLASS], DELIMITER_FILENAME_BLOCK, str(metaentry_dict[KEY_YEAR])]
	if metaentry_dict[KEY_SERIES_ID] != '':
		left_list += [DELIMITER_FILENAME_SECTION, metaentry_dict[KEY_SERIES_ID]]
		if len(metaentry_dict[KEY_SERIES_SECTION]) > 0:
			left_list += [DELIMITER_FILENAME_SECTION, DELIMITER_FILENAME_SUB.join([str(el) for el in metaentry_dict[KEY_SERIES_SECTION]])]
	left_list.append(DELIMITER_FILENAME_BLOCK)
	left_str = ''.join(left_list)

	# Right of author block: Title, annotation, file format
	right_list = [DELIMITER_FILENAME_BLOCK, metaentry_dict[KEY_TITLE].replace(' ', DELIMITER_FILENAME_SUB)]
	if metaentry_dict[KEY_ANNOTATION] != '':
		right_list += [DELIMITER_FILENAME_BLOCK, metaentry_dict[KEY_ANNOTATION].replace(' ', DELIMITER_FILENAME_SUB)]
	right_str = ''.join(right_list)

	# Get authors
	author_str = authors_dict_to_string(
		metaentry_dict[KEY_AUTHORS_DICT],
		max_length_int = FIMENAME_MAXLENGTH_INT - len(left_str) + len(right_str),
		etal_input_bool = metaentry_dict[KEY_ETAL_BOOL]
		)

	return left_str + author_str + right_str
