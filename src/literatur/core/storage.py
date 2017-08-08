#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *

from collections import OrderedDict
import pprint
import pickle


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STORAGE ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def lit_create_pickle(list_full, picklefile):
	
	ff = open(picklefile, 'wb+')
	pickle.dump(list_full, ff, -1)
	ff.close()


def lit_read_pickle(picklefile):
	
	ff = open(picklefile, 'rb')
	list_full = pickle.load(ff)
	ff.close()
	
	return list_full


def lit_write_plaintext(plaintext, textfile):
	
	ff = open(textfile, "w+")
	ff.write(plaintext) # .encode('utf-8')
	ff.close()


def lit_read_plaintext(textfile):
	
	ff = open(textfile, "r")
	plaintext = ff.read()
	ff.close()
	
	return plaintext


def lit_write_pprint(p_object, pfile):
	
	ff = open(pfile, "w+")
	pprint.pprint(p_object, stream=ff)
	ff.close()

