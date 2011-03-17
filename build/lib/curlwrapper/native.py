import basebrowser
import socks
import urllib2
import httplib

from basebrowser import BrowserRequest, BrowserResponse
class Browser(basebrowser.BaseBrowser):
    def __init__(self, cookies=False, redirect=True, 
        verbose=True):
        super(Browser, self).__init__(cookies=cookies, redirect=redirect, 
        verbose=verbose)
    def request(self, r):
        if r.proxy:
            proxy = r.proxy.split(':')
            tor_socks = socks.SockedHTTPHandler(proxy[0], int(proxy[1]))
            opener = urllib2.build_opener(tor_socks)
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        req = urllib2.Request(url=r.url)
        req.add_header('Referer', r.referer)


        response = opener.open(req)
        return BrowserResponse(code=200, response=response.read(),
                                response_URI=response.geturl())

