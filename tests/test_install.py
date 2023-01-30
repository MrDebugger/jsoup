import unittest
from jsoup import install
from bs4 import builder

class TestInstall(unittest.TestCase):
    def test_install(self):
        install()
        self.assertTrue("JsonTreeBuilder" in builder.__all__)
        self.assertIn("JsonTreeBuilder", builder.builder_registry.registry.keys())

    def test_install_debug(self):
        with self.assertRaises(AttributeError):
            install(debug=True)

if __name__ == '__main__':
    unittest.main()
