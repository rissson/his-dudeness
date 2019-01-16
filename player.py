from collections import deque
from functools import lru_cache

import pygame
from graphalama.colors import ImageBrush
from graphalama.constants import STRETCH, FIT
from graphalama.core import Widget
from graphalama.maths import Pos
from graphalama.shadow import NoShadow

from config import CONFIG
from constants import MAX_SPEED

ZERO_DIR = Pos(0, 0)
UP = Pos(0, -1)
DOWN = Pos(0, 1)
RIGHT = Pos(1, 0)
LEFT = Pos(-1, 0)


class Player(Widget):
    ACCEPT_KEYBOARD_INPUT = True

    def __init__(self, pos, path):
        super().__init__(pos=pos,
                         shape=(76, 70),
                         bg_color=ImageBrush(path, STRETCH),
                         shadow=NoShadow())
        self.opposite_image = pygame.transform.flip(self.bg_color.image, True, False)

        size = pygame.display.get_surface().get_size()
        self.min_x = 0
        self.min_y = 0
        self.max_x = size[0] - self.shape.width
        self.max_y = size[1] - self.shape.height
        self.score = 0
        self.focus = True

        self.speed = Pos(0, 0)
        self.acceleration = Pos(0, 0)
        self.going_left = id(self) % 2  # random enough so the initial orentation changes

        self.pos_hist = deque(maxlen=CONFIG.trail_length)

    def internal_logic(self):
        super().pre_render_update()

        # we use pressed to better handle LEFT + RIGHT or when we go out of the pause
        pressed = pygame.key.get_pressed()
        ax = ay = 0
        if pressed[pygame.K_LEFT]:
            ax -= 1
        if pressed[pygame.K_RIGHT]:
            ax += 1
        if pressed[pygame.K_UP]:
            ay -= 1
        if pressed[pygame.K_DOWN]:
            ay += 1
        self.acceleration = Pos(ax, ay)

        self.speed += self.acceleration
        # clamp the speed to MAX_SPEED
        if self.speed.norm() > MAX_SPEED:
            self.speed *= MAX_SPEED / self.speed.norm()

        # Brake
        if self.acceleration.x == 0:
            self.speed = Pos(self.speed.x / 2, self.speed.y)
        if self.acceleration.y == 0:
            self.speed = Pos(self.speed.x, self.speed.y / 2)

        self.pos += self.speed

        # Stay in the screen
        self.pos = (
            min(self.max_x, max(self.min_x, self.x)),
            min(self.max_y, max(self.min_y, self.y))
        )

        previous_direction = self.going_left
        if self.speed.x > 0:
            self.going_left = False
        elif self.speed.x < 0:
            self.going_left = True

        self.pos_hist.append((self.topleft, self.going_left))

        # updateing direction of the image if it changed
        if previous_direction != self.going_left:
            self.bg_color.image, self.opposite_image = self.opposite_image, self.bg_color.image
            self.invalidate_bg()

    def catch_coins(self, coins):
        """
        Remove the coins taht we collide in the list and update the score.

        The number of coins catched is returned.
        """

        collisions = self.absolute_rect.collidelistall([coin.absolute_rect for coin in coins])
        for i in reversed(collisions):
            coins.pop(i)
            self.score += 1
        return len(collisions)

    def render(self, display):
        for i, (pos, going_left) in enumerate(self.pos_hist):
            img = self.get_img_with_transparency(int(255 * i / CONFIG.trail_length), going_left)
            display.blit(img, pos)
        super().render(display)

    @lru_cache(maxsize=512)
    def get_img_with_transparency(self, transparency, going_left=True):
        img = self.background_image.copy()
        img.fill((255, 255, 255, transparency), None, pygame.BLEND_RGBA_MIN)

        # We need to account for the swapping of background
        if self.going_left != going_left:
            img = pygame.transform.flip(img, True, False)

        return img


