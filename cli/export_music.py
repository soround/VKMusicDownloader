#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv

import utils
from config import config
from handlers import APIHandler, LoadMusicHandler
from models import Audio
from vkapi import VKLight


class ExportMusic:
    def __init__(self):
        super().__init__()
        self.api = ...
        self.user_id = 1
        self.filename = ''

        self.get_auth_data()

    def export(self):
        """"""
        export_raw_json, export_csv = range(2)

        self.user_id = input(f"ID пользователя (по-умолчанию: {self.user_id}): ") or self.user_id
        self.update_filename()
        self.filename = input(f"Имя файла (по-умолчанию: {self.filename}): ") or self.filename

        export_type = input(
            f"Вариант экспорта ({export_raw_json} - сырые данные в формате json, {export_csv} - Экспорт в формате csv)"
            f" (по-умолчанию: {export_csv}): "
        ) or export_csv
        export_type = int(export_type)

        if export_type not in (export_raw_json, export_csv):
            exit("Неизвестный тип экспорта")

        data = self.get_audio()

        if export_type == export_raw_json:
            self.filename += '.json'
            self.export_raw_json(data)

        if export_type == export_csv:
            self.filename += '.csv'
            self.export_to_csv(data)

        exit(f'Список аудиозаписей сохранен в {self.filename}')

    def get_auth_data(self):
        auth_data = utils.read_json(config.AuthFile)
        access_token = auth_data['token']
        self.user_id = auth_data['user_id']
        self.update_filename()
        self.api = VKLight(dict(access_token=access_token))

    def update_filename(self):
        self.filename = f'{self.user_id}_audio'

    def export_raw_json(self, data):
        audios_list = [audio.__dict__ for audio in data]
        utils.save_json(self.filename, {
            'exported_time': utils.get_current_datetime(),
            'user_id': self.user_id,
            'count': len(data),
            'items': audios_list
        })

    def export_to_csv(self, data):
        headers = ("id", "artist", "title", "duration", "date", "is_explicit", "is_hq", "url")
        # TODO: Нужно что-то сделать с кодировкой в Windows
        with open(self.filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(headers)
            for i, audio in enumerate(data, 1):
                row = (
                    i,
                    audio.artist,
                    audio.title,
                    utils.time_duration(audio.duration),
                    utils.unix_time_stamp_convert(audio.date),
                    audio.is_explicit,
                    audio.is_hq,
                    audio.url
                )
                writer.writerow(row)

    def get_audio(self) -> list[Audio]:
        api_handler = APIHandler(self.api)
        music_handler = LoadMusicHandler(api_handler)
        count_audios = api_handler.get_count_audio(user_id=self.user_id)
        data = music_handler.load_all_music(user_id=self.user_id, count=count_audios)

        return data
