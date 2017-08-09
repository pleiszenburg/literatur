# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/core/strings.py: Strings constants

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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# STATIC STRINGS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

PATH_ROOT = os.getcwd() # HACK TODO root path of current project, should be config
# lit_path_external = 'LIBRARY-external' # HACK compatibility for old script

PATH_SUB_DB = 'db'
PATH_SUB_DBBACKUP = 'db/backup'
PATH_SUB_LIT = 'lit'

KEY_CURRENT = 'current'
KEY_JOURNAL = 'journal'
KEY_MASTER = 'master'

FILE_DB_CURRENT = 'lw_index_%s.pkl' % KEY_CURRENT # stage 1
FILE_DB_JOURNAL = 'lw_index_%s.pkl' % KEY_JOURNAL # stage 2
FILE_DB_MASTER = 'lw_index_%s.pkl' % KEY_MASTER # stage 3

KEY_RM = 'rm'
KEY_NEW = 'new'
KEY_MV = 'mv'
KEY_CHANGED = 'changed'

wiki_page_indexfull = 'Literature Index Overview'
wiki_page_indexbyclass = 'Literature Index by Class'
wiki_page_indexbyname = 'Literature Index by Author'
wiki_page_indexbykeyword = 'Literature Index by Keyword'
wiki_page_authorrelationship = 'Literature Author Relationship'

lw_debug_filenametoolong = 'Filename too long'
lw_debug_unknownformat = 'Unknown format'
lw_debug_shorttitle = 'Short title'
lw_debug_deprecatedtitle = 'Deprecated special title'
lw_debug_notitle = 'No title'
lw_debug_unknownvolume = 'Unknown volume'
lw_debug_unknownclass = 'Unknown class'
lw_debug_annotation = 'Unexpected annotation'
lw_debug_hash = 'Hash'
lw_debug_duplicates = 'Duplicates'
lw_debug_index = 'Index'
lw_debug_filealreadyexists = "File already exists."

FILE_ANALYSIS_AUTHORNETWORKGRAPH = 'author_network_graph.graphml'

wiki_on = False
wiki_url = '' # 'http://www.somedomain.com/wiki/api.php' # Must point to MediaWiki API php-file
wiki_user = '' # user name
wiki_pwd = '' # password

dropbox_on = False
dropbox_appkey = '' # app key
dropbox_appsecret = '' # app secret
dropbox_accesstoken = '' # access token
dropbox_userid = '' # user id (numer as string)

networkx_on = True

external_pdfviewer_file = '[file]'
external_pdfviewer_command = "okular '" + external_pdfviewer_file + "' &"

cnt_bot_version = 'R15'
cnt_message_bot = "''Do not edit, managed by bot: [[User:" + wiki_user + "|" + wiki_user + "]] (" + cnt_bot_version + ").''"
cnt_category_lit = '[[Category:Literature]]'
cnt_cmd_notoc = '__NOTOC__ '
cnt_n = '\n'
# cnt_tag_begin = u'<!-- BEGIN -->'
# cnt_tag_end = u'<!-- END -->'

lit_class_default = 'AA'
lit_year_default = str(1000)
lit_authors_default = 'ANONYMOUS'
lit_authors_etal = 'ETAL'
lit_title_default = 'NOTITLE'
lit_ann_default = ''
lit_fileformat_default = 'pdf'

lit_filename_maxlength = 255 # EXT4 & NTFS

lit_class_chapter = 'CHAPTER'
lit_class_book = 'BOOK'
lit_class_proceedings = 'PROCEEDINGS'
lit_class_journal = 'JOURNAL'

# TODO improve the following and the above statement
lit_classes_sp = [
	lit_class_chapter, lit_class_book, lit_class_proceedings, lit_class_journal
	]
lit_classes = [
	lit_class_chapter, lit_class_book, lit_class_proceedings, lit_class_journal,
	"ABSTRACT", "ABSTRACTS", "PAPER", "ANNOUNCEMENT",
	"ARTICLE", "LETTER", "MANUAL", "NOTE", "PATENT", "POSTER",
	"PRESENTATION", "REPORT", "RESOLUTION", "SCRIPT", "THESIS",
	"THESIS-MSC", "THESIS-BSC", "THESIS-PHD", "THESIS-DIPLOMA",
	"WEB", "PROPOSAL", "DATASHEET", "SPEECH", "SPEC",
	"TUTORIAL", "STANDARD", "REVIEW", "DATA", "CALL"
	]

lit_id_class = 'item_class'
lit_id_year = 'item_year'
lit_id_authors = 'item_authors'
lit_id_firstauthor = 'item_firstauthor'
lit_id_title = 'item_title'
lit_id_keywords = 'item_keywords'
lit_id_ann = 'item_annotation'

