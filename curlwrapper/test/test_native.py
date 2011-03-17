import unittest 
import sys
import os

sys.path += [os.path.abspath('../..')]   
#TODO make sure this is correct
from curlwrapper.native import Browser, BrowserRequest
class BrowserTests(unittest.TestCase):

    def setUp(self):
        self.b = Browser()

    def test_useragent(self):

        self.assertEqual(self.b.user_agent.find('Mozilla'), 0)

        self.assertNotEqual(self.b.user_agent, '')

    def test_proxy(self):
        self.assertNotEqual(self.b.user_agent, '')

    def test_basicHTTP(self):
        #print response.response
        self.assertEqual(self.b.simple_request('http://www.google.com'). 
            statusCode , 200)
        #print self.b.simpleRequest('htxp://www.google.com').errorMsg
        #self.assertEqual(self.b.simple_request('htxp://www.google.com'). 
        #    errorCode , 1)
        
        self.assertEqual(self.b.simple_request('http://www.google.com/admin/'). 
            statusCode , 404)
    def test_unicode(self):
        #print response.response
        self.assertEqual(self.b.simple_request('http://www.google.com'). 
            statusCode , 200)
        #print self.b.simpleRequest('htxp://www.google.com').errorMsg
        #self.assertEqual(self.b.simple_request('htxp://www.google.com'). 
        #    errorCode , 1)
        
        self.assertEqual(self.b.simple_request('http://www.google.com/admin/'). 
            statusCode , 404)
    def test_environment(self):
        #print response.response
        self.b.set_keep_alive()
        r = self.b.simple_request('http://www.entropy.ch/software/macosx/php/test.php').response
    def test_proxy(self):
        #testing proxy using tor
        response = self.b.request(BrowserRequest(url='http://www.google.com', post=None, 
                        referer='', proxy='127.0.0.1:9050'))
        if response.success:
            print "worked"
        #logging.debug(r)

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(BrowserTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
