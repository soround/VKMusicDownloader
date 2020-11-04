#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

from vkapi import VKLightError
from models import Audio
from utils import save_json, stat
from config import NoSaveToFile


class LoadMusic(QThread):

    music = pyqtSignal(list)
    error = pyqtSignal(str)
    count_tracks = pyqtSignal(int)

    def __init__(self, api, user_id):
        super().__init__()
        self.api = api
        self.user_id = user_id
        self.audios = None

    
    def run(self):
        try:

            self.audios = self.api.call('audio.get')            
            self.count_tracks.emit(self.audios['response']['count'])

            data = [Audio(item) for item in self.audios['response']['items']]

            if not NoSaveToFile: save_json('response.json', self.audios)

            self.music.emit(data)

            stat.setuserid(user_id=self.user_id)
            stat.send()

        except VKLightError as e:
            self.error.emit(repr(e))
            self.music.emit([])
            self.count_tracks.emit(0)

        except Exception as e:
            self.error.emit(str(e))
            self.music.emit([])
            self.count_tracks.emit(0)

    def __del__(self):
        print("Bye bye ...")
        self.audios = None
