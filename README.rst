::

	██╗     ██╗████████╗███████╗██████╗  █████╗ ████████╗██╗   ██╗██████╗
	██║     ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║   ██║██╔══██╗
	██║     ██║   ██║   █████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
	██║     ██║   ██║   ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
	███████╗██║   ██║   ███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
	╚══════╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

/lɪtəʀaˈtuːɐ̯/ (literature: German, noun, feminine)

Synopsis
========

Literature management with (C)Python (3), Dropbox and MediaWiki.
Alpha for newcomers, production-ready for insiders. LGPL.

Prerequisites
=============

The following Python packages are required:

- git+https://github.com/alexz-enwp/wikitools.git@py3#egg=wikitools
- dropbox
- PyQt5
- networkx

Installation
============

.. code:: bash

	pip install git+https://github.com/pleiszenburg/literatur.git@master

Commands
========

.. code:: bash

	l_init
	l_buildindex
	l_rebuildindex
	l_commit_journal
	l_commit_master
	l_sanity
	l_findduplicates
	l_dumpdb
	l_report
	l_getnetwork
	l_pushwiki
	l_rename

Need help?
==========

Feel free to post questions in the `GitHub issue tracker`_ of this project.
Make sure to label them as `question`_.

.. _question: https://github.com/pleiszenburg/literatur/labels/question

Bugs & issues
=============

Report bugs in literatur here: `GitHub issue tracker`_

Miscellaneous
=============

- `License`_ (**LGPL v2.1**)
- `Contributing`_ (**Contributions are highly welcomed!**)
- `Authors`_

.. _License: LICENSE
.. _Contributing: CONTRIBUTING.rst
.. _Authors: AUTHORS.rst
