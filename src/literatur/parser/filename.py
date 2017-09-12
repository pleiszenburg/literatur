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
	string_to_authors_dict,
	string_to_keywords_list
	)
from .string import clean_str

from ..const import (
	ANNOTATION_LIST,
	DEFAULT_TITLE,
	KEY_ANNOTATION,
	KEY_AUTHORS_DICT,
	KEY_AUTHOR_FIRST,
	KEY_CLASS,
	KEY_EDITORS_LIST,
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
	MSG_DEBUG_UNKNWNSERIES
	)
from ..filetypes import KNOWN_EXTENSIONS_LIST


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def filename_str_to_metaentry_dict(filename_str):

	def debug_msg(filename_long_str, msg_list, msg_type_str, msg_str):
		msg_list.append('%s: %s (%s)\n' % (
			msg_type_str, msg_str, __short_filename_str_for_log__(filename_long_str)
			))

	cnt_n = '\n'

	# Debug messages
	item_msg = []

	# Check length filename
	if len(filename_str) > lit_filename_maxlength:
		debug_msg(item_msg, MSG_DEBUG_FILENAMETOOLONG, filename_str)

	# Split filename and extention
	item_fileformat, filename_str_clean = __extract_extension_from_filename_str__(filename_str)
	if item_fileformat == '':
		debug_msg(filename_str, item_msg, MSG_DEBUG_UNKNOWNEXTENSION, '?')

	# Breake file name into items
	items = filename_str_clean.split('_')

	# 1st item: Class
	item_class = items[0]
	if item_class not in KNOWN_CLASSES_LIST:
		debug_msg(filename_str, item_msg, MSG_DEBUG_UNKNOWNCLASS, item_class)

	# 2nd item: Year, series, section
	items_block = items[1].split('.')
	item_year = items_block[0]
	if len(items_block) > 1:
		item_bookid = items_block[1]
		item_book, item_editors, item_type = get_book_from_bookid(item_year, item_bookid)
		if item_bookid not in list(lit_book_ids.keys()):
			debug_msg(filename_str, item_msg, MSG_DEBUG_UNKNWNSERIES, item_bookid)
	else:
		item_bookid = ''
		item_book = ''
		item_type = ''
		item_editors = OrderedDict()
	if len(items_block) > 2:
		item_section = items_block[2].replace('-', '.')
	else:
		item_section = ''

	# 3rd item: Authors
	item_first, item_names, item_etal = string_to_authors_dict(items[2])

	# 4th item: Title
	if len(items) > 3:
		item_title = items[3].replace('-', ' ')
		item_keywords = string_to_keywords_list(item_title)
		if len(item_title) < 12 and item_title.split(' ')[0] not in MATTER_LIST:
			debug_msg(filename_str, item_msg, MSG_DEBUG_SHORTTITLE, item_title)
	else:
		debug_msg(filename_str, item_msg, MSG_DEBUG_NOTITLE, '?')
		item_title = DEFAULT_TITLE
		item_keywords = []
	# Handle special titles, frontmatters etc
	if item_title.split(' ')[0] in MATTER_LIST:
		item_flag_sp = True
	else:
		item_flag_sp = False

	# Deal with special files, frontmatters etc - TODO remove this section eventually
	if items[2].split('-')[0] in MATTER_LIST:
		item_title = '[' + items[2].replace('-', ' ') + ']'
		debug_msg(filename_str, item_msg, MSG_DEBUG_RESERVEDTITLE, item_title)
		# item_flag_sp = True
	# else:
		# item_flag_sp = False

	# 5th item: Annotations (optional)
	if len(items) > 4:
		item_ann = items[4]
		if len(items) > 5:
			item_ann_d = items[5:]
			for zz in item_ann_d:
				item_ann += ' ' + zz
		if item_ann not in ANNOTATION_LIST:
			debug_msg(filename_str, item_msg, MSG_DEBUG_UNEXPECTEDANNOTATION, item_ann)
	else:
		item_ann = ''

	# Build object
	return {
		KEY_ANNOTATION: item_ann,
		KEY_AUTHOR_FIRST: item_first,
		KEY_AUTHORS_DICT: item_names,
		KEY_CLASS: item_class,
		KEY_EDITORS_LIST: item_editors,
		KEY_ETAL_BOOL: item_etal,
		KEY_KEYWORDS_LIST: item_keywords,
		KEY_MATTER_BOOL: item_flag_sp,
		KEY_SERIES_ID: item_bookid,
		KEY_SERIES_NAME: item_book,
		KEY_SERIES_SECTION: item_section,
		KEY_SERIES_TYPE: item_type,
		KEY_TITLE: item_title,
		KEY_YEAR: item_year
		}, ''.join(item_msg).strip(' \n\t')


def metaentry_dict_to_filename_str(lwObject):

	# Left of author block: Class, year, book and section
	lFile_lAuthor = lwObject[lit_id_class] + "_" + lwObject[lit_id_year]
	if lwObject[lit_id_bookid] != '':
		lFile_lAuthor += "." + lwObject[lit_id_bookid]
		if lwObject[lit_id_section] != '':
			lFile_lAuthor += "." + lwObject[lit_id_section].replace(" ", "-")
	lFile_lAuthor += "_"

	# Right of author block: Title, annotation, file format
	lFile_rAuthor = "_" + lwObject[lit_id_title_d].replace(" ", "-")
	if lwObject[lit_id_ann_d] != '':
		lFile_rAuthor += "_" + lwObject[lit_id_ann_d].replace(" ", "-")
	lFile_rAuthor += "." + lwObject[lit_id_fileformat]

	# Length of filename without author block
	lFile_len = len(lFile_lAuthor) + len(lFile_rAuthor)
	# Length of author block
	lFile_author_len = 0
	# Empty author string
	lFile_Author = ''

	# Iterate over authors
	check_etal = False
	for uu in list(lwObject[lit_id_authors].keys()):
		uu_temp = lwObject[lit_id_authors][uu].replace(" ", "-") + "-"
		if (lFile_len + lFile_author_len + len(uu_temp) + len(lit_authors_etal)) <= lit_filename_maxlength:
			lFile_author_len += len(uu_temp)
			lFile_Author += uu_temp
		else:
			lFile_author_len += len(lit_authors_etal)
			lFile_Author += lit_authors_etal
			check_etal = True
			break
	# ETAL flag from object?
	if not check_etal and lwObject[lit_id_flag_etal]:
		lFile_author_len += len(lit_authors_etal)
		lFile_Author += lit_authors_etal
		check_etal = True

	lFile_Author = lFile_Author.strip('-')

	lFile = lFile_lAuthor + lFile_Author + lFile_rAuthor

	return lFile


def __extract_extension_from_filename_str__(filename_str):

	# Check for known file formats
	for ext in KNOWN_EXTENSIONS_LIST:
		if filename_str.endswith(ext) or filename_str.endswith(ext.upper()):
			return ext, filename_str[:-(len(ext) + 1)]

	return '', filename_str


def __short_filename_str_for_log__(filename_str):

	len_cut = 80

	if len(filename_str) > len_cut:
		ext, name = __extract_extension_from_filename_str__(filename_str)
		short_name = name[:(len_cut - 10)] + '...' + name[-6:]
		if ext != '':
			short_name += '.' + ext
		return short_name
	else:
		return filename_str
