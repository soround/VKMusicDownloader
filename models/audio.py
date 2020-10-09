#!/usr/bin/python3
# -*- coding: utf-8 -*-


from utils import fix_filename


class Audio:
    def __init__(self, obj):
        self.artist = obj.get('artist')
        self.title = obj.get('title')
        self.is_hq = False
        self.is_explicit = False
        self.content_restricted = None
        self.song_name = self.artist + ' - ' + self.title
        
        self.__dict__.update(obj)

    def get_filename(self):
        return fix_filename(self.song_name) + '.mp3'

    def __str__(self):
        return self.song_name