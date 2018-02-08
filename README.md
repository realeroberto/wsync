# wsync

[![PyPI](https://img.shields.io/pypi/v/wsync.svg)](https://pypi.python.org/pypi/wsync)

A small Python utility/module for synchronizing a local folder with a remote web repository.


## Install

Just do

        pip install wsync


## Usage

### As a standalone script

Suppose that you need to mantain a local mirror of the remote repository at
`http://cdimage.debian.org/debian-cd/current/source/iso-dvd/`.

Then it is enough to do as follows:

        wsync  \
            --digest-list http://cdimage.debian.org/debian-cd/current/source/iso-dvd/SHA1SUMS  \
            --remote-repo http://cdimage.debian.org/debian-cd/current/source/iso-dvd/          \
            --local-copy ~/debian-iso-dvd

Of course, any subsequent execution of the script will detect any change and download what is needed.

You can also the [`testing`](https://github.com/robertoreale/wsync/tree/testing) branch of this repository for a quick test: just do:

        wsync  \
            --digest-list https://raw.githubusercontent.com/robertoreale/wsync/testing/SHA1SUMS  \
            --remote-repo https://raw.githubusercontent.com/robertoreale/wsync/testing/


### As a module

As before:

        from wsync import *

        digest_list_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/SHA1SUMS"
        remote_repo_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/"
        local_copy = "~/debian-iso-dvd"

        wsync = Wsync(digest_list_url, remote_repo_url, local_copy)

        wsync.sync()

Or:

        digest_list_url = "https://raw.githubusercontent.com/robertoreale/wsync/testing/SHA1SUMS"
        remote_repo_url = "https://raw.githubusercontent.com/robertoreale/wsync/testing/"
