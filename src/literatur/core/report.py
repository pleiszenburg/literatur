#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *

import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WIKI REPORT ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def report_wiki_fragmentbyletter():

	by_letter = 'By letter: '

	for ii in list_alphabet:
		by_letter += "'''[[#" + ii + "|" + ii + "]]''' "
		if ii != list_alphabet[-1]:
			by_letter += ' | '

	return by_letter


def report_wiki_indexbykeyword(list_by_keywords):

	cnt_index = []

	cnt_index.append(cnt_message_bot + cnt_n + cnt_n)
	cnt_index.append('The following tables lists all entries in ' + lit_path_external + ' on Dropbox by keyword(s).' + cnt_n + cnt_n)

	cnt_index.append(report_wiki_fragmentbyletter())
	cnt_index.append(cnt_n + cnt_n)

	list_by_keywords_keys = list(list_by_keywords.keys())
	list_by_keywords_keys.sort()

	for ii in list_by_keywords_keys:

		if ii[0] != (list_by_keywords_keys[list_by_keywords_keys.index(ii) - 1][0]):

			cnt_index.append('==' + ii[0].upper() + '== ' + cnt_n + cnt_n)

			cnt_index.append('<table class="wikitable" style="width: 100%">' + cnt_n)
			cnt_index.append('<tr>' + cnt_n)
			cnt_index.append('<th width="20%">keyword</th>' + cnt_n)
			cnt_index.append('<th width="80%">(class, year, first author) title</th>' + cnt_n)
			cnt_index.append('</tr>' + cnt_n)

		cnt_index.append('<tr>' + cnt_n)
		cnt_index.append('<td valign="top">' + ii + '</td>' + cnt_n)
		cnt_index.append('<td valign="top">')

		for jj in list_by_keywords[ii]:

			cnt_index.append('(' + jj[lit_id_class].lower() + ', ' + jj[lit_id_year] + ', [[Literature_Index_by_Author#' + jj[lit_id_firstauthor] + '|' + jj[lit_id_authors][jj[lit_id_firstauthor]] + ']]) ')
			if dropbox_on:
				cnt_index.append('[' + jj[lit_id_url] + ' ')
			cnt_index.append(jj[lit_id_title])
			if dropbox_on:
				cnt_index.append(']')

			if jj[lit_id_title] != list_by_keywords[ii][-1][lit_id_title]:
				cnt_index.append('<br>')

		cnt_index.append('</td>' + cnt_n)
		cnt_index.append('</tr>' + cnt_n)

		if ii[0] != 'z' and list_by_keywords_keys[-1] != ii: # HACK
			if ii[0] != list_by_keywords_keys[list_by_keywords_keys.index(ii) + 1][0]:
				cnt_index.append('</table>' + cnt_n)
		if list_by_keywords_keys[-1] == ii:
			cnt_index.append('</table>' + cnt_n)

	cnt_index.append(cnt_cmd_notoc + cnt_n)
	cnt_index.append(cnt_category_lit + cnt_n)

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j


def report_wiki_indexbyname(list_by_name):

	cnt_index = []

	cnt_index.append(cnt_message_bot + cnt_n + cnt_n)
	cnt_index.append('The following tables list all entries in ' + lit_path_external + ' on Dropbox by author(s).' + cnt_n + cnt_n)

	cnt_index.append(report_wiki_fragmentbyletter())
	cnt_index.append(cnt_n + cnt_n)

	list_by_name_keys = list(list_by_name.keys())
	list_by_name_keys.sort()

	for ii in list_by_name_keys:

