import unittest, sys
sys.path.append('..')
from browser import Browser
class BrowserTests(unittest.TestCase):

    def setUp(self):
        self.b = Browser()

    def test_useragent(self):

        self.assertEqual(self.b.userAgent.find('Mozilla'), 0)

        self.assertNotEqual(self.b.userAgent, '')

    def test_proxy(self):
        self.assertNotEqual(self.b.userAgent, '')



if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(BrowserTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
