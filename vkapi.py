#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union, Any, Dict

import requests

from utils import get_user_agent

host: str = "api.vk.com"
host_oauth: str = "oauth.vk.com"
apiVersion: str = "5.89"

headers: Dict[str, str] = {
    'user-agent': get_user_agent(True),
    'x-vk-android-client': 'new'
}

#  необходим для refresh токена
receipt: str = "JSv5FBbXbY:APA91bF2K9B0eh61f2WaTZvm62GOHon3-vElmVq54ZOL5PHpFkIc85WQUxUH_" + \
               "wae8YEUKkEzLCcUC5V4bTWNNPbjTxgZRvQ-PLONDMZWo_6hwiqhlMM7gIZHM2K2KhvX-9oCcyD1ERw4"

# client_id и client_secret приложений
clients_credential: Dict[Union[str, Any], Union[Union[
    dict[str, Union[int, str]], dict[str, Union[int, str]], dict[str, Union[int, str]], dict[str, Union[int, str]],
    dict[str, Union[int, str]], dict[str, Union[int, str]], dict[str, Union[int, str]], dict[str, Union[int, str]],
    dict[str, Union[int, str]], dict[str, Union[int, str]]], Any]] = {
    'android': {
        'client_id': 2274003,
        'client_secret': 'hHbZxrka2uZ6jB1inYsH'
    },
    'iPhone': {
        'client_id': 3140623,
        'client_secret': 'VeWdmVclDCtn6ihuP1nt'
    },
    'iPad': {
        'client_id': 3682744,
        'client_secret': 'mY6CDUswIVdJLCD3j15n'
    },
    'WindowsPC': {
        'client_id': 3697615,
        'client_secret': 'AlVXZFMUqyrnABp8ncuU'
    },
    'KateMobile': {
        'client_id': 2685278,
        'client_secret': 'lxhD8OD7dMsqtXIm5IUY'
    },
    'VKMessenger': {
        'client_id': 5027722,
        'client_secret': 'Skg1Tn1r2qEbbZIAJMx3'
    },
    'Snapster': {
        'client_id': 4580399,
        'client_secret': 'wYavpq94flrP3ERHO4qQ'
    },
    'Nokia': {
        'client_id': 2037484,
        'client_secret': 'gpfDXet2gdGTsvOs7MbL'
    },
    'WindowsPhone': {
        'client_id': 3502557,
        'client_secret': 'PEObAuQi6KloPM4T30DV'
    },
    'Lynt': {
        'client_id': 3469984,
        'client_secret': 'kc8eckM3jrRj8mHWl9zQ'
    },
    'Vika': {
        'client_id': 3032107,
        'client_secret': 'NOmHf1JNKONiIG5zPJUu'
    }
}


class VKLightOauth:

    def __init__(self, param: Dict = None):
        if param is None:
            param = dict()
        self.__param = param
        self.oauth_param = {
            'grant_type': 'password',
            'client_id': '',
            'client_secret': '',
            'username': self.__param.get('login', ''),
            'password': self.__param.get('password', ''),
            '2fa_supported': self.__param.get('2fa_supported', 1),
            'code': self.__param.get('code', None),
            'captcha_sid': self.__param.get('captcha_sid', None),
            'captcha_key': self.__param.get('captcha_key', None),
            'force_sms': 1
        }
        self.host = self.__param.get("host", host_oauth)
        self.baseURL = f"https://{self.host}/token/"

        self.apiVersion = self.__param.get("v", apiVersion)
        self.url_param = {'v': self.apiVersion}

        self.application_name = self.__param.get('application_name', 'android')
        self.oauth_data = {
            **self.oauth_param,
            **clients_credential.get(self.application_name)
        }

    def go(self) -> dict:
        try:
            resp = requests.post(
                self.baseURL,
                params=self.url_param,
                data=self.oauth_data,
                headers=headers,
                timeout=10
                # verify=False
            ).json()
        except Exception as e:
            raise e

        if 'error' in resp:
            raise VKLightOauthError(resp)

        return resp


class VKLight:

    def __init__(self, param: Dict = None):
        super(VKLight, self).__init__()
        if param is None:
            param = dict()
        self.access_token = param.get("access_token", "")
        self.apiVersion = param.get("v", apiVersion)
        self.lang = param.get("lang", "ru")

        self.host = param.get("host", host)
        self.baseURL = f"https://{self.host}/method/"
        self.url_param = dict(lang=self.lang, v=self.apiVersion)

    def __call__(self, method: str, args=None):
        if args is None:
            args = dict()
        return self.call(method, args)

    def call(self, method: str, args=None) -> dict:
        if args is None:
            args = dict()
        args['access_token'] = self.access_token

        try:
            resp = requests.post(
                f"{self.baseURL}{method}",
                data=args,
                params=self.url_param,
                headers=headers,
                timeout=10
                # verify=False
            ).json()

        except Exception as e:
            raise e

        if 'error' in resp:
            error_code, error_msg = resp['error']['error_code'], resp['error']['error_msg']
            raise VKLightError(error_code, error_msg)

        return resp

    def execute(self, code: str = ""):
        return self.call("execute", {"code": code})

    def is_usage_domain_me(self):
        """Используется ли домен .me"""
        return self.host == "api.vk.me"


class VKLightError(Exception):
    """ VKLight Exception for errors from VK APIs """

    def __init__(self, error_code, message):
        """
        :param error_code: Code of error
        :param message:  message
        """
        self.message, self.error_code = message, error_code

    def __repr__(self):
        return "VKLightError ({}): {}".format(self.error_code, self.message)

    def __str__(self):
        return "VKLightError ({}): {}".format(self.error_code, self.message)


class VKLightOauthError(Exception):
    """ VKLight Exception for errors from VK Oauth APIs """

    def __init__(self, response):
        self.error = response.get('error', '')
        self.error_description = response.get('error_description', '')

        self.__dict__.update(response)

    def __repr__(self):
        return "VKLightOauthError: ({}) {}".format(self.error, self.error_description)

    def __str__(self):
        return "VKLightOauthError: ({}) {}".format(self.error, self.error_description)
