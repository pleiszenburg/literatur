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

import pyinotify

from ..const import (
	KEY_HANDLER,
	KEY_LOGGER
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def generate_notifier(event_handler, root_path, exclude_filter_list, logger):

	notifier_wm = pyinotify.WatchManager()

	notifier = pyinotify.Notifier(
		notifier_wm, __repo_event_handler_class__(**{
			KEY_HANDLER: event_handler,
			KEY_LOGGER: logger
			})
		)

	notifier_repo = notifier_wm.add_watch(
		root_path,
		pyinotify.ALL_EVENTS,
		rec = True,
		auto_add = True,
		exclude_filter = pyinotify.ExcludeFilter(exclude_filter_list)
		)

	# Start the notifier in its own thread
	notifier_thread = Thread(target = notifier.loop)
	notifier_thread.daemon = True

	return (
		notifier,
		notifier_repo,
		notifier_wm,
		notifier_thread,
		pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']
		)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
