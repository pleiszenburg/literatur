# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/dropbox.py: Dropbox support

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


from .strings import *
from .groups import lit_book_ids

import sys
import pprint

from collections import OrderedDict

import dropbox


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DROPBOX ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def dropbox_geturl(ff):

	try:

		dropbox_file = dropbox_client.share(ff, short_url=True)
		ff_url = dropbox_file['url']

	except:

		print("dropbox_geturl: some error", ff)
		ff_url = ''

	return ff_url


def dropbox_listfullupdate(list_full):

	list_new = []

	ic = 0

	for ii in list_full:

		ii[lit_id_url] = dropbox_geturl(lit_path_subfolder_lit + ii[lit_id_filename])
		list_new.append(ii)

		ic += 1
		sys.stdout.write("\rDropbox: %d. " % ic)
		sys.stdout.flush()

	return list_new


def dropbox_listpartialupdate(list_old_full, list_new_full):

	list_updated = []

	ic = 0

	for ii in list_new_full:

		exist_match = False
		old_url = ''

		for jj in list_old_full:

			match_filename = (ii[lit_id_filename] == jj[lit_id_filename])
			match_hash = (ii[lit_id_hash] == jj[lit_id_hash])

			if match_filename and match_hash:
				exist_match = True
				old_url = jj[lit_id_url]
				break

		if exist_match and old_url != '':
			ii[lit_id_url] = old_url
		else:
			ii[lit_id_url] = dropbox_geturl(lit_path_subfolder_lit + ii[lit_id_filename])

		list_updated.append(ii)

		ic += 1
		sys.stdout.write("\rDropbox: %d. " % ic)
		sys.stdout.flush()

	print(cnt_n)

	return list_updated


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# DROPBOX CLIENT INIT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

dropbox_client = dropbox.client.DropboxClient(dropbox_accesstoken)
