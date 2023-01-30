from bs4 import BeautifulSoup
from jsoup import install
install()

json = {
    "doctype": "html PUBLIC",
    "html": {
        "head": {
            "title": "My webpage",
            "meta": {
                "attrs": {
                    "charset": "UTF-8"
                }
            }
        },
        "body": {
            "header": {
                "h1": {"attrs":{"class":["heading1"]}, "text":"Hello World"},
                "nav": {
                    "ul": {
                        "li": [   
                            {"a": {"attrs":{"href":"/home"}, "text":"Home"}},
                            {"a": {"attrs":{"href":"/about"}, "text":"About"}}
                        ]
                    }
                }
            },
            "main": {
                "section": {
                    "h2": "Introduction",
                    "p": ["this ", "is ", None,"test 1<2 && 2>1 ", {"comment":["this part of paragraph tag",{"a":"this is an anchor tag"},"this is a comment"]}],
                    "img": {"attrs":{"src":"/images/image.jpg", "alt":"image"}},
                    "br": None
                },
                "aside": {
                    "h3": "Related links",
                    "ul": {
                        "li": [
                            {"a": {"attrs":{"href":"/link1"}, "text":"Link 1"}},
                            {"a": {"attrs":{"href":"/link2"}, "text":"Link 2"}},
                            {"a": {"attrs":{"href":"/link3"}, "text":"Link 3"}}
                        ]
                    }
                }
            },
            "footer": {
                "p": "Copyright © 2021 My Webpage"
            }
        }
    }
}

# Convert JSON to BeautifulSoup object
soup = BeautifulSoup(json, 'jsoup')
# Print the title of the webpage
print(soup.html.head.title.string)
# Print the text of the first link in the nav
print(soup.html.body.header.nav.ul.li.a.string)
# Print the source of the image
print(soup.html.body.main.section.img['src'])
# Print the text of the first li in the aside
print(soup.html.body.main.aside.ul.li.a.string)
# Print the copyright text in the footer
print(soup.html.body.footer.p.string)
# Print all the anchors tags in the main section
for a in soup.html.body.main.find_all('a'):
    print(a)
# Print all the attributes of the first li in the aside
for attr, value in soup.html.body.main.aside.ul.li.a.attrs.items():
    print(f'{attr}: {value}')
# Print the html data
print(soup.prettify())
