# -*- coding: utf-8 -*-
import math as m
import os
import pygame
from graphalama.rectangle import Rectangle
from graphalama.CONSTANTS import *


class Photo(Rectangle):
    def __init__(self, x, y, w, h, name):
        self.original_rectangle = Rectangle(x, y, w, h, border=(BLACK, 2))

        self.original_image = pygame.image.load(name).convert_alpha()  # We load the image
        self.original_image_h = self.original_image.get_height()
        self.original_image_w = self.original_image.get_width()

        self.image = self.original_image  # just for a few milliseconds

        super().__init__(x, y, w, h, TRANSPARENT, border=(BLACK, 2))
        # self.original_image_w/SCREEN_SIZE[0], self.original_image_h/SCREEN_SIZE[1]

        self.resize()

    def resize(self):
        coeff_to_go_from_original_to_real = min(self.original_rectangle.real_w / self.original_image_w,
                                                self.original_rectangle.real_h / self.original_image_h)

        # print(self.real_size)
        # print(self.original_image_w, self.original_image_h)

        w = m.floor(self.original_image_w * coeff_to_go_from_original_to_real)
        h = m.floor(self.original_image_h * coeff_to_go_from_original_to_real)

        # print(w, '----', h)

        self.real_size = (w, h)
        # super().resize()  #  Diego le 22/07 :
            # cette fonction n'existe lus, mtn le render() resize automatiquement, si besoin donc :
        super().render()

        self.image = pygame.transform.scale(self.original_image, (w, h))
        self.render()

    def resize2(self):  # FIXME : Can we delete this code ?
        super().resize()
        coeff = self.real_w / self.real_h

        # print(coeff, '---', '--')
        self.image = pygame.transform.scale(self.original_image,
                                            (int(self.real_w / coeff), int(self.real_h))).convert_alpha()
        self.real_w = self.real_w / (self.real_w / self.real_h)
        # print(self.relative_h)

        self.render()

    def resize1(self):  # diego's shit  # FIXME : Can we delete this shit's code ?
        super().resize()
        coeff_w = self.real_w / self.original_image_w
        coeff_h = self.real_h / self.original_image_h
        coeff = max(coeff_h, coeff_w)  # we find the min scale to go from the last size to the new

        new_w = m.floor(self.original_image_h / coeff)
        new_y = m.floor(self.original_image_w / coeff)
        new_size = (new_w, new_y)
        # print(new_size, '---', coeff_w, '--', coeff_h)
        self.image = pygame.transform.scale(self.original_image, new_size).convert_alpha()

        self.render()

    def render(self):
        super().render()
        self.blit(self.image, (0, 0))


class PhotosList(list):
    def __init__(self, path, dim_value, marge):
        super().__init__()
        files = os.listdir(path)  # TODO : verifier que ce sont des photos
        level = 0
        # print(files)

        for i, file in enumerate(files):
            if i == 0:
                self.append(Photo(marge, 0.1, 0.3, dim_value, path + '/' + file))
            else:
                self.append(Photo(self[i - 1].relative_midright[0] + marge, 0.1, 0.3, dim_value, path + '/' + file))

    def render(self, display):
        for photo in self:
            display.blit(photo, photo.real_topleft)

    def resize(self, dim_value, marge):
        for i, photo in enumerate(self):
            if i == 0:
                photo.x = marge
            else:
                photo.x = self[i - 1].relative_midright[0] + marge

            photo.resize()

__all__ = ['Photo', 'PhotosList']
