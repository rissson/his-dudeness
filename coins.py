import random
import time

import pygame
from graphalama.colors import ImageBrush
from graphalama.constants import STRETCH
from graphalama.core import Widget, WidgetList
from graphalama.shadow import NoShadow


class Coins(WidgetList):
    def __init__(self):
        super().__init__([])
        self.last_spawn = time.time() - 4.2

    def spawn(self, score):
        spawn_interval = 4.2 ** (-score / 42 + 1) + 0.42
        if time.time() - self.last_spawn > spawn_interval:
            self.last_spawn = time.time()
            self.append(Coin())


class Coin(Widget):
    BRUSH = None

    def __init__(self):
        # If we define it before, it complains about no diplay created
        if Coin.BRUSH is None:
            Coin.BRUSH = ImageBrush("assets/coin.png", STRETCH)

        size = pygame.display.get_surface().get_size()
        pos = (random.randrange(0, (size[0] - 30)),
               random.randrange(0, (size[1] - 40)))
        super().__init__(pos=pos,
                         shape=(40, 40),
                         bg_color=Coin.BRUSH,
                         shadow=NoShadow())
