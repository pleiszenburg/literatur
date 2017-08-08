#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from lw_strings import *
from lw_groups import *

import hashlib
import pprint
import sys
import os

from collections import OrderedDict


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STRING ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def filename_ext(fraw):
	
	fname = ''
	fext = ''
	
	# HACK handle upper case file formats
	list_all = list_ext + [x.upper() for x in list_ext]
	
	# Check for known file formats
	for ii in list_all:
		if fraw.endswith(ii):
			fext = ii
			fname = fraw[:-(len(fext) + 1)]
			break
	
	# No match, no file format ...
	if fname == '':
		fname = fraw
	
	return fext, fname


def clean_string(lString): # TODO strings must be moved to header file
	
	# Remove stuff left and right
	lString = lString.strip(' \n\t')
	
	# Tabs, underlines and line breaks etc become spaces
	for ii in '\t\n\'"”/()+,:_—–;<=>[\\]{|}&`‘’':
		lString = lString.replace(ii, " ")
	
	# Remove multiple spaces
	lString = ' '.join(lString.split())
	
	# Kill special alphabets
	for ii in list(list_letters_replace.keys()):
		lString = lString.replace(ii, list_letters_replace[ii])
	
	# Remove remaining special characters ...
	for ii in '!$%&*.?@^°':
		lString = lString.replace(ii, "")
	
	# Finally spaces become dashes and vice versa
	lString = lString.replace(" ", "-")
	lString = lString.replace("-", " ")
	
	# Remove multiple space
	lString = ' '.join(lString.split())
	
	return lString


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# FOLDER AND LIST ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def hashfile(apath, hasher, blocksize=65536):
	
	afile = open(apath, 'rb')
	
	buf = afile.read(blocksize)
	
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	
	afile.close()
	
	return hasher.hexdigest()


def string_to_authors_dict(authors):
	
	temp_list = authors.replace('-', ' ').split(' ')
	
	authors_list = OrderedDict()
	temp_author = ''
	temp_author_k = ''
	flag_first = False
	first_author = ''
	authors_etal = False
	
	for jj in temp_list:
		if (jj not in list_authors_exclude) and (not jj.isdigit()) and (len(jj) > 0):
			if jj[0].islower():
				temp_author += jj + ' '
				temp_author_k += '_' + jj
			else:
				id_count = 1
				while (jj + temp_author_k + '_' + str(id_count)) in list(authors_list.keys()):
					id_count += 1
				jj_id = jj + temp_author_k + '_' + str(id_count)
				authors_list.update({jj_id:(temp_author + jj)})
				if not flag_first:
					first_author = jj_id
					flag_first = True
				temp_author = ''
				temp_author_k = ''
		if jj == lit_authors_etal:
			authors_etal = True
	
	return first_author, authors_list, authors_etal


def string_to_keywords_list(title):
	
	temp_list = title.replace('-', ' ').lower().split(' ')
	
	keywords_list = []
	
	for ii in temp_list:
		if (ii not in keywords_list) and (ii not in list_alphabet_low) and (ii not in list_keywords_exclude):
			if (not ii.isdigit()) and (not any(x in ii for x in string_numbers)):
				keywords_list.append(ii)
	
	return keywords_list


def lit_get_book_from_bookid(year, bookid):
	
	item_book = ''
	item_editors = OrderedDict()
	item_type = ''
	
	if bookid in lit_book_ids:
		if year in lit_book_ids[bookid]:
			item_book = lit_book_ids[bookid][year][lit_id_title]
			item_type = lit_book_ids[bookid][year][lit_id_type]
			if lit_id_editors in lit_book_ids[bookid][year]:
				_, item_editors, _ = string_to_authors_dict(lit_book_ids[bookid][year][lit_id_editors])
	
	return item_book, item_editors, item_type


