import unittest
from jsoup import install
from bs4 import builder


class TestInstall(unittest.TestCase):
    def test_install(self):
        install()
        self.assertIn("JsonTreeBuilder", builder.__all__)

    def test_install_debug(self):
        # Should print "Builder installed" without error
        install(debug=True)

    def test_install_usable(self):
        """After install(), 'jsoup' should be usable as a parser string."""
        install()
        from bs4 import BeautifulSoup
        json = {"p": "hello"}
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<p>hello</p>')


if __name__ == '__main__':
    unittest.main()
