# LITERATUR
# Literature management with Python, Dropbox and MediaWiki
# https://github.com/pleiszenburg/literatur
#
#	ui/makefile: GNU makefile for ui files
#
# 	Copyright (C) 2017 Sebastian M. Ernst <ernst@pleiszenburg.de>
#
# <LICENSE_BLOCK>
# The contents of this file are subject to the GNU Lesser General Public License
# Version 2.1 ("LGPL" or "License"). You may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
# https://github.com/pleiszenburg/literatur/blob/master/LICENSE
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
# specific language governing rights and limitations under the License.
# </LICENSE_BLOCK>

QTC        = pyuic5
QTC_FLAGS  = -i 0
QTC_SOURCE = $(wildcard *.ui)
QTC_TARGET = $(QTC_SOURCE:%.ui=%.py)
QTC_FLD    = ../src/literatur/ui

all: uifiles

uifiles: $(QTC_SOURCE)
	$(QTC) $(QTC_FLAGS) $(QTC_SOURCE) > $(QTC_FLD)/$(QTC_TARGET)
