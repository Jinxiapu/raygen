#!/usr/bin/env/python3

import re
import os
from jinja2 import Environment, FileSystemLoader

from util import make_sure_path_exists
from pathwalker import convert_site


content_dir = "../content"
conf_path = "./site.json"


def get_output_filename(relurl, output_dir):
    output_filedir = os.path.join(output_dir, relurl)
    make_sure_path_exists(output_filedir)
    return os.path.join(output_filedir, "index.html")


def gen_sections(env, sections, output_dir, site):
    for s in sections:
        output_filename = get_output_filename(sections[s]["url"], output_dir)
        rendered_html = env.get_template("section.html").render(
            page=sections[s], site=site
        )
        with open(output_filename, "w") as fh:
            fh.write(rendered_html)


def gen_sitepages(env, sitepages, output_dir, site):
    for sp in sitepages:
        output_filename = get_output_filename(sitepages[sp]["url"], output_dir)
        rendered_html = env.get_template("sectionpage.html").render(
            page=sitepages[sp], site=site
        )
        with open(output_filename, "w") as fh:
            fh.write(rendered_html)


def gen_posts(env, posts, output_dir, site):
    for p in posts:
        output_filename = get_output_filename(p["url"], output_dir)
        rendered_html = env.get_template("post.html").render(
            page=p, site=site
        )
        with open(output_filename, "w") as fh:
            fh.write(rendered_html)


def main():
    site, sitepages, sections = convert_site(content_dir, conf_path)
    site["url"]="http://127.0.0.1:8000/"
    j2_env = Environment(loader=FileSystemLoader("./template"),
                         trim_blocks=True)
    gen_sections(j2_env, sections, "./output", site)
    for s in sections:
        gen_posts(j2_env, sections[s]["posts"] , "./output", site)
    gen_sitepages(j2_env, sitepages, "./output", site)


if __name__ == '__main__':
    main()
