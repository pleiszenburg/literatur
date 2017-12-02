# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/ignore.py: Matching paths against ignore patterns

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

import pathspec

from ..const import (
	FILE_IGNORE,
	PATH_REPO
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class is_path_ignored_callable_class():


	def __init__(self, root_path):

		self.root_path = os.path.abspath(root_path)
		self.root_path_len = len(self.root_path) + 1 # +1 for tailing delimiter excluded by abspath

		try:
			f = open(os.path.join(self.root_path, PATH_REPO, FILE_IGNORE), 'r')
			ignore_spec_raw = f.read()
			f.close()
		except FileNotFoundError:
			ignore_spec_raw = ''

		ignore_spec_raw += '\n' + PATH_REPO # HACK make sure the repo folder is excluded by default

		self.ignore_spec = pathspec.PathSpec.from_lines(
			pathspec.patterns.GitWildMatchPattern,
			ignore_spec_raw.splitlines()
			)


	def __call__(self, full_in_path):

		# Just to be on the safe side ...
		abs_in_path = os.path.abspath(full_in_path)

		# Remove root path from in path
		abs_in_path_cut = abs_in_path[self.root_path_len:]

		# Match and return true/false
		return self.ignore_spec.match_file(abs_in_path_cut)
