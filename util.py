#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
utils
----------------
Helper functions
"""

import errno
import os
import sys
import re

def urlify(s):
    return re.sub(r"\s+", "-", s)

def minify_html(html):
    """
    Removes spaces and new lines from a HTML file
    :param html: HTML that should be minified
    """

    # Removes whitespaces, and new lines between tags using this RE
    return re.sub(r">\s+<", '><', html)

def make_sure_path_exists(path):
    """
    Ensures that a directory exists.
    :param path: A directory path.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True