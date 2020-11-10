# -*- coding: utf-8 -*-

import platform

class Config():
	def __init__(self, username, ilias_url, target_dir):
		self.USERNAME = username
		self.ILIAS_URL = ilias_url
		self.TARGET_DIR = target_dir


# just a name, is used as id for keyring if you change this after your pwd has been stored 
# you will need to reenter your password
SPIDER_NAME = "ilias"

# User Platform
PLATFORM = platform.system()

# since urls might change
ILIAS_LOGIN_URL = 'https://ilias.uni-konstanz.de/ilias/login.php'

# only needed for linux
TMP_DIR = "/tmp/"

# ignored file extensions
IGNORE_FILE_EXTENSIONS = ['mp4']

# manage output
VERBOSE = True