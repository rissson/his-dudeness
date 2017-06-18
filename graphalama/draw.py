# -*- coding: utf-8 -*-
import pygame
import pygame.gfxdraw

from graphalama.CONSTANTS import TRANSPARENT


def circle(area, pos, r, color):
    x = int(pos[0])
    y = int(pos[1])
    r = int(r)
    surf = pygame.Surface((2*r + 3, 2*r + 3), pygame.SRCALPHA)
    surf.fill(TRANSPARENT)
    pygame.gfxdraw.aacircle(surf, r + 1, r + 1, r-1, color)
    pygame.gfxdraw.filled_circle(surf, r + 1, r + 1, r-1, color)
    area.blit(surf, (x-r - 1, y - r - 1))


__all__ = ['circle']