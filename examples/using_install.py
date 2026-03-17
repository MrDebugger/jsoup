"""Using jsoup via install() for cleaner syntax."""

from bs4 import BeautifulSoup
from jsoup import install

install()

# Full webpage structure
json = {
    "doctype": "html",
    "html": {
        "head": {
            "title": "My Webpage",
            "meta": {"attrs": {"charset": "UTF-8"}}
        },
        "body": {
            "header": {
                "h1": {"attrs": {"class": ["heading1"]}, "text": "Hello World"},
                "nav": {
                    "ul": {"li": [
                        {"a": {"attrs": {"href": "/home"}, "text": "Home"}},
                        {"a": {"attrs": {"href": "/about"}, "text": "About"}}
                    ]}
                }
            },
            "main": {
                "section": {
                    "h2": "Introduction",
                    "p": ["First paragraph.", "Second paragraph."],
                    "img": {"attrs": {"src": "/images/photo.jpg", "alt": "Photo"}},
                    "br": None
                },
                "aside": {
                    "h3": "Related Links",
                    "ul": {"li": [
                        {"a": {"attrs": {"href": "/link1"}, "text": "Link 1"}},
                        {"a": {"attrs": {"href": "/link2"}, "text": "Link 2"}}
                    ]}
                }
            },
            "footer": {"p": "Copyright 2026"}
        }
    }
}

soup = BeautifulSoup(json, 'jsoup')

print("Title:", soup.html.head.title.string)
print("First nav link:", soup.html.body.header.nav.ul.li.a.string)
print("Image src:", soup.html.body.main.section.img['src'])
print()
print(soup.prettify())
