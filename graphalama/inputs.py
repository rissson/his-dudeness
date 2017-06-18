# -*-coding:utf-8 -*
import pygame
from graphalama.borg import Borg
borg_baby = Borg()

pygame.init()
pygame.key.set_repeat(50, 5)


class Inputs(dict):
    """permet de connaitre tous les inputs
    contient A, B, X, Y, DOWN, UP, RIGHT, LEFT, QUIT et PAUSE"""

    def __init__(self):

        # noinspection PyTypeChecker
        dict.__init__(self)

        # simplification
        key_dict = {'is pressed': False, 'just pressed': False, 'press time': -1}

        # keyboard
        self['right arrow'] = dict(key_dict)
        self['left arrow'] = dict(key_dict)
        self['up arrow'] = dict(key_dict)
        self['down arrow'] = dict(key_dict)
        self['space bar'] = dict(key_dict)
        self['tab'] = dict(key_dict)
        self['enter'] = dict(key_dict)
        self['F12'] = dict(key_dict)
        self['alt'] = dict(key_dict)
        self['F4'] = dict(key_dict)
        self['close'] = dict(key_dict)
        self['escape'] = dict(key_dict)
        # mouse click
        self['left click'] = dict(key_dict)
        self['middle click'] = dict(key_dict)
        self['right click'] = dict(key_dict)

        # special
        self['screen'] = {'change': False, 'size': (0, 0), 'fullscreen': True}
        self['mouse'] = {'real x': 0, 'real y': 0, 'rel x': 0, 'rel y': 0, 'scroll': 0}

        self.list_events = []

        self['screen']['size'] = borg_baby.SCREEN_SIZE

    @property
    def mouse_click(self):
        # if there's a click somewhere
        return self['left click']['just pressed'] or self['middle click']['just pressed'] or self['right click'][
            'just pressed']

    def press(self, key):
        self[key]['is pressed'] = True
        self[key]['just pressed'] = True
        self[key]['press time'] = 0

    def unpress(self, key):
        self[key]['is pressed'] = False
        self[key]['just pressed'] = False
        self[key]['press time'] = -1

    def update(self):

        self.list_events = pygame.event.get()

        mouse_pos = pygame.mouse.get_pos()
        self['mouse']['real x'] = mouse_pos[0]
        self['mouse']['real y'] = mouse_pos[1]
        self['mouse']['rel x'] = mouse_pos[0] / self['screen']['size'][0]  # I can't be more precise
        self['mouse']['rel y'] = mouse_pos[1] / self['screen']['size'][1]  # idem
        self['mouse']['scroll'] = 0

        # we reset every 'just pressed' values so you wont think x) that the key is pressed twice or more
        for key, sub_dict in self.items():
            if sub_dict.__contains__('just pressed'):  # normally it's has_key() but strangely it doesn'T work
                sub_dict['just pressed'] = False
        self['screen']['change'] = False

        # On incrément tous les compteurs if needed
        for key, sub_dict in self.items():
            if sub_dict.__contains__('is pressed'):
                if sub_dict['is pressed']:
                    sub_dict['press time'] += 1

        for event in self.list_events:
            # la tit' croix
            if event.type == pygame.QUIT:  # on verifie le type d'event
                self['close']['is pressed'] = True

                # clavier
            # appui sur une touche
            if event.type == pygame.KEYDOWN:  # on verifie le type d'event
                if event.key == pygame.K_RIGHT:  # on test pour connaitre la touche
                    self.press('right arrow')
                elif event.key == pygame.K_LEFT:  # on test pour connaitre la touche
                    self.press('left arrow')
                elif event.key == pygame.K_UP:
                    self.press('up arrow')
                elif event.key == pygame.K_DOWN:
                    self.press('down arrow')
                elif event.key == pygame.K_SPACE:
                    self.press('space bar')
                elif (event.key == pygame.K_RALT or event.key == pygame.K_LALT):
                    self.press('alt')
                elif event.key == pygame.K_F4:  # on test pour connaitre la touche
                    self.press('F4')
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.press('enter')
                elif event.key == pygame.K_F12:
                    self.press('F12')
                elif event.key == pygame.K_TAB:
                    self.press('tab')
                elif event.key == pygame.K_ESCAPE:
                    self.press('escape')
            # touche relachée
            elif event.type == pygame.KEYUP:  # on verifie le type d'event
                if event.key == pygame.K_RIGHT:  # on test pour connaitre la touche
                    self.unpress('right arrow')
                elif event.key == pygame.K_LEFT:  # on test pour connaitre la touche
                    self.unpress('left arrow')
                elif event.key == pygame.K_UP:  # on test pour connaitre la touche
                    self.unpress('up arrow')
                elif event.key == pygame.K_SPACE:
                    self.unpress('space bar')
                elif event.key == pygame.K_DOWN:  # on test pour connaitre la touche
                    self.unpress('down arrow')
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.unpress('enter')
                elif event.key == pygame.K_F12:
                    self.unpress('F12')
                elif event.key == pygame.K_TAB:
                    self.unpress('tab')
                elif event.key == pygame.K_ESCAPE:
                    self.unpress('escape')


                    # les clics
            elif event.type == pygame.MOUSEBUTTONDOWN:  # on verifie le type d'event
                if event.button == 1:  # on test pour connaitre le bouton 1 = gauche
                    self.press('left click')
                elif event.button == 2:  # on test pour connaitre le bouton 2 = clic mollette
                    self.press('middle click')
                elif event.button == 3:  # on test pour connaitre le bouton 3 = clic droit
                    self.press('right click')
                elif event.button == 4:
                    self['mouse']['scroll'] = -1
                elif event.button == 5:
                    self['mouse']['scroll'] = 1
            elif event.type == pygame.MOUSEBUTTONUP:  # on verifie le type d'event
                if event.button == 1:  # on test pour connaitre le bouton 1 = gauche
                    self.unpress('left click')
                if event.button == 2:  # on test pour connaitre le bouton 2 = clic mollette
                    self.unpress('middle click')
                if event.button == 3:  # on test pour connaitre le bouton 3 = clic droit
                    self.unpress('right click')
                    # le changement de taille de fenetre
            elif event.type == pygame.VIDEORESIZE:  # on verifie le type d'event
                self['screen']['change'] = True
                self['screen']['size'] = event.size

__all__ = ['Inputs']
