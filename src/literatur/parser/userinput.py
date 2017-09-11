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

from .string import clean_str

from ..const import (
	DEFAULT_CLASS,
	DEFAULT_YEAR,
	DEFAULT_YEAR_MAX,
	DEFAULT_YEAR_MIN,
	DELIMITER_USERINPUT_BLOCK,
	DELIMITER_USERINPUT_SERIES,
	KEY_ANNOTATION,
	KEY_AUTHOR_FIRST,
	KEY_AUTHORS_DICT,
	KEY_AUTHORS_LIST,
	KEY_CLASS,
	KEY_EDITORS_DICT,
	KEY_EDITORS_LIST,
	KEY_ETAL_BOOL,
	KEY_EXTENSION,
	KEY_SERIES_ID,
	KEY_SERIES_NAME,
	KEY_SERIES_SECTION,
	KEY_SERIES_TYPE,
	KEY_TITLE,
	KEY_YEAR
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def userinput_str_to_metaentry_dict(in_str):

	fragments_list = in_str.split(DELIMITER_USERINPUT_BLOCK)

	# Step 1: Class
	item_class = DEFAULT_CLASS
	if len(fragments_list) > 0:
		item_class = clean_str(in_str).upper().replace(' ', '-')
		if item_class not in lit_classes:
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
				if item_year > DEFAULT_YEAR_MAX or int(item_year) < DEFAULT_YEAR_MIN:
					item_year = str(DEFAULT_YEAR)
				# Fetch series etc
				if len(item_year_f) > 4:
					item_book_s = item_year_f[4:].split(DELIMITER_USERINPUT_SERIES)
					item_bookid = item_book_s[0].strip(' ').replace(" ", "-")
					item_book, item_editors, item_type = lit_get_book_from_bookid(item_year, item_bookid)
					if len(item_book_s) > 1:
						item_section = item_book_s[1].strip(' ')

	# Step 3: Authors
	item_authors_d = lit_authors_default
	if len(fragments_list) > 2:
		item_authors_d = clean_str(fragments_list[2])
		if len(item_authors_d) == 0:
			item_authors_d = lit_authors_default
	# Generate author dictionary
	item_first, item_names, item_etal = string_to_authors_dict(item_authors_d.replace(" ", "-"))

	# Step 4: Title
	item_title_d = lit_title_default
	if len(fragments_list) > 3:
		item_title_d = clean_str(fragments_list[3])
		if len(item_title_d) == 0:
			item_title_d = lit_title_default

	# Step 5: Annotation
	item_ann_d = lit_ann_default
	if len(fragments_list) > 4:
		item_ann_d = clean_str(fragments_list[4])
		if len(item_ann_d) == 0:
			item_ann_d = lit_ann_default

	# Step 6: File format
	item_fileformat = lit_fileformat_default
	if len(fragments_list) > 5:
		item_fileformat = fragments_list[5].replace(".", " ")
		item_fileformat = clean_str(item_fileformat).replace(" ", ".").lower()
		if item_fileformat not in list_ext:
			item_fileformat = lit_fileformat_default

	# Build and object
	return {
		KEY_ANNOTATION: item_ann_d,
		KEY_AUTHOR_FIRST: item_first,
		KEY_AUTHORS_DICT: item_authors_d,
		KEY_AUTHORS_LIST: item_names,
		KEY_CLASS: item_class,
		KEY_EDITORS_LIST: item_editors,
		KEY_ETAL_BOOL: item_etal,
		KEY_EXTENSION: item_fileformat
		KEY_SERIES_ID: item_bookid,
		KEY_SERIES_NAME: item_book,
		KEY_SERIES_TYPE: item_type,
		KEY_SERIES_SECTION: item_section,
		KEY_TITLE: item_title_d,
		KEY_YEAR: item_year,
		}
