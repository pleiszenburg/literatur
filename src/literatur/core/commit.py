#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from lw_strings import *
from lw_groups import *

import os
import shutil
import time
import pprint


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES?
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def commit_push(c_original, c_target, working_path):
	
	# If previous commit exists, kill it
	if os.path.isfile(c_target):
		os.remove(c_target)
	
	# Copy original to target
	shutil.copyfile(
		working_path + lit_path_subfolder_db + c_original,
		working_path + lit_path_subfolder_db + c_target
		)


def commit_backup(commit_file, working_path):
	
	# Get creation time of file
	ctime = os.path.getmtime(working_path + lit_path_subfolder_db + commit_file)
	
	# Form string from creation time
	ctime_string = commit_datestring(ctime)
	
	# Create new file name with creation time
	commit_file_target = commit_file.replace('.', '_' + ctime_string + '.');
	
	# Copy file for backup
	shutil.copyfile(
		working_path + lit_path_subfolder_db + commit_file,
		working_path + lit_path_subfolder_dbbackup + commit_file_target
		)


def commit_datestring(ctime):
	
	# Get time in sec, convert to GMT and time object
	ctime_object = time.gmtime(ctime)
	
	# Convert time object into string
	ctime_string = "{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}".format(
		ctime_object.tm_year, ctime_object.tm_mon, ctime_object.tm_mday, ctime_object.tm_hour, ctime_object.tm_min, ctime_object.tm_sec
		)
	
	return ctime_string

