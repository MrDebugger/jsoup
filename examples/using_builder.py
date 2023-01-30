from jsoup import JsonTreeBuilder
from bs4 import BeautifulSoup


json = {
        "body": {
            "h1": {"attrs":{"class":"heading1"}, "text":"Hello World"},
            "p": ["this ", "is ", "a ","test 1<2 && 2>1", {"comment":["this is not the comment","this is a comment"], "text":"this is in paragraph"}],
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