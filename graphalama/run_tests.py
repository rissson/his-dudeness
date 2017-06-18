# -*- coding: utf-8 -*-
import pygame
import graphalama
from graphalama.CONSTANTS import *
from graphalama.borg import Borg
from graphalama.text import Text
from graphalama.fonts import Font, Calibri

borg_baby = Borg()
__version__ = '0.0.1a'
borg_baby.version = __version__


def main():
    display = graphalama.screen.new_display(name='Nothing', size=[1500, 900], full_screen=False,
                                            icon_path='assets/icons/home.png')
    borg_baby.display = display

    inputs = graphalama.Inputs()
    borg_baby.inputs = inputs

    clock = pygame.time.Clock()

    fps = 60

    hello = Text('Hello World', (0, 0, 1, 1), graphalama.Font(size=200), ORANGE, ('cc', 0, 0), graphalama.FILL_SPACE)
    while not inputs['quit']['is pressed'] and not inputs['close']['is pressed']:
        graphalama.screen.resize(display, inputs)
        inputs.update()

        # update all objects
        hello.update()

        # then render them all
        hello.render()

        # and blit them all
        display.fill(WHITE)
        display.blit(hello, hello.real_topleft)

        clock.tick(fps)

        fps_text = Text(str(round(clock.get_fps())), (0, -20, 50, 20, (0, 0, 0, 128)),
                        Font(Calibri, 1), GREEN, ('tl', 0, 0))
        fps_text.render()
        display.blit(fps_text, fps_text.real_topleft)


        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
