# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/storage.py: Stores and reads data structures

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