def parse_userinput(lwInput):
	
	lwFragments = lwInput.split(input_delimiter)
	
	# Step 1: Class
	item_class = lit_class_default
	if len(lwFragments) > 0:
		item_class = clean_string(lwFragments[0]).upper().replace(" ", "-")
		# Only known classes, otherwise default class
		if item_class not in lit_classes:
			item_class = lit_class_default
	
	# Step 2: Year
	item_year = lit_year_default
	item_bookid = ''
	item_book = ''
	item_editors = ''
	item_type = ''
	item_section = ''
	if len(lwFragments) > 1:
		item_year_f = clean_string(lwFragments[1])
		if len(item_year_f) > 3:
			# Is year a number? Go back to default if not
			if item_year_f[:4].isdigit():
				item_year = item_year_f[:4]
				# Check for unrealistic years
				if int(item_year) > 2100 or int(item_year) < 1000:
					item_year = lit_year_default
				# Fetch books etc
				if len(item_year_f) > 4:
					item_book_s = item_year_f[4:].split(input_delimiter2)
					item_bookid = item_book_s[0].strip(' ').replace(" ", "-")
					item_book, item_editors, item_type = lit_get_book_from_bookid(item_year, item_bookid)
					if len(item_book_s) > 1:
						item_section = item_book_s[1].strip(' ')
	
	# Step 3: Authors
	item_authors_d = lit_authors_default
	if len(lwFragments) > 2:
		item_authors_d = clean_string(lwFragments[2])
		if len(item_authors_d) == 0:
			item_authors_d = lit_authors_default
	# Generate author dictionary
	item_first, item_names, item_etal = string_to_authors_dict(item_authors_d.replace(" ", "-"))
	
	# Step 4: Title
	item_title_d = lit_title_default
	if len(lwFragments) > 3:
		item_title_d = clean_string(lwFragments[3])
		if len(item_title_d) == 0:
			item_title_d = lit_title_default
	
	# Step 5: Annotation
	item_ann_d = lit_ann_default
	if len(lwFragments) > 4:
		item_ann_d = clean_string(lwFragments[4])
		if len(item_ann_d) == 0:
			item_ann_d = lit_ann_default
	
	# Step 6: File format
	item_fileformat = lit_fileformat_default
	if len(lwFragments) > 5:
		item_fileformat = lwFragments[5].replace(".", " ")
		item_fileformat = clean_string(item_fileformat).replace(" ", ".").lower()
		if item_fileformat not in list_ext:
			item_fileformat = lit_fileformat_default
	
	# Build object
	lwObject = {
		lit_id_class:item_class,
		lit_id_year:item_year,
		lit_id_authors_d:item_authors_d,
		lit_id_authors:item_names,
		lit_id_book:item_book,
		lit_id_bookid:item_bookid,
		lit_id_editors:item_editors,
		lit_id_type:item_type,
		lit_id_section:item_section,
		lit_id_firstauthor:item_first,
		lit_id_flag_etal:item_etal,
		lit_id_title_d:item_title_d,
		lit_id_ann_d:item_ann_d,
		lit_id_fileformat:item_fileformat
		}
	
	return lwObject


def generate_filename(lwObject):
	
	# Left of author block: Class, year, book and section
	lFile_lAuthor = lwObject[lit_id_class] + "_" + lwObject[lit_id_year]
	if lwObject[lit_id_bookid] != '':
		lFile_lAuthor += "." + lwObject[lit_id_bookid]
		if lwObject[lit_id_section] != '':
			lFile_lAuthor += "." + lwObject[lit_id_section].replace(" ", "-")
	lFile_lAuthor += "_"
	
	# Right of author block: Title, annotation, file format
	lFile_rAuthor = "_" + lwObject[lit_id_title_d].replace(" ", "-")
	if lwObject[lit_id_ann_d] != '':
		lFile_rAuthor += "_" + lwObject[lit_id_ann_d].replace(" ", "-")
	lFile_rAuthor += "." + lwObject[lit_id_fileformat]
	
	# Length of filename without author block
	lFile_len = len(lFile_lAuthor) + len(lFile_rAuthor)
	# Length of author block
	lFile_author_len = 0
	# Empty author string
	lFile_Author = ''
	
	# Iterate over authors
	check_etal = False
	for uu in list(lwObject[lit_id_authors].keys()):
		uu_temp = lwObject[lit_id_authors][uu].replace(" ", "-") + "-"
		if (lFile_len + lFile_author_len + len(uu_temp) + len(lit_authors_etal)) <= lit_filename_maxlength:
			lFile_author_len += len(uu_temp)
			lFile_Author += uu_temp
		else:
			lFile_author_len += len(lit_authors_etal)
			lFile_Author += lit_authors_etal
			check_etal = True
			break
	# ETAL flag from object?
	if not check_etal and lwObject[lit_id_flag_etal]:
		lFile_author_len += len(lit_authors_etal)
		lFile_Author += lit_authors_etal
		check_etal = True
	
	lFile_Author = lFile_Author.strip('-')
	
	lFile = lFile_lAuthor + lFile_Author + lFile_rAuthor
	
	return lFile


