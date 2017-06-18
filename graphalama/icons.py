# -*- coding: utf-8 -*-
import pygame
import os
import graphalama


class Icon:
    _cache = dict()

    def __init__(self, path):
        if path in Icon._cache:
            pass
        else:
            icon = pygame.image.load(path)
            Icon._cache[path] = dict(original=icon)

        self.path = path

    def get(self, size):
        """ Returns the Icon"""
        if size in Icon._cache[self.path]:
            return Icon._cache[self.path][size]
        else:
            try:
                icon = pygame.transform.smoothscale(Icon._cache[self.path]['original'], (size, size))#.convert_alpha()
            except pygame.error:
                icon = pygame.transform.scale(Icon._cache[self.path]['original'], (size, size)).convert_alpha()

            Icon._cache[self.path][size] = icon
            return icon

path = str(os.path.dirname(graphalama.__file__)).replace('\\', '/') + '/assets/icons/'

icon_info = Icon(path + 'info.png')
icon_info2 = Icon(path + 'info2.png')
pause_icon = Icon(path + 'pause.png')
play_icon = Icon(path + 'play.png')
next_icon = Icon(path + 'next.png')
prev_icon = Icon(path + 'prev.png')
plus_icon = Icon(path + 'plus.png')
eye_icon = Icon(path + 'eye.png')
home_icon = Icon(path + 'home.png')
song_icon = Icon(path + 'song.png')
artist_icon = Icon(path + 'artist.png')
album_icon = Icon(path + 'cd.png')
folder_icon = Icon(path + 'folder.png')
file_icon = Icon(path + 'file.png')
search_icon = Icon(path + 'search.png')
color_picker_icon = Icon(path + 'colorpicker.png')
upload_icon = Icon(path + 'upload.png')
download_icon = Icon(path + 'download.png')
repeat_icon = Icon(path + 'repeat.png')
repeat_once_icon = Icon(path + 'repeat_once.png')
shuffle_icon = Icon(path + 'shuffle.png')
mute_icon = Icon(path + 'mute.png')
unmute_icon = Icon(path + 'unmute.png')
loading_icon = Icon(path + 'loading.png')
back_icon = Icon(path + 'back.png')
