#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


# Домен API, OAuth
HOST_API = 'api.vk.com'
HOST_OAUTH = 'oauth.vk.com'

# Прокси
HOST_API_PROXY ="vk-api-proxy.xtrafrancyz.net"
HOST_OAUTH_PROXY = "vk-oauth-proxy.xtrafrancyz.net"

# Базовый URL
BASE_API_URL = "https://{0}/method/".format(HOST_API)
BASE_OAUTH_URL = "https://{0}/".format(HOST_OAUTH)

# Базовый Proxy URL
BASE_PROXY_API_URL = "https://{0}/method/".format(HOST_API_PROXY)
BASE_PROXY_OAUTH_URL = "https://{0}/".format(HOST_OAUTH_PROXY)

# Версия API
VK_API_VERSION = "5.89"

#Время ожидания ответа
TIME_OUT = 10

# Юзер-агент пользователя
HEADER = {'user-agent': 'VKAndroidApp/5.40-3904'}

# Прокси от KateMobile
PROXY_KATE = {'https' : 'https://proxy.katemobile.ru:3752'}

# Мне было лень генерировать receipt.
# По хорошему его можно получить тут(android.clients.google.com/c2dm/register3)
#receipt = "GF54PiFkdbb:APA91bEgyuoeagtS_1avbyY-_6UPRQ5fCJZwbv016qlNY-84iM81bfJgzIc28Tq_U7rvCqWb04nCOlj1M5A2yvZ793cnF8uZHhvKoGeHv9IzmR2ysSkKCn3aAff01IYFEv5nZFf02_hkVfszB2TRJ21XTNaUtvYO9A"
receipt = "JSv5FBbXbY:APA91bF2K9B0eh61f2WaTZvm62GOHon3-vElmVq54ZOL5PHpFkIc85WQUxUH_wae8YEUKkEzLCcUC5V4bTWNNPbjTxgZRvQ-PLONDMZWo_6hwiqhlMM7gIZHM2K2KhvX-9oCcyD1ERw4"

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


class VKException(Exception):
  pass


def call_oauth(method, proxy, param=None, **kwargs):
    
    HOST = ''

    if proxy:
      HOST = BASE_OAUTH_URL
    else:
      HOST = BASE_PROXY_OAUTH_URL

    try:
        response = requests.get(HOST + method,
            params=param, headers=HEADER, timeout=TIME_OUT).json()
    except Exception as e:
        raise e

    if 'error' in response:
        if 'need_captcha' == response['error']:
            return dict(type="need_captha", raw=response)
        
        elif 'need_validation' == response['error']:
            if 'ban_info' in response:
                # print(response)
                raise VKException("Error: {error_description}".format(**response))
            
            return "Error: 2fa isn't supported"
        
        else:
            raise VKException("Error : {error_description}".format(**response))

    return response


def call(method, proxy, param=None, **kwargs):
    HOST = ''
    if proxy:
      HOST = BASE_PROXY_API_URL
    else:
      HOST = BASE_API_URL
    try:
        response = requests.get(HOST + method,
            params=param, headers=HEADER, timeout=TIME_OUT).json()
    except Exception as e:
        raise e

    if 'error' in response:
        raise VKException("VKError ("+ method +") #{error_code}: {error_msg}".format(**response['error']))

    return response


def autorization(login, password, proxy=False, code=None, captcha_sid=None, captcha_key=None):
    param = {
      'grant_type': 'password',
      'client_id': client_keys[0][0],
      'client_secret': client_keys[0][1],
      'username': login,
      'password': password,
      'v': VK_API_VERSION,
      '2fa_supported': '1',
      'code':code,
      'captcha_sid' : captcha_sid,
      'captcha_key' : captcha_key
    }
    return call_oauth("token", proxy, param)


def refreshToken(access_token, proxy=False):
    param = {
        'access_token': access_token,
        'receipt' : receipt,
        'v' : VK_API_VERSION
    }

    return call("auth.refreshToken", proxy, param)


def user_get(access_token, proxy=False):
    param = {
        'access_token':access_token,
        'v':VK_API_VERSION
    }

    return call("users.get", proxy, param)


def get_audio(refresh_token, proxy=False):
    param = {
        'access_token':refresh_token,
        'v': VK_API_VERSION
    }

    return call("audio.get", proxy, param)


def get_catalog(refresh_token, proxy=False):
    param = {
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

    return call("audio.getCatalog", proxy, param)


def get_playlist(refresh_token, proxy=False):
    param = {
      'access_token':refresh_token,
      'owner_id':'',
      'id':'',
      'need_playlist':1,
      'v': VK_API_VERSION
    }

    return call("execute.getPlaylist", proxy, param)


def get_music_page(refresh_token, proxy=False):
    param = {
      'func_v':3,
      'need_playlists':1,
      'access_token':refresh_token,
      'v': VK_API_VERSION
    }

    return call("execute.getMusicPage", proxy, param)
    