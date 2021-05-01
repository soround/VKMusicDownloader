#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os.path import abspath


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=MetaSingleton):
	ApplicationName = "VKMusicDownloader"
	ApplicationVersion = "1.1.12"
	ApplicationBranch = "Public Pre-Release"
	Description = "Кроссплатформенный клиент для массового скачивания музыки из ВКонтакте."

	ApplicationFullName = f"{ApplicationName} {ApplicationVersion} {ApplicationBranch}"

	IconPath = abspath("assets/icon/vk_downloader_icon.ico")
	IconPathV2 = abspath("assets/icon/downloader_icon.png")
	IconPathV3 = abspath("assets/icon/downloader.png")

	License = "https://github.com/keyzt/VKMusicDownloader/blob/master/LICENSE"
	SourceCode = "https://github.com/keyzt/VKMusicDownloader"

	NoSaveToFile = True
	UseAnalytics = True


config = Config()