#		try:

			if ii[0] != (list_by_name_keys[list_by_name_keys.index(ii) - 1][0]):

				cnt_index.append('==' + ii[0] + '== ' + cnt_n + cnt_n)

				cnt_index.append('<table class="wikitable" style="width: 100%">' + cnt_n)
				cnt_index.append('<tr>' + cnt_n)
				cnt_index.append('<th width="20%">(co-) author</th>' + cnt_n)
				cnt_index.append('<th width="80%">(class, year) title</th>' + cnt_n)
				cnt_index.append('</tr>' + cnt_n)

			cnt_index.append('<tr>' + cnt_n)
			cnt_index.append('<td valign="top"><div id="' + ii.split(lit_delimiter)[0] + '">' + ii.split(lit_delimiter)[1] + '</div></td>' + cnt_n)
			cnt_index.append('<td valign="top">')

			for jj in list_by_name[ii]:
				cnt_index.append('(' + jj[lit_id_class].lower() + ', ' + jj[lit_id_year] + ') ')
				if jj[lit_flag_firstauthor]:
					cnt_index.append("'''")
				if dropbox_on:
					cnt_index.append('[' + jj[lit_id_url] + ' ')
				cnt_index.append(jj[lit_id_title])
				if dropbox_on:
					cnt_index.append(']')
				if jj[lit_flag_firstauthor]:
					cnt_index.append("'''")
				if jj[lit_id_title] != list_by_name[ii][-1][lit_id_title]:
					cnt_index.append('<br>')

			cnt_index.append('</td>' + cnt_n)
			cnt_index.append('</tr>' + cnt_n)

			if ii[0] != 'Z' and list_by_name_keys[-1] != ii: # HACK
				if ii[0] != list_by_name_keys[list_by_name_keys.index(ii) + 1][0]:
					cnt_index.append('</table>' + cnt_n)
			if list_by_name_keys[-1] == ii:
				cnt_index.append('</table>' + cnt_n)

#		except:
#
#			print u"report_wiki_indexbyname: some error"
#			pprint.pprint(ii)

	cnt_index.append(cnt_cmd_notoc + cnt_n)
	cnt_index.append(cnt_category_lit + cnt_n)

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j


def report_wiki_authorrelationship(list_by_relationship):

	cnt_index = []

	cnt_index.append(cnt_message_bot + cnt_n + cnt_n)
	cnt_index.append('The following table lists relationships between authors of documents in ' + lit_path_external + '.' + cnt_n + cnt_n)

	cnt_index.append(report_wiki_fragmentbyletter())
	cnt_index.append(cnt_n + cnt_n)

	list_by_relationship_keys = list(list_by_relationship.keys())
	list_by_relationship_keys.sort()

	for ii in list_by_relationship_keys:

		if ii[0] != (list_by_relationship_keys[list_by_relationship_keys.index(ii) - 1][0]):

			cnt_index.append('==' + ii[0] + '== ' + cnt_n + cnt_n)

			cnt_index.append('<table class="wikitable" style="width: 100%">' + cnt_n)
			cnt_index.append('<tr>' + cnt_n)
			cnt_index.append('<th width="20%">author</th>' + cnt_n)
			cnt_index.append('<th width="80%">co-authors</th>' + cnt_n)
			cnt_index.append('</tr>' + cnt_n)

		if (ii.split(lit_delimiter)[1] != ii.split(lit_delimiter)[1].upper()) and (len(list_by_relationship[ii]) > 0):

			cnt_index.append('<tr>' + cnt_n)
			cnt_index.append('<td valign="top">' + ii.split(lit_delimiter)[1] + '</td>' + cnt_n)
			cnt_index.append('<td valign="top">')


			list_by_relationship_sub_keys = list(list_by_relationship[ii].keys())
			list_by_relationship_sub_keys.sort()

			for jj in list_by_relationship_sub_keys:

				cnt_index.append('(' + str(list_by_relationship[ii][jj][lit_id_coauthorscount]) + ') ')
				if list_by_relationship[ii][jj][lit_id_coauthorscount] > 1:
					cnt_index.append("'''")
				cnt_index.append(jj.split(lit_delimiter)[1])
				if list_by_relationship[ii][jj][lit_id_coauthorscount] > 1:
					cnt_index.append("'''")
				cnt_index.append(' (' + str(list_by_relationship[ii][jj][lit_id_year_start]) + ' - ' + str(list_by_relationship[ii][jj][lit_id_year_end]) + ')')

				if jj != list_by_relationship_sub_keys[-1]:
					cnt_index.append('<br>')

			cnt_index.append('</td>' + cnt_n)
			cnt_index.append('</tr>' + cnt_n)

		if ii[0] != 'Z' and list_by_relationship_keys[-1] != ii: # HACK
			if ii[0] != list_by_relationship_keys[list_by_relationship_keys.index(ii) + 1][0]:
				cnt_index.append('</table>' + cnt_n)
		if list_by_relationship_keys[-1] == ii:
			cnt_index.append('</table>' + cnt_n)

	cnt_index.append(cnt_cmd_notoc + cnt_n)
	cnt_index.append(cnt_category_lit + cnt_n)

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j


