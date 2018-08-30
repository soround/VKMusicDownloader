#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import datetime
import json

import requests
import socket
import wget


def remove_symbols(filename):
	return re.sub(r'[\/:;*?<>|«»",]', "", filename)


def check_file_path(path):
	try:
		os.stat(path)
	except OSError as e:
		return False

	return True


def get_path(self, Object):
	return Object.getExistingDirectory(
		self, "Выберите папку для скачивания", "", Object.ShowDirsOnly)


def check_connection(url):
	try:
		requests.get(url, timeout=5)
	except Exception as e:
		return False
		
	return True
	
	
def get_internal_ip():
	return socket.gethostbyname(socket.getfqdn())


def get_external_ip():
	try:
		return bytes(requests.get("http://ident.me/", timeout=5).content
			).decode("utf-8")
		
	except Exception as e:
		return None


def get_network_info():
	return requests.get("http://ipinfo.io", timeout=5).json()


def unix_time_stamp_convert(time):
	return datetime.datetime.fromtimestamp(int(time)
		).strftime("%d.%m.%Y %H:%M:%S")


def time_duration(time):
	return str(datetime.timedelta(seconds=int(time)))


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            

def downloads_files_in_wget(url, filename):
	wget.download(url, filename)


def get_size_content(url):
	try:
		return requests.head(url, timeout=5).headers['content-length']
	except 	Exception as e:
		return 0 


def downloads_files(url, filename):
	data = requests.get(url, stream=True)
	size = 0
	with open(filename, 'wb') as f:
		for chunk in data.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				size += 1024

	return filename