def generate_userinput(item_filename):
	
	userinput_d = []
	
	if follow_convention_guess(item_filename):
		
		lwObject, _ = filename_to_lit_object(item_filename)
		
		userinput_d.append(lwObject[lit_id_class])
		userinput_d.append(cnt_n)
		userinput_d.append(input_delimiter)
		userinput_d.append(cnt_n)
		userinput_d.append(lwObject[lit_id_year])
		if lwObject[lit_id_bookid] != '':
			userinput_d.append(' ' + lwObject[lit_id_bookid])
			if lwObject[lit_id_section] != '':
				userinput_d.append(' ' + input_delimiter2 + ' ' + lwObject[lit_id_section].replace(".", " "))
		userinput_d.append(cnt_n)
		userinput_d.append(input_delimiter)
		userinput_d.append(cnt_n)
		for uu in list(lwObject[lit_id_authors].keys()):
			userinput_d.append(lwObject[lit_id_authors][uu] + ' ')
		if lwObject[lit_id_flag_etal]:
			userinput_d.append(lit_authors_etal + ' ')
		userinput_d.append(cnt_n)
		userinput_d.append(input_delimiter)
		userinput_d.append(cnt_n)
		userinput_d.append(lwObject[lit_id_title])
		userinput_d.append(cnt_n)
		userinput_d.append(input_delimiter)
		userinput_d.append(cnt_n)
		if lwObject[lit_id_ann] != '':
			userinput_d.append(lwObject[lit_id_ann])
		userinput_d.append(cnt_n)
		userinput_d.append(input_delimiter)
		userinput_d.append(cnt_n)
		userinput_d.append(lwObject[lit_id_fileformat].lower())
		userinput_d.append(cnt_n)
		
		userinput = ''.join(userinput_d)
		
	else:
		
		fext, fname = filename_ext(item_filename)
		userinput = cnt_n + fname + cnt_n + input_delimiter + cnt_n + fext + cnt_n
	
	return userinput


def follow_convention_guess(item_filename):
	
	# Try *quick* guess if this might be a filename following the convention
	isfilename = False
	
	# Breake file name into items
	items = item_filename.split('_')
	
	if len(items) > 2:
		if items[0] in lit_classes:
			if len(items[1]) > 3:
				if items[1][:4].isdigit():
					# It likely follows the pattern
					isfilename = True
	
	return isfilename


def shorten_filename(item_filename):
	
	len_cut = 80
	
	if len(item_filename) > len_cut:
		fext, fname = filename_ext(item_filename)
		short_name = fname[:(len_cut - 10)] + '...' + fname[-6:]
		if fext != '':
			short_name += '.' + fext
	else:
		short_name = item_filename
	
	return short_name


