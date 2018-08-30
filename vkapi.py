#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# Домен API
HOST_API = 'https://api.vk.com/'
# Домен OAuth
OAUTH = 'https://oauth.vk.com/'

HOST_API_PROXY ="https://vk-api-proxy.xtrafrancyz.net/"
OAUTH_PROXY = "https://vk-oauth-proxy.xtrafrancyz.net/"

# Версия API
VK_API_VERSION = "5.87" 

#Время ожидания ответа
TIME_OUT = 10

# Юзер-агент пользователя
HEADER = {'user-agent': 'VKAndroidApp/5.11.1-2316'}

# Мне было день генерировать receipt. 
# По хорошему его можно получить тут(android.clients.google.com/c2dm/register3)
receipt = "GF54PiFkdbb:APA91bEgyuoeagtS_1avbyY-_6UPRQ5fCJZwbv016qlNY-84iM81bfJgzIc28Tq_U7rvCqWb04nCOlj1M5A2yvZ793cnF8uZHhvKoGeHv9IzmR2ysSkKCn3aAff01IYFEv5nZFf02_hkVfszB2TRJ21XTNaUtvYO9A","TyQdnFs5xZ9:APA91bHzXMZxDmbDNegbUGDCWeB5KHo2TnpH6uaFRFCv_1ylko0umUOVP9tLZ-m5NuTeW6FlRJuRVXh4LzWg2Ki4LpKI9oaC5j1iMTJIJ4mdZ6GL6b0NCvvd0TTWwtf2u0OblTN5MbgNeLzdFdgX5P1Y0k_m1MdW8A","Z4k7n0LCsKL:APA91bGQH_Sz-wmgWJmAucpNeh7MQWgQ7hPe6HRi5hKU56cAlx8crzbiURoYW-1BMU0ncs7l5esX4B4MoJU2FQVwebKtYxb2Poz-hdgRr66ea2jcU8m08G3ADMyiV3cR3uTmGHfDZHry_3uQ8iitYG37c2hW6LYrSg"

# client_id и client_secret приложений
client_keys = [
  [2274003, 'hHbZxrka2uZ6jB1inYsH'], # 'Android'
  [3140623, 'VeWdmVclDCtn6ihuP1nt'], # 'iPhone' 
  [3682744, 'mY6CDUswIVdJLCD3j15n'], # 'iPad'
  [3697615, 'AlVXZFMUqyrnABp8ncuU'], # 'Windows PC'  
  [2685278, 'lxhD8OD7dMsqtXIm5IUY'], # 'Kate Mobile'
  [5027722, 'Skg1Tn1r2qEbbZIAJMx3'], # 'VK Messenger'
  [4580399, 'wYavpq94flrP3ERHO4qQ'], # 'Snapster (Android)'  
  [2037484, 'gpfDXet2gdGTsvOs7MbL'], # 'Nokia (Symbian)'
  [3502557, 'PEObAuQi6KloPM4T30DV'], # 'Windows Phone'
  [3469984, 'kc8eckM3jrRj8mHWl9zQ'], # 'Lynt'
  [3032107, 'NOmHf1JNKONiIG5zPJUu']  # 'Vika (Blackberry)'
]

# https://oauth.vk.com/token?grant_type=password&client_id=&client_secret=&username=&password=&v=5.80&2fa_supported=1
def autorization(login, password, client_id,
 client_secret, captcha_sid, captcha_key, path):
  try:
    param = {
      'grant_type': 'password',
      'client_id': client_id,
      'client_secret': client_secret,
      'username': login,
      'password': password,
      'v': VK_API_VERSION,
      '2fa_supported': '1',
      'captcha_sid' : captcha_sid,
      'captcha_key' : captcha_key
    }

    return requests.get(f'{path}token', 
      params=param, headers=HEADER, timeout=TIME_OUT).json()
    
  except Exception as e:
    return e


def check_token(access_token, path):
  try:
    params = {
      'access_token': access_token,
      'v' : VK_API_VERSION
    }

    return requests.get(f'{path}method/secure.checkToken', 
      params=params, headers=HEADER, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def refreshToken(access_token, path):
  try:
    params = {
      'access_token': access_token,
      'receipt' : receipt,
      'v' : VK_API_VERSION
    }

    return requests.get(f'{path}method/auth.refreshToken', 
      params=params, headers=HEADER, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def user_get(access_token, user_id, path):
  try:
    param = {
      'access_token':access_token,
      'user_id': user_id,
      'v': VK_API_VERSION
    }

    return requests.get(f'{path}method/users.get', 
      params=param, headers=HEADER, timeout=TIME_OUT).json()

  except Exception as e:
    return e


def get_audio(refresh_token, path):
  try:
    param = {
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

    return requests.get(f'{path}method/audio.get', 
      params=param, headers=HEADER,  timeout=TIME_OUT).json()

  except Exception as e:
    return e


# Рекомендации
def get_catalog(refresh_token, path):
  try:
    param = {
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

    return requests.get(f'{path}method/audio.getCatalog',
      params=param, headers=HEADER, timeout=TIME_OUT).json()

  except Exception as e:
     return e
     