lit_id_title_d = 'title_d'
lit_id_authors_d = 'authors_d'
lit_id_ann_d = 'annotation_d'

lit_id_editors = 'volume_editors'
lit_id_book = 'volume_title'
lit_id_bookid = 'volume_id'
lit_id_type = 'volume_type'
lit_id_section = 'volume_section'

lit_id_filename = 'file_name'
lit_id_fileformat = 'file_format'
lit_id_url = 'file_url'
lit_id_size = 'file_size'
lit_id_hash = 'file_hash'

lit_id_flag_etal = 'flag_etal'
lit_flag_sp = 'flag_special'

lit_flag_firstauthor = 'flag_firstauthor'
lit_id_year_start = 'year_start'
lit_id_year_end = 'year_end'
lit_id_coauthorscount = 'co_authors_count'
lit_delimiter = ';'
lit_id_list = 'items_list'

lit_id_filename_new = 'filename_new'
lit_id_hash_new = 'hash_new'

list_ext = ["pdf", "doc", "docx", "odt", "epub", "ps.gz", "ps", "eps", "djvu", "xps", "ppt", "pptx", "txt", "key", "gif", "png", "jpg", "jpeg", "tiff"]

list_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
list_alphabet_low = [x.lower() for x in list_alphabet]
string_numbers = '1234567890'

input_delimiter = '#'
input_delimiter2 = '~'

list_publication_special = ['plate', 'frontmatter', 'backmatter']
list_authors_exclude = [lit_authors_etal, 'plate', 'frontmatter', 'backmatter', 'hires']
list_keywords_exclude = ['advanced', 'advances', 'analyses', 'analysis', 'annual', 'an', 'among', 'all', 'and', 'of', 'with',
	'anomalous', 'anomaly', 'approach', 'approaches', 'approximation', 'are', 'around', 'articles', 'another', 'as', 'assessing',
	'assessment', 'asset', 'assets', 'associated', 'at', 'au', 'available', 'back', 'based', 'basic', 'bd', 'be', 'become',
	'behavior', 'behaviour', 'benefits', 'best', 'better', 'between', 'beyond', 'big', 'brief', 'briefing', 'build', 'building',
	'built', 'by', 'can', 'capabilities', 'capability', 'capable', 'case', 'causes', 'ce', 'certify', 'chief', 'ci', 'ck',
	'close', 'cm', 'cmas', 'comprehensive', 'concept', 'concepts', 'conceptual', 'concerning', 'concerns', 'conclusion',
	'conjugated', 'considerations', 'content', 'context', 'continued', 'contribution', 'corrected', 'cr', 'on', 'data', 'de',
	'days', 'december', 'der', 'des', 'details', 'developing', 'easily', 'for', 'from', 'high', 'hires', 'development', 'do',
	'does', 'due', 'during', 'early', 'how', 'ii', 'iii', 'im', 'in', 'inside', 'into', 'is', 'it', 'its', 'iv', 'low',
	'made', 'new', 'no', 'non', 'october', 'off', 'one', 'ongoing', 'only', 'onto', 'or', 'our', 'plate', 'pre', 're',
	'results', 'short', 'small', 'smaller', 'soon', 'study', 'system', 'take', 'than', 'that', 'the', 'their', 'them',
	'three', 'to', 'tp', 'tr', 'two', 'um', 'und', 'under', 'up', 'update', 'upon', 'vi', 'vii', 'viii', 'vs', 'we',
	'what', 'who', 'will', 'without', 'zu', 'end', 'highly', 'imply', 'importance', 'important', 'improved', 'improvement',
	'increasing', 'independent', 'indicate', 'initial', 'just', 'known', 'knowledge', 'large', 'largest', 'left', 'let', 'like',
	'long', 'looking', 'lower', 'lucky', 'mid', 'not', 'novel', 'other', 'over', 'proper', 'recap', 'realizing', 'realize',
	'reality', 'realities', 'realistic', 'real', 'recent', 'revealed', 'reveals', 'second', 'six', 'success', 'successful',
	'understanding', 'understand', 'understood', 'unknown', 'viable', 'yet'] # TODO expand

list_ann = ['OCR', 'WATERMARKED-DO-NOT-DISTRIBUTE', 'PREPRINT', 'SM', 'SM-PREPRINT']

list_letters_replace = {
	"ä":"ae", "Ä":"Ae", "ö":"oe", "Ö":"Oe", "ü":"ue", "Ü":"Ue",
	"é":"e", "É":"E", "è":"e", "È":"E",
	"á":"a", "Á":"A", "à":"a", "À":"A", "Á":"A", "À":"A",
	"ĉ":"c", "Ĉ":"C",
	"ß":"ss", "š":"s",
	"ﬀ":"ff", "ﬁ":"fi", "ﬂ":"fl",
	"í":"i",
	"µ":"u",
	"ñ":"n"
	}
