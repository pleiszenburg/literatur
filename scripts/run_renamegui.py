#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui

from lw_renamegui import *


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# RUN GUI / APP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
	
	app = QtGui.QApplication(sys.argv)
	app_mainwindow = lw_instance_class()
	app_mainwindow.show()
	sys.exit(app.exec_())
