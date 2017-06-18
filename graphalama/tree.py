# -*- coding: utf-8 -*-
import pygame
from graphalama.borg import Borg
from graphalama.rectangle import Rectangle

borg_baby = Borg()

class TreeCell(Rectangle):

    def __init__(self, y, w, h):
        Rectangle.__init__(self, 0, y, w, h)
        self.render()
        self.item = None

    def set_item(self, item):
        self.item = item
        self.render_cell(self.item)

    def render_cell(self, item):
        pass


class StringTreeCell(TreeCell):

    def render_cell(self, item):
        self.fill((0, 0, 0, 0))
        if item is not None:
            string = str(item)
            font = pygame.font.Font(None, 18)
            text = font.render(string, 1, (10, 10, 10))
            self.blit(text, (10, ((self.get_height() - 18) / 2)))

class TreeView(Rectangle):

    def __init__(self, rect_args, cell_height=50, cell_type=StringTreeCell):
        Rectangle.__init__(self, *rect_args)
        self.cell_height = cell_height
        self.scroll = 0
        self.gap = 0
        self.scroll_speed = 1
        self.scroll_reset = 15
        self.nodes = []
        w = self.real_w
        self.cells = [cell_type(i*self.cell_height, w, self.cell_height) for i in range(int((self.real_h/self.cell_height)+2))]

    def __state__(self):
        s = dict()
        s.update(Rectangle.__state__(self))
        s['cell_height'] = self.cell_height
        s['roots'] = self.nodes
        s['cells'] = self.cells
        s['scroll'] = self.scroll
        s['gap'] = self.gap
        s['active cells'] = self.active_cells()
        return s

    def add_node(self, node):
        self.nodes.append(node)
        self.set_cells()

    def add_all_node(self, node_list):
        self.nodes.extend(node_list)
        self.set_cells()

    def set_cells(self):
        i = 0
        cell_i = 0
        print("Check 1")
        while cell_i <= len(self.cells):
            try:
                print("Check 2")
                node = self.nodes[i-self.gap]
                self.cells[cell_i].set_item(node)
                node.level = 0
                cell_i+=1
                print("Check 3")
                cell_i = self.set_cells_rec(self.nodes[i], cell_i, 1)
                print("Check 4")
                i+=1
            except IndexError:
                break
        print(cell_i, len(self.cells))
        try:
            for i_cell in range(cell_i, len(self.cells)):
                print(i_cell)
                self.cells[i_cell].set_item(None)
        except IndexError:
            pass


    def set_cells_rec(self, node, cell_i, level):
        if node.has_children() and node.expend:
            for child in node.get_childrens():
                try:
                    self.cells[cell_i].set_item(child)
                    child.level = level
                    cell_i+=1
                    cell_i = self.set_cells_rec(child, cell_i, level+1)
                except IndexError:
                    return cell_i
        return cell_i


    def active_cells(self):
        i = 0
        for node in self.nodes:
            i+=1
            i+=self.get_children_rec(node)
        return i

    def get_children_rec(self, node):
        i = 0
        if node.has_children() and node.expend:
            for child in node.get_childrens():
                i+=1
                i+=self.get_children_rec(child)
        return i

    def update(self):
        direction = 0
        if self.mouse_click_area(4) or self.mouse_click_area(5):
            if borg_baby.inputs['mouse']['scroll'] == -1 and self.gap < 0:
                direction = +1
            elif borg_baby.inputs['mouse']['scroll'] == +1 and abs(self.gap) < (self.active_cells()-(self.real_h//self.cell_height)):
                # TODO: check the value of scroll
                direction = -1
            if direction != 0:
                self.scroll_speed+=0.1
                self.scroll += int(direction*self.real_h/10*self.scroll_speed)
            if abs(self.scroll) >= self.cell_height:
                self.gap += (self.scroll // self.cell_height)
                self.scroll = (self.scroll % self.cell_height)
                self.set_cells()
        else:
            if self.scroll_reset == 0:
                self.scroll_speed = 0.1
                self.scroll_reset = 15
            else:
                self.scroll_reset -= 1
        item = self.item_click(1)
        if item is not None:
            if item.expend:
                item.expend = False
            else:
                item.expend = True
            self.set_cells()
            self.render()

    def render(self):
        self.fill(self.rect_color.RGBA)
        for cell in self.cells:
            cell.y = self.cell_height * self.cells.index(cell) + self.scroll
            try:
                cell.x = cell.item.level*10
            except AttributeError:
                cell.x = 0
            self.blit(cell, cell.real_topleft)

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

class Node():

    def __init__(self, item):
        self.item = item
        self.expend = True
        self.childrens = []
        self.level = 0

    def add_children(self, item):
        self.childrens.append(item)

    def add_all_children(self, list):
        self.childrens.extend(list)

    def has_children(self):
        if len(self.childrens) > 0:
            return True
        else:
            return False

    def get_childrens(self):
        return self.childrens

    def __str__(self):
        return str(self.item)
