# -*- coding: utf-8 -*-
"""
A Shape object : The rectangle is defined here
"""
import pygame
from math import sqrt

import graphalama
from graphalama.borg import Borg
from graphalama.color import Color, get_rainbow
from graphalama.CONSTANTS import *
from graphalama.functions import *
import math as m

from graphalama.maths import V2

borg_baby = Borg()


class Area(pygame.Surface):
    def __init__(self, x, y, w, h, function_on_click=None):
        """
        Defines an area in the plan (windows hehe).

        The x, y, w, h, are any float or a function (that takes no argumants an returns a float).
         If a param is between -1 and 1, area will have a relative size/postion in the screen. Else it's a pixel size/pos
         if a param is negative, it's like if you start counting from the botom left for the position and
         modulo SCREEN_SIZE for the size

        The function_on_click is called every time update() is called. You must detect in the function_on_click if it's
         the right click, the right place... The function_on_click takes to parameters : the Area object and the inputs
        """

        self._x = x
        self._y = y
        self._w = w
        self._h = h

        pygame.Surface.__init__(self, self.real_size, pygame.SRCALPHA)

        self.function_on_click = function_on_click

        self.previous_state = {'real size': 0}

    def __state__(self):
        state = dict()
        state['real size'] = self.real_size
        return state

    # ------------------------------------------------- PROPERTIES --------------------------------------------------- #

    # The x position
    @property
    def x(self):
        if isinstance(self._x, type(get_rainbow)):  # i picked one random function cause the 'function' class does not
            # exists like that
            return round(self._x(), 5)
        return round(self._x, 5)

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def relative_x(self):
        if -1 < self.x < 0:
            x = 1 + self.x
        elif self.x < -1:
            x = borg_baby.SCREEN_SIZE[0] + self.x
        else:
            x = self.x

        return to_prop(x, borg_baby.SCREEN_SIZE[0])

    @property
    def real_x(self):
        if -1 < self.x < 0:
            x = 1 + self.x
        elif self.x < -1:
            x = borg_baby.SCREEN_SIZE[0] + self.x
        else:
            x = self.x

        return to_pixels(x, borg_baby.SCREEN_SIZE[0])

    # The y position
    @property
    def y(self):
        if isinstance(self._y, type(get_rainbow)):
            return round(self._y(), 5)
        return round(self._y, 5)

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def relative_y(self):
        if -1 < self.y < 0:
            y = 1 + self.y
        elif self.y < -1:
            y = borg_baby.SCREEN_SIZE[1] + self.y
        else:
            y = self.y

        return to_prop(y, borg_baby.SCREEN_SIZE[1])

    @property
    def real_y(self):
        if -1 < self.y < 0:
            y = 1 + self.y
        elif self.y < -1:
            y = borg_baby.SCREEN_SIZE[1] + self.y
        else:
            y = self.y

        return to_pixels(y, borg_baby.SCREEN_SIZE[1])

    # the width
    @property
    def w(self):
        if isinstance(self._w, type(get_rainbow)):
            return round(self._w(), 5)
        return round(self._w, 5)

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def relative_w(self):
        if -1 < self.w < 0:
            w = 1 + self.w
        elif self.w < -1:
            w = borg_baby.SCREEN_SIZE[0] + self.w
        else:
            w = self.w

        return to_prop(w, borg_baby.SCREEN_SIZE[0])

    @property
    def real_w(self):
        if -1 < self.w < 0:
            w = 1 + self.w
        elif self.w < -1:
            w = borg_baby.SCREEN_SIZE[0] + self.w
        else:
            w = self.w

        return to_pixels(w, borg_baby.SCREEN_SIZE[0])

    # the height
    @property
    def h(self):
        if isinstance(self._h, type(get_rainbow)):
            return round(self._h(), 5)
        return round(self._h, 5)

    @h.setter
    def h(self, value):
        self._h = value

    @property
    def relative_h(self):
        if -1 < self.h < 0:
            h = 1 + self.h
        elif self.h < -1:
            h = borg_baby.SCREEN_SIZE[1] + self.h
        else:
            h = self.h

        return to_prop(h, borg_baby.SCREEN_SIZE[1])

    @property
    def real_h(self):
        if -1 < self.h < 0:
            h = 1 + self.h
        elif self.h < -1:
            h = borg_baby.SCREEN_SIZE[1] + self.h
        else:
            h = self.h

        return to_pixels(self.relative_h, borg_baby.SCREEN_SIZE[1])

    # the size
    @property
    def relative_size(self):
        rs = V2(self.relative_w, self.relative_h)
        return rs

    @relative_size.setter
    def relative_size(self, value):
        self.w = round(value[0], 5)
        self.h = round(value[1], 5)

    @property
    def real_size(self):
        return V2(*scale(self.relative_size, borg_baby.SCREEN_SIZE))

    @real_size.setter
    def real_size(self, value):
        self.w = m.ceil(value[0])
        self.h = m.ceil(value[1])

    # the topleft position
    @property
    def relative_topleft(self):
        return V2(self.relative_x, self.relative_y)

    @relative_topleft.setter
    def relative_topleft(self, value):
        self.x = round(value[0], 5)
        self.y = round(value[1], 5)

    @property
    def real_topleft(self):
        return V2(*scale(self.relative_topleft, borg_baby.SCREEN_SIZE))

    @real_topleft.setter
    def real_topleft(self, value):
        self.x = m.ceil(value[0])
        self.y = m.ceil(value[1])

    # the midtop position
    @property
    def relative_midtop(self):
        return V2(self.relative_x + self.relative_w / 2, self.relative_y)

    @relative_midtop.setter
    def relative_midtop(self, value):
        self.x = round(value[0] - self.relative_w / 2)
        self.y = round(value[1])

    @property
    def real_midtop(self):
        return V2(*scale(self.relative_midtop, borg_baby.SCREEN_SIZE))

    @real_midtop.setter
    def real_midtop(self, value):
        self.x = m.ceil(value[0] - self.real_w / 2)
        self.y = m.ceil(value[1])

    # the topright position
    @property
    def relative_topright(self):
        return V2(self.relative_x + self.relative_w, self.relative_y)

    @relative_topright.setter
    def relative_topright(self, value):
        self.x = round(value[0] - self.relative_w, 5)
        self.y = round(value[1], 5)

    @property
    def real_topright(self):
        return V2(*scale(self.relative_topright, borg_baby.SCREEN_SIZE))

    @real_topright.setter
    def real_topright(self, value):
        self.x = m.ceil(value[0] - self.real_w)
        self.y = m.ceil(value[1])

    # the center position
    @property
    def relative_center(self):
        return V2(self.relative_x + self.relative_w / 2, self.relative_y + self.relative_h / 2)

    @relative_center.setter
    def relative_center(self, value):
        self.x = round(value[0] - self.relative_w / 2, 5)
        self.y = round(value[1] - self.relative_h / 2, 5)

    @property
    def real_center(self):
        return V2(*scale(self.relative_center, borg_baby.SCREEN_SIZE))

    @real_center.setter
    def real_center(self, value):
        self.x = m.ceil(value[0] - self.real_w / 2)
        self.y = m.ceil(value[1] - self.real_y / 2)

    # The midleft position
    @property
    def relative_midleft(self):
        return V2(self.relative_x, self.relative_y + self.relative_h / 2)

    @relative_midleft.setter
    def relative_midleft(self, value):
        self.x = round(value[0], 5)
        self.y = round(value[1] - self.relative_h / 2, 5)

    @property
    def real_midleft(self):
        return V2(*scale(self.relative_midleft, borg_baby.SCREEN_SIZE))

    @real_midleft.setter
    def real_midleft(self, value):
        self.x = m.ceil(value[0])
        self.y = m.ceil(value[1] - self.real_h / 2)

    # The midright position
    @property
    def relative_midright(self):
        return V2(self.relative_x + self.relative_w, self.relative_y + self.relative_h / 2)

    @relative_midright.setter
    def relative_midright(self, value):
        self.x = round(value[0] - self.relative_w, 5)
        self.y = round(value[1] - self.relative_y, 5)

    @property
    def real_midright(self):
        return V2(*scale(self.relative_midright, borg_baby.SCREEN_SIZE))

    @real_midright.setter
    def real_midright(self, value):
        self.x = m.ceil(value[0] - self.real_w)
        self.y = m.ceil(value[1] - self.real_y)

    # The bottomleft position
    @property
    def relative_bottomleft(self):
        return V2(self.relative_x, self.relative_y + self.relative_h)

    @relative_bottomleft.setter
    def relative_bottomleft(self, value):
        self.x = round(value[0], 5)
        self.y = round(value[1] - self.relative_h, 5)

    @property
    def real_bottomleft(self):
        return V2(*scale(self.relative_bottomleft, borg_baby.SCREEN_SIZE))

    @real_bottomleft.setter
    def real_bottomleft(self, value):
        self.x = m.ceil(value[0])
        self.y = m.ceil(value[1] - self.real_h)

    # the midbottom position
    @property
    def relative_midbottom(self):
        return V2(self.relative_x + self.relative_w / 2, self.relative_y + self.relative_h)

    @relative_midbottom.setter
    def relative_midbottom(self, value):
        self.x = round(value[0] - self.relative_w / 2, 5)
        self.y = round(value[1] - self.relative_h, 5)

    @property
    def real_midbottom(self):
        return V2(scale(self.relative_midbottom, borg_baby.SCREEN_SIZE))

    @real_midbottom.setter
    def real_midbottom(self, value):
        self.x = m.ceil(value[0] - self.real_w / 2)
        self.y = m.ceil(value[1] - self.real_h)

    # The bottomright position
    @property
    def relative_bottomright(self):
        return V2(self.relative_x + self.relative_w, self.relative_y + self.relative_h)

    @relative_bottomright.setter
    def relative_bottomright(self, value):
        self.x = round(value[0] - self.relative_w, 5)
        self.y = round(value[1] - self.relative_h, 5)

    @property
    def real_bottomright(self):
        return V2(*scale(self.relative_bottomright, borg_baby.SCREEN_SIZE))

    @real_bottomright.setter
    def real_bottomright(self, value):
        self.x = m.ceil(value[0] - self.real_w)
        self.y = m.ceil(value[1] - self.real_h)

    def update(self):
        if self.function_on_click is not None and self.mouse_click_area(1):
            self.function_on_click(self)

    def render(self):
        """
        Keeps the area at the right size and fill it TRANSPARENT
        :return:
        """
        if self.real_size != self.previous_state['real size']:
            pygame.Surface.__init__(self, self.real_size, pygame.SRCALPHA)  # resize

        self.fill(TRANSPARENT)  # That beautiful color !
        self.convert_alpha()

    # -------------------------------------------------- ALGORITHMS -------------------------------------------------- #
    def mouse_click_area(self, *num_buttons, option=JUST_PRESSED):
        """
        Returns True if one of the mouse's buttons passed in args clicks over the R, False otherwise
        0 = no click : the mouse is over the rect
        1 = left
        2 = middle
        3 = right
        4 = scroll down
        5 = scroll left

        option is JUST_PRESSED or IS_PRESSED if you want to know if the mouse just click the area or it keeps clicking
        option must be passed as kw arg if you want it
        """
        inputs = borg_baby.inputs

        if self.check_if_point_in_area(inputs['mouse']['real x'], inputs['mouse']['real y']):
            # we check if the wanted button is an actually pressed button
            if 0 in num_buttons:
                return True
            if 1 in num_buttons and inputs['left click'][option]:
                return True
            if 2 in num_buttons and inputs['middle click'][option]:
                return True
            if 3 in num_buttons and inputs['right click'][option]:
                return True
            if 4 in num_buttons and inputs['mouse']['scroll'] == -1:
                return True
            if 5 in num_buttons and inputs['mouse']['scroll'] == +1:
                return True
        return False

    def check_if_point_in_area(self, x, y):
        """
        Checks if the point (x, y) is inside the Area. They should be in pixels.
        :param x:
        :param y:
        :return:
        """
        if self.real_x <= x <= self.real_x + self.real_w and self.real_y <= y <= self.real_y + self.real_h:
            return True
        else:
            return False

    @execution_number
    def blit(self, *args, **kwargs):
        pygame.Surface.blit(self, *args, **kwargs)


