#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *
from lw_storage import *
from lw_index import *
from lw_report import *

import pprint

if networkx_on:
	import networkx


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
