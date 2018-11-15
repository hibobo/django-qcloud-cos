#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import (
    setup,
    find_packages,
)


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


NAME = "django_qcloud_cos"
DESCRIPTION = "Django qcloud cos storage backend"
AUTHOR = "hibobo"
AUTHOR_EMAIL = "abc00cba@gmail.com"
URL = "https://github.com/hibobo"
VERSION = '0.1'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    include_package_data=True,
    license="BSD",
    url=URL,
    packages=find_packages(),
    install_requires=[
        'django',
        'djangorestframework',
    ],
    zip_safe=False,
)
