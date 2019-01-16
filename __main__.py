#!/bin/python

import pygame; pygame.init()

from graphalama.app import App

from game import GameScreen
from menu import MenuScreen
from settings import SettingsScreen
from constants import MENU, GAME, SETTINGS
from config import CONFIG


def main():
    App({
        MENU: MenuScreen,
        GAME: GameScreen,
        SETTINGS: SettingsScreen
    }, MENU).run()


if __name__ == "__main__":
    # ensure it saves
    with CONFIG:
        main()
