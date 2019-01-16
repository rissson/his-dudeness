import os
import re
from functools import partial

import configlib

from constants import BACKGROUND_FOLDER, PLAYER_FOLDER

BG_REGEX = re.compile(r'background_(.*)\.jpg')
PLAYER_REGEX = re.compile(r'(.*).png')


def get_available(what, where):
    names = []

    for file in os.listdir(where):
        name = os.path.basename(file)
        match = what.match(name)
        if match:
            names.append(match.group(1).title())

    return sorted(names)


get_available_bg = partial(get_available, BG_REGEX, BACKGROUND_FOLDER)
get_available_players = partial(get_available, PLAYER_REGEX, PLAYER_FOLDER)


def bg_name_to_file(name):
    """Get the filename of the given background."""
    return os.path.join(BACKGROUND_FOLDER, f'background_{name.lower()}.jpg')


def player_name_to_file(name):
    return os.path.join(PLAYER_FOLDER, f'{name.lower()}.png')


class DudeConfig(configlib.Config):
    __config_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/config.json'))

    game_background = 'Walter'

    trail_length = 4

    player = 'His-Dudeness'


CONFIG = DudeConfig()

if __name__ == '__main__':
    configlib.update_config(DudeConfig)
