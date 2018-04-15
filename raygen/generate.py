#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
raygen.convert
-------------------
Functions for convert markdown file.

"""

import os
import shutil
import logging

from jinja2 import Environment, FileSystemLoader

from .util import make_sure_path_exists
from .config import site, OUTPUT_DIR, TEMPLATE_DIR
from .construct import construct_site


def copy_assets(assets_dir, output_dir):
    """
    Copies static assets over from `assets_dir` to `output_dir`.
    :param assets_dir: The project assets directory,
        e.g. `project/assets/`.
    :paramtype assets_dir: directory
    :param output_dir: The output directory, e.g. `www/`.
    :paramtype output_dir: directory
    """

    assets = os.listdir(assets_dir)
    for item in assets:
        item_path = os.path.join(assets_dir, item)

        # Only copy allowed dirs
        if os.path.isdir(item_path) and item != 'scss' and item != 'less':
            new_dir = os.path.join(output_dir, item)
            print('Copying directory {0} to {1}'.format(item, new_dir))
            try:
                shutil.copytree(item_path, new_dir)
            except FileExistsError:
                logging.warn("assets has existed.")

        # Copy over files in the root of assets_dir
        if os.path.isfile(item_path):
            new_file = os.path.join(output_dir, item)
            print('Copying file {0} to {1}'.format(item, new_file))
            shutil.copyfile(item_path, new_file)


def get_output_filename(relurl, output_dir):
    output_filedir = os.path.join(output_dir, relurl)
    make_sure_path_exists(output_filedir)
    return os.path.join(output_filedir, "index.html")


def format_datetime(value, format='date'):
    format_dict = {
        "full": "%Y-%m-%d %H:%M:%S",
        "date": "%Y-%m-%d",
        "lastmod": "%Y-%m-%dT%H:%M:%S+08:00"
    }
    return value.strftime(format_dict[format])


def write_output(rendered_html, output_filename):
    make_sure_path_exists(os.path.dirname(output_filename))
    with open(output_filename, "w") as fh:
        fh.write(rendered_html)
        logging.debug("wirte content to {}".format(output_filename))


def gen_rendered_html(page, env):
    return env.get_template("{}.html".format(page["type"])).render(page=page, site=site)


def raygen(islocal=False):
    if islocal:
        site["url"] = "http://127.0.0.1:8080/"
    allpages, allposts = construct_site()
    j2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                         trim_blocks=True)
    j2_env.filters['datetime'] = format_datetime
    for p in allpages:
        write_output(gen_rendered_html(p, j2_env),
                     get_output_filename(p["url"], OUTPUT_DIR))
    write_output(
        j2_env.get_template("sitemap.xml").render(
            allpages=allpages, site=site),
        os.path.join(OUTPUT_DIR, "sitemap.xml")
    )
    copy_assets("./static", OUTPUT_DIR)

