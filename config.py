# -*- coding: utf-8 -*-

import platform

class Config():
	def __init__(self, username, ilias_url, target_dir, assignments_id_str, slides_id_str, assignments_dir, slides_dir):
		self.USERNAME = username
		self.ILIAS_URL = ilias_url
		self.TARGET_DIR = target_dir

		self.ASSIGNMENTS_ID_STR = assignments_id_str
		self.SLIDES_ID_STR = slides_id_str

		self.ASSIGNMENTS_DIR = self.TARGET_DIR + assignments_dir
		self.SLIDES_DIR = self.TARGET_DIR + slides_dir


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