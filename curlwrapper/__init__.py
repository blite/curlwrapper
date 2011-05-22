"""curlwrapper for Python"""
VERSION = (0, 0, 1)
__version__ = ".".join(map(str, VERSION))
__author__ = "Ben Holloway"
__contact__ = "yawollohneb@yahoo.com"
__homepage__ = "http://github.com/pythonben/curlwrapper"
__docformat__ = "restructuredtext"
__name__ = "curlwrapper"
__all__ = [
    'Browser',
    'NativeBrowser',
    'BaseBrowser',
    'Request',
    'Response'
]
"""
__all__ = [
    'Browser',
    'Cookie',
    'CookieJar',
    'CookiePolicy',
    'History',
    'Link',
    'LinkNotFoundError',
    'LinksFactory',
    'LoadError',
    'Request',
    'UserAgent',
    'Proxy',
    ]
"""
from basebrowser import BaseBrowser
from request import Request
from response import Response
from browser import Browser
from native import Browser as NativeBrowser

BrowserResponse = Response
BrowserRequest = Request    
