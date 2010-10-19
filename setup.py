# -*- coding: utf-8 -*-
#
# python-curl-wrapper: Setup
#
# Author: Ben Holloway <yawollohneb@yahoo.com>
#
from distutils.core import setup

setup(
    name="curlwrapper",
    version='0.1.3',
    author="Ben Holloway",
    author_email="yawollohneb@yahoo.com",
    description="curlwrapper (browser interface for curl)",
    scripts=['bin/tamperConvert.py'],
    url="http://http://github.com/pythonben/curlwrapper",
    packages=['curlwrapper', 'curlwrapper.test'],
    license="LICENSE.txt",
    long_description=open('README.txt').read(),
    zip_safe=True,
)

