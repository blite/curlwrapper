# -*- coding: utf-8 -*-
#
# python-curl-wrapper: Setup
#
# Author: Ben Holloway <yawollohneb@yahoo.com>
#
from distutils.core import setup

setup(
    name="CurlWrapper",
    version='0.1.0',
    author="Ben Holloway",
    author_email="yawollohneb@yahoo.com",
    description="CurlWrapper (browser)",
    scripts=['bin/tamperConvert.py'],
    url="http://github.com/pythonben/Python-Curl-Wrapper",
    packages=['curlwrapper', 'curlwrapper.test'],
    license="LICENSE.txt",
    long_description=open('README.txt').read(),
)

