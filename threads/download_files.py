#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import utils
from PyQt5.QtCore import QThread, pyqtSignal


class DownloadsFile(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    progress_range = pyqtSignal(int)
    abort_download = pyqtSignal(str)
    loading_audio = pyqtSignal(str)
    unavailable_audio = pyqtSignal(str)
    message = pyqtSignal(str)
    content_restricted = pyqtSignal(int, str)

    def __init__(self, count_track, path, downloads_list=None, data=None):
        super().__init__()
        self.count_track = count_track
        self.downloads_list = downloads_list
        self.selected_audios = len(self.downloads_list)
        self.completed = 0
        self.current_track = ''
        self.msg = f"Всего аудиозаписей: {self.count_track}  Выбрано: {self.selected_audios}  Загружено: {self.completed}"
        self.data = data
        self.current_path = path

    def run(self):
        try:
            for item in self.downloads_list:
                self.current_track = str(self.data[item])
                filename = f"{self.current_path}/{self.data[item].get_filename()}"

                if self.data[item].url == "":
                    if self.data[item].content_restricted:
                        self.content_restricted.emit(int(self.data[item].content_restricted), self.current_track)
                    else:
                        self.unavailable_audio.emit(self.current_track)

                else:
                    self.message.emit(self.msg)
                    self.loading_audio.emit(self.current_track)

                    utils.downloads_files_in_wget(
                        self.data[item].get_url(),
                        filename,
                        self.update_progress
                    )

                    self.completed += 1

            self.finished.emit()
            self.loading_audio.emit('')

        except Exception as e:
            self.abort_download.emit(str(e))

    # Magic. Do not touch.
    def update_progress(self, current, total, wight=80):
        self.message.emit(self.msg)
        self.progress_range.emit(total)
        self.progress.emit(current)
