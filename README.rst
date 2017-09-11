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
- ``tqdm``
- ``humanize``
- ``msgpack-python``

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

First, run ``lit init`` at the root of a new repository.
Show difference to ``current`` index with ``lit diff``.
Commit to the ``current`` index with ``lit commit``.
Merge the changes into the ``journal`` branch with ``lit merge_journal``.
Make changes permanent by further merging them into ``master`` with ``lit merge_master``.
Dump the database into plain text files with ``lit dump``.
Find duplicates in the repository by file hash with ``lit duplicates``.
Get meta information from file with ``lit meta``, JSON output.
Show repository statistics with ``lit stats``.

.. _Add literature and adjust the filenames with ``l_rename``.
.. _Check the repository state, i.e. the file names, with ``l_sanity``.
.. _Generate all sorts of useful reports with ``l_report``.
.. _Determine the type of a file with ``l_file``, JSON output.
.. _Push the latest state of the repository to a MediaWiki server with ``l_pushwiki``.
.. _Analyse the network of authors with ``l_getnetwork``.

Full list of commands
---------------------

.. code:: bash

	lit init
	lit diff
	lit commit
	lit merge_journal
	lit merge_master
	lit dump
	lit stats
	lit meta

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
