# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/mediawiki.py: MediaWiki support

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
import pprint

from .strings import *

from wikitools import wiki, api, page


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MEDIAWIKI ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def wiki_login(w_url, w_user, w_pwd):

	print("Login ...")
	w_site = wiki.Wiki(w_url)
	w_site.login(w_user, w_pwd)
	print("... done.")

	return w_site


def wiki_logout(w_site):

	w_site.logout()


def wiki_get_edittoken(w_site):

	params = {'action':'tokens'}
	req = api.APIRequest(w_site, params)
	res = req.query(querycontinue = False)
	w_site_edittoken = res['tokens']['edittoken']

	print('token: ' + w_site_edittoken)

	return w_site_edittoken


def wiki_page_set_cnt(w_site, w_site_edittoken, p_title, p_content, p_summary):

	print("Upload ...")
	params = {
		'action':'edit',
		'title':p_title,
		'summary':p_summary,
		'text':p_content,
		'token':w_site_edittoken
		}
	req = api.APIRequest(w_site, params)
	res = req.query(querycontinue = False)
	print("... done.")

	pprint.pprint(res)
