#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import utils
from PyQt5.QtCore import QThread, pyqtSignal


class Downloads_file(QThread):

    finished = pyqtSignal()
    abort_download = pyqtSignal(str)
    progress_range = pyqtSignal(int)
    progress = pyqtSignal(int)
    loading_audio = pyqtSignal(str)
    message = pyqtSignal(str)
    unavailable_audio = pyqtSignal(str)
    content_restricted = pyqtSignal(int, str)

    def __init__(self, count_track, PATH, downloads_list=None, data=None):
        super().__init__()
        self.count_track = count_track
        self.downloads_list = downloads_list
        self.selected_audios = len(self.downloads_list)
        self.completed = 0
        self.current_track = ''
        self.speed = ''
        self.time_started = 0
        self.msg = f"Всего аудиозаписей: {str(self.count_track)}  Выбрано: {str(self.selected_audios)}  Загружено: {str(self.completed)}  Скорость: {self.speed}"
        self.data = data
        self.PATH = PATH


    def run(self):
        try:

            for item in self.downloads_list:

                self.current_track = str(self.data[item])
                filename = f"{self.PATH}/{self.data[item].get_filename()}"
                self.time_started = int(time.time())

                if (self.data[item].url == ""):
                    if (self.data[item].content_restricted):
                        self.content_restricted.emit(
                            int(
                                self.data[item].content_restricted
                            ),  self.current_track
                        )

                    else:
                        self.unavailable_audio.emit(
                            self.current_track
                        )
                    
                    self.time_started = 0
                else:
                    self.message.emit(self.msg)
                    self.loading_audio.emit(self.current_track)
                    
                    utils.downloads_files_in_wget(
                        self.data[item].get_url(), 
                        filename, 
                        self.update_progress
                    )
                    
                    self.completed += 1
                    self.time_started = 0

            self.finished.emit()
            self.loading_audio.emit('')

        except Exception as e:
            self.abort_download.emit(str(e))

    # Magic. Do not touch.
    def update_progress(self, current, total, width=80):
        self.speed = utils.speed(
            int(time.time() - self.time_started), 
            bytesIn=current
        )
        self.msg = f"Всего аудиозаписей: {str(self.count_track)}  Выбрано: {str(self.selected_audios)}  Загружено: {str(self.completed)}  Скорость: {self.speed}"
        self.message.emit(self.msg)
        self.progress_range.emit(total)
        self.progress.emit(current)