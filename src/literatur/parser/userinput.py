# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/parser/userinput.py: Handle metadata in userinput format

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

from .lib import (
	get_book_from_bookid,
	get_default_metaentry_dict,
	string_to_authors_dict
	)
from .string import clean_str

from ..const import (
	AUTHORS_ETAL,
	DEFAULT_YEAR_MAX,
	DEFAULT_YEAR_MIN,
	DELIMITER_FILENAME_SECTION,
	DELIMITER_USERINPUT_BLOCK,
	DELIMITER_USERINPUT_SERIES,
	KEY_ANNOTATION,
	KEY_AUTHOR_FIRST,
	KEY_AUTHORS_DICT,
	KEY_CLASS,
	KEY_EDITORS_DICT,
	KEY_EDITORS_LIST,
	KEY_ETAL_BOOL,
	KEY_SERIES_ID,
	KEY_SERIES_NAME,
	KEY_SERIES_SECTION,
	KEY_SERIES_TYPE,
	KEY_TITLE,
	KEY_YEAR,
	KNOWN_CLASSES_LIST
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_basic_userinput_str(in_a_str, in_b_str = ''):

	cnt_n = '\n'

	return cnt_n + in_a_str + cnt_n + DELIMITER_USERINPUT_BLOCK + cnt_n + in_b_str + cnt_n


def metaentry_dict_to_userinput_str(metaentry_dict):

	cnt_n = '\n'

	userinput_list = [
		metaentry_dict[KEY_CLASS], cnt_n,
		DELIMITER_USERINPUT_BLOCK, cnt_n,
		metaentry_dict[KEY_YEAR]
		]
	if metaentry_dict[KEY_SERIES_ID] != '':
		userinput_list += [' ', metaentry_dict[KEY_SERIES_ID]]
		if metaentry_dict[KEY_SERIES_SECTION] != '':
			userinput_list += [
				' ', DELIMITER_USERINPUT_SERIES,
				' ', ' '.join(metaentry_dict[KEY_SERIES_SECTION])
				]
	userinput_list += [cnt_n, DELIMITER_USERINPUT_BLOCK, cnt_n]
	for author_key in list(metaentry_dict[KEY_AUTHORS_DICT].keys()):
		userinput_list += [metaentry_dict[KEY_AUTHORS_DICT][author_key], ' ']
	if metaentry_dict[KEY_ETAL_BOOL]:
		userinput_list += [AUTHORS_ETAL + ' ']
	userinput_list += [
		cnt_n, DELIMITER_USERINPUT_BLOCK, cnt_n,
		metaentry_dict[KEY_TITLE], cnt_n
		]
	if metaentry_dict[KEY_ANNOTATION] != '':
		userinput_list += [
			DELIMITER_USERINPUT_BLOCK, cnt_n,
			metaentry_dict[KEY_ANNOTATION], cnt_n
			]

	return ''.join(userinput_list)


def userinput_str_to_metaentry_dict(userinput_str):

	metaentry_dict = get_default_metaentry_dict()
	fragments_list = userinput_str.split(DELIMITER_USERINPUT_BLOCK)

	# Step 1: Class
	if len(fragments_list) > 0:
		item_class = clean_str(fragments_list[0]).upper().replace(' ', '-')
		if item_class in KNOWN_CLASSES_LIST:
			metaentry_dict[KEY_CLASS] = item_class

	# Step 2: Year & series
	if len(fragments_list) > 1:
		item_year_str = clean_str(fragments_list[1])
		if len(item_year_str) > 3:
			# Is year a number? Go back to default if not
			if item_year_str[:4].isdigit():
				item_year_int = int(item_year_str[:4])
				# Check for unrealistic years
				if item_year_int <= DEFAULT_YEAR_MAX and item_year_int >= DEFAULT_YEAR_MIN:
					metaentry_dict[KEY_YEAR] = item_year_int
				# Fetch series etc
				if len(item_year_str) > 4:
					item_book_s = item_year_str[4:].split(DELIMITER_USERINPUT_SERIES)
					metaentry_dict[KEY_SERIES_ID] = item_book_s[0].strip(' ').replace(' ', DELIMITER_FILENAME_SUB)
					(
						metaentry_dict[KEY_SERIES_NAME],
						metaentry_dict[KEY_EDITORS_DICT],
						metaentry_dict[KEY_SERIES_TYPE]
						) = get_book_from_bookid(item_year_int, metaentry_dict[KEY_SERIES_ID])
					if len(item_book_s) > 1:
						metaentry_dict[KEY_SERIES_SECTION] = item_book_s[1].strip(' ').split(' ')

	# Step 3: Authors
	if len(fragments_list) > 2:
		item_authors_str = clean_str(fragments_list[2]).replace(' ', '-')
		if len(item_authors_str) > 0:
			(
				metaentry_dict[KEY_AUTHOR_FIRST],
				metaentry_dict[KEY_AUTHORS_DICT],
				metaentry_dict[KEY_ETAL_BOOL]
				) = string_to_authors_dict(item_authors_d)

	# Step 4: Title
	if len(fragments_list) > 3:
		item_title_str = clean_str(fragments_list[3])
		if len(item_title_str) > 0:
			metaentry_dict[KEY_TITLE] = item_title_str

	# Step 5: Annotation
	if len(fragments_list) > 4:
		item_ann_str = clean_str(fragments_list[4])
		if len(item_ann_str) > 0:
			metaentry_dict[KEY_ANNOTATION] = item_ann_str

	return metaentry_dict
