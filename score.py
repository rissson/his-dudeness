from graphalama.app import Screen
from graphalama.colors import MultiGradient, ImageBrush
from graphalama.constants import RAINBOW, TOP, BOTTOMRIGHT, FILL
from graphalama.font import default_font
from graphalama.maths import Pos
from graphalama.shapes import RoundedRect
from graphalama.widgets import WidgetList, SimpleText

from config import bg_name_to_file, CONFIG
from widgets import MenuButton


class NewScoresScreen(Screen):
    def __init__(self, app, score):
        self.score = score
        size = Pos(app.display.get_size())

        self.score_text = SimpleText(f"Score: {score}", (size.x / 2, 30), RoundedRect(border=1, rounding=100, padding=5),
                                     bg_color=(240, 240, 240, 120), border_color=MultiGradient(*RAINBOW),
                                     font=default_font(80), anchor=TOP)
        widgets = WidgetList([
            self.score_text,
            MenuButton(app, size - (30, 30), BOTTOMRIGHT)
        ])

        super().__init__(app, widgets, ImageBrush(bg_name_to_file(CONFIG.game_background), FILL))
