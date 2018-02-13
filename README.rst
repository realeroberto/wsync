wsync
=====

|PyPI| |License: MIT| |Build Status| |AppVeyor Build Status|
|Documentation Status| |Code Health| |Waffle.io| |Say Thanks!|

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

You can also the
```testing`` <https://github.com/robertoreale/wsync/tree/testing>`__
branch of this repository for a quick test: just do:

::

        wsync  \
            --digest-list https://raw.githubusercontent.com/robertoreale/wsync/testing/SHA1SUMS  \
            --remote-repo https://raw.githubusercontent.com/robertoreale/wsync/testing/

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

        digest_list_url = "https://raw.githubusercontent.com/robertoreale/wsync/testing/SHA1SUMS"
        remote_repo_url = "https://raw.githubusercontent.com/robertoreale/wsync/testing/"

.. |PyPI| image:: https://img.shields.io/pypi/v/wsync.svg
   :target: https://pypi.python.org/pypi/wsync
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |Build Status| image:: https://travis-ci.org/robertoreale/wsync.svg?branch=master
   :target: https://travis-ci.org/robertoreale/wsync
.. |AppVeyor Build Status| image:: https://ci.appveyor.com/api/projects/status/github/robertoreale/wsync
   :target: https://ci.appveyor.com/project/robertoreale/wsync/branch/master
.. |Documentation Status| image:: https://readthedocs.org/projects/wsync/badge/?version=latest
   :target: http://wsync.readthedocs.io/en/latest/?badge=latest
.. |Code Health| image:: https://landscape.io/github/robertoreale/wsync/master/landscape.svg?style=flat
   :target: https://landscape.io/github/robertoreale/wsync/master
.. |Waffle.io| image:: https://badge.waffle.io/robertoreale/wsync.svg?columns=done
   :target: https://waffle.io/robertoreale/wsync
.. |Say Thanks!| image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/robertoreale
