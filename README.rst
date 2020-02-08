wsync
=====

|PyPI| |License: MIT| |Build Status| |AppVeyor Build Status|
|Documentation Status| |Coveralls| |Code Health|

A small Python utility/module for synchronizing a local folder with a
remote web repository.

Install
-------

Just do

::

        pip install wsync

Usage
-----

As a standalone script
~~~~~~~~~~~~~~~~~~~~~~

Suppose that you need to mantain a local mirror of the remote repository
at ``http://cdimage.debian.org/debian-cd/current/source/iso-dvd/``.

Then it is enough to do as follows:

::

        wsync  \
            --digest-list http://cdimage.debian.org/debian-cd/current/source/iso-dvd/SHA1SUMS  \
            --remote-repo http://cdimage.debian.org/debian-cd/current/source/iso-dvd/          \
            --local-copy ~/debian-iso-dvd

Of course, any subsequent execution of the script will detect any change
and download what is needed.

You can also use the
`testing <https://github.com/reale/wsync/tree/testing>`_
branch of the GitHub repository for a quick test: just do:

::

        wsync  \
            --digest-list https://raw.githubusercontent.com/reale/wsync/testing/SHA1SUMS  \
            --remote-repo https://raw.githubusercontent.com/reale/wsync/testing/

As a module
~~~~~~~~~~~

As before:

::

        from wsync import *

        digest_list_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/SHA1SUMS"
        remote_repo_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/"
        local_copy = "~/debian-iso-dvd"

        wsync = Wsync(digest_list_url, remote_repo_url, local_copy)

        wsync.sync()

Or:

::

        digest_list_url = "https://raw.githubusercontent.com/reale/wsync/testing/SHA1SUMS"
        remote_repo_url = "https://raw.githubusercontent.com/reale/wsync/testing/"

.. |PyPI| image:: https://img.shields.io/pypi/v/wsync.svg
   :target: https://pypi.python.org/pypi/wsync
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |Build Status| image:: https://travis-ci.com/reale/wsync.svg?branch=master
   :target: https://travis-ci.com/reale/wsync
.. |AppVeyor Build Status| image:: https://ci.appveyor.com/api/projects/status/github/reale/wsync?svg=true
   :target: https://ci.appveyor.com/project/reale/wsync/branch/master
.. |Documentation Status| image:: https://readthedocs.org/projects/wsync/badge/?version=latest
   :target: http://wsync.readthedocs.io/en/latest/?badge=latest
.. |Coveralls| image:: https://coveralls.io/repos/github/reale/wsync/badge.svg?branch=master
   :target: https://coveralls.io/github/reale/wsync?branch=master
.. |Code Health| image:: https://landscape.io/github/reale/wsync/master/landscape.svg?style=flat
   :target: https://landscape.io/github/reale/wsync/master
