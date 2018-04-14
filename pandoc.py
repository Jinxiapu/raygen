#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
wrap pandoc for python.
"""
import subprocess
from os import path


def convert_md2html(md_file_path):
    if not path.exists(md_file_path):
        return None
    run_content = ["pandoc", "-f", "markdown",
                   "-t", "html", md_file_path, "--mathjax"]
    return subprocess.run(run_content, stdout=subprocess.PIPE).stdout.decode('utf-8')


def generate_mdtoc(md_file_path, depth=2):
    """
    generate markdown file's TOC. depth for depth of TOC.
    """
    if not path.exists(md_file_path):
        return None
    run_content = ["pandoc", md_file_path, "-f", "markdown", "--template",
                   "toc.pandoc_template", "--toc", "--toc-depth={}".format(depth)]
    return subprocess.run(run_content, stdout=subprocess.PIPE).stdout.decode('utf-8')
