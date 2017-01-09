wsync
=====

A small Python utility for synchronizing a local folder with a remote web repository.


## Install

Just do

```
pip install wsync
```


## Example

Suppose that you need to mantain a local mirror of the remote repository at
http://cdimage.debian.org/debian-cd/current/source/iso-dvd/.

Then it is enough to do as follows:

```
from wsync import *

working_copy = "~/debian-iso-dvd"
digest_list_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/SHA1SUMS"
remote_repo_url = "http://cdimage.debian.org/debian-cd/current/source/iso-dvd/"

wsync = Wsync(working_copy, digest_list_url, remote_repo_url)

wsync.sync()
```
