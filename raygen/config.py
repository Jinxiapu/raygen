#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
raygen.config
-------------------
config for raygen

"""

import json
import os
import logging

logging.info("read site.json from {}".format(os.path.realpath("./")))


with open("./site.json", "r") as f:
    try:
        site = json.load(f)
    except FileNotFoundError as e:
        print("Maybe this is not a raygen project. please make sure site.json in current path.")
        raise e
    if "output_dir" in site:
        OUTPUT_DIR = site["output_dir"]
    else:
        OUTPUT_DIR = "./output/"

    if "content_dir" in site:
        CONTENT_DIR = site["content_dir"]
    else:
        CONTENT_DIR = "./content/"

    if "template_dir" in site:
        TEMPLATE_DIR = site["template_dir"]
    else:
        TEMPLATE_DIR = "./template/"

