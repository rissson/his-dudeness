from graphalama.app import Screen
from graphalama.colors import ImageBrush
from graphalama.constants import FILL

from constants import GAME
from widgets import PlayButton, SettingsButton, QuitButton, Title


class MenuScreen(Screen):
    """The Menu screen"""

    FPS = 30

    def __init__(self, app):
        size = app.display.get_size()
        widgets = [
            Title("His Dudeness", size),
            PlayButton(lambda: app.set_screen(GAME), (size[0] // 2, size[1] // 2 - 65)),
            SettingsButton(app, (size[0] // 2, size[1] // 2)),
            QuitButton(app, (size[0] // 2, size[1] // 2 + 65)),
        ]

        name = 'color'
        super().__init__(app, widgets, ImageBrush(f"assets/backgrounds/background_{name}.jpg", FILL))

