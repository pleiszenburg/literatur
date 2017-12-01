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

import logging
import os
import random

import daemonocle
import psutil

from ..const import (
	ADDRESS_LOCALHOST,
	FILE_DAEMON_LOG,
	FILE_DAEMON_PID,
	FILE_DAEMON_PORT,
	FILE_DAEMON_SECRET,
	KEY_ADDRESS,
	KEY_DAEMON,
	KEY_PORT,
	KEY_SECRET,
	KEY_TERMINATE,
	PATH_REPO,
	PATH_SUB_LOGS,
	SECRET_HASH_LENGTH
	)
from ..errors import no_pid_error
from ..repo import (
	find_root_path,
	repository_class
	)
from ..rpc import (
	get_free_port,
	mp_client_class
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_repo_client():
	"""Returns either a client on a running server daemon or a temporary server
	"""

	# Find root path: Raises an error if CWD is not in a repo
	repo_root_path = find_root_path(os.getcwd())

	try:
		pid = __load_pid__(repo_root_path)
		daemon_up = True
	except no_pid_error:
		daemon_up = False

	if daemon_up:

		daemon_port = int(__load_repo_info__(repo_root_path, '%s.%d' % (FILE_DAEMON_PORT, pid)))
		daemon_secret = __load_repo_info__(repo_root_path, '%s.%d' % (FILE_DAEMON_SECRET, pid))

		return mp_client_class(
			(ADDRESS_LOCALHOST, daemon_port),
			daemon_secret
			)

	else:

		return repository_class(
			repo_root_path,
			__generate_logger__(repo_root_path)
			)


def get_daemon_pid():
	"""Returns pid if daemon is up and None if daemon is down
	"""

	# Find root path: Raises an error if CWD is not in a repo
	repo_root_path = find_root_path(os.getcwd())

	# Get the pit and return status
	try:
		return __load_pid__(repo_root_path)
	except no_pid_error:
		return None


def script_daemon(deamon_command):
	"""Starts, stops or checks status of daemon (user commands)
	"""

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
		KEY_TERMINATE: None
		}

	repo_server = repository_class(
		repo_root_path,
		logger = __generate_logger__(repo_root_path),
		server_p_dict = server_p_dict,
		daemon = lit_daemon
		)
	lit_daemon.worker = repo_server.run_server
	# lit_daemon.shutdown_callback = repo_server.__terminate__

	lit_daemon.do_action(deamon_command)


def __generate_logger__(repo_root_path):

	# create logger with 'spam_application'
	logger = logging.getLogger(KEY_DAEMON)
	logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	fh = logging.FileHandler(
		os.path.join(repo_root_path, PATH_REPO, PATH_SUB_LOGS, FILE_DAEMON_LOG)
		)
	fh.setLevel(logging.DEBUG)

	# create formatter and add it to the handlers
	formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
	fh.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(fh)

	return logger


def __generate_secret__():

	return ('%0' + str(SECRET_HASH_LENGTH) + 'x') % random.randrange(16**SECRET_HASH_LENGTH)


def __load_pid__(repo_root_path):

	try:
		pid_data = __load_repo_info__(repo_root_path, FILE_DAEMON_PID)
	except FileNotFoundError:
		raise no_pid_error()

	try:
		pid = int(pid_data)
	except ValueError:
		raise no_pid_error()

	if pid is not None and psutil.pid_exists(pid):
		return pid
	else:
		os.remove(pid_path)
		raise no_pid_error()


def __load_repo_info__(repo_root_path, file_name):

	f = open(os.path.join(repo_root_path, PATH_REPO, file_name), 'r')
	info = f.read()
	f.close()

	return info
