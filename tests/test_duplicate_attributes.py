import unittest
from bs4 import BeautifulSoup
from jsoup import install

class TestOnDuplicateAttribute(unittest.TestCase):
    def setUp(self) -> None:
        install()
    def test_replace(self):
        json = {
            "body": {
                "p": {"attrs": [{"class": "first-para"}, {"class": "second-para"}], "text": "First paragraph"}
            }
        }
        soup = BeautifulSoup(json, "jsoup", on_duplicate_attribute="replace")
        p_tag = soup.body.p
        self.assertEqual(p_tag["class"], ["second-para"])

    def test_ignore(self):
        json = {
            "body": {
                "p": {"attrs": [{"class": "first-para"}, {"class": "second-para"}], "text": "First paragraph"}
            }
        }
        soup = BeautifulSoup(json, "jsoup", on_duplicate_attribute="ignore")
        p_tag = soup.body.p
        self.assertEqual(p_tag["class"], ["first-para"])

    def test_callable(self):
        def merge_classes(attrs, attr_name, attr_value):
            attrs[attr_name] += " " + attr_value
        json = {
            "body": {
                "p": {"attrs": [{"class": "first-para"}, {"class": "second-para"}], "text": "First paragraph"}
            }
        }
        soup = BeautifulSoup(json, "jsoup", on_duplicate_attribute=merge_classes)
        p_tag = soup.body.p
        self.assertEqual(p_tag["class"], ["first-para", "second-para"])

if __name__ == '__main__':
    unittest.main()
