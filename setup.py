#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


setup(
    name="outlook-calendar-sync",
    version="0.0.2",
    license="BSD-2-Clause",
    description="CLI interface to scrape outlook calendar events from the webapp and insert them to a google calendar account.",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub("", read("README.rst")),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Ellis Lunnon",
    author_email="ellislunnon@gmail.com",
    url="https://github.com/mr55p-dev/python-outlook-calendar-sync",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://python-outlook-calendar-sync.readthedocs.io/",
        "Changelog": "https://python-outlook-calendar-sync.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/mr55p-dev/python-outlook-calendar-sync/issues",
    },
    keywords=["outlook", "calendar", "gcal", "office365", "web-scraping", "selenium", "cli"],
    python_requires=">=3.7",
    install_requires=[
        "selenium>=4.6",
        "beautifulsoup4>=4.11",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    extras_require={"dev": ["pytest", "bump2version", "twine", "flake8", "black"]},
    entry_points={
        "console_scripts": [
            "outlook-calendar-sync = outlook_calendar_sync.cli:main",
        ]
    },
)
