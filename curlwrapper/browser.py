#!/usr/bin/env python
import pycurl
import StringIO
#todo switch to cStringIO
import string
import os
import sys
import time
import urllib
import tempfile
import random
PROXY_TYPES = ['SOCKS4','SOCKS4A','SOCKS5','AUTO','NONE']


class Browser:
    def __init__(self, cookies=False, redirect =True, 
        verbose = True):
        # The browser doesn't need a proxy list it could be beneficial in
        # the case of repeated failures, but honestly probably doesn't 
        # contribute much
        self.hasCookies = cookies
        self.redirect = redirect
        self.proxyList = proxyList
        self.verbose = verbose
        self.currentProxy = ''
        self.tempfile = ''
        self.tempfilename = ''
        self.userAgents = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; ro; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'
        ]
        self.userAgent = random.choice(self.userAgents)
        self.retryLimit = 2
        self.timeout = 30
        self.keepAlive = False
        self.useProxyDns = True
        self.range = None
        
        self.proxyType = "SOCKS4"
        self.proxiesOnly = False # for secure only connections
        if cookies == True:
            self.tempfile, self.tempfilename = tempfile.mkstemp()
            #self.tempfile, self.tempfilename = tempfile.TemporaryFile()
        self.get_random_proxy()
        self.headers = ["""Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5""" ,
                       """Accept-Language: en-US,en;q=0.5""",
                       """Accept-Encoding: gzip,deflate""",
                       """Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3"""
                       ]

    def __del__(self):
    
        #print 'garbage collected'
        self.close()
    def set_keep_alive(self):
        #This should only be settable once
        #currently doesn't allow you to turn off keep alive
        if self.keepAlive == False:
            self.headers.append('Connection: keep-alive')
            self.headers.append('Keep-Alive: 300')
            self.keepAlive = True
    def get_random_proxy(self):
        if len(self.proxyList) > 1:
            self.currentProxy = random.choice(self.proxyList)
    def getCookies(self):
        return ''
    def close(self):
        #file exists
        if self.hasCookies == True:
            os.close(self.tempfile)
            os.remove(self.tempfilename)
    def simple_request(self, url):
        return self.request(BrowserRequest(url=url))
    def request(self, r):
        url = r.url
        referer = r.referer
        post = r.post
        proxy = r.proxy
        tries = r.tries
        cookies = r.cookies
        try:
            c = pycurl.Curl()
            if tries >= self.retryLimit:
                return BrowserResponse(success=False, 
                                        errorMsg="tries greater than " +
                                        str(self.retryLimit) + " " + url)
                exit
            elif tries > 0:
                #print "retry "  + str(tries) + " " + str(id) + " " + time.strftime("%I:%M:%S %p",time.localtime())
                pass
            tries += 1
            c.setopt(pycurl.URL, url)
            if referer != '':
                c.setopt(pycurl.REFERER, referer)
            #if using socks4 this is useless anyway
            #c.setopt(pycurl.DNS_CACHE_TIMEOUT, 360)
            #c.setopt(pycurl.DNS_USE_GLOBAL_CACHE, 1) 
            c.setopt(pycurl.IPRESOLVE, pycurl.IPRESOLVE_V4)
            c.setopt(pycurl.TIMEOUT, self.timeout)
            c.setopt(pycurl.USERAGENT, self.userAgent)
            c.setopt(pycurl.ENCODING, 'gzip, deflate')
            if self.range:
                c.setopt(pycurl.RANGE, '0-%s'%(self.range*1024))
            if self.redirect == True:
                c.setopt(pycurl.FOLLOWLOCATION, True)
                c.setopt(pycurl.MAXREDIRS, 5)
            elif self.redirect ==False:
                c.setopt(pycurl.FOLLOWLOCATION, False)
                c.setopt(pycurl.MAXREDIRS, 0)
            c.setopt(pycurl.NOSIGNAL, 1)
            #c.setopt(pycurl.HEADER,1) # show headers?
            
            if self.hasCookies == True:
                c.setopt(pycurl.COOKIEFILE, self.tempfilename)
                c.setopt(pycurl.COOKIEJAR, self.tempfilename)
            if cookies != '':
                c.setopt(pycurl.COOKIE, cookies)
            
            if post != None:
                #print self.post
                self.headers.append('Content-Type: application/x-www-form-urlencoded; charset=UTF-8')
                
                c.setopt(pycurl.POST, 1);
                if type(post) != type([]):
                    
                    c.setopt(pycurl.POSTFIELDS, post);
                else:
                    #c.setopt(c.VERBOSE, 1)
                    c.setopt(pycurl.HTTPPOST, post);
            else:
                #print "not using post"
                pass
            if self.currentProxy != '':
                proxy = self.currentProxy
            if proxy != None:
                c.setopt(pycurl.PROXY, proxy)
                #c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS4)
                #6 should be socks4a
                if self.useProxyDns and self.proxyType == "SOCKS4":
                    c.setopt(pycurl.PROXYTYPE,6)
                elif self.proxyType == "SOCKS4":
                    c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS4)
                elif self.proxyType == "SOCKS5":
                    c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS5)
            elif proxy == None and self.proxiesOnly == True:
                return BrowserResponse(success=False, errorMsg="alert no proxy")
            c.setopt(pycurl.HTTPHEADER, self.headers)
            IO = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, IO.write)
            c.perform()
            
            code = c.getinfo(pycurl.HTTP_CODE)
            responseURI = c.getinfo(pycurl.EFFECTIVE_URL)
            c.close()
            response = IO.getvalue()
            
            return BrowserResponse(code=code, response=response,
                                    responseURI=responseURI)
        except pycurl.error, e:
            if self.verbose:
                pass
                #print "pycurl error tries", tries, str(inst.args) ,  url
            #TODO add retry code here
            return BrowserResponse(success=False, errorMsg="raised a \
                            pycurl.error " + str(e.args), errorCode = e[0])
        except Exception, inst:
            if self.verbose:
				
                #print "pycurl error tries", tries, str(inst.args) ,  url
                e = sys.exc_info()[1]
                print e

            return BrowserResponse(success=False,errorMsg = "raised a general exception")
        return BrowserResponse(success=False,errorMsg = "did nothing")
class BrowserResponse:
    def __init__(self, success = True, response = '',code= '', 
            errorCode = '', errorMsg='', responseURI = ''):
        
        #unimplemented------------------------
        #name of server that sent response
        self.server = '' 
        #Gets the URI of the Internet resource that responded to 
        #the request.
        self.responseURI = responseURI
        #Gets or sets the cookies that are associated with this response.
        self.cookies = ''
        
        #implemented------------------------
        self.statusCode = code
        self.response = response
        self.success = success
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        return None
class BrowserRequest:
    def __init__(self, url='', post=None, referer=''):
        #unimplemented
        self.cookies =''
        
        #implemented
        self.url= url
        if referer == '':
            self.referer = self.url
        else:
            self.referer = referer
        self.post = post
        self.proxy = None
        self.tries = 0
    
        return None
if __name__ == "__main__":
    b = Browser()
    b.keepAlive = True
    response = b.simpleRequest('http://www.google.com')
    print response.statusCode, response.response
    print response.success
    print response.errorMsg
