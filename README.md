[![PyPi version](https://img.shields.io/pypi/v/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![PyPi pyversions](https://img.shields.io/pypi/pyversions/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)
[![PyPi license](https://img.shields.io/pypi/l/jsoup.svg)](https://pypi.python.org/pypi/jsoup/)

# Jsoup

Jsoup is a python library that helps to parse and build HTML/XML structures using JSON format.

Installation
----

Use the package manager pip to install jsoup.


```
pip install jsoup

```


Usage
----

```python
from jsoup import JsonTreeBuilder
from bs4 import BeautifulSoup

json = {
        "body": {
            "h1": {"attrs":{"class":"heading1"}, "text":"Hello World"},
            "p": ["this ", "is ", "a ","test 1<2 && 2>1", {"comment":["this is a comment"]}],
            "comment": "this is also a comment",
            "br": None,
            "form" : {
                "attrs": {
                    "method": "post"
                },
                "input": {"attrs":{
                    "type": "text",
                    "name": "username"
                }}
            }
        }
}

soup = BeautifulSoup(json, builder=JsonTreeBuilder)
print(soup.prettify())
```

Output
----

```html
<body>
 <h1 class="heading1">
  Hello World
 </h1>
 <p>
  this
 </p>
 <p>
  is
 </p>
 <p>
  a
 </p>
 <p>
  test 1&lt;2 &amp;&amp; 2&gt;1
 </p>
 <p>
  <!--this is a comment-->
 </p>
 <!--this is also a comment-->
 <br/>
 <form method="post">
  <input name="username" type="text"/>
 </form>
</body>
```



Contributing
----

We welcome contributions to `jsoup`. To get started, follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your changes.
3. Make your changes and write tests to cover them.
4. Ensure all tests pass by running `python -m unittest discover -v`.
5. Push your changes to your fork and create a pull request.

We appreciate all contributions and thank all the contributors!

<a href = "https://github.com/MrDebugger/jsoup/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=MrDebugger/jsoup"/>
</a>
