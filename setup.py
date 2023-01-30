#! /usr/bin/env python3

from setuptools import setup, find_packages
from jsoup import __version__

url = "https://github.com/MrDebugger/jsoup"

setup(
    name="jsoup",
    packages=find_packages(),
    url=url,
    version=__version__,
    license="MIT",
    author="Ijaz Ur Rahim",
    author_email="ijazkhan095@gmail.com",
    description="Convert JSON to BeautifulSoup object",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    keywords=[
        "parser",
        "html",
        "bs4",
        "BeautifulSoup",
        "soup",
        "jsoup",
        "json",
        "builder"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],

    install_requires=[
        'beautifulsoup4==4.9.3'
    ],
    python_requires='>=3.6',
)
