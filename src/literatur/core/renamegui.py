# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/renamegui.py: GUI for renaming files with name pattern

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
import pprint

from PyQt5 import QtCore, QtGui, QtWidgets

from .strings import *
from .groups import *
from .file import *
from literatur.ui.filerename import Ui_lwFileRenameDialog


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# GUI CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class instance_class(QtWidgets.QDialog):

	def __init__(self, parent = None):

		self.working_path = lit_path_local

		# Initializing window
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_lwFileRenameDialog()
		self.ui.setupUi(self)

		# Types of documents
		self.documenttypes = lit_classes # Fetch from API
		self.documenttypes.sort()
		self.ui.lwTypeCombo.addItems(self.documenttypes)

		# Types of files
		self.filetypes = list_ext # Fetch from API
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
			lit_path_subfolder_lit,
			self.ui.lwFileList.currentItem().data(0)
			)
		pdf_command = external_pdfviewer_command.replace(external_pdfviewer_file, pdf_file)
		os.system(pdf_command)


	def reloadfilelist(self):

		self.ui.lwFileList.clear()
		self.ui.lwFileList.addItems(get_dir_list(
			os.path.join(self.working_path, lit_path_subfolder_lit)
			)) # Fetch from API


	def movefile(self):

		oldname = str(self.ui.lwPathLine.toPlainText())
		newname = str(self.ui.lwFilenameText.toPlainText())

		if oldname != newname:

			if not os.path.isfile(os.path.join(self.working_path, lit_path_subfolder_lit, newname)):

				# Move to target
				shutil.move(
					os.path.join(self.working_path, lit_path_subfolder_lit, oldname),
					os.path.join(self.working_path, lit_path_subfolder_lit, newname)
					)

				self.ui.lwFileList.currentItem().setText(newname)
				self.updateuserinput()

			else:

				msgBox = QtGui.QMessageBox()
				msgBox.setText(lw_debug_filealreadyexists)
				msgBox.exec_()


	def clearform(self):

		self.ui.lwMetaText.setPlainText("")
		self.ui.lwFilenameText.setPlainText("")


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

		# Get file from list
		item_text = self.ui.lwFileList.currentItem().data(0)

		self.ui.lwPathLine.setPlainText(item_text)
		self.ui.lwMetaText.setPlainText(generate_userinput(item_text))


	def updatefilename(self):

		lwFileObject = parse_userinput(str(self.ui.lwMetaText.toPlainText()))
		lwFileName = generate_filename(lwFileObject)

		lwFileParserObject, item_msg = filename_to_lit_object(lwFileName)
		lwFileParserObject_text = pprint.pformat(lwFileParserObject)

		self.ui.lwFilenameText.setPlainText(lwFileName)
		self.ui.lwParserText.setPlainText(lwFileParserObject_text)

		pal = QtGui.QPalette()
		if item_msg != '':
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(200, 160, 160))
		else:
			pal.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
		self.ui.lwDebugText.setPlainText(item_msg)
		self.ui.lwDebugText.setPalette(pal)

	# Killing the app
	def exit_application(self):

		QtGui.QApplication.quit()
