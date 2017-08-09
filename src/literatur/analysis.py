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

import pprint

from .core.strings import *
from .core.groups import lit_book_ids
from .core.storage import *
from .core.index import *
from .core.report import *

if networkx_on:
	import networkx


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_author_network():

	lit_working_path = lit_path_local # TODO read path from config

	# Load new index
	lit_list_full_new = lit_read_pickle(lit_working_path + lit_path_subfolder_db + lit_path_pickle_new)

	# Reorganize index
	lit_list_author_relationship = lit_list_organize_author_relationship(lit_list_full_new)

	if networkx_on:

		# Generate content
		lit_list_author_relationship_graph = lit_list_get_author_relationship_graph(lit_list_author_relationship)

		# Write content to local file
		networkx.write_graphml(lit_list_author_relationship_graph, lit_working_path + lit_path_subfolder_db + lit_path_report_new_network_authorrelationship)
