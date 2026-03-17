"""JsonTreeBuilder — a BeautifulSoup TreeBuilder that accepts JSON input."""

from typing import Any, Dict, List, Optional, Union
from html import unescape
from copy import deepcopy
from bs4.builder import (
    HTMLTreeBuilder,
    HTML,
    STRICT,
    FAST,
)
from bs4.element import Comment, Doctype


JSOUP = "jsoup"


class JsonTreeBuilder(HTMLTreeBuilder):
    """A BeautifulSoup TreeBuilder that converts JSON dicts into HTML/XML trees.

    Accepts JSON structures where keys are tag names and values are content,
    attributes, or nested elements. Supports both the standard jsoup format
    and bs2json's ordered output format (with 'children' key).

    Usage:
        soup = BeautifulSoup(json_data, builder=JsonTreeBuilder)
        soup = BeautifulSoup(json_data, "jsoup")  # after install()
    """

    is_xml: bool = False
    picklable: bool = True
    NAME: str = JSOUP
    features: List[str] = [NAME, HTML, STRICT, FAST, "json"]
    TRACKS_LINE_NUMBERS: bool = False

    REPLACE: str = "replace"
    IGNORE: str = "ignore"
    CDATA_CONTENT_ELEMENTS: tuple = ("script", "style")

    def __init__(self, parser_args=None, parser_kwargs=None, **kwargs) -> None:
        extra_parser_kwargs = {}
        for arg in ('on_duplicate_attribute', 'attr_name', 'text_name', 'children_name'):
            if arg in kwargs:
                extra_parser_kwargs[arg] = kwargs.pop(arg)
        super().__init__(**kwargs)
        parser_args = parser_args or []
        parser_kwargs = parser_kwargs or {}
        parser_kwargs.update(extra_parser_kwargs)
        self.parser_args = (parser_args, parser_kwargs)

    def __repr__(self) -> str:
        return f"JsonTreeBuilder(features={self.features})"

    def _decode(self, text: Union[str, bytes]) -> str:
        """Decode bytes to string if needed."""
        if isinstance(text, bytes):
            text = text.decode()
        return text

    def _handle_charref(self, tag_name: str, tag_text: Any) -> Any:
        """Unescape HTML character references unless in CDATA elements."""
        convert_charref = self.parser_args[1].get('convert_charref', True)
        if tag_name not in self.CDATA_CONTENT_ELEMENTS and convert_charref:
            if isinstance(tag_text, list):
                tag_text = [self._handle_charref(tag_name, t) for t in tag_text]
            elif isinstance(tag_text, (str, bytes)):
                tag_text = unescape(self._decode(tag_text))
        return tag_text

    def _to_string(self, tag_name: str, lst: Any, strict: bool = True,
                   delimiter: str = " ") -> str:
        """Convert a value to a string, joining lists with delimiter."""
        if isinstance(lst, (str, bytes)):
            return self._decode(lst)
        string_list = []
        for item in lst:
            if isinstance(item, (str, bytes)):
                string_list.append(self._to_string(tag_name, item))
            elif strict:
                raise ValueError(
                    f"Attributes of '{tag_name}' must be of type 'str' or "
                    f"'bytes' not '{type(item)}'"
                )
        return delimiter.join(string_list)

    def _prepare_attrs(self, attrs: List[Dict]) -> Dict:
        """Merge a list of attribute dicts, handling duplicates."""
        on_duplicate = self.parser_args[1].get(
            'on_duplicate_attribute', self.REPLACE
        )
        if not isinstance(attrs[0], dict):
            raise SyntaxError(
                f"Tag attributes of type '{type(attrs[0])}' is not supported, "
                f"attribute must be of type 'dict'"
            )
        tag_attrs = {}
        for attr in attrs:
            for attr_name, attr_value in attr.items():
                if attr_name in tag_attrs:
                    if on_duplicate == self.IGNORE:
                        pass
                    elif on_duplicate in [None, self.REPLACE]:
                        tag_attrs[attr_name] = attr_value
                    else:
                        on_duplicate(tag_attrs, attr_name, attr_value)
                else:
                    tag_attrs[attr_name] = attr_value
        return tag_attrs

    def _handle_comment(self, comment: Any) -> None:
        """Insert an HTML comment node."""
        if isinstance(comment, list):
            for item in comment:
                self._handle_comment(item)
            return
        self.feed(comment)
        self.soup.endData(Comment)

    def feed(self, markup: Any) -> None:
        """Feed JSON markup into the builder.

        Makes a deep copy of mutable inputs to avoid modifying the original data.
        """
        if isinstance(markup, (list, dict, tuple)):
            markup = deepcopy(markup)
        self._html_feed(markup)

    def _html_feed(self, markup: Any) -> None:
        """Recursive HTML feed that processes JSON structures into soup elements."""
        if isinstance(markup, dict):
            self._feed_dict(markup)
        elif isinstance(markup, list):
            for item in markup:
                self.feed(item)
        else:
            self.soup.endData()
            self.soup.handle_data(self._decode(markup or ''))

    def _feed_dict(self, markup: Dict) -> None:
        """Process a JSON dict, converting keys to HTML tags."""
        attr_name = self.parser_args[1].get('attr_name', 'attrs')
        text_name = self.parser_args[1].get('text_name', 'text')
        children_name = self.parser_args[1].get('children_name', 'children')

        for tag_name, tag_datum in markup.items():
            # Text content
            if tag_name == text_name:
                self.feed(self._to_string(tag_name, tag_datum, False, "\n"))
                continue

            # Children list (bs2json ordered format)
            if tag_name == children_name and isinstance(tag_datum, list):
                for child in tag_datum:
                    self.feed(child)
                continue

            if not isinstance(tag_datum, dict):
                # Comment
                if tag_name.lower() == 'comment':
                    self._handle_comment(tag_datum)
                    continue
                # Doctype
                if tag_name.lower() == 'doctype':
                    self.feed(self._to_string(tag_name, tag_datum))
                    self.soup.endData(Doctype)
                    continue
                # Simple tag with text or None (empty element)
                if not isinstance(tag_datum, list):
                    self.soup.handle_starttag(tag_name, None, None, {})
                    if not self.can_be_empty_element(tag_name):
                        self.feed(self._handle_charref(tag_name, tag_datum))
                    self.soup.handle_endtag(tag_name)
                    continue

            # Tag with attributes and/or nested content
            tag_attrs = {}
            tag_text = ""
            if isinstance(tag_datum, dict):
                tag_attrs = tag_datum.pop(attr_name, tag_attrs) or tag_attrs
                tag_text = tag_datum.pop(text_name, tag_text) or tag_text
                # Handle children key (bs2json ordered format)
                children = tag_datum.pop(children_name, None)
                if children is not None:
                    if tag_attrs and isinstance(tag_attrs, list):
                        tag_attrs = self._prepare_attrs(tag_attrs)
                    self.soup.handle_starttag(tag_name, None, None, tag_attrs)
                    if tag_text:
                        self.soup.handle_data(self._decode(tag_text))
                    for child in children:
                        self.feed(child)
                    self.soup.handle_endtag(tag_name)
                    continue
                tag_datum = [tag_datum]

            if tag_attrs and isinstance(tag_attrs, list):
                tag_attrs = self._prepare_attrs(tag_attrs)

            for tag_data in tag_datum:
                self.soup.handle_starttag(tag_name, None, None, tag_attrs)
                if not self.can_be_empty_element(tag_name):
                    if tag_text:
                        self.soup.handle_data(self._decode(tag_text))
                    self.feed(self._handle_charref(tag_name, tag_data))
                self.soup.handle_endtag(tag_name)
