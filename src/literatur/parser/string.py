# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/parser/string.py: Cleaning and converting strings

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

from ..const import LETTER_SUB_DICT


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def clean_str(in_str):

	# Remove stuff left and right
	out_str = in_str.strip(' \n\t')

	# Tabs, underlines and line breaks etc become spaces
	for ii in '\t\n\'"”/()+,:_—–;<=>[\\]{|}&`‘’':
		out_str = out_str.replace(ii, ' ')

	# Remove multiple spaces
	out_str = ' '.join(out_str.split())

	# Kill special alphabets
	for ii in LETTER_SUB_DICT.keys():
		out_str = out_str.replace(ii, LETTER_SUB_DICT[ii])

	# Remove remaining special characters ...
	for ii in '!$§#%&*.?@^°':
		out_str = out_str.replace(ii, '')

	return out_str
