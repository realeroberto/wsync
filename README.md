wsync
=====

A small Python utility for synchronizing a local folder with a remote web repository.

## Example

Suppose that you need to mantain a local mirror of the remote repository at
http://cdimage.debian.org/debian-cd/7.6.0/ia64/iso-dvd/.  Then it is enough to
do as follows:

```
from wsync import *

working_copy = "~/debian-iso-dev"
digest_list_url = "http://cdimage.debian.org/debian-cd/7.6.0/ia64/iso-dvd/SHA1SUMS"
remote_repo_url = "http://cdimage.debian.org/debian-cd/7.6.0/ia64/iso-dvd/")

wsync = Wsync(working_copy, digest_list_url, remote_repo_url)

wsync.sync()
```
