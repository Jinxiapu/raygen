#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
raygen.convert
-------------------
Functions for convert markdown file.

"""

import subprocess
from os import path
import yaml

def md2html(md_file_path, pipefunc=None, markdown_type="markdown"):
    """
    convert markdown file to html.
    :param pipefunc: function who modify output.
    """
    if not path.exists(md_file_path):
        raise FileExistsError("{} don't exists".format(md_file_path))
    run_content = ["pandoc", "-f", markdown_type,
                   "-t", "html", md_file_path, "--mathjax"]
    result = subprocess.run(run_content, stdout=subprocess.PIPE).stdout.decode('utf-8')
    if pipefunc is None:
        return result
    else:
        return pipefunc(result)


def md2toc(md_file_path, depth=2, pipefunc=None, markdown_type="markdown"):
    """
    generate markdown file's TOC(table of content). depth for depth of TOC.
    :param pipefunc: function who modify output.

    """
    if not path.exists(md_file_path):
        raise FileExistsError("{} don't exists".format(md_file_path))
    template = path.join(path.dirname(__file__), "toc.pandoc_template")
    run_content = ["pandoc", md_file_path, "-f", markdown_type, "--template",
                   template, "--toc", "--toc-depth={}".format(depth)]
    result = subprocess.run(run_content, stdout=subprocess.PIPE).stdout.decode('utf-8')
    if pipefunc is None:
        return result
    else:
        return pipefunc(result)

def md2meta(md_file_path):
    with open(md_file_path, "rt", encoding="utf-8") as f:
        data = f.read()
        meta_origin = yaml.load(data.split("---")[1])
        return meta_origin