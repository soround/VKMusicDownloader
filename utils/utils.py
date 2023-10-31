#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import socket

import requests

import wget


def fix_filename(filename) -> str:
    invalid_letters: list = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    sanitized_filename: str = ''.join(c for c in filename if c not in invalid_letters)
    return sanitized_filename.translate(str.maketrans('', '', '\0'))[:255]


def file_exists(path: str) -> bool:
    return os.path.exists(path)


def check_connection(url):
    try:
        requests.head(f"https://{url}", timeout=5)
    except requests.ConnectionError:
        return False

    return True


def get_internal_ip():
    return socket.gethostbyname(socket.gethostname())


def get_network_info():
    return requests.get("http://ipinfo.io", timeout=5).json()


def unix_time_stamp_convert(time) -> str:
    return datetime.datetime.fromtimestamp(int(time)).strftime("%d.%m.%Y %H:%M:%S")


def time_duration(time) -> str:
    return str(datetime.timedelta(seconds=int(time)))


def get_current_datetime() -> str:
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.loads(file.read())


def downloads_files_in_wget(url, filename, progress):
    wget.download(url, out=filename, bar=progress)
