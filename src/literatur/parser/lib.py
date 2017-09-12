# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/parser/lib.py: Parser helper routines

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
import string

from ..const import AUTHORS_EXCLUDE_LIST
from ..repo import get_series_dict


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# TODO use established lib instead
EXCLUDE_WORDS_LIST = ['advanced', 'advances', 'analyses', 'analysis', 'annual', 'an', 'among', 'all', 'and', 'of', 'with',
	'anomalous', 'anomaly', 'approach', 'approaches', 'approximation', 'are', 'around', 'articles', 'another', 'as', 'assessing',
	'assessment', 'asset', 'assets', 'associated', 'at', 'au', 'available', 'back', 'based', 'basic', 'bd', 'be', 'become',
	'behavior', 'behaviour', 'benefits', 'best', 'better', 'between', 'beyond', 'big', 'brief', 'briefing', 'build', 'building',
	'built', 'by', 'can', 'capabilities', 'capability', 'capable', 'case', 'causes', 'ce', 'certify', 'chief', 'ci', 'ck',
	'close', 'cm', 'cmas', 'comprehensive', 'concept', 'concepts', 'conceptual', 'concerning', 'concerns', 'conclusion',
	'conjugated', 'considerations', 'content', 'context', 'continued', 'contribution', 'corrected', 'cr', 'on', 'data', 'de',
	'days', 'december', 'der', 'des', 'details', 'developing', 'easily', 'for', 'from', 'high', 'hires', 'development', 'do',
	'does', 'due', 'during', 'early', 'how', 'ii', 'iii', 'im', 'in', 'inside', 'into', 'is', 'it', 'its', 'iv', 'low',
	'made', 'new', 'no', 'non', 'october', 'off', 'one', 'ongoing', 'only', 'onto', 'or', 'our', 'plate', 'pre', 're',
	'results', 'short', 'small', 'smaller', 'soon', 'study', 'system', 'take', 'than', 'that', 'the', 'their', 'them',
	'three', 'to', 'tp', 'tr', 'two', 'um', 'und', 'under', 'up', 'update', 'upon', 'vi', 'vii', 'viii', 'vs', 'we',
	'what', 'who', 'will', 'without', 'zu', 'end', 'highly', 'imply', 'importance', 'important', 'improved', 'improvement',
	'increasing', 'independent', 'indicate', 'initial', 'just', 'known', 'knowledge', 'large', 'largest', 'left', 'let', 'like',
	'long', 'looking', 'lower', 'lucky', 'mid', 'not', 'novel', 'other', 'over', 'proper', 'recap', 'realizing', 'realize',
	'reality', 'realities', 'realistic', 'real', 'recent', 'revealed', 'reveals', 'second', 'six', 'success', 'successful',
	'understanding', 'understand', 'understood', 'unknown', 'viable', 'yet']


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_book_from_bookid(year, bookid):

	item_book = ''
	item_editors = OrderedDict()
	item_type = ''
	lit_book_ids = get_series_dict()

	if bookid in lit_book_ids.keys():
		if year in lit_book_ids[bookid]:
			item_book = lit_book_ids[bookid][year][lit_id_title]
			item_type = lit_book_ids[bookid][year][lit_id_type]
			if lit_id_editors in lit_book_ids[bookid][year]:
				_, item_editors, _ = string_to_authors_dict(lit_book_ids[bookid][year][lit_id_editors])

	return item_book, item_editors, item_type


def string_to_authors_dict(authors):

	temp_list = authors.replace('-', ' ').split(' ')

	authors_dict = OrderedDict()
	temp_author = ''
	temp_author_k = ''
	flag_first = False
	first_author = ''
	authors_etal = False

	for jj in temp_list:
		if (jj not in AUTHORS_EXCLUDE_LIST) and (not jj.isdigit()) and (len(jj) > 0):
			if jj[0].islower():
				temp_author += jj + ' '
				temp_author_k += '_' + jj
			else:
				id_count = 1
				while (jj + temp_author_k + '_' + str(id_count)) in list(authors_dict.keys()):
					id_count += 1
				jj_id = jj + temp_author_k + '_' + str(id_count)
				authors_dict.update({jj_id:(temp_author + jj)})
				if not flag_first:
					first_author = jj_id
					flag_first = True
				temp_author = ''
				temp_author_k = ''
		if jj == lit_authors_etal:
			authors_etal = True

	return first_author, authors_dict, authors_etal


def string_to_keywords_list(in_str):
	"""
	This routine is an ugly HACK and must be replaced by a real lexer.
	"""

	alphabet_lowercase_list = list(string.ascii_lowercase)
	word_list = in_str.replace('-', ' ').lower().split(' ')
	keywords_list = []

	for word in word_list:
		if (
			word not in keywords_list
			) and (
			word not in alphabet_lowercase_list
			) and (
			word not in EXCLUDE_WORDS_LIST # TODO remove from this file (header)
			):
			if (
				not word.isdigit()
				) and (
				not any(letter in word for letter in string.digits)
				):
				keywords_list.append(word)

	return keywords_list
