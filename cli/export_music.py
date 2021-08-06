#!/usr/bin/python3
# -*- coding: utf-8 -*-

import utils

from config import config
from vkapi import VKLightOauth, VKLight, VKLightError, VKLightOauthError
from handlers import APIHandler, LoadMusicHandler


class ExportMusic:

    def __init__(self):
        super().__init__()
        self.api = None
        self.user_id = 0
        self.COUNT_LOADING_AUDIO = 200

    def export(self, user_id=0, filename=""):
        self.user_id = user_id
        
        access_token = utils.read_json(config.AuthFile)['token']
        self.api = VKLight(dict(access_token=access_token))

        api_handler = APIHandler(self.api)
        music_handler = LoadMusicHandler(api_handler=api_handler)
        
        count_audios = api_handler.get_count_audio(user_id=user_id)
        data = music_handler.load_all_music(user_id=user_id, count=count_audios)
        
        audios_list = []
        for audio in data:
            audios_list.append(audio.__dict__)

        filename = f'{self.user_id}_EXPORTED_AUDIOS.json'
        utils.save_json(filename, {
            'expoted_time': utils.get_current_datetime(),
            'user_id': self.user_id,
            'count': count_audios,
            'items': audios_list
        })

        exit(f'Список аудиозаписей сохранен в {filename}')
