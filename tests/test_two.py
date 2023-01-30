import unittest
from bs4 import BeautifulSoup
from jsoup import install

class JsonTreeBuilderTestCase(unittest.TestCase):
    def setUp(self):
        install()

    def test_simple_html_structure(self):
        json = {
            "body": {
                "h1": "Hello World",
                "p": "This is a test."
            }
        }
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<body><h1>Hello World</h1><p>This is a test.</p></body>')

    def test_html_structure_with_attributes(self):
        json = {
            "body": {
                "h1": {"attrs": {"class": "title"}, "text": "Hello World"},
                "p": {"attrs": {"class": "text"}, "text": "This is a test."}
            }
        }
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<body><h1 class="title">Hello World</h1><p class="text">This is a test.</p></body>')

    def test_html_structure_with_list(self):
        json = {
            "body": {
                "ul": {
                    "li": [
                        "Item 1",
                        "Item 2",
                        "Item 3"
                    ]
                }
            }
        }
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<body><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></body>')

    def test_html_structure_with_nested_elements(self):
        json = {
            "body": {
                "ul": {
                    "li": [
                        "Item 1",
                        {
                            "text": "Item 2",
                            "ul": {
                                "li": [
                                    "Subitem 1",
                                    "Subitem 2"
                                ]
                            }
                        },
                        "Item 3"
                    ]
                }
            }
        }
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<body><ul><li>Item 1</li><li>Item 2<ul><li>Subitem 1</li><li>Subitem 2</li></ul></li><li>Item 3</li></ul></body>')

    def test_html_structure_with_comments(self):
        json = {
            "body": {
                "p": "This is a test.",
                "comment": "This is a comment."
            }
        }
        soup = BeautifulSoup(json, "jsoup")
        self.assertEqual(str(soup), '<body><p>This is a test.</p><!--This is a comment.--></body>')



if __name__ == '__main__':
    unittest.main()