# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/index.py: Builds and manipulates the file index

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
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from collections import OrderedDict
import pprint
import sys

if networkx_on:
	import networkx

from .strings import *
from .groups import lit_book_ids


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INDEX REBUILD ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def lit_find_duplicates(list_full, working_path):

	key_duplicates = {}
	key_groups = {}

	hash_duplicates = {}
	hash_groups = {}

	# Iterate over list - find matches
	for ii in list_full:

		ii[lit_id_keywords].sort()
		search_key = ' '.join(ii[lit_id_keywords])
		if search_key not in list(key_groups.keys()):
			key_groups.update({search_key:[ii]})
		else:
			key_groups[search_key].append(ii)

		if ii[lit_id_hash] not in list(hash_groups.keys()):
			hash_groups.update({ii[lit_id_hash]:[ii]})
		else:
			hash_groups[ii[lit_id_hash]].append(ii)

	# Iterate over key groups, isolate multiples
	for ii in list(key_groups.keys()):

		if len(key_groups[ii]) > 1 and ii != "":
			key_duplicates.update({ii:key_groups[ii]})

	# Iterate over hash groups, isolate multiples
	for ii in list(hash_groups.keys()):

		if len(hash_groups[ii]) > 1:
			hash_duplicates.update({ii:hash_groups[ii]})

	return key_duplicates, hash_duplicates


def lit_diff_lists(list_old, list_new):

	# OUT: Missing (no name match AND no hash match)
	diff_rm = []
	# OUT: New (new name AND new hash)
	diff_new = []
	# OUT: Moved (new name AND hash match)
	diff_mv = []
	# OUT: Changed (name match AND new hash)
	diff_changed = []

	# Iterate over OLD list
	for ii in list_old:

		exist_filename = False
		exist_hash = False
		exist_match = False
		new_filename = ''
		new_hash = ''

		# Iterate over NEW list
		for jj in list_new:

			match_filename = (ii[lit_id_filename] == jj[lit_id_filename])
			match_hash = (ii[lit_id_hash] == jj[lit_id_hash])

			if match_filename:
				exist_filename = True
				new_hash = jj[lit_id_hash]
			if match_hash:
				exist_hash = True
				new_filename = jj[lit_id_filename]
			if match_filename and match_hash:
				exist_match = True

		# Collect deleted files
		if not exist_filename and not exist_hash:
			diff_rm.append(ii)

		# Collect moved files
		if not exist_filename and exist_hash:
			ii[lit_id_filename_new] = new_filename
			diff_mv.append(ii)

		# Collect changed files
		if exist_filename and not exist_hash:
			ii[lit_id_hash_new] = new_hash
			diff_changed.append(ii)

	# Iterate over NEW list
	for jj in list_new:

		exist_filename = False
		exist_hash = False
		exist_match = False

		# Iterate over OLD list
		for ii in list_old:

			match_filename = (ii[lit_id_filename] == jj[lit_id_filename])
			match_hash = (ii[lit_id_hash] == jj[lit_id_hash])

			if match_filename:
				exist_filename = True
			if match_hash:
				exist_hash = True
			if match_filename and match_hash:
				exist_match = True

		# Collect new files
		if not exist_filename and not exist_hash:
			diff_new.append(jj)

	return diff_rm, diff_new, diff_mv, diff_changed


def lit_list_organize_by_class(list_full):

	by_class = lit_book_ids

	# Iterate over volumes (journals and books)
	for ii in list(by_class.keys()):

		# Iterate over sub-volumes
		for jj in list(by_class[ii].keys()):

			# Add list for file objects
			item = by_class[ii][jj][lit_id_list] = []

	# Iterate over all files
	for ii in list_full:

		if ii[lit_id_bookid] in by_class.keys():
			if ii[lit_id_year] in by_class[ii[lit_id_bookid]].keys():

				by_class[ii[lit_id_bookid]][ii[lit_id_year]][lit_id_list].append(ii)

	return by_class


def lit_get_all_authors(list_full):

	authors = {}

	for ii in list_full:
		authors.update(ii[lit_id_authors])

	return authors


def lit_list_organize_author_relationship(list_full):

	authors = lit_get_all_authors(list_full)

	author_relationship = {}
	for author in list(authors.keys()):
		author_relationship.update({(author + lit_delimiter + authors[author]):{}})

	for publication in list_full:
		for author in list(publication[lit_id_authors].keys()):
			author_key = author + lit_delimiter + publication[lit_id_authors][author]
			for coauthor in list(publication[lit_id_authors].keys()):
				coauthor_key = (coauthor + lit_delimiter + publication[lit_id_authors][coauthor])
				if author_key != coauthor_key:
					if coauthor_key not in list(author_relationship[author_key].keys()):
						author_relationship[author_key].update({coauthor_key:{
							lit_id_coauthorscount:1,
							lit_id_year_start:int(publication[lit_id_year]),
							lit_id_year_end:int(publication[lit_id_year])
							}})
					else:
						author_relationship[author_key][coauthor_key][lit_id_coauthorscount] += 1
						if author_relationship[author_key][coauthor_key][lit_id_year_start] > int(publication[lit_id_year]):
							author_relationship[author_key][coauthor_key][lit_id_year_start] = int(publication[lit_id_year])
						if author_relationship[author_key][coauthor_key][lit_id_year_end] < int(publication[lit_id_year]):
							author_relationship[author_key][coauthor_key][lit_id_year_end] = int(publication[lit_id_year])

	return author_relationship


def lit_list_organize_by_name(list_full):

	authors = lit_get_all_authors(list_full)

	list_by_author = {}

	for name in list(authors.keys()):
		list_by_author.update({(name + lit_delimiter + authors[name]):[]})

	for publication in list_full:
		for name in list(publication[lit_id_authors].keys()):
			publication[lit_flag_firstauthor] = (name == publication[lit_id_firstauthor])
			list_by_author[name + lit_delimiter + publication[lit_id_authors][name]].append(publication.copy())

	return list_by_author


def lit_list_organize_by_keyword(list_full):

	list_by_keyword = {}

	for publication in list_full:
		for keyword in publication[lit_id_keywords]:
			list_by_keyword.update({keyword:[]})

	for publication in list_full:
		for keyword in publication[lit_id_keywords]:
			list_by_keyword[keyword].append(publication)

	return list_by_keyword


def lit_list_get_author_relationship_graph(list_by_relationship):

	relationships_graph = []
	graph_object = networkx.Graph()

	list_by_relationship_keys = list(list_by_relationship.keys())
	list_by_relationship_keys.sort()

	for ii in list_by_relationship_keys:

			list_by_relationship_sub_keys = list(list_by_relationship[ii].keys())
			list_by_relationship_sub_keys.sort()

			for jj in list_by_relationship_sub_keys:

				relationships_graph.append((ii.split(lit_delimiter)[1], jj.split(lit_delimiter)[1]))

	graph_object.add_edges_from(relationships_graph)

	return graph_object
