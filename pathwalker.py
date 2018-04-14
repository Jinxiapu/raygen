#!/usr/bin/env/python3

import os
import json
import re
from datetime import date
import yaml

from pandoc import convert_md2html, generate_mdtoc
from util import urlify

content_dir = "../content"
conf_path = "./site.json"


def get_meta(md_file):
    with open(md_file, "rt", encoding="utf-8") as f:
        data = f.read()
        return yaml.load(data.split("---")[1])


def get_site_conf(conf_path):

    return {"url": "https://jinxiapu.com/", "author": "Jinxiapu", "section": ["home", "blog", "translate", "about", "links"]}


def convert_post(md, d):
    mdpath = os.path.join(content_dir, d, md)
    meta = get_meta(mdpath)
    buildtime = meta["date"] if "date" in meta else date.fromtimestamp(
        os.stat(mdpath).st_atime)
    url = "{0}/{1}-{2}/".format(d,
                                buildtime.strftime("%Y%m%d"), md.split(".")[0])

    post = {
        "type": "post",
        "author": meta["author"] if "author" in meta else "Jinxiapu",
        "title": meta["title"] if "title" in meta else md.split(".")[0],
        "section": d,
        "url": url,
        "datetime": buildtime,
        "detailtime": buildtime.strftime("%Y-%m-%d %H:%M:%S"),
        "date": buildtime.strftime("%Y-%m-%d"),
        "content": convert_md2html(mdpath),
        "toc": generate_mdtoc(mdpath),
        "tags": [],
        "requirements": ["isso", "markdown", "highlight"],

    }
    if "desc" in meta:
        post["desc"] = meta["desc"]

    if "mathjax" in meta and meta["mathjax"]:
        post["requirements"].append("mathjax")

    if "tags" in meta:
        post["tags"].extend(map(
            lambda tag: {
                "name": tag,
                "url": "tag/{}/".format(urlify(tag))
            },
            meta["tags"]
        )
        )
    return post


def convert_section(d, site):
    section = {
        "type": "section",
        "author": site["author"],
        "title": d,
        "section": d if d in site["section"] else "",
        "url": urlify(d)+"/",
        "requirements": [],
        "posts": []
    }

    subfiles = os.listdir(os.path.join(content_dir, d))
    # TODO 要对subfile做个筛选, 去除非markdown文件. 或者干脆支持不同格式的文件转HTML
    for md in subfiles:
        section["posts"].append(convert_post(md, d))
    return section


def convert_site(content_dir, conf_path):
    """
    获取网址结构, 去除一级目录中不需要作为Section的部分.
    """
    site = get_site_conf(conf_path)
    __, dirnames, filenames = next(os.walk(content_dir))

    sitepages = {}
    for fn in filenames:
        name = fn.split(".")[0]
        sitepages[name] = {
            "type": "sectionpage",
            "author": site["author"],
            "title": name,
            "section": name if name in site["section"] else "",
            "url": urlify(name)+"/",
            "requirements": ["markdown", "isso"],
            "content": convert_md2html(os.path.join(content_dir, fn))
        }

    sections = {}
    for d in dirnames:
        sections[d] = convert_section(d, site)

    return site, sitepages, sections
