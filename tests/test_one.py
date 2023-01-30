import unittest
from bs4 import BeautifulSoup
from jsoup import JsonTreeBuilder

class TestJsonTreeBuilder(unittest.TestCase):
    def test_simple_json(self):
        # Test case for a simple JSON string
        json = {
            "body": {
                "h1": {"attrs": {"class": "heading1"}, "text": "Hello World"},
                "p": "This is a test"
            }
        }
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><h1 class="heading1">Hello World</h1><p>This is a test</p></body>')

    def test_nested_json(self):
        # Test case for a nested JSON string
        json = {
            "body": {
                "h1": {"attrs": {"class": "heading1"}, "text": "Hello World"},
                "ul": {
                    "li": [
                        "Item 1",
                        "Item 2",
                        {"text":"Item 3"}
                    ]
                }
            }
        }
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><h1 class="heading1">Hello World</h1><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></body>')

if __name__ == '__main__':
    unittest.main()
