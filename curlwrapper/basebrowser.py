#!/usr/bin/env python
import os
import sys
import tempfile
import random
import logging
import time
import StringIO
import urllib
import Cookie
import io
from curlwrapper.request import Request as Request
from curlwrapper.response import Response as Response
#todo switch to cStringIO

class NullHandler(logging.Handler):
    def emit(self, record):
        pass



h = NullHandler()
logging.getLogger("browser").addHandler(h)

PROXY_TYPES = [
    'SOCKS4',
    'SOCKS4A',
    'SOCKS5',
    'HTTP',
    'AUTO',
    'NONE'
]

REGULAR_USER_AGENTS = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ro; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',   
]

MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17',
    'Mozilla/5.0 (Linux; U; Android 1.5; en-us; MB200 Build/CUPCAKE) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1',
    'Mozilla/5.0 (Linux; U; Android 1.5; en-us; Android Dev Phone 1 Build/CRB21) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1',
    'Mozilla/5.0 (webOS/1.0; U; en-US) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/1.0 Safari/525.27.1 Pre/1.0',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_1_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5A345 Safari/525.20',
    'SAMSUNG-SGH-T919/T919UVHL3 SHP/VPP/R5 NetFront/3.5 SMM-MMS/1.2.0 profile/MIDP-2.1 configuration/CLDC-1.1',
    'Nokia3650/1.0 UP.Browser/6.2',
    'MOT-RAZRV3x',
    'AUDIOVOX-CDM180',
    'SIE-M46',
    'Mozilla/5.0 (Linux; U; Android 1.5; en-us; ADR6200 Build/CUPCAKE) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
    'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C25 Safari/419.3',
    
]


class BaseBrowser(object):
    def __init__(self, cookies=False, redirect=True, 
        verbose=True, mobile=False):
        # The browser doesn't need a proxy list it could be beneficial in
        # the case of repeated failures, but honestly probably doesn't 
        # contribute much
        self.has_cookies = cookies
        self.use_real_cookie_file = False
        self.redirect = redirect
        self.proxy_list = []
        self.verbose = verbose
        self.current_proxy = ''
        if mobile:
            self.user_agent = random.choice(MOBILE_USER_AGENTS) 
        else:
            self.user_agent = random.choice(REGULAR_USER_AGENTS)
        self.retry_limit = 2
        self.timeout = 30
        self.keep_alive = False
        self.use_proxy_dns = True
        self.range = None
        #TODO: set default proxy type to AUTO req- enable detection
        self.proxy_type = "SOCKS4"
        self.proxies_only = False # for secure only connections
        #TODO: maybe make cookies read from memory
        if self.has_cookies:
            if self.use_real_cookie_file:
                self.cookie_file = tempfile.NamedTemporaryFile()
                self.cookie_file_path = self.cookie_file.name
            else:
                self.cookie_file_path = ""

            #self.tempfile, self.tempfilename = tempfile.TemporaryFile()
        self.headers = {
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        }

    def __del__(self):
        """
        Shutdown
        """
        #print 'garbage collected'
        self.close()
    def enable_keep_alive(self):
        """
        turn on keep alives
        """
        if self.keep_alive == False:
            self.headers['Connection'] = 'keep-alive'
            self.headers['Keep-Alive'] = '300'
            self.keep_alive = True

    def disable_keep_alive(self):
        """
        turn off keep alives
        """
        if self.keep_alive == True:
            del self.headers['Connection']
            del self.headers['Keep-Alive']
            self.keep_alive = False 
    def get_cookies(self):
        """
        stub for getting cookies
        """
        pass
    def set_cookies(self, cookies):
        """
        stub for setting cookies
        """
        pass      
    def detect_proxy_type(self):
        """
        stub for detecting the type of proxy
        """
        pass
    def close(self):
        """
        this is a shutdown method
        """

    def fetch(self, url):
        """
        this is a simple call wrapper
        """
        return self.request(Request(url=url))
    def request(self, r):
        """
        Performs a http request
        """
        pass
        

if __name__ == "__main__":
    b = Browser()
    b.keepAlive = True
    response = b.simple_request('http://www.google.com')
    print response.status_code, response.response
    print response.success
    print response.error_msg
