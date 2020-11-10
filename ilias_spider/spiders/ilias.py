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
				callback=lambda x: self.generic_visit(x,'')
			)

	# Applicable for crs, fold
	def generic_visit(self, response, relPath):
		if VERBOSE:
			print(" call: generic_visit(response, relPath=%s)" % relPath)

		sel = Selector(response)
		rows = sel.css("div.ilCLI.ilObjListRow.row").extract()

		for row in rows:
			rowSel = Selector(text=row)
			name = rowSel.css("h4.il_ContainerItemTitle a::text").get()
			href = rowSel.css("div.il_ContainerItemTitle a::attr(href)").get()

			if VERBOSE:
				print("\tProcessing: %s" % name)

			# Handle different types, switch statement for poor people
			if "download" in href:
				# get properties
				rawProperties = rowSel.css("div.ilListItemSection.il_ItemProperties").get()
				properties = list(map(lambda x: x.strip(),Selector(text=rawProperties).css("span.il_ItemProperty::text").extract()))
				
				ext = properties[0]
				size = properties[1]
					
				self.items[href] = {
					'href': href,
					'name': name,
					'ext': ext,
					'size': size
				}

				return
				if self.verify_download(href,relPath):
					yield Request(
						url=href,
						callback=lambda x: self.store(x,relPath)
					)
				continue

			if "goto_ilias_uni_fold" in href:
				newPath = relPath + name.replace(" ","") + os.path.sep

				if VERBOSE:
					print("Started: %s, %s" %(relPath,name))
					print("Searching folder: %s" % newPath)

				yield Request(
					url=href,
					callback=lambda x: self.generic_visit(x,newPath)
				)
				continue

			if "goto_ilias_uni_svy" in href:
				print("Skipping survey: %s" % name)
				continue

			if "goto_ilias_uni_frm" in href:
				print("Skipping forum: %s" % name)
				continue

			if "goto_ilias_uni_grp" in href:
				print("Skipping group: %s" % name)
				continue

			print("Can't handle link: %s, %s" % (name,href))


	# Verifiy if item should be downloaded
	def verify_download(self, href, relPath):
		href = self.items[href]['href']
		name = self.items[href]['name']
		ext = self.items[href]['ext']
		size = self.items[href]['size']

		if not "download" in href:
			if VERBOSE:
				print("Ignoring file, cause: NO_DOWNLOAD_LINK :      %s.%s" % (name, ext))
			return False
		
		if ext in IGNORE_FILE_EXTENSIONS:
			if VERBOSE:
				print("Ignoring file, cause: FILE_EXTENSION_IGNORED : %s.%s" % (name, ext))
			return False

		# verify if file already exists
		filename = self.prepFileName(name, ext)
		path = self.getStoreDir(filename) + relPath + filename
		if os.path.exists(path):
			if VERBOSE:
				print("Ignoring file, cause: FILE_ALREADY_DOWNLOADED : %s.%s" % (name, ext))
			return False

		return True


	# save file
	def store(self, response, relPath):
		url = str(response.url)
		filename = self.prepFileName(self.items[url]['name'], self.items[url]['ext'])
		content = response.body
		
		storeDir = self.getStoreDir(filename)

		if not os.path.exists(storeDir + relPath):
			os.mkdir(storeDir + relPath)

		path = storeDir + relPath + filename

		print("Downloading %s to %s" %(filename, storeDir))
		if PLATFORM == "Linux":
			# in linux files has to be stored first in the tmp folder
			with open(TMP_DIR + filename, "wb") as f:
				f.write(content)
			os.system("mv " + TMP_DIR + filename + " " + path)
		elif PLATFORM == "Windows":
			with open(path, "wb") as f:
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
		# if self.slides_id_str in filename:
		# 	return self.slides_dir
		# elif self.assignments_id_str in filename:
		# 	return self.assignments_dir
		return self.target_dir


	# format file size
	def format_fsize(self, size):
		num,unit = size.split()
		if unit == 'Bytes':
			unit = ' B'
		return ('%5.1f %s' % (float(num.replace(',','.')), unit))

