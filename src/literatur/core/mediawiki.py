#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from lw_strings import *
from lw_groups import *

import pprint

from collections import OrderedDict

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

