#!/usr/bin/env python

# A small Python utility for synchronizing a local folder with a remote web
# repository.

# The MIT License (MIT)
# 
# Copyright (c) 2014-8 Roberto Reale
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
import sys

from wsync import Wsync, WsyncByConfigFile


def short_usage():
    print >>sys.stderr, """Usage:
    wsync [-y CONFIG ]
    wsync [-l URL] [-r URL] [-c PATH]
Try `wsync --help' for more information."""


def full_usage():
    print >>sys.stderr, """Usage:
    wsync [-y CONFIG ]
    wsync [-l URL] [-r URL] [-c PATH]
Synchronize a local copy of remote repository, over HTTP/S.

      --help                   display this help and exit
  -y, --config        CONFIG   use config fragment CONFIG
  -l, --digest-list   URL      url of the digest list, defaults to ENV[WSYNC_DIGEST_LIST]
  -r, --remote-repo   URL      url of the remote repository, defaults to ENV[WSYNC_REMOTE_REPO]
  -c, --local-copy    PATH     path to local copy, defaults to ENV[WSYNC_LOCAL_COPY]
      --verify-cert            verify SSL certificates
      --dont-verify-cert       disable verifying SSL certificates
      --SCHEMA-proxy  URL      proxy settings for the SCHEMA protocol"""


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hy:l:r:c:",
                                         ["help", "config=", "digest-list=",
                                          "remote-repo=", "local-copy=",
                                          "http-proxy=", "https-proxy=",
                                          "verify-cert", "dont-verify-cert"])

    except getopt.GetoptError, err:
        print >>sys.stderr, err
        short_usage()
        sys.exit(2)

    digest_list_url = os.environ.get("WSYNC_DIGEST_LIST")
    remote_repo_url = os.environ.get("WSYNC_REMOTE_REPO")
    local_copy_path = os.environ.get("WSYNC_LOCAL_COPY")

    config_file = None
    verify_cert = True
    proxies = dict()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            full_usage()
            sys.exit()
        elif opt in ("-y", "--config"):
            config_file = arg
            break
        elif opt in ("-l", "--digest-list"):
            digest_list_url = arg
        elif opt in("-r", "--remote-repo"):
            remote_repo_url = arg
        elif opt in("-c", "--local-copy"):
            local_copy_path = arg
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

    if config_file:
        wsync = WsyncByConfigFile()

        if not wsync.load_config(config_file):
            print >>sys.stderr, "Cannot find config"
            sys.exit(2)

    else:
        if not digest_list_url or not remote_repo_url:
            if not digest_list_url:
                print >>sys.stderr,\
                "WSYNC_DIGEST_LIST not set in environment and not",\
                "specified by --digest-list URL or -l URL"

            elif not remote_repo_url:
                print >>sys.stderr,\
                "WSYNC_REMOTE_REPO not set in environment and not",\
                "specified by --remote-repo URL or -r URL"

            short_usage()
            sys.exit(2)

        if not local_copy_path:
            local_copy_path = os.getcwd()

        wsync = Wsync(digest_list_url, remote_repo_url, local_copy_path)
        wsync.set_verify_cert(verify_cert)
        wsync.set_proxies(proxies)

    if not wsync:
        print >>sys.stderr, "Cannot instantiate sync handler"
        sys.exit(1)

    wsync.sync()

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
