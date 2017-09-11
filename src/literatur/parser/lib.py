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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_book_from_bookid(year, bookid):

	item_book = ''
	item_editors = OrderedDict()
	item_type = ''

	if bookid in lit_book_ids:
		if year in lit_book_ids[bookid]:
			item_book = lit_book_ids[bookid][year][lit_id_title]
			item_type = lit_book_ids[bookid][year][lit_id_type]
			if lit_id_editors in lit_book_ids[bookid][year]:
				_, item_editors, _ = string_to_authors_dict(lit_book_ids[bookid][year][lit_id_editors])

	return item_book, item_editors, item_type


def string_to_authors_dict(authors):

	temp_list = authors.replace('-', ' ').split(' ')

	authors_list = OrderedDict()
	temp_author = ''
	temp_author_k = ''
	flag_first = False
	first_author = ''
	authors_etal = False

	for jj in temp_list:
		if (jj not in list_authors_exclude) and (not jj.isdigit()) and (len(jj) > 0):
			if jj[0].islower():
				temp_author += jj + ' '
				temp_author_k += '_' + jj
			else:
				id_count = 1
				while (jj + temp_author_k + '_' + str(id_count)) in list(authors_list.keys()):
					id_count += 1
				jj_id = jj + temp_author_k + '_' + str(id_count)
				authors_list.update({jj_id:(temp_author + jj)})
				if not flag_first:
					first_author = jj_id
					flag_first = True
				temp_author = ''
				temp_author_k = ''
		if jj == lit_authors_etal:
			authors_etal = True

	return first_author, authors_list, authors_etal
