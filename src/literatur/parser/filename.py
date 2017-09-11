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

from .string import clean_str

from ..filetypes import KNOWN_EXTENSIONS_LIST


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def filename_str_to_metaentry_dict(filename_str):

	# Debug messages
	item_msg = []

	# Check length filename
	if len(filename_str) > lit_filename_maxlength:
		item_msg.append(lw_debug_filenametoolong + ': ' + __short_filename_str_for_log__(filename_str) + cnt_n)

	# Split filename and extention
	item_fileformat, filename_str_clean = __extract_extension_from_filename_str__(filename_str)
	if item_fileformat == '':
		item_msg.append(lw_debug_unknownformat + ': ' + __short_filename_str_for_log__(filename_str) + cnt_n)

	# Breake file name into items
	items = filename_str_clean.split('_')

	# Set empty hash
	item_hash = ''

	# Set empty file size
	item_size = 0

	# Set empty (Dropbox) URL
	item_url = ''

	# 1st item: Class
	item_class = items[0]
	if item_class not in lit_classes:
		item_msg.append(lw_debug_unknownclass + ': ' + item_class + ' (' + __short_filename_str_for_log__(filename_str) + ')' + cnt_n)

	# 2nd item: Year, series, section
	items_block = items[1].split('.')
	item_year = items_block[0]
	if len(items_block) > 1:
		item_bookid = items_block[1]
		item_book, item_editors, item_type = lit_get_book_from_bookid(item_year, item_bookid)
		if item_bookid not in list(lit_book_ids.keys()):
			item_msg.append(lw_debug_unknownvolume + ': ' + item_bookid + ' (' + __short_filename_str_for_log__(filename_str) + ')' + cnt_n)
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
		if len(item_title) < 12 and item_title.split(' ')[0] not in list_publication_special:
			item_msg.append(lw_debug_shorttitle + ': ' + __short_filename_str_for_log__(filename_str) + cnt_n)
	else:
		item_msg.append(lw_debug_notitle + ': ' + __short_filename_str_for_log__(filename_str) + cnt_n)
		item_title = lit_title_default
		item_keywords = []
	# Handle special titles, frontmatters etc
	if item_title.split(' ')[0] in list_publication_special:
		item_flag_sp = True
	else:
		item_flag_sp = False

	# Deal with special files, frontmatters etc - TODO remove this section eventually
	if items[2].split('-')[0] in list_publication_special:
		item_title = '[' + items[2].replace('-', ' ') + ']'
		item_msg.append(lw_debug_deprecatedtitle + ': ' + item_title + ' (' + __short_filename_str_for_log__(filename_str) + ')' + cnt_n)
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
		if item_ann not in list_ann:
			item_msg.append(lw_debug_annotation + ': ' + item_ann + ' (' + __short_filename_str_for_log__(filename_str) + ')' + cnt_n)
	else:
		item_ann = ''

	# Build object
	item_ii = {
		lit_id_class:item_class,
		lit_id_year:item_year,
		lit_id_book:item_book,
		lit_id_bookid:item_bookid,
		lit_id_editors:item_editors,
		lit_id_type:item_type,
		lit_id_section:item_section,
		lit_id_authors:item_names,
		lit_id_firstauthor:item_first,
		lit_id_flag_etal:item_etal,
		lit_id_title:item_title,
		lit_id_keywords:item_keywords,
		lit_id_ann:item_ann,
		lit_id_filename:filename_str,
		lit_id_fileformat:item_fileformat,
		lit_id_url:item_url,
		lit_flag_sp:item_flag_sp,
		lit_id_size:item_size,
		lit_id_hash:item_hash
		}

	# Handle debug messages
	item_msg = ''.join(item_msg)
	item_msg = item_msg.strip(' \n\t')

	return item_ii, item_msg


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
