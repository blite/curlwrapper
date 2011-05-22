import urllib

class Request:
    """This is the Request object that contains the tricky stuff 
    for a http request"""
    def __init__(self, url='', post=None, referer='', 
            proxy=None, extraheaders={}, forbid_redirect=False,
            trycount=None, fd=None, onprogress=None, only_head=False):
        """Download an URL with GET or POST methods.

        @param post: It can be a string that will be POST-ed to the URL.
            When None is given, the method will be GET instead.
        @param extraheaders: You can add/modify HTTP headers with a dict here.
        @param forbid_redirect: Set this flag if you do not want to handle
            HTTP 301 and 302 redirects.
        @param trycount: Specify the maximum number of retries here.
            0 means no retry on error. Using -1 means infinite retring.
            None means the default value (that is self.trycount).
        @param fd: You can pass a file descriptor here. In this case,
            the data will be written into the file. Please note that
            when you save the raw data into a file then it won't be cached.
        @param onprogress: A function that has two parameters:
            the size of the resource and the downloaded size. This will be
            called for each 1KB chunk. (If the HTTP header does not contain
            the content-length field, then the size parameter will be zero!)
        @param only_head: Create the openerdirector and return it. In other
            words, this will not retrieve any content except HTTP headers.

        @return: The raw HTML page data, unless fd was specified. When fd
            was given, the return value is undefined.
        """   
        #unimplemented
        self.cookies = ''
        #implemented
        self.url = url
        if referer == '':
            self.referer = self.url
        else:
            self.referer = referer

        self.multipart = False 

        if isinstance(post, dict) :
            self.post = urllib.urlencode(post)
        elif isinstance(post, list) and not self.multipart:
            self.post = urllib.urlencode(post)  
        else:
            self.post = post
        self.proxy = proxy
        self.tries = 0
        self.additional_headers = None
        
    
        return None    
	
