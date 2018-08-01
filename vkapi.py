#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# Домен API
HOST_API = 'https://api.vk.com/'
# Домен OAuth
OAUTH = 'https://oauth.vk.com/'
# Версия API
VK_API_VERSION = "5.83"
#Время ожидания ответа
TIME_OUT = 10 

header = {'user-agent': 'VKAndroidApp/5.11.1-2316'}
# Прокси
#api_proxys = {"http" : "http://vk-api-proxy.xtrafrancyz.net:443"}
#oauth_proxys = {"http" : "http://vk-oauth-proxy.xtrafrancyz.net:443"}

# За receipt спасибо @danyadev
receipt = "JSv5FBbXbY:APA91bF2K9B0eh61f2WaTZvm62GOHon3-vElmVq54ZOL5PHpFkIc85WQUxUH_wae8YEUKkEzLCcUC5V4bTWNNPbjTxgZRvQ-PLONDMZWo_6hwiqhlMM7gIZHM2K2KhvX-9oCcyD1ERw4"

client_keys = [
  [2274003, 'hHbZxrka2uZ6jB1inYsH'], # 'Android'
  [3140623, 'VeWdmVclDCtn6ihuP1nt'], # 'iPhone' 
  [3682744, 'mY6CDUswIVdJLCD3j15n'], # 'iPad'
  [3697615, 'AlVXZFMUqyrnABp8ncuU'], # 'Windows'  
  [2685278, 'lxhD8OD7dMsqtXIm5IUY'], # 'Kate Mobile'
  [5027722, 'Skg1Tn1r2qEbbZIAJMx3'], # 'VK Messenger'
  [4580399, 'wYavpq94flrP3ERHO4qQ'], # 'Snapster'  
  [2037484, 'gpfDXet2gdGTsvOs7MbL'], # 'Symbian (Nokia)'
  [3502557, 'PEObAuQi6KloPM4T30DV'], # 'Windows Phone'
  [3469984, 'kc8eckM3jrRj8mHWl9zQ'], # 'Lynt'
  [3032107, 'NOmHf1JNKONiIG5zPJUu']  # 'Vika'
]

# https://oauth.vk.com/token?grant_type=password&client_id=&client_secret=&username=&password=&v=5.80&2fa_supported=1
def autorization(login, password, client_id, client_secret):
  try:
    param = {
      'grant_type': 'password',
      'client_id': client_id,
      'client_secret': client_secret,
      'username': login,
      'password': password,
      'v': VK_API_VERSION,
      '2fa_supported': '1'
    }

    return requests.get(f'{OAUTH}token', 
      params=param, headers=header, timeout=TIME_OUT).json()
    
  except Exception as e:
    return e


def check_token(access_token):
  try:
    params = {
      'access_token': access_token,
      'v' : VK_API_VERSION
    }

    return requests.get(f'{HOST_API}method/secure.checkToken', 
      params=params, headers=header, proxies=None, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def refreshToken(access_token):
  try:
    params = {
      'access_token': access_token,
      'receipt' : receipt,
      'v' : VK_API_VERSION
    }

    return requests.get(f'{HOST_API}method/auth.refreshToken', 
      params=params, headers=header, proxies=None, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def user_get(access_token, user_id):
  try:
    param = {
      'access_token':access_token,
      'user_id': user_id,
      'v': VK_API_VERSION
    }

    return requests.get(f'{HOST_API}method/users.get', 
      params=param, headers=header, proxies=None, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def get_audio(refresh_token):
  try:
    param = {
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

    return requests.get(f'{HOST_API}method/audio.get', 
      params=param, headers=header, proxies=None, timeout=TIME_OUT).json()

  except Exception as e:
    return e
