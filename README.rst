::

	██╗     ██╗████████╗███████╗██████╗  █████╗ ████████╗██╗   ██╗██████╗
	██║     ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║   ██║██╔══██╗
	██║     ██║   ██║   █████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
	██║     ██║   ██║   ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
	███████╗██║   ██║   ███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
	╚══════╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

/lɪtəʀaˈtuːɐ̯/ *(German, noun, feminine: literature)*

Synopsis
========

(Scientific) literature management with (C)Python 3, Dropbox and MediaWiki.
Entirely offline at its core, all online functionality is optional.
(Unix) shell friendly approach, enabling file management with ``find``, ``ls`` and friends.
Alpha for newcomers, production-ready for insiders. LGPL.

Prerequisites
=============

The following Python packages are required:

- ``git+https://github.com/alexz-enwp/wikitools.git@py3#egg=wikitools``
- ``dropbox``
- ``PyQt5``
- ``networkx``
- ``python-magic``
- ``pdfminer.six``
- ``xmltodict``

Installation
============

.. code:: bash

	pip install git+https://github.com/pleiszenburg/literatur.git@master

It should be platform independent, but it really has only been tested on Linux.

Basic usage & philosophy
========================

Think of *git* with two hard-coded branches (``journal`` and ``master``) and a staging area (``current``).
Think of the folder ``.l`` like you would think about ``.git``.
Find reports and analysis data in ``.l/reports``.

First, run ``l_init`` at the root of a new repository.
Add literature and adjust the filenames with ``l_rename``.
Check the repository state, i.e. the file names, with ``l_sanity``.
Build an index for ``current`` with ``l_buildindex``, update it with ``l_rebuildindex``.
Commit changes to the ``journal`` branch with ``l_commit_journal``.
Make changes permanent by further pushing to `master` with ``l_commit_master``.
Find duplicate entries with ``l_findduplicates``.
Dump the database into plain text files with ``l_dumpdb``.
Generate all sorts of useful reports with ``l_report``.
Determine the type of a file with ``l_file``, JSON output.
Get meta information from file with ``l_meta``, JSON output.
Push the latest state of the repository to a MediaWiki server with ``l_pushwiki``.
Show repository statistics with ``l_stat``.
Analyse the network of authors with ``l_getnetwork``.

Full list of commands
---------------------

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
	l_stat
	l_getnetwork
	l_pushwiki
	l_rename
	l_meta
	f_file

Need help?
==========

Feel free to post questions in the `GitHub issue tracker`_ of this project.
Make sure to label them as `question`_.

.. _question: https://github.com/pleiszenburg/literatur/labels/question

Bugs & issues
=============

Report bugs in literatur here: `GitHub issue tracker`_

.. _GitHub issue tracker: https://github.com/pleiszenburg/literatur/issues

Miscellaneous
=============

- `License`_ (**LGPL v2.1**)
- `Contributing`_ (**Contributions are highly welcomed!**)
- `Authors`_

.. _License: LICENSE
.. _Contributing: CONTRIBUTING.rst
.. _Authors: AUTHORS.rst
