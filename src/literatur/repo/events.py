# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/events.py: File system event handling

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

from functools import partial
from pprint import pformat as pf
from threading import Thread

import pyinotify

from ..const import (
	KEY_HANDLER,
	KEY_LOGGER
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class fs_event_notifier_class:


	def __init__(self, event_handler, root_path, exclude_filter_list, is_path_ignored_func, logger):

		self.logger = logger
		self.root_path = root_path

		self.notifier_wm = pyinotify.WatchManager()

		self.notifier_raw_handler = __handle_raw_fs_event_callable_class__(
			event_handler,
			root_path,
			is_path_ignored_func,
			logger
			)

		self.notifier = pyinotify.Notifier(
			self.notifier_wm, __repo_event_handler_class__(**{
				KEY_HANDLER: self.notifier_raw_handler,
				KEY_LOGGER: logger
				})
			)

		self.notifier_repo = self.notifier_wm.add_watch(
			root_path,
			pyinotify.ALL_EVENTS,
			rec = True,
			auto_add = True,
			exclude_filter = pyinotify.ExcludeFilter(exclude_filter_list)
			)

		self.notifier_thread = Thread(target = self.notifier.loop)
		self.notifier_thread.daemon = True


	# def get_flags(self):
    #
	# 	return {v: k for k, v in pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS'].items()}
	# 	return pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']


	def start(self):

		self.notifier_thread.start()


class __handle_raw_fs_event_callable_class__:


	def __init__(self, event_handler, root_path, is_path_ignored_func, logger):

		self.event_handler = event_handler
		self.is_path_ignored_func = is_path_ignored_func
		self.logger = logger
		self.root_path = root_path

		# self.pending_events = []


	def __call__(self, event_code, raw_event):

		# # Ignore events on directories
		# if raw_event.dir:
		# 	return

		# Ignore files and directories from ignore list
		if self.is_path_ignored_func(raw_event.pathname):
			return

		# Get move cookie
		_cookie = -1
		if hasattr(raw_event, 'cookie'):
			_cookie = raw_event.cookie

		# Log the raw_event ([cookie] raw_event code, raw_event name, full path)
		self.logger.debug('[%d] Code %d (%s): %s' % (
			_cookie, event_code, raw_event.maskname, raw_event.pathname
			))

		# Trigger event in parent
		self.event_handler({'ping': 'pong'})


class __repo_event_handler_class__(pyinotify.ProcessEvent):


	def __init__(self, *args, **kwargs):

		self.__logger__ = kwargs[KEY_LOGGER]
		self.__handler__ = kwargs[KEY_HANDLER]
		kwargs.pop(KEY_LOGGER)
		kwargs.pop(KEY_HANDLER)
		self.__event_handler_factory__()
		super().__init__(*args, **kwargs)


	def __event_handler_factory__(self):

		prefix = 'process_'
		for pyinotify_event_flag in pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS'].keys():
			setattr(self, prefix + pyinotify_event_flag, partial(
				self.__handler__,
				getattr(pyinotify, pyinotify_event_flag)
				))
