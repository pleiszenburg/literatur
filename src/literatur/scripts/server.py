# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/scripts/server.py: Server daemon

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

import daemonocle

from ..const import (
	ADDRESS_LOCALHOST,
	FILE_DAEMON_PID,
	PATH_REPO,
	SECRET_HASH_LENGTH
	)
from ..repo import (
	find_root_path,
	repository_server_class
	)
from ..rpc import get_free_port


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def script_server(deamon_command):

	# Find root path: Raises an error if CWD is not in a repo
	repo_root_path = find_root_path(os.getcwd())

	# Fire up daemon
	lit_daemon = daemonocle.Daemon(
		pidfile = os.path.join(repo_root_path, PATH_REPO, FILE_DAEMON_PID),
		workdir = repo_root_path
		)

	server_p_dict = {
		KEY_ADDRESS: ADDRESS_LOCALHOST,
		KEY_PORT: get_free_port(),
		KEY_SECRET: __generate_secret__(),
		KEY_TERMINATE: ''
		}

	__store_secret__(repo_root_path, FILE_DAEMON_SECRET, server_p_dict[KEY_SECRET])

	repo_server = repository_server_class(server_p_dict = server_p_dict, daemon = lit_daemon)
	lit_daemon.worker = repo_server.run_server

	lit_daemon.do_action(deamon_command)


def __generate_secret__():

	return ('%0' + str(SECRET_HASH_LENGTH) + 'x') % random.randrange(16**SECRET_HASH_LENGTH)


def __store_secret__(repo_root_path, file_name, secret):

	f = open(os.path.join(repo_root_path, PATH_REPO, file_name), 'w+')
	f.write(secret)
	f.close()
