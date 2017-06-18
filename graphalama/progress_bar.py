# -*- coding: utf-8 -*-
from graphalama.rectangle import Rectangle, Area
from graphalama.functions import only_if_object_changes
from graphalama.borg import Borg
from graphalama.CONSTANTS import *

borg_baby = Borg()

class ProgressBar(Rectangle):

    def __init__(self, rect_args, progress, max):
        Rectangle.__init__(self, *rect_args)
        self.bar = Rectangle(self.real_x+2, self.real_y+2, self.real_w-4, self.real_h-4, GREEN)
        self._progress = progress
        self._max = max
        self.scrolling = True
        self.new_val = False
        self.previous_state = self.__state__()
        self.previous_state['first'] = True

    def __state__(self):
        s = dict()
        s.update(Area.__state__(self))
        s['progress'] = self._progress
        s['max'] = self._max
        s['bar'] = self.bar.__state__()
        return s

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if not self.scrolling:
            self._progress = value
            self.bar.w = (self.real_w*self._progress)/self.max

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value
        self.bar.w = (self.real_w * self._progress) / self.max

    def has_new_val(self):
        if self.new_val and not self.scrolling:
            self.new_val = False
            return True
        return False

    def update(self):
        if self.mouse_click_area(1) or borg_baby.inputs['left click']['is pressed'] and self.scrolling:
            self.scrolling = True
        else:
            self.scrolling = False

        if self.scrolling:
            mouse_x = borg_baby.inputs['mouse']['real x']-self.real_x
            if mouse_x > self.real_w:
                mouse_x = self.real_w
            elif mouse_x < 0:
                mouse_x = 0
            self._progress = self.max*mouse_x/self.real_w
            self.bar.w = (self.real_w * self._progress) / self.max
            self.new_val = True

    @only_if_object_changes
    def render(self):
        self.fill(WHITE)
        self.bar.render()
        self.blit(self.bar, self.bar.real_topleft - self.real_topleft)