def report_wiki_indexbyclass(list_by_class):

	cnt_index = []

	cnt_index.append(cnt_message_bot + cnt_n + cnt_n)
	cnt_index.append('The following tables lists SOME entries in ' + lit_path_external + ' on Dropbox by class.' + cnt_n + cnt_n)

	cnt_index.append('<table class="wikitable sortable">' + cnt_n)

	cnt_index.append('<tr>' + cnt_n)
	cnt_index.append('<th width="15%">class</th>' + cnt_n)
	cnt_index.append('<th>author(s) and title</th>' + cnt_n)
	cnt_index.append('</tr>' + cnt_n)

	# Iterate over volumes (journals and books)
	for ii in list(list_by_class.keys()):

		jj_first = True

		# Iterate over sub-volumes
		for jj in list(list_by_class[ii].keys()):

			if jj_first:
				jj_first = False

			if len(list_by_class[ii][jj][lit_id_list]) > 0:
				cnt_index.append('<tr><td valign="top"><small>' + cnt_n)
				cnt_index.append(list_by_class[ii][jj][lit_id_type] + ' ' + ii + ' ' + jj)
				cnt_index.append('</small></td>' + cnt_n)
				cnt_index.append('<td valign="top">' + cnt_n)

				cnt_index.append("'''" + list_by_class[ii][jj][lit_id_title] + "'''")

			# Iterate over items
			for kk in list_by_class[ii][jj][lit_id_list]:

				cnt_index.append(cnt_n + cnt_n)

				cnt_index.append('(' + kk[lit_id_class])
				if kk[lit_id_section] != '':
					cnt_index.append(' ' + kk[lit_id_section])
				cnt_index.append(') ')

				if dropbox_on:
					cnt_index.append('[' + kk[lit_id_url] + ' ')
				cnt_index.append(kk[lit_id_title])
				if dropbox_on:
					cnt_index.append(']')

				if len(list(kk[lit_id_authors].keys())) > 0:
					cnt_index.append("<br><small>''")
					for mm in list(kk[lit_id_authors].keys()):
						cnt_index.append(kk[lit_id_authors][mm])
						if mm != list(kk[lit_id_authors].keys())[-1]:
							cnt_index.append(', ')
					cnt_index.append("''</small>")

			if len(list_by_class[ii][jj][lit_id_list]) > 0:
				cnt_index.append('</td></tr>' + cnt_n)

	cnt_index.append('</table>' + cnt_n)

	cnt_index.append(cnt_cmd_notoc + cnt_n)
	cnt_index.append(cnt_category_lit + cnt_n)

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j


