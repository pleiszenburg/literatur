# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/scripts/ui_filerename.py: GUI, renaming files w/ name pattern

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

import os
import shutil
from pprint import pformat as pf

from PyQt5 import QtCore, QtGui, QtWidgets

# from .file import *
from ..const import (
	MSG_DEBUG_FILEALREADYEXISTS,
	KNOWN_CLASSES_LIST
	)
from ..filetypes import filetypes
from ..parser import (
	filename_str_to_metaentry_dict,
	follows_filename_convention_guess,
	get_basic_userinput_str,
	metaentry_dict_to_filename_str,
	metaentry_dict_to_userinput_str,
	userinput_str_to_metaentry_dict
	)
from ..ui import ui_filename_dialog_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GUI CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ui_filerename_class(QtWidgets.QDialog):

	def __init__(self, parent = None):

		self.working_path = os.getcwd()

		# Initializing window
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = ui_filename_dialog_class()
		self.ui.setupUi(self)

		# Types of documents
		self.documenttypes = KNOWN_CLASSES_LIST # Fetch from API
		self.documenttypes.sort()
		self.ui.lwTypeCombo.addItems(self.documenttypes)

		# Types of files
		self.filetypes = filetypes.keys() # Fetch from API
		self.filetypes.sort()
		self.ui.lwFiletypeCombo.addItems(self.filetypes)

		# All files in repository
		self.reloadfilelist()

		# Events - selected file
		self.ui.lwFileList.itemSelectionChanged.connect(self.updateuserinput)

		# Event - new filename changed
		self.ui.lwFilenameText.textChanged.connect(self.trackfilenamechange)

		# Events - form changed, update (new) file name
		self.ui.lwTypeCombo.currentIndexChanged.connect(self.updatefilename)
		self.ui.lwYearSpin.valueChanged.connect(self.updatefilename)
		self.ui.lwMetaText.textChanged.connect(self.updatefilename)
		self.ui.lwFiletypeCombo.currentIndexChanged.connect(self.updatefilename)

		# Events - buttons
		self.ui.lwClearButton.clicked.connect(self.clearform)
		self.ui.lwMvButton.clicked.connect(self.movefile)
		self.ui.lwReload.clicked.connect(self.reloadfilelist)
		self.ui.lwOpenFile.clicked.connect(self.openfileinviewer)


	def openfileinviewer(self):

		pdf_file = os.path.join(
			self.working_path,
			self.ui.lwFileList.currentItem().data(0)
			)
		pdf_command = external_pdfviewer_command.replace(external_pdfviewer_file, pdf_file)
		os.system(pdf_command)


	def reloadfilelist(self):

		self.ui.lwFileList.clear()
		self.ui.lwFileList.addItems(get_dir_list(self.working_path)) # Fetch from API


	def movefile(self):

		oldname = str(self.ui.lwPathLine.toPlainText())
		newname = str(self.ui.lwFilenameText.toPlainText())

		if oldname != newname:

			if not os.path.isfile(os.path.join(self.working_path, newname)):

				# Move to target
				shutil.move(
					os.path.join(self.working_path, oldname),
					os.path.join(self.working_path, newname)
					)

				self.ui.lwFileList.currentItem().setText(newname)
				self.updateuserinput()

			else:

				msgBox = QtGui.QMessageBox()
				msgBox.setText(MSG_DEBUG_FILEALREADYEXISTS)
				msgBox.exec_()


	def clearform(self):

		self.ui.lwMetaText.setPlainText('')
		self.ui.lwFilenameText.setPlainText('')


	def trackfilenamechange(self):

		oldname = str(self.ui.lwPathLine.toPlainText())
		newname = str(self.ui.lwFilenameText.toPlainText())

		pal = QtGui.QPalette()

		if oldname != newname:
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(200, 160, 160))
		else:
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(160, 200, 160))

		self.ui.lwPathLine.setPalette(pal)


	def updateuserinput(self):

		filename_str = self.ui.lwFileList.currentItem().data(0)

		if follows_filename_convention_guess(filename_str):
			metaentry_dict = filename_str_to_metaentry_dict(filename_str)
			userinput_str = metaentry_dict_to_userinput_str(metaentry_dict)
		else:
			userinput_str = get_basic_userinput_str(filename_str)

		self.ui.lwPathLine.setPlainText(filename_str)
		self.ui.lwMetaText.setPlainText(userinput_str)


	def updatefilename(self):

		userinput_str = str(self.ui.lwMetaText.toPlainText())

		a_metaentry_dict = userinput_str_to_metaentry_dict(userinput_str)
		filename_str = metaentry_dict_to_filename_str(a_metaentry_dict)

		b_metaentry_dict, debug_message_str = filename_str_to_metaentry_dict(filename_str)
		b_metaentry_str = pf(b_metaentry_dict)

		self.ui.lwFilenameText.setPlainText(filename_str)
		self.ui.lwParserText.setPlainText(b_metaentry_str)

		pal = QtGui.QPalette()
		if debug_message_str != '':
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(200, 160, 160))
		else:
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
		self.ui.lwDebugText.setPlainText(debug_message_str)
		self.ui.lwDebugText.setPalette(pal)

	# Killing the app
	def exit_application(self):

		QtGui.QApplication.quit()
