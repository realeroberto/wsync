#!/usr/bin/env python

# A small Python utility for synchronizing a local folder with a remote web
# repository.

# The MIT License (MIT)
# 
# Copyright (c) 2014 Roberto Reale
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import getopt
import os
import requests
import sys
import urlparse
import yaml
from CheckableString import *

version = "0.0.7"


class RequestsHandler(object):

    """ HTTP/S requests handler """

    def get(self, url):
        response = requests.get(url, verify=self.verify_cert, proxies=self.proxies)
        if response:
            return response.content
        else:
            return None

    def __init__(self, verify_cert=True, proxies=None):
        self.verify_cert = verify_cert
        self.proxies = proxies


class RemoteRepo(object):

    """ The remote repository """

    def get_file(self, url, ignore_base_url=False):
        if ignore_base_url:
            full_url = url
        else:
            full_url = urlparse.urljoin(self.base_url, url)
        return self.requests_handler.get(full_url)

    def __init__(self, base_url, requests_handler):
        self.base_url = base_url
        self.requests_handler = requests_handler


class RemoteDigestList(RemoteRepo):

    """ The remote digest list """

    def _retrieve_digest_list(self, list_url):
        response = self.get_file(list_url, ignore_base_url=True)
        if response:
            return response.split("\n")
        else:
            return None

    def __init__(self, list_url, requests_handler, ignore_path=False):
        RemoteRepo.__init__(self, None, requests_handler)  # base_url = None
        digest_list = self._retrieve_digest_list(list_url)
        if digest_list:
            self.digest_list = digest_list
            self.ignore_path = ignore_path
            self.current = 0
            self.high = len(self.digest_list)
        else:
            # TODO add error handling
            pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.high:
            raise StopIteration
        else:
            self.current += 1
            digest_item = self.digest_list[self.current - 1]
            try:
                [digest, full_path] = digest_item.split()
            except ValueError:
                return self.__next__()  # skip line; TODO warn user
            if self.ignore_path:
                path = os.path.basename(full_path)
            else:
                path = full_path
            return [path, digest]

    def next(self):
        return self.__next__()  # compatibility hack for Python 2.x


class LocalCopy(object):

    """ The local working copy """

    to_get = []

    def check_file(self, path, digest):
        """ verifies a file's digest """
        with open(path, "rb") as f:
            contents = CheckableString(f.read())
            f.close()
            return contents.check(digest, hexdigest=True)
        return None
        
    def compare(self):
        local_files = []
        for [path, digest] in self.remote_digest_list:
            full_path = os.path.join(self.base_path, path)
            if not os.path.exists(full_path):
                self.to_get.append(path)
            elif not self.check_file(full_path, digest):
                self.to_get.append(path)
            else:
                print "file %s is ok" % path

    def write_file(self, name, contents):
        print "writing file %s" % name
        with open (os.path.join(self.base_path, name), "wb+") as f:
            f.write(contents)

    def sync(self):
        for file in self.to_get:
            print "getting file %s" % file
            self.write_file(file, self.remote.get_file(file))

    def __init__(self, base_path, remote, remote_digest_list):
        self.base_path = base_path
        self.remote = remote
        self.remote_digest_list = remote_digest_list


class Wsync(object):

    """ Wsync object """

    def sync(self):
        requests_handlers = RequestsHandler(self.verify_cert, self.proxies)
        if not requests_handlers:
            print >>sys.stderr, "Cannot instantiate requests handler"
            sys.exit(1)

        remote_repo = RemoteRepo(self.remote_repo_url, requests_handlers)

        remote_digest_list = RemoteDigestList(self.digest_list_url,
                                              requests_handlers,
                                              ignore_path=True)

        local = LocalCopy(self.local_copy_path, remote_repo, remote_digest_list)

        local.compare()
        local.sync()

    def set_local_copy_path(self, value):
        self.local_copy_path = value

    def set_digest_list_url(self, value):
        self.digest_list_url = value

    def set_remote_repo_url(self, value):
        self.remote_repo_url = value

    def set_verify_cert(self, value):
        self.verify_cert = value

    def add_proxy(self, schema, url):
        self.proxies[schema] = url

    def __init__(self, local_copy_path=None, digest_list_url=None,
                 remote_repo_url=None):
        self.local_copy_path = local_copy_path
        self.digest_list_url = digest_list_url
        self.remote_repo_url = remote_repo_url
        self.verify_cert = False
        self.proxies = dict()


