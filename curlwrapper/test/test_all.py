import unittest, sys
import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
sys.path.append('..')
from curlwrapper.browser import Browser
class BrowserTests(unittest.TestCase):

    def setUp(self):
        self.b = Browser()

    def test_useragent(self):

        self.assertEqual(self.b.userAgent.find('Mozilla'), 0)

        self.assertNotEqual(self.b.userAgent, '')

    def test_proxy(self):
        self.assertNotEqual(self.b.userAgent, '')

    def test_basicHTTP(self):
        #print response.response
        self.assertEqual(self.b.simple_request('http://www.google.com'). 
            statusCode , 200)
        #print self.b.simpleRequest('htxp://www.google.com').errorMsg
        self.assertEqual(self.b.simple_request('htxp://www.google.com'). 
            errorCode , 1)
        
        self.assertEqual(self.b.simple_request('http://www.google.com/admin/'). 
            statusCode , 404)
    def test_environment(self):
        #print response.response
        self.b.set_keep_alive()
        r = self.b.simple_request('http://www.entropy.ch/software/macosx/php/test.php').response
        #logging.debug(r)

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(BrowserTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
