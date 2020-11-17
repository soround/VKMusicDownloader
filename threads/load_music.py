#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from vkapi import VKLightError
from models import Audio
from utils import save_json, stat
from config import NoSaveToFile


class LoadMusic(QThread):
    music = pyqtSignal(list)
    error = pyqtSignal(str)
    count_tracks = pyqtSignal(int)
    warning_message_count_audios = pyqtSignal(str)
    loaded = pyqtSignal(bool)

    def __init__(self, api, user_id):
        super().__init__()
        self.api = api
        self.user_id = user_id
        self.audios = None
        self.COUNT_LOADING_AUDIO = 200 # Количество аудио которое возвращает API

    def run(self):
        try:
            self.loaded.emit(False)
            data = []
            count_calls = 1
            count_audios = self.api.call("audio.get", {
                "count": 0,
            })['response']['count']
            
            self.count_tracks.emit(count_audios)
            
            if count_audios > self.COUNT_LOADING_AUDIO:
                
                count_calls = round(count_audios / self.COUNT_LOADING_AUDIO)

                for i in range(count_calls):
                    try:
                        self.audios = self.api.call('audio.get', {
                                "offset": self.COUNT_LOADING_AUDIO * i
                            }
                        )
                        _data = [Audio(item) for item in self.audios['response']['items']]
                        data = [*data, *_data]
                        self.music.emit(data)

                    except VKLightError as e:
                        self.error.emit(str(e))
                        break

                    if i != 0 and i % 10 == 0:
                        sleep(9)

            else:
                self.audios = self.api.call('audio.get')
                data = [Audio(item) for item in self.audios['response']['items']]

            
            if not NoSaveToFile:
                save_json('response.json', self.audios)

            self.music.emit(data)
            self.loaded.emit(True)

            stat.set_userid(user_id=self.user_id)
            stat.send()

        except (VKLightError, Exception) as e:
            self.loaded.emit(True)
            self.error.emit(str(e))
            self.music.emit([])
            self.count_tracks.emit(0)

    def __del__(self):
        print("Bye bye ...")
        self.audios = None
