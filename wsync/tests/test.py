import os
import shutil
import tempfile
from unittest import TestCase

from wsync import Wsync

class Test(TestCase):
    def test(self):
        digest_list_url = "https://raw.githubusercontent.com/reale/wsync/testing/SHA1SUMS"
        remote_repo_url = "https://raw.githubusercontent.com/reale/wsync/testing/"
        local_copy = tempfile.mkdtemp()

        wsync = Wsync(digest_list_url, remote_repo_url, local_copy)

        wsync.sync()

        self.assertTrue(os.listdir(local_copy) > 2)

        shutil.rmtree(local_copy)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
