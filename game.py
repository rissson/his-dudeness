#!/bin/python

import pygame
from graphalama.app import Screen
from graphalama.colors import MultiGradient, ImageBrush
from graphalama.constants import (CENTER, RAINBOW, BOTTOMRIGHT, LLAMA,
                                  TRANSPARENT, FILL)
from graphalama.maths import Pos
from graphalama.widgets import Button, SimpleText

from coins import Coins
from config import bg_name_to_file, CONFIG, player_name_to_file
from constants import GAME_DURATION
from player import Player
from score import NewScoresScreen
from widgets import CountDown, PlayButton, QuitButton, MenuButton, Title


class PauseScreen(Screen):
    FPS = 30

    def __init__(self, app, game_screen_paused):
        self.paused_game = game_screen_paused  # Type: GameScreen

        size = Pos(app.display.get_size())
        widgets = [
            Title("Paused", size),
            PlayButton(self.paused_game.resume, size / 2 - (0, 65)),
            QuitButton(app, size / 2 + (0, 65), CENTER),
            MenuButton(app, size / 2, CENTER)
        ]
        super().__init__(app, widgets)

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused_game.resume()
        else:
            super().update(event)

    def draw_background(self, display):
        # We draw the game as it should be behind, but we never update it
        self.paused_game.render(display)


class GameScreen(Screen):
    def __init__(self, app):
        size = Pos(app.display.get_size())
        self.coins = Coins()
        self.player = Player(size / 2, player_name_to_file(CONFIG.player))
        self.score = SimpleText(text=self.player.score,
                                pos=size - (100, 30),
                                color=MultiGradient(*RAINBOW),
                                anchor=BOTTOMRIGHT)
        self.countdown = CountDown(GAME_DURATION, size / 2, anchor=CENTER)

        widgets = [
            self.countdown,
            Button(text="||",
                   function=self.pause,
                   pos=size - (50, 30),
                   color=LLAMA,
                   bg_color=TRANSPARENT,
                   anchor=BOTTOMRIGHT),
            self.coins,
            self.score,
            self.player,
        ]

        super().__init__(app, widgets, ImageBrush(bg_name_to_file(CONFIG.game_background), FILL))

    def pause(self, *args):
        """Pause the game by going into PauseScreen"""
        self.countdown.pause()
        self.app.set_temp_screen(lambda sm: PauseScreen(sm, self))

    def resume(self):
        """Resume the game after a PauseScreen."""

        self.app.set_temp_screen(self)
        self.countdown.resume()

    def update(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause()
        else:
            super().update(event)

    def internal_logic(self):
        self.player.internal_logic()
        self.coins.spawn(self.player.score)
        catch = self.player.catch_coins(self.coins)
        if catch:
            self.countdown.add(0.5 * catch)
            self.score.text = self.player.score
            self.score.invalidate()

        fps = round(self.app.clock.get_fps())
        if fps < 50:
            print(f"\033[31mLOW FPS: {fps}\033[m")

        if self.countdown.over:
            self.app.set_temp_screen(NewScoresScreen(self.app, self.player.score))
