# -*- coding: utf-8 -*-
import pygame
import pygame.gfxdraw

import graphalama
from graphalama import fonts as f
from graphalama.CONSTANTS import *
from graphalama.color import lighter
from graphalama.fonts import Font
from graphalama.functions import only_if_object_changes
import graphalama.icons as i
from graphalama.rectangle import Rectangle, Area
from graphalama.text import Text
from graphalama.time import Time


class StatesButton(Rectangle):
    """
    A button to choice between more than 2 states
    """

    def __init__(self, x, y, w, main_text, states_list, color=WHITE, border=(L_LIGHT_BLUE, 1), hint=None):
        """
        The x, y, params are basically the position of the rect
        The w is the width but there's no height because the rect always has a proportion of phi between h & w
        The color is the bg color of the bubbles_style_button
        The states_list is a list of more than two states.
            Each state is a dict containing 2 keys :
                - 'txt': str        --> The text who'll be displayed
                - 'clr': Color      --> The color of the text who'll be displayed
                - 'value: obj       --> SB.update will return this object if this state is the current
        The border refers to the rect class. It's a tuple (color, width) of the border
        """

        h = w / PHI  # the golden rect proportions

        # transforming each dict state of the list into a  dict with more items : rendered texts...
        self.states = states_list
        for state in self.states:
            state['big txt'] = Text(state['txt'], (0, 0, w, 1 / 3 * h),
                                    f.Font(), state['clr'], anchor=('cc', 0, 0), options=ONELINE)
            state['small txt'] = Text(state['txt'], (0, 0, w, 1 / 6 * h),
                                      f.Font(), GREY_25, anchor=('cc', 0, 0), options=ONELINE)

        self.num_state = 0
        self.main_text = Text(main_text, (x, y, w, 1 / 3 * h), f.Font(), anchor=('cc', 0, 0), options=ONELINE)

        super().__init__(x, y, w, h, color, ROUNDED, border=border)

        if hint is not None:
            self.hint = Text(hint, (x, y, w, h, TRANSPARENT, ROUNDED, 0.1), anchor=('tl', 0, 0), options=FILL_SPACE)
            self.icon_info_area = Area(self.real_x + self.real_w - 25, self.real_y + self.real_h - 25, 20, 20)
        else:
            self.hint = None
        self.hinting = False

        self.previous_state = self.__state__()
        self.previous_state['F'] = 1

    def __state__(self):
        state = dict()
        state.update(Rectangle.__state__(self))
        state['num_state'] = self.num_state
        state['main_state'] = self.main_text.__state__()
        state['big_text'] = self.states[self.num_state]['big txt'].__state__()
        state['hinting'] = self.hinting
        if self.hint is None:
            state['hint'] = None
        else:
            state['hint'] = self.hint.__state__()
        return state

    def update(self, inputs):
        """

        """

        if self.mouse_click_area(4):
            self.num_state -= 1
        if self.mouse_click_area(5):
            self.num_state += 1

        if self.hint is not None:
            self.icon_info_area.real_topleft = self.real_bottomright - (25, 25)
            if self.icon_info_area.mouse_click_area(0):
                self.hinting = True
            else:
                self.hinting = False

        self.num_state %= len(self.states)  # it can'T be more than the number of states or less than 0

        return self.states[self.num_state]['value']

    @only_if_object_changes
    def render(self):

        # the rectangle + actualisation of the surface
        Rectangle.render(self)

        if self.hinting:
            self.hint.render()
            self.blit(self.hint, (0, 0))
        else:
            # simplification
            p = self.main_text  # The button main text
            t = self.states[(self.num_state - 1) % len(self.states)]['small txt']  # The current state text
            m = self.states[self.num_state]['big txt']  # The current state text
            b = self.states[(self.num_state + 1) % len(self.states)]['small txt']  # The text behind the current

            # render every text
            p.render()
            t.render()
            m.render()
            b.render()

            # center set
            w, h = self.relative_size
            p.relative_center = (0.5*w, 1/6*h)  # The button main text
            t.relative_center = (0.5*w, 0.42*h)  # The current state text - 1
            m.relative_center = (0.5*w, 0.63*h)  # The current state text
            b.relative_center = (0.5*w, 0.88*h)  # The text behind the current

            # displaying the 4 texts
            self.blit(p, p.real_topleft)  # The button main text
            self.blit(t, t.real_topleft)  # The current state text - 1
            self.blit(m, m.real_topleft)  # The current state text
            self.blit(b, b.real_topleft)  # The text behind the current

        if self.hint is not None:
            self.blit(i.icon_info.get(20), [self.real_w - 25, self.real_h - 25])

        self.convert_alpha()

    def value_to_num(self, value):
        try:
            i = 0
            while self.states[i]['value'] != value:
                i += 1
            return i
        except IndexError:
            print("This value doesn't exists :", value)
            for state in self.states:
                print(state['value'])
            print("Value used instead :", self.states[0]['value'])
            return 1

    def go_to_value(self, value):
        self.num_state = self.value_to_num(value)


