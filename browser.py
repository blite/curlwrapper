#!/usr/bin/env python
import pycurl
import StringIO
#todo switch to cStringIO
import string, os, sys, time, urllib, tempfile, random

class Browser:
    def __init__(self, cookies=False, redirect =True, proxyList = [], verbose = True):
        self.hasCookies = cookies
        self.redirect = redirect
        self.proxyList = proxyList
        self.verbose = verbose
        self.currentProxy = ''
        self.tempfile = ''
        self.tempfilename = ''
        self.userAgents = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6']
        self.userAgent = self.userAgents[random.randrange(len(self.userAgents))]
        self.retryLimit = 2
        self.timeout = 30
        self.keepAlive = False
        self.useProxyDns = True
        self.range = None
        self.proxyType = "s4"
        if cookies == True:
            self.tempfile, self.tempfilename = tempfile.mkstemp()
            #self.tempfile, self.tempfilename = tempfile.TemporaryFile()
        self.getRandomProxy()
        self.headers = ["""Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5""" ,
                       """Accept-Language: en-us,en;q=0.5""",
                       """Accept-Encoding: gzip,deflate""",
                       """Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7"""
                       ]
        if self.keepAlive:
            self.headers.append('Connection: keep-alive')
            self.headers.append('Keep-Alive: 300')
    def __del__(self):
        #print 'garbage collected'
        self.close()
    def getRandomProxy(self):
        if len(self.proxyList) > 1:
            self.currentProxy = self.proxyList[random.randrange(len(self.proxyList))]
    def getCookies(self):
        return ''
    def close(self):
        #file exists
        if self.hasCookies == True:
            os.close(self.tempfile)
            os.remove(self.tempfilename)
    def request(self, url, referer='', post=None, proxy="NO_PROXY", id='', tries=0, cookies = ''):
        try:
            c = pycurl.Curl()
            if tries >= self.retryLimit:
                return BrowserResponse(success=False,errorMsg = "tries greater than " + str(self.retryLimit), url)
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
            if self.currentProxy != '' and proxy != "NO_PROXY":
                proxy = self.currentProxy
            if proxy != None and proxy != "NO_PROXY":
                c.setopt(pycurl.PROXY, proxy)
                #c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS4)
                #6 should be socks4a
                if self.useProxyDns and self.proxyType == "s4":
                    c.setopt(pycurl.PROXYTYPE,6)
                elif self.proxyType == "s4":
                    c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS4)
                elif self.proxyType == "s5":
                    c.setopt(pycurl.PROXYTYPE,pycurl.PROXYTYPE_SOCKS5)
            elif proxy != "NO_PROXY":
                return BrowserResponse(success=False,errorMsg = "alert no proxy")
                exit
            c.setopt(pycurl.HTTPHEADER, self.headers)
            IO = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, IO.write)
            c.perform()
            
            code = c.getinfo(pycurl.HTTP_CODE)
            c.close()
            response = IO.getvalue()
            
            BrowserResponse(code=code,response=response)
        except pycurl.error, inst:
            if self.verbose:
                pass
                #print "pycurl error tries", tries, str(inst.args) ,  url
            self.getRandomProxy()
            self.request(url,referer,post,proxy,id,tries)
            return BrowserResponse(success=False)
        except Exception, inst:
            if self.verbose:
				
                #print "pycurl error tries", tries, str(inst.args) ,  url
                e = sys.exc_info()[1]
                print e

            return BrowserResponse(success=False)
        return BrowserResponse(success=False)
class BrowserResponse:
    def __init__(self, success = True, response = '',code= '', 
            errorCode = '', errorMsg=''):
        self.statusCode = code
        self.response = response
        self.success = success
        self.errorCode = errorCode
        self.errorMsg = errorMsg
    
class BrowserRequest:
    def __init__():
        pass
