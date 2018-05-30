#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
raygen.construct
-------------------
Functions for construct site's category, post, etc.

"""
from datetime import datetime, date, time
import os

from .config import site, CONTENT_DIR
from .convert import md2meta, md2html, md2toc
from .util import urlify, get_content_lastmod_time, refactor_toc_html


def get_real_path(relpath):
    return os.path.join(CONTENT_DIR, relpath)


def tag_url(tag_name):
    return "tags/{}".format(urlify(tag_name))


def make_base_page(type, title, url,
                   requirements=None, author=None, lastmod=None):
    # if type not in site["type"].keys():
    #     raise Exception("type {} don't exist.".format(type))
    if requirements is None:
        requirements = []
    if author is None:
        author = site["author"]
    if lastmod is None:
        lastmod = datetime.now()
    return {
        "type": type,
        "author": author,
        "title": title,
        "url": url,
        "requirements": requirements,
        "lastmodtime": lastmod,
        "thumbnail": site["thumbnail"]
    }


def construct_tag_pages(allposts):
    tags = {}
    for p in allposts:
        for tag in p["tags"]:
            if tag["name"] not in tags:
                tags[tag["name"]] = make_base_page(
                    "tag",
                    tag["name"],
                    tag_url(tag["name"]),
                )
                tags[tag["name"]]["posts"] = [p]
            else:
                tags[tag["name"]]["posts"].append(p)
    # Because allposts is sorted, tag["posts"] must be sorted too.
    return list(tags.values())


def construct_post_page(md_file_path):
    category = os.path.split(os.path.dirname(md_file_path))[1]
    meta = md2meta(get_real_path(md_file_path))
    lastmodtime = get_content_lastmod_time(get_real_path(md_file_path))
    buildtime = meta["date"] if "date" in meta else lastmodtime
    if not isinstance(buildtime, datetime):
        buildtime = datetime.combine(buildtime, time(0, 0))
    basename = os.path.basename(md_file_path).split(".")[0]
    url = "{0}/{1}-{2}/".format(
        category,
        buildtime.strftime("%Y%m%d"),
        basename
    )
    post = make_base_page(
        "post",
        meta["title"] if "title" in meta else basename,
        url,
        requirements=site["requirements"],
        author=meta["author"] if "author" in meta else None,
        lastmod=lastmodtime
    )
    post["buildtime"] = buildtime
    post["categroy"] = category
    post["content"] = md2html(get_real_path(md_file_path))
    post["toc"] = md2toc(get_real_path(md_file_path), pipefunc=refactor_toc_html)
    if "desc" in meta:
        post["desc"] = meta["desc"]

    if "isbest" in meta:
        post["isbest"] = meta["isbest"]
    if "thumbnail" in meta:
        post["thumbnail"] = meta["thumbnail"]

    if ("use" in meta) and ("mathjax" in meta["use"]):
        post["requirements"].append("mathjax")

    if "tags" in meta:
        post["tags"] = list(map(
            lambda tag: {
                "name": tag,
                "url": tag_url(tag)
            },
            meta["tags"]
        ))

    return post


def construct_category_page(category_path):
    category = make_base_page(
        "section",
        category_path,
        category_path+"/",
        lastmod=get_content_lastmod_time(get_real_path(category_path))
    )
    subfiles = os.listdir(os.path.join(CONTENT_DIR, category_path))
    # TODO 要对subfile做个筛选, 去除非markdown文件. 或者干脆支持不同格式的文件转HTML
    category["posts"] = list(map(
        lambda md_file: construct_post_page(
            os.path.join(category_path, md_file)),
        subfiles
    ))
    category["posts"] = sorted(
        category["posts"],
        key=lambda p: p["buildtime"],
        reverse=True
    )
    return category


def construct_article_page(article_file_path):
    name = article_file_path.split(".")[0]
    article = make_base_page("article", name,
                             urlify(name)+"/", requirements=["isso", "markdown"],
                             lastmod=get_content_lastmod_time(
                                 get_real_path(article_file_path))
                             )
    article["content"] = md2html(get_real_path(article_file_path))
    return article


def construct_links_page():
    return make_base_page(
        "links",
        "links",
        "links/",
    )


def construct_home_page(allposts):
    home = make_base_page(
        "home",
        site["title"],
        "",
    )
    home["posts"] = allposts[:4]
    return home


def construct_site():
    allpages = []
    allposts = []
    __, dirnames, filenames = next(os.walk(CONTENT_DIR))

    categorys = list(map(
        lambda d: construct_category_page(d),
        dirnames
    ))
    allpages.extend(categorys)

    for ct in categorys:
        allpages.extend(ct["posts"])
        allposts.extend(ct["posts"])

    allposts = sorted(
        allposts,
        key=lambda p: p["buildtime"],
        reverse=True
    )
    allpages.extend(list(
        map(
            lambda f: construct_article_page(f),
            filenames
        )
    ))
    allpages.append(construct_home_page(allposts))
    #allpages.append(construct_links_page())
    allpages.extend(construct_tag_pages(allposts))
    return allpages, allposts
