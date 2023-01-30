#! /usr/bin/env python
# -*- coding: utf-8 -*-
from html import unescape
from copy import deepcopy
from bs4 import builder
from bs4.builder import (
    HTMLTreeBuilder,
    HTML,
    STRICT,
    FAST
)
from bs4.element import (
    Comment,
    Doctype,
    )

__license__ = "MIT"
__version__ = "0.0.1"
__VERSION__ = [0, 0, 1]

__name = 'JsonTreeBuilder'


JSOUP = "jsoup"

class JsonTreeBuilder(HTMLTreeBuilder):
    is_xml = False
    picklable = True
    NAME = JSOUP
    features = [NAME, HTML, STRICT, FAST, "json"]
    TRACKS_LINE_NUMBERS = False
    REPLACE = "replace"
    IGNORE = "ignore"
    CDATA_CONTENT_ELEMENTS = ("script", "style")

    def __init__(self, parser_args=None, parser_kwargs=None, **kwargs):
        extra_parser_kwargs = dict()
        for arg in ('on_duplicate_attribute',):
            if arg in kwargs:
                value = kwargs.pop(arg)
                extra_parser_kwargs[arg] = value
        super(JsonTreeBuilder, self).__init__(**kwargs)
        parser_args = parser_args or []
        parser_kwargs = parser_kwargs or {}
        parser_kwargs.update(extra_parser_kwargs)
        self.parser_args = (parser_args, parser_kwargs)
    
    def decode(self, text):
        if isinstance(text, bytes):
            text = text.decode()
        return text
    
    def handle_charref(self, tag_name, tag_text):
        convert_charref = self.parser_args[1].get('convert_charref', True)
        if tag_name not in self.CDATA_CONTENT_ELEMENTS and convert_charref:
            if isinstance(tag_text, list):
                *tag_text, = map(lambda text: self.handle_charref(tag_name, text), tag_text)
            elif isinstance(tag_text, (str, bytes)):
                tag_text = unescape(self.decode(tag_text))
        return tag_text

    def toString(self, tag_name, lst, strict=True, delimiter=" "):
        if isinstance(lst, (str, bytes)):
            return self.decode(lst)
        string_list = []
        for item in lst:
            if isinstance(item, (str, bytes)):
                string_list.append(self.toString(tag_name, item))
            elif strict:
                raise ValueError("Attributes of '%s' must be of type 'str' or 'bytes' not '%s'" % (tag_name, type(item)))
        return delimiter.join(string_list)

    def prepare_attrs(self, attrs):
        on_duplicate_attribute = self.parser_args[1].get('on_duplicate_attribute', self.REPLACE)
        if not isinstance(attrs[0], dict):
            raise SyntaxError("Tag attributes of type '%s' is not supported, attribute must be of type 'dict'" % type(attrs[0]))
        tag_attrs = {}
        for attr in attrs:
            for attr_name, attr_value in attr.items():
                if attr_name in tag_attrs:
                    if on_duplicate_attribute == self.IGNORE:
                        pass
                    elif on_duplicate_attribute in [None, self.REPLACE]:
                        tag_attrs[attr_name] = attr_value
                    else:
                        on_duplicate_attribute(tag_attrs, attr_name, attr_value)
                else:
                    tag_attrs[attr_name] = attr_value
        return tag_attrs

    def handle_comment(self, comment):
        self.feed(comment)
        self.soup.endData(Comment)

    def xml_feed(self, markup):
        raise NotImplementedError

    def feed(self, markup):
        # avoind modifying the original json data
        if isinstance(markup, (list, dict, tuple)):
            markup_copy = deepcopy(markup)
        else:
            markup_copy = markup
        if self.is_xml:
            return self.xml_feed(markup_copy)
        else:
            return self.html_feed(markup_copy)

    def html_feed(self, markup):
        if isinstance(markup, dict):
            attr_name = self.parser_args[1].get('attr_name', 'attrs')
            text_name = self.parser_args[1].get('text_name', 'text')
            for tag_name, tag_datum in markup.items():
                if tag_name == text_name:
                    self.feed(self.toString(tag_name, tag_datum, "\n"))
                    continue
                if not isinstance(tag_datum, dict):
                    if tag_name.lower() == 'comment':
                        self.handle_comment(tag_datum)
                        continue
                    if tag_name.lower() == 'doctype':
                        self.feed(self.toString(tag_name, tag_datum))
                        self.soup.endData(Doctype)
                        continue
                    if not isinstance(tag_datum, list):
                        self.soup.handle_starttag(tag_name, None, None, {})
                        if not self.can_be_empty_element(tag_name):
                            self.feed(self.handle_charref(tag_name, tag_datum))
                        self.soup.handle_endtag(tag_name)
                        continue
                tag_attrs = {}
                tag_text = ""
                if isinstance(tag_datum, dict):
                    tag_attrs = tag_datum.pop(attr_name, tag_attrs) or tag_attrs
                    tag_text = tag_datum.pop(text_name, tag_text) or tag_text
                    tag_datum = [tag_datum]
                if tag_attrs and isinstance(tag_attrs, list):
                    tag_attrs = self.prepare_attrs(tag_attrs)
                for tag_data in tag_datum:
                    self.soup.handle_starttag(tag_name, None, None, tag_attrs)
                    if not self.can_be_empty_element(tag_name):
                        if tag_text:
                            self.soup.handle_data(self.decode(tag_text))
                        self.feed(self.handle_charref(tag_name, tag_data))
                    self.soup.handle_endtag(tag_name)
        elif isinstance(markup, list):
            for tag_data in markup:
                self.feed(tag_data)
        else:
            self.soup.endData()
            self.soup.handle_data(self.decode(markup or ''))


def install(debug=False):
    # Register our builder
    setattr(builder, "JsonTreeBuilder", JsonTreeBuilder)
    builder.__all__.append("JsonTreeBuilder")
    builder.builder_registry.register(JsonTreeBuilder)
    if debug:
        print("Builder installed")


__all__ = [
    __name,
    'install'
]

__locals = locals()
setattr(__locals[__name], "__module__", JSOUP)