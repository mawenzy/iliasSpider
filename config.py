# -*- coding: utf-8 -*-

import os
import platform

class Config():
	def __init__(self, username, ilias_url, target_dir):
		self.USERNAME = username
		self.ILIAS_URL = ilias_url
		self.TARGET_DIR = target_dir

def runSpider(c):
	call = "scrapy crawl ilias -s LOG_ENABLED=False -a username=%s -a iliasUrl=%s -a targetDir=%s"%(c.USERNAME, c.ILIAS_URL, c.TARGET_DIR)
	os.system(call)

# just a name, is used as id for keyring if you change this after your pwd has been stored 
# you will need to reenter your password
SPIDER_NAME = "ilias"

# User Platform
PLATFORM = platform.system()

# since urls might change
ILIAS_LOGIN_URL = 'https://ilias.uni-konstanz.de/ilias/login.php'
ILIAS_BASE_URL = 'https://ilias.uni-konstanz.de/ilias/'

# only needed for linux
TMP_DIR = "/tmp/"

# ignored file extensions
IGNORE_FILE_EXTENSIONS = ['mp4']

# manage output
VERBOSE = False