def report_wiki_full(list_full):

	cnt_index = []

	cnt_index.append(cnt_message_bot + cnt_n + cnt_n)
	cnt_index.append('The following table lists all entries in ' + lit_path_external + ' on Dropbox.' + cnt_n + cnt_n)

	cnt_index.append('<table class="wikitable sortable">' + cnt_n)

	cnt_index.append('<tr>' + cnt_n)
	cnt_index.append('<th width="15%">class</th>' + cnt_n)
	cnt_index.append('<th width="15%">year</th>' + cnt_n)
	cnt_index.append('<th>author(s) and title</th>' + cnt_n)
	cnt_index.append('</tr>' + cnt_n)

	for ii in list_full:

		cnt_index.append('<tr>' + cnt_n)
		cnt_index.append('<td>' + ii[lit_id_class].lower() + '</td>' + cnt_n)
		cnt_index.append('<td>' + ii[lit_id_year] + '</td>' + cnt_n)

		cnt_index.append('<td>')
		if len(list(ii[lit_id_authors].keys())) > 0:
			cnt_index.append("''")
			for jj in list(ii[lit_id_authors].keys()):
				cnt_index.append(ii[lit_id_authors][jj])
				if jj != list(ii[lit_id_authors].keys())[-1]:
					cnt_index.append(', ')
			cnt_index.append("''<br>")

		if dropbox_on:
			cnt_index.append('[' + ii[lit_id_url] + ' ')
		cnt_index.append(ii[lit_id_title])
		if dropbox_on:
			cnt_index.append(']')

		if ii[lit_id_book] != '':
			cnt_index.append('<br><small>In ' + ii[lit_id_type].lower() + ': ' + ii[lit_id_book] + '')
			if ii[lit_id_section] != '':
				cnt_index.append(', ' + ii[lit_id_section])
			if len(ii[lit_id_editors]) > 0:
				cnt_index.append(" (edited by ''")
				for jj in list(ii[lit_id_editors].keys()):
					cnt_index.append(ii[lit_id_editors][jj])
					if jj != list(ii[lit_id_editors].keys())[-1]:
						cnt_index.append(', ')
				cnt_index.append("'')")
			cnt_index.append('</small>')
		cnt_index.append('</td>' + cnt_n)

		# cnt_index.append(u'<td>' + ii[lit_id_ann] + u'</td>' + cnt_n)

		cnt_index.append('</tr>' + cnt_n)

	cnt_index.append('</table>' + cnt_n)

	cnt_index.append(cnt_cmd_notoc + cnt_n)
	cnt_index.append(cnt_category_lit + cnt_n)

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DEBUG REPORT ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def report_debug_duplicates(duplicate_list):

	cnt_duplicates = []

	for ii in list(duplicate_list.keys()):
		cnt_duplicates.append(ii + cnt_n)
		for jj in duplicate_list[ii]:
			cnt_duplicates.append("  " + jj[lit_id_filename] + cnt_n)

	cnt_duplicates_j = ''.join(cnt_duplicates)

	return cnt_duplicates_j


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MAIL REPORT ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def report_mail_newfiles(diff_new):

	cnt_index = []

	cnt_index.append('New library entries on Dropbox!' + cnt_n + cnt_n)

	cnt_index.append('Editorial note: ' + cnt_n + cnt_n)

	for ii in reversed(diff_new):

		cnt_index.append('(' + ii[lit_id_class].lower() + ', ' + ii[lit_id_year] + ') ')

		cnt_index.append('')
		if len(list(ii[lit_id_authors].keys())) > 0:
			cnt_index.append('')
			for jj in list(ii[lit_id_authors].keys()):
				cnt_index.append(ii[lit_id_authors][jj])
				if jj != list(ii[lit_id_authors].keys())[-1]:
					cnt_index.append(',')
				else:
					cnt_index.append(':')
				cnt_index.append(' ')

		cnt_index.append(cnt_n)

		cnt_index.append(ii[lit_id_title] + cnt_n)

		if ii[lit_id_book] != '':
			cnt_index.append('In ' + ii[lit_id_type].lower() + ': ' + ii[lit_id_book] + '')
			if ii[lit_id_section] != '':
				cnt_index.append(', ' + ii[lit_id_section])
			if len(ii[lit_id_editors]) > 0:
				cnt_index.append(' (edited by ')
				for jj in list(ii[lit_id_editors].values()): # TODO: Review 'values'
					cnt_index.append(jj)
					if jj != list(ii[lit_id_editors].values())[-1]: # TODO: Review 'values'
						cnt_index.append(', ')
				cnt_index.append(')')
			cnt_index.append('' + cnt_n)

		if ii[lit_id_url] != '':
			cnt_index.append('' + ii[lit_id_url] + '' + cnt_n)

		cnt_index.append(' ' + cnt_n)

	cnt_index.append('Full inventory index:' + cnt_n + 'http://xxx.com/abc/wiki/index.php?title=Literature_Index')

	cnt_index_j = ''.join(cnt_index)

	return cnt_index_j
