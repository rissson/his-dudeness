# -*- coding: utf-8 -*-
import random
import pygame
import os
import graphalama
from graphalama.borg import Borg
from graphalama import fonts as f
from graphalama.color import Color
from graphalama.rectangle import Rectangle
from graphalama.text import Text
from graphalama.CONSTANTS import *

path = str(os.path.dirname(graphalama.__file__)).replace('\\', '/') + '/assets/img/'
wait_party_images = [pygame.image.load(path + 'wait_party/bunch_of_mms.png')]  # we load the wait party image
icon_image = pygame.image.load(path + 'logo.png')  # we load the logo image
borg_baby = Borg()


def new_display(name='Test with Graphalama', size=(0, 0), full_screen=False, icon_path='icon.png'):

    if not full_screen:
        display = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.SRCALPHA)  # window creation w/o fullscreen
    else:
        display = pygame.display.set_mode([0, 0], pygame.FULLSCREEN | pygame.SRCALPHA)  # window creation w/ fullscreen
    pygame.display.set_caption(name + ' ' + str(Borg().version))  # the window title

    try:
        icon_image = pygame.image.load(icon_path)  # we load the logo image
        pygame.display.set_icon(icon_image)  # the logo (task bar)
    except pygame.error:
        print('Icon file not found or unreadable')

    Borg().SCREEN_SIZE = display.get_size()
    return display


def resize(display, inputs):
    """

    :param display: The pygame display, created with new_display()
    :param inputs: An Inputs object
    :return:
    """
    screen_size_before = borg_baby.SCREEN_SIZE

    if inputs['F12']['just pressed']:
        inputs['screen']['fullscreen'] = not inputs['screen']['fullscreen']

        if not inputs['screen']['fullscreen']:
            display = pygame.display.set_mode([800, 500], pygame.RESIZABLE | pygame.SRCALPHA)
        else:
            display = pygame.display.set_mode([0, 0], pygame.FULLSCREEN | pygame.SRCALPHA)

    elif inputs['screen']['size'] != borg_baby.SCREEN_SIZE:
        display = pygame.display.set_mode(inputs['screen']['size'], pygame.RESIZABLE | pygame.SRCALPHA)
    inputs['screen']['change'] = False

    borg_baby.SCREEN_SIZE = display.get_size()

    if screen_size_before != borg_baby.SCREEN_SIZE:
        inputs['screen']['size'] = borg_baby.SCREEN_SIZE


def wait_party(surface):

    max_w = surface.get_width()
    h = surface.get_height()

    def color_mode_function(color):
        color.do_rainbow(random.randint(20, 50))
        return color.rainbow
    color = Color(WHITE, my_rainbow=color_mode_function)
    color.mode = 'my_rainbow'
    bpoints = [0]
    hpoints = [0]
    allc = list()
    while bpoints[-1] < max_w or hpoints[-1] < max_w:
        bpoints.append(bpoints[-1] + random.randint(20, 100))
        hpoints.append(hpoints[-1] + random.randint(20, 100))
        allc.append(color.RGB)
        points = ((hpoints[-2], 0), (hpoints[-1], 0), (bpoints[-1], h), (bpoints[-2], h))
        pygame.draw.polygon(surface, allc[-1], points)

    for c, hx, bx in zip(allc, bpoints, hpoints):
        pygame.draw.aaline(surface, c, (bx, 0), (hx, h))

    pygame.display.update()


# TODO : Faire retourner ça chez lui, dans Hubert. Et modifier le fonctionnement avec une Queue.
# Pour plus d'info, envoyez QUEUE au 06 95 40 21 62 !
def error_screen(display, inputs, error, fatal_error=False):
    wait_party(display)
    log_rect = Rectangle(0.1, 0.25, 0.8, 0.5, WHITE, border=(RED, 1))
    text_1_error = 'An error occured :', 'en'
    text_2_error = 'Please press enter to continue', 'en'
    error_1_text = Text(text_1_error, (0.15, 0.28, 0.7, 0.05), f.Font(f.Calibri, 1, True), color=RED,
                        anchor=('tc', 0, 0))
    error_2_text = Text(str(error), (0.15, 0.37, 0.7, 0.05),
                        f.Font(f.Calibri, 1, True), anchor=('tc', 0, 0), color=RED)
    error_3_text = Text(text_2_error, (0.15, 0.49, 0.7, 0.05),
                        f.Font(f.Calibri, 1, True), anchor=('tc', 0, 0), color=RED)
    valid_button = Text('Ok :/', (0.4, 0.62, 0.2, 0.1, L_BLUE, ROUNDED, 0.5), f.Font(f.Calibri, 0.3), RED,
                        anchor=('cc', 0, 0))
    enter = False
    while not (enter or valid_button.mouse_click_area(1)):  # tant qu'on pèse pas sur Entrée
        if inputs['enter']['is pressed']:
            enter = True
        log_rect.render()
        error_1_text.render()
        error_2_text.render()
        error_3_text.render()
        valid_button.render()
        display.blit(log_rect, log_rect.real_topleft)
        display.blit(error_1_text, error_1_text.real_topleft)
        display.blit(error_2_text, error_2_text.real_topleft)
        display.blit(error_3_text, error_3_text.real_topleft)
        display.blit(valid_button, valid_button.real_topleft)
        yield "APOUAAAAAAAAAAAAAAAAAAAAAL nick fury ta maire de Strasbourg #rolandries"
    if fatal_error:
        quit()

__all__ = ['new_display', "resize", 'wait_party', 'error_scren']
