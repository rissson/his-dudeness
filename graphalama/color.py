# -*- coding: utf-8 -*-
import time
import random
from graphalama.CONSTANTS import *


def get_rainbow(speed=0.1):
    """ This returns a RAINBOW color ! """
    rainbow = Color(WHITE)
    rainbow.mode = 'rainbow'
    rainbow.auto_rainbow = speed
    return rainbow


def anti_color(color):
    r, g, b, *a = color
    x = [255 - r, 255 - g, 255 - b]  # we make the opposite of each color
    return x + a


def grey_scale(color):
    r, g, b, *a = color
    grey = 0.21 * r + 0.72 * g + 0.07 * b
    return [grey, grey, grey] + a


def random_flash_color():
    color = [255, 0, random.randrange(0, 256)]  # we take a flash color : 1 param at 255 one at 0 and 1 between
    random.shuffle(color)  # we shuffle them. Else it will be always red/purple
    return color


def total_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    return r, g, b, a


def lighter(color, prop):
    r, g, b, *a = color
    r = r * (1-prop) + 255 * prop
    g = g * (1-prop) + 255 * prop
    b = b * (1-prop) + 255 * prop
    c = [round(r), round(g), round(b)] + a
    return c


# noinspection PyPep8Naming
class Color:
    """Create and control un tuple-like object of dimension 3 or 4, that is a RGB color.
    do_auto_rainbow is badasse method that make the color a UNICORN behavior"""

    def __init__(self, color=(255, 255, 255), **kwargs):
        """
        This is the last kind of COLORS !

        The 'color' is the main color of the color xD
        You can pass other key worded arguments. They are other states that are returned week calling .RGB
            week the .mode is a keyword. they are other possible state of the color : Everything is quantum !
            Some keywords are already defined :
                - 'default'     --> the color passed in first arg
                - 'rainbow'     --> the color that automatically rainbows #UNICORN
                - 'anti'  --> the opposite of the default color
                - 'B&W'         --> the black and whit color of the default
        """

        if type(color) == Color:  # if the color passed is already a Color obj
            # If we want to re-color a Color, like mylist = list(mylist)
            self.default = color.default
            self.states = dict(color.states)
            self.mode = color.mode
            self.auto_rainbow = color.auto_rainbow
            self.rainbow_time = color.rainbow_time
            self.phase = color.phase
            self.rainbow = color.rainbow
        else:
            if len(color) == 3:  # if it's not a RGBA color,
                color = tuple(color) + (255,)  # we change it to RGBA
            self.default = color

            # the other states
            self.states = dict()
            for key, clr in kwargs.items():
                if isinstance(clr, type(get_rainbow)):
                    pass
                elif len(clr) == 3:  # if there's no alpha value
                    clr += (255,)  # we add one

                self.states[key] = clr

            self.mode = 'default'

            self.auto_rainbow = 1 / 10  # this describe the number of revolutions of the rainbow
            self.rainbow_time = time.time()
            self.phase = 'y'
            self.rainbow = (255, 0, 0, 255)

    def __str__(self):
        r, g, b, a = self.RGBA
        return "Color({}, {}, {}, {})".format(r, g, b, a)

    def __repr__(self):
        r, g, b, a = self.RGBA
        ret = "color{}-{}-{}-{}!".format(r, g, b, a)
        for state in self.states:
            r, g, b, a = self.states[state]
            ret += state + '{}-{}-{}-{}'.format(r, g, b, a)

        return ret

    def do_rainbow(self, t):
        r, g, b, a = self.rainbow

        if self.phase == 'y':
            g += t
            if g >= 255:
                g = 255
                self.phase = 'g'
        if self.phase == 'g':
            r -= t
            if r <= 0:
                r = 0
                self.phase = 'c'
        if self.phase == 'c':
            b += t
            if b >= 255:
                b = 255
                self.phase = 'b'
        if self.phase == 'b':
            g -= t
            if g <= 0:
                g = 0
                self.phase = 'm'
        if self.phase == 'm':
            r += t
            if r >= 255:
                r = 255
                self.phase = 'r'
        if self.phase == 'r':
            b -= t
            if b <= 0:
                b = 0
                self.phase = 'y'

        self.rainbow = (r, g, b, a)

    def do_auto_rainbow(self):

        time_passed = time.time() - self.rainbow_time  # the time passed since the last call of the function
        self.rainbow_time = time.time()  # we reset the 'date' in order to make the upper line effective
        t = self.auto_rainbow * time_passed * 1530 % 255  # nbr of revolution * time * nbr of incrementation needed
        self.do_rainbow(t)

    @property
    def anti_color(self):
        # we do the opposite of red, green and blue values
        r, g, b, a = self.default
        return 255 - r, 255 - g, 255 - b, a

    @property
    def grey_scale(self):
        # http://www.johndcook.com/blog/2009/08/24/more-on-colors-and-grayscale/
        # http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/
        # I've add myself the last parameter

        return grey_scale(self.default)

    @property
    def RGB(self):
        return self.RGBA[:3]  # without the A

    @property
    def RGBA(self):

        if self.mode == 'rainbow':
            self.do_auto_rainbow()
            return self.rainbow
        elif self.mode == 'anti':
            return self.anti_color
        elif self.mode == 'B&W':
            return self.grey_scale
        elif self.mode in self.states:  # if the mode is one of the state passed in the .__init__
            if isinstance(self.states[self.mode], type(get_rainbow)):
                return self.states[self.mode](self)
            else:
                return self.states[self.mode]
        elif self.mode == 'default':
            return self.default
        else:
            print("THE COLOR MODE DOESN'T MATCH ANYTHING : ", self.mode)
            raise Exception

    @property
    def is_living(self):
        if self.mode == 'rainbow':
            return True
        else:
            return False


__all__ = ['Color', 'get_rainbow', 'lighter', 'grey_scale', 'random_flash_color', 'total_random_color', 'anti_color']
