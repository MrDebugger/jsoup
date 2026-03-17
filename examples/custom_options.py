"""Custom label names and duplicate attribute handling."""

from bs4 import BeautifulSoup
from jsoup import JsonTreeBuilder

# Custom attribute and text label names
json = {
    "p": {"@": {"class": "highlight"}, "#text": "Custom labels!"}
}
soup = BeautifulSoup(json, builder=JsonTreeBuilder,
                     attr_name='@', text_name='#text')
print("Custom labels:", soup)

# Duplicate attributes - replace (default)
json_dup = {
    "p": {"attrs": [{"class": "first"}, {"class": "second"}], "text": "hello"}
}
soup = BeautifulSoup(json_dup, builder=JsonTreeBuilder,
                     on_duplicate_attribute="replace")
print("Replace:", soup)

# Duplicate attributes - ignore
soup = BeautifulSoup(json_dup, builder=JsonTreeBuilder,
                     on_duplicate_attribute="ignore")
print("Ignore:", soup)

# Duplicate attributes - merge callable
def merge_classes(attrs, name, value):
    attrs[name] += " " + value

soup = BeautifulSoup(json_dup, builder=JsonTreeBuilder,
                     on_duplicate_attribute=merge_classes)
print("Merge:", soup)
