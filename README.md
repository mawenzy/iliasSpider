# iliasSpider

`iliasSpider` is a web scraper which downloads your materials from an ilias course (@Uni Constance) written in python. 

## Approach
I am using [scrapy (docs)](https://docs.scrapy.org/en/latest/index.html) to login and download the files. 

> Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival.

## Get things going

### Setup
Install (if not satisfied):
 - Python 3.x  https://www.python.org/downloads/ 
 - pip https://pip.pypa.io/en/stable/
 - the following python reqs. via pip:
`$ pip install -r requirements.txt`

### Run it
You can create for every ilias folder a download program via `create.py`.  Simply run it with `pyhton create.py`.
You will be prompted a few questions to config your spider. Everything you need to know will be explained there.

## Possible Errors
Since all files are downloaded with a .pdf extension there might occur an error downloading files of another file format. 
In most cases, it is sufficient to just change the .pdf extension to the correct one.
If any errors occur, try to restart the program and check your config. If it still occurs open a new [issue](https://github.com/MisterXY89/iliasSpider/issue).
