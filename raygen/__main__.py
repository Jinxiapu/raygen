#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main part of `raygen`

"""


import argparse
import logging


logging.basicConfig(level=logging.DEBUG)


def get_raygen_argparser():
    """
    Get the command line input/output arguments passed in to `raygen`.
    """

    parser = argparse.ArgumentParser(
        description='A simple static site generator, for those who want to fully the generation of blog.'
    )
    parser.add_argument(
        '--server',
        help='run the server.',
        action="store_true"
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Port number to serve files on.'
    )
    return parser


def main():
    """ Entry point for the package, as defined in `setup.py`. """

    parser = get_raygen_argparser()
    try:
        from .raygen import raygen
        from .server import serve_static_site
        args = parser.parse_args()
        if args.server:
            raygen("http://127.0.0.1:{}/".format(args.port))
            serve_static_site(port=args.port)
        else:
            raygen()
    except FileExistsError as e:
        logging.critical(e)
        print("Please make sure `site.json` exists in current path\n")
        parser.print_help()

if __name__ == '__main__':
    main()