def filename_to_lit_object(item_filename):
	
	# Debug messages
	item_msg = []
	
	# Check length filename
	if len(item_filename) > lit_filename_maxlength:
		item_msg.append(lw_debug_filenametoolong + ': ' + shorten_filename(item_filename) + cnt_n)
	
	# Split filename and extention
	item_fileformat, item_filename_clean = filename_ext(item_filename)
	if item_fileformat == '':
		item_msg.append(lw_debug_unknownformat + ': ' + shorten_filename(item_filename) + cnt_n)
	
	# Breake file name into items
	items = item_filename_clean.split('_')
	
	# Set empty hash
	item_hash = ''
	
	# Set empty file size
	item_size = 0
	
	# Set empty (Dropbox) URL
	item_url = ''
	
	# 1st item: Class
	item_class = items[0]
	if item_class not in lit_classes:
		item_msg.append(lw_debug_unknownclass + ': ' + item_class + ' (' + shorten_filename(item_filename) + ')' + cnt_n)
	
	# 2nd item: Year, series, section
	items_block = items[1].split('.')
	item_year = items_block[0]
	if len(items_block) > 1:
		item_bookid = items_block[1]
		item_book, item_editors, item_type = lit_get_book_from_bookid(item_year, item_bookid)
		if item_bookid not in list(lit_book_ids.keys()):
			item_msg.append(lw_debug_unknownvolume + ': ' + item_bookid + ' (' + shorten_filename(item_filename) + ')' + cnt_n)
	else:
		item_bookid = ''
		item_book = ''
		item_type = ''
		item_editors = OrderedDict()
	if len(items_block) > 2:
		item_section = items_block[2].replace('-', '.')
	else:
		item_section = ''
	
	# 3rd item: Authors
	item_first, item_names, item_etal = string_to_authors_dict(items[2])
	
	# 4th item: Title
	if len(items) > 3:
		item_title = items[3].replace('-', ' ')
		item_keywords = string_to_keywords_list(item_title)
		if len(item_title) < 12 and item_title.split(' ')[0] not in list_publication_special:
			item_msg.append(lw_debug_shorttitle + ': ' + shorten_filename(item_filename) + cnt_n)
	else:
		item_msg.append(lw_debug_notitle + ': ' + shorten_filename(item_filename) + cnt_n)
		item_title = lit_title_default
		item_keywords = []
	# Handle special titles, frontmatters etc
	if item_title.split(' ')[0] in list_publication_special:
		item_flag_sp = True
	else:
		item_flag_sp = False
	
	# Deal with special files, frontmatters etc - TODO remove this section eventually
	if items[2].split('-')[0] in list_publication_special:
		item_title = '[' + items[2].replace('-', ' ') + ']'
		item_msg.append(lw_debug_deprecatedtitle + ': ' + item_title + ' (' + shorten_filename(item_filename) + ')' + cnt_n)
		# item_flag_sp = True
	# else:
		# item_flag_sp = False
	
	# 5th item: Annotations (optional)
	if len(items) > 4:
		item_ann = items[4]
		if len(items) > 5:
			item_ann_d = items[5:]
			for zz in item_ann_d:
				item_ann += ' ' + zz
		if item_ann not in list_ann:
			item_msg.append(lw_debug_annotation + ': ' + item_ann + ' (' + shorten_filename(item_filename) + ')' + cnt_n)
	else:
		item_ann = ''
	
	# Build object
	item_ii = {
		lit_id_class:item_class,
		lit_id_year:item_year,
		lit_id_book:item_book,
		lit_id_bookid:item_bookid,
		lit_id_editors:item_editors,
		lit_id_type:item_type,
		lit_id_section:item_section,
		lit_id_authors:item_names,
		lit_id_firstauthor:item_first,
		lit_id_flag_etal:item_etal,
		lit_id_title:item_title,
		lit_id_keywords:item_keywords,
		lit_id_ann:item_ann,
		lit_id_filename:item_filename,
		lit_id_fileformat:item_fileformat,
		lit_id_url:item_url,
		lit_flag_sp:item_flag_sp,
		lit_id_size:item_size,
		lit_id_hash:item_hash
		}
	
	# Handle debug messages
	item_msg = ''.join(item_msg)
	item_msg = item_msg.strip(' \n\t')
	
	return item_ii, item_msg


def lit_listpartialupdate_hashsize(list_full, working_path):
	
	list_updated = []
	
	ic = 0
	
	for ii in list_full:
		
		# Hash file content
		ii[lit_id_hash] = hashfile(os.path.join(working_path + lit_path_subfolder_lit + ii[lit_id_filename]), hashlib.sha256())
		
		# Get file sizelString
		ii[lit_id_size] = os.path.getsize(working_path + lit_path_subfolder_lit + ii[lit_id_filename])
		
		list_updated.append(ii)
	
		ic += 1
		sys.stdout.write("\r" + lw_debug_hash + ": %d. " % ic)
		sys.stdout.flush()
	
	print(cnt_n)
	
	return list_updated


def get_dir_list(lpath):
	
	llist = []
	
	# List all files in folder
	temp_list = os.listdir(lpath)
	
	# Clean list
	for ii in temp_list:
		if os.path.isfile(os.path.join(lpath, ii)) and ('desktop.ini' not in ii) and ('dropbox' not in ii):
			llist.append(ii)
	
	# Sort them all
	llist.sort()
	
	return llist


def lit_get_list(working_path):
	
	ic = 0
	
	lit_list = []

	# Build path to literature
	lit_path = working_path + lit_path_subfolder_lit
	
	# Get list of files, cleaned
	temp_list = get_dir_list(lit_path)
	
	for ii in temp_list:
		
		# Generate object
		item_ii, item_msg = filename_to_lit_object(ii)
		
		# Append object to list
		lit_list.append(item_ii)
		
		ic += 1
		sys.stdout.write("\r" + lw_debug_index + ": %d. " % ic)
		sys.stdout.flush()
	
		# Print debug messages
		if item_msg != '':
			print(item_msg)
		
	print(cnt_n)
	
	return lit_list

