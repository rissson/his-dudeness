# -*- coding: utf-8 -*-
# BASE FONTS AFTER THE CLASS
import pygame
import os
import graphalama

pygame.init()


# http://websemantics.co.uk/resources/font_size_conversion_chart/
#  TODO : add more fonts : https://github.com/showcases/fonts
#  TODO : add emoji support : https://github.com/showcases/emoji
# If you are using very small fonts, 10px or less, I advise using Verdana as it's actually
# designed to work at small sizes. At larger sizes Arial appears to be clearer.


class MetaClassFont(type):
    def __new__(mcs, names, bases=(type,), dic=None):
        if dic is not None:
            print('WTF -- ', dic)
        else:
            dic = {}

        return type.__new__(mcs, names, bases, dic)

    def __init__(cls, names, bases=(type,), dic=None):

        if dic is not None:
            print('WTF -- ', dict)
        else:
            dic = {}

        type.__init__(cls, names, bases, dic)

        cls._cached_fonts = dict()

        cls.name = names

        path = str(os.path.dirname(graphalama.__file__)).replace('\\', '/') + '/assets/fonts/'

        cls.regular = path + names + 'R.ttf'
        cls.bold = path + names + 'B.ttf'
        cls.italic = path + names + 'I.ttf'
        cls.bold_italic = path + names + 'BI.ttf'

    def get_font(cls, size=20, bold=False, italic=False):
        key = (size, bold, italic)
        if key in cls._cached_fonts:  # if the font already exists
            return cls._cached_fonts[key]  # we just return it

        else:  # we create it and store it in the _cached_fonts dict
            # here we get the right name
            if bold and italic:
                name = cls.bold_italic
            elif bold:
                name = cls.bold
            elif italic:
                name = cls.italic
            else:
                name = cls.regular

            # here we get a lot of fonts :/ to change the right height (it's easier to use a pixel height in the whole
            # code and here only convert it into the pygame font size
            # maybe there is a function to do this better than with a while loop, but I haven't find a good one
            real_size = size + 1  # only to enters the loop, without being aberrant
            delta = 0
            while real_size > size:  # we want a smaller or equal font size, 1 pxl bigger could be ugly, 1 less... Nope
                real_size = pygame.font.Font(name, size - delta).get_height()
                delta += 1
                if delta >= size:  # hum... negative size...
                    break

            font = pygame.font.Font(name, size - delta + 1)  # we have add 1 more
            cls._cached_fonts[key] = font  # we store the font
            return font


Calibri = MetaClassFont('Calibri')
DroidSerif = MetaClassFont('DroidSerif')
Verdana = MetaClassFont('verdana')


class Font(list):
    def __init__(self, clas=Calibri, size=1, bold=False, italic=False):
        """
        Return a list with theatributs that caractherize a font.
        For every argument you can pass None (or nothing) to get the defaults parameters
        """

        prev_defaults = Font.__init__.__defaults__
        if clas is None:
            clas = prev_defaults[0]
        if size is None:
            size = prev_defaults[1]
        if bold is None:
            bold = prev_defaults[2]
        if italic is None:
            italic = prev_defaults[3]

        super(Font, self).__init__([clas, size, bold, italic])

    @classmethod
    def set_defaults(cls, clas=None, size=None, bold=None, italic=None):
        """
        Changes the defaults parametters of Font.__init__
        Use it if you have a default font size for your program : you won't need to pass it each time you want a font
        """
        prev_defaults = Font.__init__.__defaults__
        if clas is None:
            clas = prev_defaults[0]
        if size is None:
            size = prev_defaults[1]
        if bold is None:
            bold = prev_defaults[2]
        if italic is None:
            italic = prev_defaults[3]

        Font.__init__.__defaults__ = (clas, size, bold, italic)

    @property
    def clas(self):
        return self[0]

    @clas.setter
    def clas(self, value):
        self[0] = value

    @property
    def size(self):
        return self[1]

    @size.setter
    def size(self, value):
        self[1] = value

    @property
    def bold(self):
        return self[2]

    @bold.setter
    def bold(self, value):
        self[2] = value

    @property
    def italic(self):
        return self[3]

    @italic.setter
    def italic(self, value):
        self[3] = value
