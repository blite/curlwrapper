import urllib

class Request:
    """This is the Request object that contains the tricky stuff 
    for a http request"""
    def __init__(self, url='', post=None, referer='', proxy=None):
        #unimplemented
        self.cookies = ''
        #implemented
        self.url = url
        if referer == '':
            self.referer = self.url
        else:
            self.referer = referer
        if isinstance(post, dict):
            self.post = urllib.urlencode(post)
        else:
            self.post = post
        self.proxy = proxy
        self.tries = 0
    
        return None    
	
