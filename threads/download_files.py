#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
        self.data = data
        self.PATH = PATH


    def run(self):
        try:
            self.completed = 0

            for item in self.downloads_list:
                msg = "Всего аудиозаписей: " + str(self.count_track) + \
                      " Выбрано: " + str(self.selected_audios) + \
                      " Загружено: " + str(self.completed)

                filename = self.PATH + "/" + self.data[item].get_filename()

                if (self.data[item].url == ""):
                    if (self.data[item].content_restricted):
                        self.content_restricted.emit(
                            int(
                                self.data[item].content_restricted
                            ),  str(self.data[item])
                        )

                    else:
                        self.unavailable_audio.emit(
                            str(self.data[item])
                        )
                else:
                    self.message.emit(msg)
                    self.loading_audio.emit(str(self.data[item]))
                    
                    utils.downloads_files_in_wget(
                        self.data[item].url, 
                        filename, 
                        self.update_progress
                    )
                    
                    self.completed += 1

            self.finished.emit()
            self.loading_audio.emit('')

        except Exception as e:
            self.abort_download.emit(str(e))

    # Magic. Do not touch.
    def update_progress(self, current, total, width=80):
        self.progress_range.emit(total)
        self.progress.emit(current)