from graphalama.app import Screen
from graphalama.colors import ImageBrush
from graphalama.constants import FILL, BOTTOMRIGHT, CENTER
from graphalama.core import Widget
from graphalama.maths import Pos
from graphalama.shapes import RoundedRect

from config import CONFIG, get_available_bg, bg_name_to_file, get_available_players
from constants import DARK
from widgets import MenuButton, Title, SettingsCarousel, SettingsLabel


class SettingsScreen(Screen):
    FPS = 30

    def __init__(self, app):
        size = Pos(app.display.get_size())
        def pos(i):
            return size.x / 2, 60*(i + 5)

        bg_carousel = SettingsCarousel(get_available_bg(), self.set_bg, pos(1))

        trails = [0] + [2**i for i in range(10)]
        trail_carousel = SettingsCarousel(trails, self.set_trail, pos(2))

        player_carousel = SettingsCarousel(get_available_players(), self.set_player, pos(3))

        widgets = [
            Widget(pos(2), RoundedRect((650, 60*4), percent=False), bg_color=DARK, anchor=CENTER),
            Title("Settings", size),
            SettingsLabel("Background", pos(1)),
            bg_carousel,
            SettingsLabel("Trail", pos(2)),
            trail_carousel,
            SettingsLabel("Player", pos(3)),
            player_carousel,
            MenuButton(app, size - (30, 30), BOTTOMRIGHT),
        ]

        super().__init__(app, widgets)

        # Setting the current state
        bg_carousel.option_index = bg_carousel.options.index(CONFIG.game_background)
        trail_carousel.option_index = trail_carousel.options.index(CONFIG.trail_length)
        player_carousel.option_index = player_carousel.options.index(CONFIG.player)

    def set_bg(self, name):
        """Set the game background."""

        self.bg_color = ImageBrush(bg_name_to_file(name), FILL)
        CONFIG.game_background = name

    def set_trail(self, length):
        CONFIG.trail_length = length

    def set_player(self, player):
        CONFIG.player = player