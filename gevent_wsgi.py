#!/usr/bin/env python

# Copyright (C) Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
For running with the Gevent WSGI server.

This serves up static resources, e.g. /static, which may be fine for
development, but the idea is that it's reverse-proxied behind a webserver,
with the static resources served directly by the webserver.

Example invocation:
$ /path/to/gevent_wsgi.py -l <logfile> -p <port> &
"""

import sys
import os
import getopt
import signal
# gevent.wsgi is very fast and allows high concurrency, but does not support
# streaming (for large file upload requests or large responses).  Another
# option is gevent.pywsgi.
from gevent.wsgi import WSGIServer
from app import app


port = 8080
log = 'default'
pidfile = None
interface = ''


def usage():
    print 'gevent_wsgi.py [[-h] | [-i <interface, e.g. "127.0.0.1">] ', \
        '[-p <port>] [-l <log>] [--pidfile=<file>]'

def main(argv):
    global port, log, pidfile, interface
    try:
        opts, args = getopt.getopt(argv, "p:l:i:h", ["pidfile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-p':
            port = int(arg)
        elif opt == '-l':
            try:
                log = open(arg, 'w')
            except:
                sys.stderr.write("Can not open log file.\n")
                sys.exit(1)
        elif opt == '-i':
            interface = arg
        elif opt == '--pidfile':
            pidfile = arg
    if pidfile:
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()))
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    http_server = WSGIServer((interface, port), application=app, log=log)
    try:
        http_server.serve_forever()
    except:
        clean_pidfile()
        sys.exit()  # Don't print backtrace for KeyboardInterrupt

def clean_pidfile():
    try:
        os.unlink(pidfile)
    except:
        pass

def signal_handler(signum, frame):
    clean_pidfile()
    sys.exit()

if __name__ == '__main__':
   main(sys.argv[1:])

