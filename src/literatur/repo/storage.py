# -*- coding: utf-8 -*-

"""

LITERATUR
Literature management with Python, Dropbox and MediaWiki
https://github.com/pleiszenburg/literatur

	src/literatur/repo/storage.py: Serialize / deserialize data

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

import json

import msgpack
import yaml

from ..const import (
	DEFAULT_INDEX_FORMAT,
	KEY_JSON,
	KEY_MP,
	KEY_PKL,
	KEY_YAML
	)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def load_data(path, mode = DEFAULT_INDEX_FORMAT):

	f = open(path, 'rb')

	if mode == KEY_PKL:
		import_dict = pickle.load(f)
	elif mode == KEY_MP:
		import_dict = msgpack.unpackb(f.read(), encoding = 'utf-8')
	elif mode == KEY_JSON:
		import_dict = json.load(f)
	else:
		f.close()
		raise # TODO

	f.close()

	return import_dict


def store_data(path, in_data, mode = DEFAULT_INDEX_FORMAT):

	if mode == KEY_PKL:
		f = open(path, 'wb+')
		pickle.dump(export_dict, f, -1)
	elif mode == KEY_MP:
		f = open(path, 'wb+')
		msg_pack = msgpack.packb(export_dict, use_bin_type = True)
		f.write(msg_pack)
	elif mode == KEY_JSON:
		f = open(path, 'w+')
		json.dump(export_dict, f, indent = '\t', sort_keys = True)
	elif mode == KEY_YAML:
		if hasattr(yaml, 'CDumper'):
			dumper = yaml.CDumper
		else:
			dumper = yaml.Dumper
		f = open(path, 'w+')
		yaml.dump(export_dict, f, Dumper = dumper, default_flow_style = False)
	else:
		raise # TODO

	f.close()