class IntPicker(Area):
    def __init__(self, x, y, w, range, color):
        h = 4*w
        super(IntPicker, self).__init__(x, y, w, h)

        self.beg = range.start
        self.end = range.stop
        self.step = range.step
        self.pos = self.beg

        self.color = color

    def update(self, inputs):
        if self.mouse_click_area(0):
            self.pos += inputs['mouse']['scroll'] * self.step
            self.pos = max(min(self.end, self.pos), self.beg)

    def render(self):
        super(IntPicker, self).render()

        # the up arrow
        pygame.draw.polygon(self, lighter(self.color, 0.5), [(self.real_w / 2, 0),
                                                             (0, 1/8*self.real_h),
                                                             (self.real_w, 1/8*self.real_h)])

        # The previous number
        if self.pos > self.beg:  # if there's one
            C_up = Text(str(self.pos - self.step), (0, 0, self.w, self.w), color=GREY_50, anchor=('cc', 0, 0))
        else:
            C_up = Text('-', (0, 0, self.w, self.w), color=GREY_50, anchor=('cc', 0, 0))
        C_up.render()
        self.blit(C_up, (0, int(1/8*self.real_h)) )

        # the sep line #1
        pygame.draw.line(self, self.color, (0, int(3/8 * self.real_h)), (self.real_w, int(3/8 * self.real_h)), 2)

        # the current number
        C = Text(str(self.pos), (0, 0, self.w, self.w), anchor=('cc', 0, 0))
        C.render()
        self.blit(C, (0, int(3/8 * self.real_h)))

        # the sep line #2
        pygame.draw.line(self, self.color, (0, int(5/8 * self.real_h)), (self.real_w, int(5/8 * self.real_h)), 2)

        # the next number
        if self.pos < self.end:
            C_down = Text(str(self.pos + self.step), (0, 0, self.w, self.w), color=GREY_50, anchor=('cc', 0, 0))
        else:
            C_down = Text('-', (0, 0, self.w, self.w), color=GREY_50, anchor=('cc', 0, 0))
        C_down.render()
        self.blit(C_down, (0, int(5/8*self.real_h)) )

        # the down arrow
        pygame.draw.polygon(self, lighter(self.color, 0.5), [(self.real_w / 2, self.real_h),
                                   (0, 7 / 8 * self.real_h),
                                   (self.real_w, 7 / 8 * self.real_h)])


class TimePicker(Area):
    def __init__(self,name, x, y, w, beg, end, color=GREY_50):
        h = w * 2
        super(TimePicker, self).__init__(x, y, w, h)

        self.beg = beg
        self.end = end
        self.color = color

        self.name = Text(name, (0, 4/5*h, w, 1/5*h), Font(), color, ('cc', 0, 0), ONELINE)
        self.hour_picker = IntPicker(x, y, w/2.5, range(beg.h, end.h), color)
        self.min_picker = IntPicker(x+3/5*w, y, w/2.5, range(0, 60, 5), color)

    @property
    def time(self):
        return Time(self.hour_picker.pos, self.min_picker.pos)

    @time.setter
    def time(self, value):
        self.hour_picker.pos = value.h
        self.min_picker.pos = value.m

    def update(self, inputs):
        self.hour_picker.update(inputs)
        self.min_picker.update(inputs)

    def render(self):
        super(TimePicker, self).render()

        self.hour_picker.render()
        self.blit(self.hour_picker, self.hour_picker.real_topleft - self.real_topleft)

        graphalama.draw.circle(self, (self.real_w / 2, (2 / 5 + 1 / 18) * self.real_h), self.real_w / 20, self.color)
        graphalama.draw.circle(self, (self.real_w / 2, (2 / 5 - 1 / 18) * self.real_h), self.real_w / 20, self.color)

        self.min_picker.render()
        self.blit(self.min_picker, self.min_picker.real_topleft - self.real_topleft)

        if self.name.text != '':
            self.name.render()
            self.blit(self.name, self.name.real_topleft)


__all__ = ['StatesButton', 'TimePicker', 'IntPicker']
