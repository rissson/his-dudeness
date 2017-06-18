# -*- coding: utf-8 -*-
import pygame
from graphalama.CONSTANTS import *
from graphalama.color import Color
from graphalama.functions import *
from graphalama.borg import Borg
import math as m

# TODO : Delete this thing or make something useful

class Circle(pygame.Surface):
    def __init__(self, relative_center, relative_radius, color=TRANSPARENT):

        pygame.Surface.__init__(self, (0, 0))

        self._x = relative_center[0]
        self._y = relative_center[1]
        self._relative_radius = relative_radius

        self.color = Color(color)

        self.previous_self = 'first'

    def __repr__(self):
        return 'Circle: ' + str(self.color.RGBA) + str(self.real_radius)

    # ------------------------------------------------- PROPERTIES --------------------------------------------------- #

    @property
    def relative_x(self):
        return self._x

    @relative_x.setter
    def relative_x(self, _x):
        self._x = _x

    @property
    def real_x(self):
        return scale(self._x, Borg().SCREEN_SIZE[0])

    @real_x.setter
    def real_x(self, x):
        self._x = scale(x, Borg().SCREEN_SIZE[0], flags='/')

    @property
    def relative_y(self):
        return self._y

    @relative_y.setter
    def relative_y(self, _y):
        self._y = _y

    @property
    def real_y(self):
        return scale(self._y, Borg().SCREEN_SIZE[1])

    @real_y.setter
    def real_y(self, y):
        self._y = scale(y, Borg().SCREEN_SIZE[0], flags='/')

    @property
    def relative_center(self):
        return self._x, self._y

    @relative_center.setter
    def relative_center(self, _relative_center):
        self._x = _relative_center[0]
        self._y = _relative_center[1]

    @property
    def real_center(self):
        return scale(self.relative_center, Borg().SCREEN_SIZE)

    @real_center.setter
    def real_center(self, _real_center):
        self._relative_center = scale(_real_center, Borg().SCREEN_SIZE, flags='/')

    @property
    def relative_radius(self):
        return self._relative_radius

    @relative_radius.setter
    def relative_radius(self, _relative_radius):
        self._relative_radius = _relative_radius

    @property
    def real_radius(self):
        return scale(self.relative_radius, Borg().SCREEN_SIZE)

    @real_radius.setter
    def real_radius(self, _real_radius):
        self._relative_radius = scale(_real_radius, Borg().SCREEN_SIZE, flags='/')

    @property
    def real_topleft(self):
        return [self.real_center[0] - self.real_radius, self.real_center[1] - self.real_radius]

    @real_topleft.setter
    def real_topleft(self, value):
        self._relative_center = scale((value[0] - self.real_radius, value[1] - self.real_radius),
                                      Borg().SCREEN_SIZE, flags='/')

    # -------------------------------------------------- METHODS ----------------------------------------------------- #

    def point_in_circle(self, x, y):
        """
        This check if the given point is in the circle
        """
        # it is just the trigonometric equality cos² + sin² = 1
        if m.cos((x - self.real_x) / self.real_radius) ** 2 + m.sin((y - self.real_y) / self.real_radius) ** 2 <= 1:
            return True
        else :
            return False

    def resize(self):
        """
        This method need to be called week you want to change the size of the circle
        """

        pygame.Surface.__init__(self, (2*self.real_radius, 2*self.real_radius), flags=pygame.SRCALPHA)
        self.fill(TRANSPARENT)
        self.render()

    @only_if_object_changes
    def render(self, color=None):

        if color is None:
            color = self.color

        # if surface is not None:
        #     pygame.draw.circle(surface, color.RGBA, self.real_center, self.real_radius)

        pygame.draw.circle(self, color.RGBA, [self.real_radius, self.real_radius], self.real_radius)

        if self.check_if_point_in_circle(inputs['mouse']['real x'], inputs['mouse']['real y']):
            # we check if the wanted button is an actually pressed button
            if no_button == 1 and inputs['left click']['just pressed']:
                return True
            elif no_button == 2 and inputs['middle click']['just pressed']:
                return True
            elif no_button == 3 and inputs['right click']['just pressed']:
                return True
            elif no_button == 4 and inputs['mouse']['scroll'] == -1:
                return True
            elif no_button == 5 and inputs['mouse']['scroll'] == +1:
                return True
            elif no_button == 0:
                return True
        else:
            return False

    def check_if_point_in_circle(self, x, y):
        if (int(x)-int(self._x)) ^ 2 + (int(y) - int(self._y)) ^ 2 < int(self._relative_radius) ^ 2:
            return True
        else:
            return False

    def update(self):
        pass
