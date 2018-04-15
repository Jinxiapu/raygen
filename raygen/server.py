#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
raygen.server
-------------------
Functions for serving a static HTML website locally.
"""

import os
import sys


import http.server as httpserver
import socketserver

def serve_static_site(output_dir, port=8080):
    """
    Serve a directory containing static HTML files, on a specified port.
    :param output_dir: Output directory to be served.
    """
    os.chdir(output_dir)
    Handler = httpserver.SimpleHTTPRequestHandler

    # See http://stackoverflow.com/questions/16433522/socketserver-getting-rid-
    #      of-errno-98-address-already-in-use
    socketserver.TCPServer.allow_reuse_address = True

    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)

    try:
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down...")
        httpd.socket.close()
        sys.exit()