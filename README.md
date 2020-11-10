
# iliasSpider

Fork from [MisterXY89/iliasSpider](https://github.com/MisterXY89/iliasSpider).

`iliasSpider` is a web scraper which downloads your materials from an ilias course (@Uni Constance) written in python. 

## Functionality

In the current state, the scraper just tries to copy to ilias file system to the computer, creating necessary folders on the way. Everything the spider does not know is ignored.

## Features over original fork

- Correct file extensions
- Only files which do not exist locally are downloaded
- Exclusion based on file formats in the [config](config.py). By default .mp4 files are excluded
- Checks if a file should be downloaded are done before downloading:)

## Approach
I am using [scrapy (docs)](https://docs.scrapy.org/en/latest/index.html) to login and download the files. 

> Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide range of useful applications, like data mining, information processing or historical archival.
> 

For those who are not familiar with the scrapy folder structure:
The spider can be found here: `ilias_spider/spiders/ilias.py`.

## Get things going

### Setup
Install (if not satisfied):
pip https://pip.pypa.io/en/stable/
 - **FOR LINUX:** 
	- Python 2.x or 3.x  https://www.python.org/downloads/
	 - the following python reqs. via pip:
	`$ pip install -r requirements.txt`

 -  **FOR WINDOWS:** 
	 - Python 2.7 (since Python 3 is not supported on Windows with Scrapy)
	 - follow the [instructions](https://doc.scrapy.org/en/1.1/intro/install.html#windows) to set up scrapy & restart
	 - `$ pip install keyring`

### Configure Spiders
An example configuration is given in `iliasSpiders.py`:
```python
### Spider 1
c = Config(
    'vorname.nachname', 
    'entry url', 
    '/path/to/download/folder/', 
    )
runSpider(c)
```
More spiders can be configured by copying this code snippet.