class CircleArea(Area):
    def __init__(self, x, y, radius):
        self.radius = radius
        super(CircleArea, self).__init__(x, y, radius, radius)

    @property
    def w(self):
        return self.radius * 2

    @w.setter
    def w(self, value):
        self.radius = value / 2

    @property
    def h(self):
        return self.radius * 2

    @h.setter
    def h(self, value):
        self.radius = value / 2

    @property
    def real_radius(self):
        return to_pixels(self.radius, min(borg_baby.SCREEN_SIZE))

    @real_radius.setter
    def real_radius(self, value):
        self.radius = value

    @property
    def relative_radius(self):
        return to_prop(self.radius, min(borg_baby.SCREEN_SIZE))

    @relative_radius.setter
    def relative_radius(self, value):
        self.radius = value

    def check_if_point_in_area(self, x, y):
        """
        x and y must be in (screen)relative form
        :return:
        """
        if (x-self.relative_x) ^ 2 + (y - self.relative_y) ^ 2 < self.relative_radius ^ 2:
            return True
        else:
            return False


class Rectangle(Area):
    """
    The Rectangle class can be use to create, draw and interact with rectangles
    """

    def __init__(self, x, y, w, h, color=TRANSPARENT, shape=RECTANGLE, rounding=0.1, border=(TRANSPARENT, 0), function_on_click=None):
        self.shape = shape
        self.rounding = rounding

        if type(border[0]) != Color:
            self.border = Color(border[0]), border[1]
        else:
            self.border = border

        self._color = Color(color)  # it's uniformity and globalisation

        Area.__init__(self, x, y, w, h, function_on_click)

        self.previous_state = Rectangle.__state__(self)
        self.previous_state['first'] = None  # so it'll be differnet the first time

    def __repr__(self):
        #r = 'w:' + str(self.real_w) + ' h:' + str(self.real_h)
        #r += 'C:' + str(self._color.RGBA) + str(self.shape) + str(self.rounding) + str(self.border)
        r = "Rect({}, {}, {}, {}, {})".format(self.x, self.y, self.w, self.h, str(self._color))
        return str(r)

    def __state__(self):
        state = dict()
        state.update(Area.__state__(self))
        state['color'] = self._color.RGBA
        state['shape'] = self.shape
        state['rounding'] = self.rounding
        state['border'] = self.border
        return state

    @property
    def rect_as_tuple(self):
        """Use to get every parameter to make the same Rectangle object. Just do
            new_rect = Rect(*R.rect_as_tuple)
        """
        return self.x, self.y, self.w, self.h, self.rect_color, self.shape, self.rounding, self.border

    # circle radius
    @property
    def relative_circle_radius(self):
        if self.rounding > 1:
            rounding = to_prop(self.rounding, min(self.relative_w, self.relative_h))
        else:
            rounding = self.rounding

        return min(self.relative_w, self.relative_h) * rounding

    @property
    def real_circle_radius(self):
        if self.shape == ROUNDED:
            if self.rounding > 1:
                return self.rounding
            else:
                return m.ceil(min(self.real_w, self.real_h) * self.rounding)
        else:
            return 0

    # rect_color
    @property
    def rect_color(self):
        return self._color

    @rect_color.setter
    def rect_color(self, color):
        self._color = Color(color)

    # -------------------------------------------------- METHODS ----------------------------------------------------- #

    @only_if_object_changes
    def render(self):
        """
        Resize the surface if needed then choice between the different render modes to make a beautiful rectangle
        """

        Area.render(self)

        # now we draw the correct form
        if self.shape == RECTANGLE:
            self.render_rect()
        elif self.shape == ROUNDED:
            self.render_rounded_rect()
        elif self.shape == NO:
            pass
        else:
            raise Exception

        self.convert_alpha()

    def render_rect(self, color=None):
        """
        This update the object surface by drawing a rect of his size in
        """
        if color is None:
            color = self.rect_color
        self.fill(color.RGBA)  # izi

        # the border
        coucou = self.border[1]  # the width of the out lines
        point1 = (0, 0)  # the top left
        point2 = (self.real_w - coucou, 0)  # the top right
        point4 = (0, self.real_h - coucou)  # the bottom left
        point3 = (point2[0], point4[1])  # the bottom right
        points = [point1, point2, point3, point4]  # the point list

        # drawing the border
        pygame.draw.lines(self, self.border[0].RGB, True, points, self.border[1])

    def render_rounded_rect(self):
        """
        This update the object surface by drawing a rounded rect on it.
        The drawn rect is rounded in % by the R.rounding attribute
        """

        b = self.border[1]  # the border size
        c1 = self.rect_color.RGBA  # the rect color

        # less izi
        # we round the corners at rounding%
        c_r = self.real_circle_radius  # the radius of the circles in the 4 corners

        # definition of the rectangles
        #    _________
        #  _|         |_
        # | |         | |
        # |1|    2    |3|
        # |_|         |_|
        #   |_________|
        #

        #rect1 = (c_r, b, self.real_w - 2 * c_r, self.real_h - 2 * b)
        rect1 = (0, c_r, c_r, self.real_h - 2 * c_r)
        #rect2 = (b, c_r, c_r - b, self.real_h - 2 * c_r)
        rect2 = (c_r, 0, self.real_w - 2* c_r, self.real_h)
        #rect3 = (c_r, c_r, self.real_w - 2 * c_r, self.real_h - 2 * c_r)
        #rect4 = (self.real_w - c_r, c_r, c_r - b, self.real_h - 2 * c_r)
        rect3 = (self.real_w - c_r, c_r, c_r, self.real_h - 2* c_r)
        #rect5 = (c_r, self.real_h - c_r, self.real_w - 2 * c_r, c_r - b)

        # the 4 circles' positions  # TODO : arcs of circle
        pos_c1 = (c_r, c_r)  # the top left circle
        pos_c2 = (self.real_w - c_r, c_r)  # the top right circle
        pos_c3 = (c_r, self.real_h - c_r)  # the bottom left circle
        pos_c4 = (self.real_w - c_r, self.real_h - c_r)  # the bottom right circle

        # In order to draw the border we'll draw a rounded rect that have the size of the border rect,
        # then a 1 pixel smaller rect, that's the 'real' one.
        # In facts there will only the 2nd rect and the border of the first that will remain
        # To optimize, we will draw only the 4 circles and the 4 out lines

        if False:
        # if b != 0:  # if there is a particular border
            c2 = self.border[0].RGB  # the border color
            b2 = max(2*b, c_r)  # correction of ugly cbordered circle
            # the 4 circles and the 4 lines
            pygame.draw.circle(self, c2, pos_c1, c_r)  # the top left circle
            pygame.draw.circle(self, c2, pos_c2, c_r)  # the top right circle
            pygame.draw.circle(self, c2, pos_c3, c_r)  # the bottom left circle
            pygame.draw.circle(self, c2, pos_c4, c_r)  # the bottom right circle

            if b == 1:  # a little correction of a bug week the border with is 1
                a = 0  # I don'T know WHY it doesnt works
            else:  # but I know that now it works
                a = 1
            pygame.draw.line(self, c2, (c_r, a), (self.real_w - c_r, a), b)  # the top line
            pygame.draw.line(self, c2, (a, c_r), (a, self.real_h - c_r), b)  # the left line
            pygame.draw.line(self, c2, (self.real_w - b + a, c_r),
                             (self.real_w - b + a, self.real_h - c_r), b)  # the right line
            pygame.draw.line(self, c2, (c_r, self.real_h - b + a),
                             (self.real_w - c_r, self.real_h - b + a), b)  # the bottom line

        # we draw the 2 rectangles and the 4 circles

        graphalama.draw.circle(self, pos_c1, c_r, c1)  # the top left circle
        graphalama.draw.circle(self, pos_c2, c_r, c1)  # the top right circle
        graphalama.draw.circle(self, pos_c3, c_r, c1)  # the bottom left circle
        graphalama.draw.circle(self, pos_c4, c_r, c1)  # the bottom right circle

        pygame.draw.rect(self, c1, rect1)  # on l'affiche
        pygame.draw.rect(self, c1, rect2)  # on l'affiche
        # pygame.draw.rect(self, c1, rect3)  # on l'affiche
        pygame.draw.rect(self, c1, rect3)  # on l'affiche
        # pygame.draw.rect(self, c1, rect5)  # on l'affiche
__all__ = ['Rectangle', 'Area']
