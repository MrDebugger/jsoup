import unittest
from bs4 import BeautifulSoup
from jsoup import JsonTreeBuilder

class TestJsonTreeBuilder(unittest.TestCase):

    # Basic conversion
    def test_simple_tag(self):
        json = {"p": "hello"}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<p>hello</p>')

    def test_tag_with_attrs(self):
        json = {"h1": {"attrs": {"class": "heading1"}, "text": "Hello World"}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<h1 class="heading1">Hello World</h1>')

    def test_nested_tags(self):
        json = {"body": {"h1": "title", "p": "text"}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><h1>title</h1><p>text</p></body>')

    def test_list_creates_multiple_tags(self):
        json = {"ul": {"li": ["Item 1", "Item 2", "Item 3"]}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>')

    def test_nested_elements_with_text(self):
        json = {"body": {"ul": {"li": [
            "Item 1",
            {"text": "Item 2", "ul": {"li": ["Sub 1", "Sub 2"]}},
            "Item 3"
        ]}}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><ul><li>Item 1</li><li>Item 2<ul><li>Sub 1</li><li>Sub 2</li></ul></li><li>Item 3</li></ul></body>')

    # Empty elements
    def test_empty_element_br(self):
        json = {"body": {"br": None}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><br/></body>')

    def test_empty_element_hr(self):
        json = {"body": {"hr": None}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><hr/></body>')

    def test_empty_element_img(self):
        json = {"img": {"attrs": {"src": "test.png", "alt": "test"}}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertIn('src="test.png"', str(soup))
        self.assertIn('alt="test"', str(soup))

    # Comments
    def test_comment(self):
        json = {"body": {"p": "text", "comment": "a comment"}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><p>text</p><!--a comment--></body>')

    def test_comment_list(self):
        json = {"body": {"comment": ["comment 1", "comment 2"]}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertIn('<!--comment 1-->', str(soup))
        self.assertIn('<!--comment 2-->', str(soup))

    # Doctype
    def test_doctype(self):
        json = {"doctype": "html", "html": {"body": {"p": "test"}}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        output = str(soup)
        self.assertIn('html', output)
        self.assertIn('<p>test</p>', output)

    # Character references
    def test_charref_escaped(self):
        json = {"p": "1<2 && 2>1"}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<p>1&lt;2 &amp;&amp; 2&gt;1</p>')

    # bs2json roundtrip format (children key)
    def test_children_key_simple(self):
        json = {"body": {"children": [{"h1": "title"}, {"p": "text"}]}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><h1>title</h1><p>text</p></body>')

    def test_children_key_with_attrs(self):
        json = {"table": {"attrs": {"id": "t1"}, "children": [
            {"tr": {"children": [{"td": "a"}, {"td": "b"}]}}
        ]}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertIn('id="t1"', str(soup))
        self.assertIn('<td>a</td>', str(soup))
        self.assertIn('<td>b</td>', str(soup))

    def test_children_key_preserves_order(self):
        json = {"body": {"children": [
            {"h3": "first"}, {"p": "text"}, {"h3": "second"}
        ]}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<body><h3>first</h3><p>text</p><h3>second</h3></body>')

    def test_children_key_nested(self):
        """Deep nesting with children keys."""
        json = {"html": {"body": {"children": [
            {"div": {"attrs": {"class": "main"}, "children": [
                {"h1": "Title"},
                {"p": "Content"}
            ]}}
        ]}}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertIn('<div class="main">', str(soup))
        self.assertIn('<h1>Title</h1>', str(soup))

    # Bytes input
    def test_bytes_input(self):
        json = {"p": b"hello bytes"}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(str(soup), '<p>hello bytes</p>')

    # Custom label names
    def test_custom_attr_name(self):
        json = {"p": {"@": {"class": "x"}, "text": "hello"}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder, attr_name='@')
        self.assertEqual(str(soup), '<p class="x">hello</p>')

    def test_custom_text_name(self):
        json = {"p": {"#text": "hello"}}
        soup = BeautifulSoup(json, builder=JsonTreeBuilder, text_name='#text')
        self.assertEqual(str(soup), '<p>hello</p>')

    # repr
    def test_repr(self):
        b = JsonTreeBuilder()
        self.assertIn('JsonTreeBuilder', repr(b))

    # Error cases
    def test_invalid_attrs_type(self):
        json = {"p": {"attrs": ["not a dict list"]}}
        with self.assertRaises(SyntaxError):
            BeautifulSoup(json, builder=JsonTreeBuilder)

    # Does not modify original data
    def test_does_not_modify_original(self):
        json = {"body": {"p": {"attrs": {"class": "x"}, "text": "hello"}}}
        import copy
        original = copy.deepcopy(json)
        BeautifulSoup(json, builder=JsonTreeBuilder)
        self.assertEqual(json, original)


if __name__ == '__main__':
    unittest.main()
