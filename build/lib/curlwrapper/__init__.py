"""curlwrapper for Python"""
VERSION = (0, 0, 1)
__version__ = ".".join(map(str, VERSION))
__author__ = "Ben Holloway"
__contact__ = "yawollohneb@yahoo.com"
__homepage__ = "http://http://github.com/pythonben/curlwrapper"
__docformat__ = "restructuredtext"
__name__ = "curlwrapper"
__all__ = [
    'Browser',
    'BaseBrowser',
    'BrowserRequest',
    'BrowserResponse',    
]


from basebrowser import BaseBrowser, BrowserResponse, BrowserRequest   

from browser import \
     Browser
