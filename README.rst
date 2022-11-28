========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        .. | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-outlook-calendar-sync/badge/?style=flat
    :target: https://python-outlook-calendar-sync.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/mr55p-dev/python-outlook-calendar-sync/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/mr55p-dev/python-outlook-calendar-sync/actions

.. |codecov| image:: https://codecov.io/gh/mr55p-dev/python-outlook-calendar-sync/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/mr55p-dev/python-outlook-calendar-sync

.. |version| image:: https://img.shields.io/pypi/v/outlook-calendar-sync.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/outlook-calendar-sync

.. |wheel| image:: https://img.shields.io/pypi/wheel/outlook-calendar-sync.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/outlook-calendar-sync

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/outlook-calendar-sync.svg
    :alt: Supported versions
    :target: https://pypi.org/project/outlook-calendar-sync

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/outlook-calendar-sync.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/outlook-calendar-sync

.. .. |commits-since| image:: https://img.shields.io/github/commits-since/mr55p-dev/python-outlook-calendar-sync/v0.0.3.svg
..     :alt: Commits since latest release
..     :target: https://github.com/mr55p-dev/python-outlook-calendar-sync/compare/v0.0.3...main



.. end-badges

CLI interface to scrape outlook calendar events from the webapp and insert them to a google calendar account.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install outlook-calendar-sync

You can also install the in-development version with::

    pip install https://github.com/mr55p-dev/python-outlook-calendar-sync/archive/main.zip


Documentation
=============


https://python-outlook-calendar-sync.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


On the roadmap is:

- [ ] Create some error handling for the outlook sign up process
  - [ ] Exception on invalid username
  - [ ] Exception on invalid password
  - [ ] Exception on invalid auth code
- [ ] Handle the case where authenticator is not required (either auto detect or use flag)
- [ ] Switch from using css selectors to XPath
- [ ] Put dependencies in the setuptools script
