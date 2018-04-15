#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

requirements = [
    'jinja2>=2.4',
    'PyYAML>=3.10'
]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='raygen',
    version='0.1.0',
    description='A simple static site generator, for those who want to fully the generation of blog.',
    long_description=readme,
    author='Jinxiapu',
    author_email='jinxiapu@gmail.com',
    url='https://github.com/jinxiapu/raygen',
    license=license,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            "raygen = raygen.__main__:main"
        ]
    }
)
