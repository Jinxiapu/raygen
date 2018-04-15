#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main part of `raygen`

"""


import argparse
import logging


from .generate import raygen
from .server import serve_static_site
from .config import OUTPUT_DIR

logging.basicConfig(level=logging.DEBUG)


def get_raygen_args():
    """
    Get the command line input/output arguments passed in to `raygen`.
    """

    parser = argparse.ArgumentParser(
        description='A simple static site generator, for those who want to fully the generation of blog.'
    )
    parser.add_argument(
        '--server',
        help='run the server.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port number to serve files on.'
    )

    args = parser.parse_args()
    return args


def main():
    """ Entry point for the package, as defined in `setup.py`. """

    args = get_raygen_args()

    if args.server:
        raygen(True)
        serve_static_site(OUTPUT_DIR, port=args.port)
    else:
        raygen()