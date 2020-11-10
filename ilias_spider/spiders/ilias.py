# -*- coding: utf-8 -*-

import os
import platform
import scrapy
from scrapy.selector import *
from scrapy.http.request import Request
from config import *
from privacy import *

class iliasSpider(scrapy.Spider):
	name = SPIDER_NAME

	start_urls = [
		ILIAS_LOGIN_URL
	]

	def __init__(self, username=None, iliasUrl=None, targetDir=None, assignmentsIdStr=None, slidesIdStr=None, assignmentsDir=None, slidesDir=None, *args, **kwargs):
		super(iliasSpider, self).__init__(*args, **kwargs)
		self.items = {}
		self.username = username
		self.ilias_url = iliasUrl
		self.target_dir = targetDir
		self.assignments_id_str = assignmentsIdStr
		self.slides_id_str = slidesIdStr
		self.assignments_dir = assignmentsDir
		self.slides_dir = slidesDir

		setAuth(self.username)


	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formdata={'username': self.username, 'password': getPassword()},
			callback=self.after_login
		)


	def after_login(self, response):
		# check login succeed before going on
		if b"authentication failed" in response.body:
			self.logger.error("Login failed")
			print("authentication failed")
			resetPassword(self.username)
			print("The password has been reset. Please restart the program and enter your password again.")
			return
		else:
			print("Login succeesful")
			yield Request(
				url= self.ilias_url,
				callback=self.findDownloadLinksAndNames
			)


	def findDownloadLinksAndNames(self,response):
		sel = Selector(response)
		fnames = sel.css("h4.il_ContainerItemTitle a::text").extract()
		links = sel.css("div.il_ContainerItemTitle a::attr(href)").extract()
		# Extract item Properties
		rawProperties = sel.css("div.ilListItemSection.il_ItemProperties").extract()
		itemProperties = []
		for text in rawProperties:
			# Format: [fileExtension,DownloadSize,Date,[Pages]], pages field does not exist for all items
			properties = list(map(lambda x: x.strip(),Selector(text=text).css("span.il_ItemProperty::text").extract()))
			itemProperties.append(properties)
		# File extensions
		fextensions = [a[0] for a in itemProperties]
		fsize = [self.format_fsize(a[1]) for a in itemProperties]

		items = zip(fnames,links,fextensions,fsize)
		for (name,href,ext,size) in items:
			self.items[href] = {
				'href': href,
				'name': name,
				'ext': ext,
				'size': size
			}

		for item in self.items.values():
			if self.verify_item(item):
				yield Request(
					url = item['href'],
					callback = self.download
				)

	# Verifiy if item should be downloaded
	def verify_item(self, item):
		href = item['href']
		name = item['name']
		ext = item['ext']
		size = item['size']

		if not "download" in href:
			if VERBOSE:
				print("Ignoring file, cause: FILE_ALREADY_DOWNLOADED : %s.%s" % (name, ext))
			return False
		
		if ext in IGNORE_FILE_EXTENSIONS:
			if VERBOSE:
				print("Ignoring file, cause: FILE_ALREADY_DOWNLOADED : %s.%s" % (name, ext))
			return False

		# verify if file already exists
		filename = self.prepFileName(name, ext)
		path = self.getStoreDir(filename) + filename
		if os.path.exists(path):
			if VERBOSE:
				print("Ignoring file, cause: FILE_ALREADY_DOWNLOADED : %s.%s" % (filename, ext))
			return False

		return True


	# save file
	def store(self, filename, content):
		storeDir = self.getStoreDir(filename)

		print("Downloading %s to %s" %(filename, storeDir))
		if PLATFORM == "Linux":
			# in linux files has to be stored first in the tmp folder
			with open(TMP_DIR + filename, "wb") as f:
				f.write(content)
			os.system("mv " + TMP_DIR + filename + " " + storeDir + filename)
		elif PLATFORM == "Windows":
			with open(storeDir + filename, "wb") as f:
				f.write(content)


	# prep filename for easier handling
	def prepFileName(self, filename, ext):
		filename = filename.replace("/","_")
		filename = filename.replace(" ","_")
		filename = filename.replace("(","_")
		filename = filename.replace(")","_")
	
		return filename + "." + ext


	# where to move file to
	def getStoreDir(self, filename):
		if self.slides_id_str in filename:
			return self.slides_dir
		elif self.assignments_id_str in filename:
			return self.assignments_dir
		return self.target_dir


	# download controller
	def download(self, response):
		url = str(response.url)
		filename = self.prepFileName(self.items[url]['name'], self.items[url]['ext'])
		self.store(filename, response.body)

	# format file size
	def format_fsize(self, size):
		num,unit = size.split()
		if unit == 'Bytes':
			unit = ' B'
		return ('%5.1f %s' % (float(num.replace(',','.')), unit))