"""Basic usage of jsoup with JsonTreeBuilder."""

from jsoup import JsonTreeBuilder
from bs4 import BeautifulSoup

# Simple HTML structure from JSON
json = {
    "body": {
        "h1": {"attrs": {"class": "heading1"}, "text": "Hello World"},
        "p": ["this ", "is ", "a ", "test 1<2 && 2>1"],
        "comment": "this is a comment",
        "br": None,
        "form": {
            "attrs": {"method": "post"},
            "input": {"attrs": {"type": "text", "name": "username"}}
        }
    }
}

soup = BeautifulSoup(json, builder=JsonTreeBuilder)
print("=== Basic Builder Usage ===")
print(soup.prettify())

# Nested structure
json2 = {
    "html": {
        "head": {"title": "My Page"},
        "body": {
            "h1": "Welcome",
            "ul": {"li": ["Item 1", "Item 2", "Item 3"]},
            "footer": {"p": "Copyright 2026"}
        }
    }
}

soup2 = BeautifulSoup(json2, builder=JsonTreeBuilder)
print("=== Nested Structure ===")
print(soup2.prettify())
