#!/usr/bin/env python
import StringIO

class Response:
    """This is a the response object to return all variables related to
    a browser request"""
    def __init__(self, success=True, response='', code=None, 
            error_code='', error_msg='', response_URI=''):
        
        #unimplemented------------------------
        #name of server that sent response
        self.server = '' 
        #Gets the URI of the Internet resource that responded to 
        #the request.
        #Gets or sets the cookies that are associated with this response.
        self.cookies = []
        self.headers = []
        self.success = False 
        self.raw_headers = StringIO.StringIO()
        self.raw_cookies = []
        self.status_code = code
        self.response_URI = response_URI
        self.redirect_count = None
        self.redirect_url = None
        self.statusCode = self.status_code 
        self.response_buffer = StringIO.StringIO()
        self.success = success
        self.error_code = error_code
        self.error_msg = error_msg  
        self.content_length = None

        #implemented------------------------
        self.set_data(code, 
            error_code, error_msg)
    @property
    def response(self):
        return self.response_buffer.getvalue()

    def set_data(self, code=None,
            error_code='', error_msg=''):
        self.status_code = code
        self.statusCode = self.status_code
        #maybe call this .body as well?
        self.parse_headers()
        self.parse_cookies()

    def parse_headers(self):
        headers = self.raw_headers.getvalue().splitlines()
        #print headers
        #headers should be a list not a dict as there can be more than one Set-Cookie header etc
        new_h = []
        for h in headers:
            values = h.split(':', 1)
            if len(values) == 2:
                new_h.append((values[0].strip(), values[1].strip()))
        self.headers = new_h
        #print self.headers

    def parse_cookies(self):
        for cookie in self.raw_cookies:
            pass
            #print cookie.split('\t')

    def parse_refresh(self):
        refresh_url = False
        try:
            refresh_url = self.parse_refresh_line(self.headers['Refresh'])
        except KeyError:
            #print self.headers
            pass
        if refresh_url:
            return refresh_url
        return False 

    @staticmethod
    def parse_refresh_line(refresh_line):
        if refresh_line.find(';') == -1:
            return False
        refresh_line = refresh_line.split(';',2)[1]
        refresh_line = refresh_line.replace('url=','')
        refresh_line = refresh_line.replace('URL=','')
        refresh_line = refresh_line.strip()
        return refresh_line 
