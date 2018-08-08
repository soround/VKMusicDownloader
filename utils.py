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


def check_connection(url):
	try:
		requests.get(url, timeout=5)
	except Exception as e:
		return False
		
	return True
	
	
def internal_ip():
	return socket.gethostbyname(socket.getfqdn())


def external_ip():
	try:
		external_ip = requests.get("https://ident.me/", timeout=5).content
		return bytes(external_ip).decode("utf-8")
		
	except Exception as e:
		return None


def unix_time_stamp_convert(time):
	return datetime.datetime.fromtimestamp(int(time)).strftime("%d.%m.%Y %H:%M:%S")


def time_duration(time):
	return str(datetime.timedelta(seconds=int(time)))


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            

def downloads_files_in_wget(url, filename):
	wget.download(url, filename)
