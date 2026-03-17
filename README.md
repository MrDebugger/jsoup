[![PyPI version](https://img.shields.io/pypi/v/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![PyPI downloads](https://img.shields.io/pypi/dm/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![PyPI license](https://img.shields.io/pypi/l/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![GitHub stars](https://img.shields.io/github/stars/MrDebugger/jsoup.svg)](https://github.com/MrDebugger/jsoup/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/MrDebugger/jsoup.svg)](https://github.com/MrDebugger/jsoup/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/MrDebugger/jsoup.svg)](https://github.com/MrDebugger/jsoup/commits)

<h1 align="center">jsoup</h1>

<div align="center">

A Python library that converts JSON structures into BeautifulSoup HTML/XML trees.
The inverse of [bs2json](https://github.com/MrDebugger/bs2json) — build HTML from dictionaries
with full support for attributes, comments, doctypes, and nested elements.

**Python 3.8+** | Only dependency: `beautifulsoup4`

</div>

---

<details open>
<summary><b>Table of Contents</b></summary>
<br>

| Section | Description |
|---------|-------------|
| [Installation](#installation) | How to install |
| [Quick Start](#quick-start) | Basic usage |
| [Input Format](#input-format) | How JSON maps to HTML |
| [Features](#features) | Attributes, lists, comments, empty elements, doctypes |
| [bs2json Roundtrip](#bs2json-roundtrip) | Using bs2json output as jsoup input |
| [Options](#options) | Custom labels, duplicate attributes, char refs |
| [API Reference](#api-reference) | JsonTreeBuilder, install() |
| [Contributing](#contributing) | How to contribute |

</details>

---

## Installation

```bash
pip install -U jsoup
```

---

## Quick Start

```python
from jsoup import JsonTreeBuilder
from bs4 import BeautifulSoup

json = {
    "body": {
        "h1": {"attrs": {"class": "title"}, "text": "Hello World"},
        "p": "This is a paragraph.",
        "br": None,
        "ul": {
            "li": ["Item 1", "Item 2", "Item 3"]
        }
    }
}

soup = BeautifulSoup(json, builder=JsonTreeBuilder)
print(soup.prettify())
```

**Output:**
```html
<body>
 <h1 class="title">
  Hello World
 </h1>
 <p>
  This is a paragraph.
 </p>
 <br/>
 <ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
 </ul>
</body>
```

---

## Input Format

| JSON | HTML |
|------|------|
| `{"p": "text"}` | `<p>text</p>` |
| `{"br": None}` | `<br/>` |
| `{"p": {"attrs": {"class": "x"}, "text": "hello"}}` | `<p class="x">hello</p>` |
| `{"li": ["a", "b", "c"]}` | `<li>a</li><li>b</li><li>c</li>` |
| `{"comment": "note"}` | `<!--note-->` |
| `{"doctype": "html"}` | `<!DOCTYPE html>` |
| `{"div": {"children": [{"p": "a"}, {"p": "b"}]}}` | `<div><p>a</p><p>b</p></div>` |

---

## Features

<details open>
<summary><b>Attributes</b></summary>
<br>

Attributes are passed via the `attrs` key:

```python
json = {
    "a": {"attrs": {"href": "/home", "class": "nav"}, "text": "Home"},
    "img": {"attrs": {"src": "photo.jpg", "alt": "Photo"}}
}
```

Produces:
```html
<a class="nav" href="/home">Home</a>
<img alt="Photo" src="photo.jpg"/>
```

</details>

<details open>
<summary><b>Lists (Multiple Same Tags)</b></summary>
<br>

A list value creates multiple tags with the same name:

```python
json = {"ul": {"li": ["Apple", "Banana", "Cherry"]}}
```

Produces:
```html
<ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>
```

List items can also be dicts with nested content:

```python
json = {"ul": {"li": [
    "Simple item",
    {"text": "Item with link", "a": {"attrs": {"href": "/"}, "text": "click"}}
]}}
```

</details>

<details>
<summary><b>Comments</b></summary>
<br>

```python
json = {
    "body": {
        "comment": "This is a comment",
        "p": "Visible text"
    }
}
# Produces: <!--This is a comment--><p>Visible text</p>
```

</details>

<details>
<summary><b>Empty Elements</b></summary>
<br>

Use `None` for self-closing tags:

```python
json = {"body": {"br": None, "hr": None}}
# Produces: <body><br/><hr/></body>
```

</details>

<details>
<summary><b>Doctypes</b></summary>
<br>

```python
json = {
    "doctype": "html",
    "html": {"body": {"p": "content"}}
}
```

</details>

<details>
<summary><b>Nested Structures</b></summary>
<br>

Nesting works naturally:

```python
json = {
    "html": {
        "head": {"title": "My Page"},
        "body": {
            "header": {
                "nav": {"ul": {"li": [
                    {"a": {"attrs": {"href": "/"}, "text": "Home"}},
                    {"a": {"attrs": {"href": "/about"}, "text": "About"}}
                ]}}
            },
            "main": {"h1": "Welcome", "p": "Content here"},
            "footer": {"p": "Copyright 2026"}
        }
    }
}
```

</details>

---

## bs2json Roundtrip

jsoup understands the `children` key from [bs2json](https://github.com/MrDebugger/bs2json)'s ordered output, enabling **roundtrip conversion**:

```python
from bs2json import BS2Json
from bs4 import BeautifulSoup
from jsoup import JsonTreeBuilder

# HTML -> JSON (bs2json)
html = "<html><body><h1>Title</h1><p>Text</p><h1>Another</h1></body></html>"
json_data = BS2Json(html).convert()
# {'html': {'body': {'children': [{'h1': 'Title'}, {'p': 'Text'}, {'h1': 'Another'}]}}}

# JSON -> HTML (jsoup)
soup = BeautifulSoup(json_data, builder=JsonTreeBuilder)
print(soup.prettify())
# <html><body><h1>Title</h1><p>Text</p><h1>Another</h1></body></html>
```

The `children` key preserves element order, including elements with attributes:

```python
json = {
    "table": {
        "attrs": {"id": "data"},
        "children": [
            {"tr": {"children": [{"th": "Name"}, {"th": "Score"}]}},
            {"tr": {"children": [{"td": "Alice"}, {"td": "95"}]}}
        ]
    }
}
```

---

## Options

<details>
<summary><b>Using install() for Cleaner Syntax</b></summary>
<br>

Register jsoup so you can use `"jsoup"` as a parser string:

```python
from jsoup import install
install()

from bs4 import BeautifulSoup
soup = BeautifulSoup({"p": "hello"}, "jsoup")
```

</details>

<details>
<summary><b>Custom Label Names</b></summary>
<br>

Override the default key names for attributes, text, and children:

```python
json = {"p": {"@": {"class": "x"}, "#text": "hello"}}
soup = BeautifulSoup(json, builder=JsonTreeBuilder,
                     attr_name='@', text_name='#text')
# <p class="x">hello</p>
```

</details>

<details>
<summary><b>Duplicate Attributes</b></summary>
<br>

Control how duplicate attribute keys are handled when attrs is a list of dicts:

```python
json = {"p": {"attrs": [{"class": "a"}, {"class": "b"}], "text": "hello"}}

# Replace (default): last value wins
soup = BeautifulSoup(json, builder=JsonTreeBuilder, on_duplicate_attribute="replace")

# Ignore: first value wins
soup = BeautifulSoup(json, builder=JsonTreeBuilder, on_duplicate_attribute="ignore")

# Callable: custom merge logic
def merge(attrs, name, value):
    attrs[name] += " " + value

soup = BeautifulSoup(json, builder=JsonTreeBuilder, on_duplicate_attribute=merge)
```

</details>

<details>
<summary><b>Character References</b></summary>
<br>

HTML entities are escaped automatically:

```python
json = {"p": "1<2 && 2>1"}
soup = BeautifulSoup(json, builder=JsonTreeBuilder)
# <p>1&lt;2 &amp;&amp; 2&gt;1</p>
```

</details>

---

## API Reference

<details open>
<summary><b>JsonTreeBuilder</b></summary>
<br>

A BeautifulSoup `TreeBuilder` that accepts JSON dicts as input.

```python
from jsoup import JsonTreeBuilder
soup = BeautifulSoup(json_data, builder=JsonTreeBuilder, **options)
```

**Options** (passed as kwargs to `BeautifulSoup`):

| Option | Default | Description |
|--------|---------|-------------|
| `attr_name` | `"attrs"` | JSON key for element attributes |
| `text_name` | `"text"` | JSON key for text content |
| `children_name` | `"children"` | JSON key for ordered children list |
| `on_duplicate_attribute` | `"replace"` | How to handle duplicate attrs: `"replace"`, `"ignore"`, or callable |
| `convert_charref` | `True` | Whether to escape HTML entities |

</details>

<details open>
<summary><b>install()</b></summary>
<br>

Register JsonTreeBuilder so `"jsoup"` can be used as a parser string:

```python
from jsoup import install
install(debug=False)
```

After calling `install()`:
```python
soup = BeautifulSoup(json_data, "jsoup")
```

</details>

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, versioning guide, and how to submit changes.

<a href="https://github.com/MrDebugger/jsoup/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MrDebugger/jsoup"/>
</a>
