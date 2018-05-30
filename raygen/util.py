#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
raygen.utils
----------------
Helper functions
"""

import errno
import os
import re
from datetime import datetime

import lxml.html as lh


def get_content_lastmod_time(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime)


def urlify(s):
    return re.sub(r"\s+", "-", s)


def refactor_toc_html(toc_html):
    toctree = lh.fromstring(toc_html)
    toctree.attrib["class"] = "uk-nav-default uk-nav-center uk-margin-auto-vertical uk-nav-parent-icon"
    toctree.attrib["uk-nav"] = "multiple: true"

    for pli in toctree.xpath("./li[ul]"):
        pli.attrib["class"] = "uk-parent"
        pli.xpath("./ul")[0].attrib["class"] = "uk-nav-sub"

    return lh.tostring(toctree, pretty_print=True).decode('utf-8')


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


def whether_config_file_exist(config_name="./site.json"):
    return os.path.exists(config_name)