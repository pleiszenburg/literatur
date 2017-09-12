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
	string_to_authors_dict
	)
from .string import clean_str

from ..const import (
	AUTHORS_ETAL,
	DEFAULT_ANNOTATION,
	DEFAULT_AUTHOR,
	DEFAULT_CLASS,
	DEFAULT_TITLE,
	DEFAULT_YEAR,
	DEFAULT_YEAR_MAX,
	DEFAULT_YEAR_MIN,
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
				' ', metaentry_dict[KEY_SERIES_SECTION].replace('.', ' ')
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

	# userinput_list = []
	#
	# if follow_convention_guess(item_filename):
	#
	# 	# ...
	#
	# else:
	#
	# 	fext, fname = filename_ext(item_filename)
	# 	userinput = cnt_n + fname + cnt_n + DELIMITER_USERINPUT_BLOCK + cnt_n + fext + cnt_n


def userinput_str_to_metaentry_dict(userinput_str):

	fragments_list = userinput_str.split(DELIMITER_USERINPUT_BLOCK)

	# Step 1: Class
	item_class = DEFAULT_CLASS
	if len(fragments_list) > 0:
		item_class = clean_str(fragments_list[0]).upper().replace(' ', '-')
		if item_class not in KNOWN_CLASSES_LIST:
			item_class = DEFAULT_CLASS

	# Step 2: Year
	item_year = str(DEFAULT_YEAR)
	item_bookid = ''
	item_book = ''
	item_editors = ''
	item_type = ''
	item_section = ''
	if len(fragments_list) > 1:
		item_year_f = clean_str(fragments_list[1])
		if len(item_year_f) > 3:
			# Is year a number? Go back to default if not
			if item_year_f[:4].isdigit():
				item_year = item_year_f[:4]
				# Check for unrealistic years
				if int(item_year) > DEFAULT_YEAR_MAX or int(item_year) < DEFAULT_YEAR_MIN:
					item_year = str(DEFAULT_YEAR)
				# Fetch series etc
				if len(item_year_f) > 4:
					item_book_s = item_year_f[4:].split(DELIMITER_USERINPUT_SERIES)
					item_bookid = item_book_s[0].strip(' ').replace(' ', '-')
					item_book, item_editors, item_type = get_book_from_bookid(item_year, item_bookid)
					if len(item_book_s) > 1:
						item_section = item_book_s[1].strip(' ')

	# Step 3: Authors
	item_authors_d = DEFAULT_AUTHOR
	if len(fragments_list) > 2:
		item_authors_d = clean_str(fragments_list[2])
		if len(item_authors_d) == 0:
			item_authors_d = DEFAULT_AUTHOR
	# Generate author dictionary
	item_first, item_authors_dict, item_etal = string_to_authors_dict(item_authors_d.replace(' ', '-'))

	# Step 4: Title
	item_title_d = DEFAULT_TITLE
	if len(fragments_list) > 3:
		item_title_d = clean_str(fragments_list[3])
		if len(item_title_d) == 0:
			item_title_d = DEFAULT_TITLE

	# Step 5: Annotation
	item_ann_d = DEFAULT_ANNOTATION
	if len(fragments_list) > 4:
		item_ann_d = clean_str(fragments_list[4])
		if len(item_ann_d) == 0:
			item_ann_d = DEFAULT_ANNOTATION

	# Build and object
	return {
		KEY_ANNOTATION: item_ann_d,
		KEY_AUTHOR_FIRST: item_first,
		KEY_AUTHORS_DICT: item_authors_dict,
		KEY_CLASS: item_class,
		KEY_EDITORS_LIST: item_editors,
		KEY_ETAL_BOOL: item_etal,
		KEY_SERIES_ID: item_bookid,
		KEY_SERIES_NAME: item_book,
		KEY_SERIES_TYPE: item_type,
		KEY_SERIES_SECTION: item_section,
		KEY_TITLE: item_title_d,
		KEY_YEAR: item_year
		}
