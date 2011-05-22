#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# python-curl-wrapper: Setup
#
# Author: Ben Holloway <yawollohneb@yahoo.com>
#
from distutils.core import setup


CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
License :: OSI Approved :: Zope Public License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Topic :: Internet
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Indexing/Search
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Archiving :: Mirroring
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
Topic :: Text Processing
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML
"""   

setup(name="curlwrapper",
    version='0.1.57',
    author="Ben Holloway",
    author_email="yawollohneb@yahoo.com",
    description="curlwrapper (browser interface for curl)",
    #scripts=['bin/tamperConvert.py'],

    #url="http://github.com/pythonben/curlwrapper/",
    packages=['curlwrapper', 'curlwrapper.test'],
    license="LGPL/MIT",
    classifiers = [c for c in CLASSIFIERS.split("\n") if c],
    long_description="""
This module provides Python bindings for the cURL library.""", 
)