class WsyncByConfigFile(Wsync):

    """ Wsync object, defined by config file """

    def search_config(self, tag):
        if not tag:
            return None
        config_file = tag + ".yaml"
        # first try user-defined
        user_home = os.path.expanduser("~")
        path = os.path.join(user_home, ".wsync", config_file)
        if os.path.exists(path):
            return path
        # then try system-wide
        path = os.path.join("/etc/wsync.d", config_file)
        if os.path.exists(path):
            return path

    def load_config(self, tag):
        path = self.search_config(tag)
        if not path:
            return False
        with open(path, "r") as f:
            config = yaml.load(f)
            f.close()
            for key, value in config.iteritems():
                if key == "local_copy_path":
                    self.set_local_copy_path(value)
                elif key == "digest_list_url":
                    self.set_digest_list_url(value)
                elif key == "remote_repo_url":
                    self.set_remote_repo_url(value)
                elif key == "verify_cert":
                    self.set_verify_cert(value)
                elif key == "http_proxy":
                    self.add_proxy("http", value)
                elif key == "https_proxy":
                    self.add_proxy("https", value)
            return True

    def __init__(self):
        Wsync.__init__(self)



def short_usage():
    print >>sys.stderr, """Usage:
    wsync [-y CONFIG ]
    wsync [-c PATH] [-l URL] [-r URL]
Try `wsync --help' for more information."""


def full_usage():
    print >>sys.stderr, """Usage:
    wsync [-y CONFIG ]
    wsync [-c PATH] [-l URL] [-r URL]
Synchronize a local copy of remote repository, over HTTP/S.

      --help                   display this help and exit
  -y, --config        CONFIG   use config fragment CONFIG
  -c, --local-copy    PATH     path to local copy, defaults to ENV[WSYNC_LOCAL_COPY]
  -l, --digest-list   URL      url of the digest list, defaults to ENV[WSYNC_DIGEST_LIST]
  -r, --remote-repo   URL      url of the remote repository, defaults to ENV[WSYNC_REMOTE_REPO]
      --verify-cert            verify SSL certificates
      --dont-verify-cert       disable verifying SSL certificates
      --SCHEMA-proxy  URL      proxy settings for the SCHEMA protocol"""


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hy:c:l:r:",
                                         ["help", "config=", "local-copy=",
                                          "digest-list=", "remote-repo=",
                                          "http-proxy=", "https-proxy=",
                                          "verify-cert", "dont-verify-cert"])

    except getopt.GetoptError, err:
        print >>sys.stderr, err
        short_usage()
        sys.exit(2)

    local_copy_path = os.environ.get("WSYNC_LOCAL_COPY")
    digest_list_url = os.environ.get("WSYNC_DIGEST_LIST")
    remote_repo_url = os.environ.get("WSYNC_REMOTE_REPO")

    config_tag = None
    verify_cert = True
    proxies = dict()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage()
            sys.exit()
        elif opt in ("-y", "--config"):
            config_tag = arg
            break
        elif opt in("-c", "--local-copy"):
            local_copy_path = arg
        elif opt in ("-l", "--digest-list"):
            digest_list_url = arg
        elif opt in("-r", "--remote-repo"):
            remote_repo_url = arg
        elif opt in("--http-proxy", "--https-proxy"):
            if opt == "--http-proxy":
                proxies["http"] = arg
            elif opt == "--https-proxy":
                proxies["https"] = arg
        elif opt in("--verify-cert", "--dont-verify-cert"):
            if opt == "--verify-cert":
                verify_cert = True
            elif opt == "--dont-verify-cert":
                verify_cert = False

    if config_tag:
        wsync = WsyncByConfigFile()

        if not wsync.load_config(config_tag):
            print >>sys.stderr, "Cannot find config"
            sys.exit(2)

    else:
        if not local_copy_path or not digest_list_url or not remote_repo_url:
            if not local_copy_path:
                print >>sys.stderr,\
                "WSYNC_LOCAL_COPY not set in environment and not",\
                "specified by --local-copy PATH or -c PATH"

            elif not digest_list_url:
                print >>sys.stderr,\
                "WSYNC_DIGEST_LIST not set in environment and not",\
                "specified by --digest-list URL or -l URL"

            elif not remote_repo_url:
                print >>sys.stderr,\
                "WSYNC_REMOTE_REPO not set in environment and not",\
                "specified by --remote-repo URL or -r URL"

            short_usage()
            sys.exit(2)

        wsync = Wsync(local_copy_path, digest_list_url, remote_repo_url)
        wsync.set_verify_cert(verify_cert)
        wsync.set_proxies(proxies)

    if not wsync:
        print >>sys.stderr, "Cannot instantiate sync handler"
        sys.exit(1)

    wsync.sync()

if __name__ == "__main__":
    main(sys.argv[1:])
