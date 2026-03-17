"""Roundtrip: HTML -> JSON (bs2json) -> HTML (jsoup)."""

from bs2json import BS2Json
from bs4 import BeautifulSoup
from jsoup import JsonTreeBuilder

# Original HTML
html = """
<html>
<body>
    <h1>Title</h1>
    <p class="intro">Hello <b>world</b></p>
    <table id="data">
        <tr><th>Name</th><th>Score</th></tr>
        <tr><td>Alice</td><td>95</td></tr>
        <tr><td>Bob</td><td>87</td></tr>
    </table>
    <p>Footer text</p>
</body>
</html>
"""

# Step 1: HTML -> JSON using bs2json
json_data = BS2Json(html).convert()
print("=== JSON (from bs2json) ===")
import json
print(json.dumps(json_data, indent=2))

# Step 2: JSON -> HTML using jsoup
soup = BeautifulSoup(json_data, builder=JsonTreeBuilder)
print("\n=== HTML (from jsoup) ===")
print(soup.prettify())

# Verify structure is preserved
print("=== Verification ===")
print("Title:", soup.find('h1').string)
print("Table ID:", soup.find('table')['id'])
print("Rows:", len(soup.find_all('tr')))
