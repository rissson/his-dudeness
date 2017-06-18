# -*- coding: utf-8 -*-
import pygame
from graphalama.borg import Borg
from graphalama.rectangle import Rectangle, Area
from graphalama.CONSTANTS import *
from graphalama.functions import only_if_object_changes
borg_baby = Borg()


class ListCell(Rectangle):
    """Super class that represent a cell from a ListView (see ListView)"""

    def __init__(self, w, h, list_view):
        Rectangle.__init__(self, 0, 0, w, h)
        self.render()
        self.item = None
        self.list_view = list_view
        self.cell_y = 0

    def set_item(self, item):
        """Used to set the item contains in the cell"""
        self.item = item
        self.render_cell(self.item)

    def render_cell(self, item):
        """Used to draw the cell, to override in the custom cell class"""
        pass


class StringListCell(ListCell):
    """Default List Cell, display the string representation of the item"""

    def render_cell(self, item):
        self.fill((0, 0, 0, 0))
        string = str(item)
        font = pygame.font.Font(None, 18)
        text = font.render(string, 1, (10, 10, 10))
        self.blit(text, (10, ((self.get_height()-18)/2)))


class ListView(Rectangle):
    """A list view displays a list of objects. It is composed of list cells that displays
    the string representation of the objects by default.
    You can create a custom type of cells that inherit from ListCell and override the render(item) method
    to specify how the objects should be displayed"""

    def __init__(self, list, rect_args=None, cell_height=50, cell_type=StringListCell):
        Rectangle.__init__(self, *rect_args)
        self.list = list    # The list to display
        self.cell_height = cell_height
        self.scroll = 0
        self.gap = 0
        self.scroll_speed = 1
        self.scroll_reset = 15
        h = len(self.list)*self.cell_height
        if h < self.real_h:
            h = self.real_h
        w = self.real_w
        self.scroll_bar = DiegoScrollBar(w-25, 0, self.real_h, h)
        self.cells = [cell_type(w, self.cell_height, self) for i in range(int((self.real_h/self.cell_height)+2))]

    def __state__(self):
        state = dict()
        state['list_length'] = len(self.list)
        state['scroll'] = self.scroll
        state['gap'] = self.gap
        state['cell_height'] = self.cell_height
        state['scroll_bar'] = self.scroll_bar.__state__()
        return state

    def set_items(self, list):
        self.list = list
        self.scroll = 0
        self.gap = 0
        self.set_cell()
        #self.scroll_bar.total_height = (len(self.list)*self.cell_height)

    def set_cell(self):
        self.gap += (self.scroll//self.cell_height)
        self.scroll = (self.scroll % self.cell_height)

    @only_if_object_changes
    def render(self):
        if abs(self.scroll) >= self.cell_height:
            self.set_cell()
        self.fill(self.rect_color.RGBA)
        for cell in self.cells:
            try:
                if cell.item is not self.list[self.cells.index(cell)-self.gap]:
                    cell.set_item(self.list[self.cells.index(cell)-self.gap])
                cell_y = self.cell_height*self.cells.index(cell)+self.scroll
                self.blit(cell, (0, cell_y))
                cell.cell_y = cell_y
            except IndexError:
                break
        #self.scroll_bar.bar.y = self.real_h*((self.scroll+abs(self.gap)*self.cell_height)/self.real_h) / \
                                #(len(self.list)*self.cell_height)/self.real_h
        self.scroll_bar.render()
        self.blit(self.scroll_bar, self.scroll_bar.real_topleft)

    def update(self):
        direction = 0
        if self.mouse_click_area(4) or self.mouse_click_area(5):
            if borg_baby.inputs['mouse']['scroll'] == -1 and self.gap < 0:
                direction = +1
            elif borg_baby.inputs['mouse']['scroll'] == +1 and abs(self.gap) < (len(self.list)-(self.real_h//self.cell_height)):
                # TODO: check the value of scroll
                direction = -1
            if direction != 0:
                self.scroll_speed+=0.1
                self.scroll += int(direction*self.real_h/10*self.scroll_speed)
        else:
            if self.scroll_reset == 0:
                self.scroll_speed = 1
                self.scroll_reset = 15
            else:
                self.scroll_reset -= 1

        self.scroll_bar.update()

    def item_click(self, no_button, get_cell=False):
        if self.mouse_click_area(no_button):
            mouse_relative_x = borg_baby.inputs['mouse']['real x']-self.real_x
            mouse_relative_y = borg_baby.inputs['mouse']['real y']-self.real_y
            for cell in self.cells:
                cell_y = (self.cells.index(cell)*self.cell_height)+self.scroll
                if mouse_relative_y > cell_y and mouse_relative_y < cell_y + self.cell_height:
                    if get_cell:
                        return cell
                    return cell.item
        return None


class DiegoScrollBar(Area):
    def __init__(self, x, y, h, total_height):
        """
        Create a scroll bar to blit on a surface
        :param x: The x real (or relative bit from the total screen) position
        :param y: The y real (or relative bit from the total screen) position
        :param h: The height of the surface, who'll be the height of the scroll bar area
        :param total_height: The total height of the surface to scroll
        """

        self._total_height = total_height
        Area.__init__(self, x, y, 10, h)
        self.bar = Rectangle(x, y, 10, self.scroll_bar_real_size, GREY_10, border=(GREY_25, 1))
        self.position = 0
        self.scrolling = True
        self.delta_y = 0

        self.focus = False
        self.previous_state = self.__state__()
        self.previous_state['first'] = True

    def __state__(self):
        s = dict()
        s.update(Area.__state__(self))
        s['bar'] = self.bar.__state__()
        s['bar y'] = self.bar.real_y
        s['total height'] = self.total_height
        s['scrolling'] = self.scrolling
        return s

    @property
    def scroll_bar_real_size(self):
        return min(self.real_h / self.total_height, 1) * self.real_h

    @property
    def total_height(self):
        return self._total_height

    @total_height.setter
    def total_height(self, value):
        self._total_height = value
        self.bar.h = self.scroll_bar_real_size

    @property
    def start_pos_to_blit_big_surface(self):
        bar_pos = self.bar.real_topleft[1] - self.real_topleft[1]
        purcentage = bar_pos / self.real_h
        return int(self.total_height * purcentage)

    @property
    def end_pos_to_blit_big_surface(self):
        end_bar_pos = self.bar.real_bottomleft[1] - self.real_topleft[1]
        purcentage = end_bar_pos / self.real_h
        return int(self.total_height * purcentage)

    def update(self):
        self.bar.x = self.x  # in case it changes, the bar won't be clickable in the right place

        if self.bar.mouse_click_area(1):  # click
            self.scrolling = True
            self.delta_y = borg_baby.inputs['mouse']['rel y'] - self.relative_y
        elif borg_baby.inputs['left click']['is pressed'] and self.scrolling:  # keep clicked
            self.scrolling = True
        else:  # no click
            self.scrolling = False
            self.delta_y = 0

        if self.scrolling:
            y = borg_baby.inputs['mouse']['rel y'] - self.delta_y
            if y < self.relative_y:
                y = self.relative_y
            if y > self.relative_y + self.relative_h - self.bar.relative_h:
                y =  self.relative_y + self.relative_h - self.bar.relative_h
            #y = max(self.relative_y, y)  # bar must be in the area
            #y = min(self.relative_y + self.relative_h - self.bar.relative_h, y)
            self.bar.y = y
        elif self.focus == True and borg_baby.inputs['scroll']:
            y = self.bar.real_y + 5 * borg_baby.inputs['scroll']

            if y < self.relative_y:
                y = self.relative_y
            if y > self.relative_y + self.relative_h - self.bar.relative_h:
                y = self.relative_y + self.relative_h - self.bar.relative_h
            # y = max(self.relative_y, y)  # bar must be in the area
            # y = min(self.relative_y + self.relative_h - self.bar.relative_h, y)
            self.bar.y = y

    @only_if_object_changes
    def render(self):
        self.fill(TRANSPARENT)
        if self.scrolling:
            self.bar.rect_color = GREEN
        else:
            self.bar.rect_color = GREY_10
        self.bar.render()
        self.blit(self.bar, self.bar.real_topleft - self.real_topleft)


class ScrollBar(Area):    # FIXME: Make it work

    def __init__(self, list_view, rect_args):
        Area.__init__(self, *rect_args)
        self.is_dragging = True
        self.list_view = list_view
        self.scroll = 0
        try: # Pour la taille
            h = 1/(len(self.list_view.list)/(self.real_h/self.list_view.cell_height))
        except ZeroDivisionError:
            h = 1
        self.scroll_bar = Rectangle(0, 0, 15, h, GREY_50)


    def update(self, inputs):
        if self.mouse_click_area(1):
            self.is_dragging = True
        if self.is_dragging:
            if inputs['left click']['is pressed']:
                self.scroll = inputs['mouse']['real y']-self.list_view.real_y
                if self.scroll < 0:
                    self.scroll = 0
                elif self.scroll > self.list_view.real_h-self.real_h:
                    self.scroll = self.list_view.real_h-self.real_h
                self.list_view.gap = int((self.scroll/self.real_h)*len(self.list_view.list))
            else:
                self.is_dragging = True
        try:
            self.scroll = (abs(self.list_view.gap)/len(self.list_view.list)*self.list_view.cell_height) / \
                      (self.real_h-self.scroll_bar.real_h)*(len(self.list_view.list)*self.list_view.cell_height)
            print(self.scroll)
        except ZeroDivisionError:
            self.scroll = 0
            print("Zero division")

    def render(self):
        self.fill(TRANSPARENT)
        self.scroll_bar.render()
        self.blit(self.scroll_bar, (0, self.scroll))


class GridView(Rectangle):
    """A list view displays a list of objects. It is composed of list cells that displays
    the string representation of the objects by default.
    You can create a custom type of cells that inherit from ListCell and override the render(item) method
    to specify how the objects should be displayed"""

    def __init__(self, list, rect_args=None, cell_height=50, cell_width=50, cell_type=StringListCell):
        Rectangle.__init__(self, *rect_args)
        self.list = list    # The list to display
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.columns = self.real_w//self.cell_width
        self.scroll = 0
        self.gap = 0
        self.scroll_speed = 1
        self.scroll_reset = 15
        bar_height = self.cell_height*len(self.list)
        if bar_height == 0:
            bar_height = 1
        self.scroll_bar = DiegoScrollBar(0.8, 0.1, 0.75, bar_height)
        self.cells = [cell_type(int(self.real_w/self.columns), self.cell_height, self) for i in range(int((self.real_h/self.cell_height)*self.columns))]

    def __state__(self):
        state = dict()
        state['list'] = self.list
        state['scroll'] = self.scroll
        state['gap'] = self.gap
        state['cell_height'] = self.cell_height
        state['columns'] = self.columns
        state['scroll bar'] = self.scroll_bar.__state__()
        return state


    def set_items(self, list):
        self.list = list
        self.scroll = 0
        self.gap = 0
        bar_height = self.cell_height * len(self.list)
        if bar_height == 0:
            bar_height = 1
        self.scroll_bar.total_height = bar_height
        self.set_cell()

    def set_cell(self):
        self.gap += (self.scroll//self.cell_height)
        self.scroll = (self.scroll % self.cell_height)

    @only_if_object_changes
    def render(self):
        if abs(self.scroll) >= self.cell_height:
            self.set_cell()
        self.fill(self.rect_color.RGBA)
        for cell in self.cells:
            try:
                cell.set_item(self.list[self.cells.index(cell)-self.gap*self.columns])
                cell_y = (self.cells.index(cell)//self.columns)*self.cell_height+self.scroll
                cell_x = (self.cells.index(cell)%self.columns)*int(self.real_w/self.columns)
                self.blit(cell, (cell_x, cell_y))
                cell.cell_y = cell_y
            except IndexError:
                break
        self.scroll_bar.position = abs(self.gap)*self.cell_height+abs(self.scroll)
        self.scroll_bar.render()
        self.blit(self.scroll_bar, (self.real_w - 20, 0))

    def update(self):
        direction = 0
        if self.mouse_click_area(4) or self.mouse_click_area(5):
            if borg_baby.inputs['mouse']['scroll'] == -1 and self.gap < 0:
                direction = +1
            elif borg_baby.inputs['mouse']['scroll'] == +1 and abs(self.gap) < (len(self.list)/self.columns-((self.real_h//self.cell_height)/self.columns)):
                # TODO: check the value of scroll
                direction = -1
            if direction != 0:
                self.scroll_speed+=0.1
                self.scroll += int(direction*self.real_h/10*self.scroll_speed)
        else:
            if self.scroll_reset == 0:
                self.scroll_speed = 1
                self.scroll_reset = 15
            else:
                self.scroll_reset -= 1

        self.scroll_bar.update()

    def item_click(self, no_button, get_cell=False):
        if self.mouse_click_area(no_button):
            mouse_relative_x = borg_baby.inputs['mouse']['real x']-self.real_x
            mouse_relative_y = borg_baby.inputs['mouse']['real y']-self.real_y
            for cell in self.cells:
                cell_y = ((self.cells.index(cell)*self.cell_height)+self.scroll)//self.columns
                cell_x = ((self.cells.index(cell)*self.cell_width))% self.columns
                if mouse_relative_y > cell_y and mouse_relative_y < cell_y + self.cell_height and \
                                mouse_relative_x > cell_x and mouse_relative_x < cell_x + self.cell_width:
                    if get_cell:
                        return cell
                    return cell.item
        return None
