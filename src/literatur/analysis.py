# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/analysis.py: Analyse the literature database

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

import os
import pprint

from .legacy.strings import (
	networkx_on, # TODO replace by config
	PATH_REPO,
	PATH_SUB_DB,
	FILE_DB_CURRENT,
	FILE_ANALYSIS_AUTHORNETWORKGRAPH
	)
from .legacy.groups import lit_book_ids
from .legacy.storage import lit_read_pickle
from .legacy.index import (
	lit_list_get_author_relationship_graph,
	lit_list_organize_author_relationship
	)
from .legacy.repository import find_root_dir_with_message

if networkx_on:
	import networkx


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_author_network():

	path_root = find_root_dir_with_message()

	# Load new index
	list_full = lit_read_pickle(os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_DB_CURRENT))

	# Reorganize index
	list_author_relationship = lit_list_organize_author_relationship(list_full)

	if networkx_on:

		# Generate content
		list_author_relationship_graph = lit_list_get_author_relationship_graph(list_author_relationship)

		# Write content to local file
		networkx.write_graphml(
			list_author_relationship_graph,
			os.path.join(path_root, PATH_REPO, PATH_SUB_DB, FILE_ANALYSIS_AUTHORNETWORKGRAPH)
			)
