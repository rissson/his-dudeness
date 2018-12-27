from graphalama import Borg
from graphalama import Inputs, screen
from graphalama.fonts import Font, Calibri
from graphalama.text import Text
from graphalama.CONSTANTS import *
import pygame
from player import Player
from coins import Coins
from graphalama.color import get_rainbow
from params import ParamsScreen, Params
borg_baby = Borg()

__version__ = '0.3'
borg_baby.version = __version__


def main():
    pygame.init()
    pygame.key.set_repeat(50, 5)
    Params.load()

    borg_baby.display = screen.new_display("His Dudeness", full_screen=True, icon_path="assets/his-dudeness.png")
    screen.wait_party(borg_baby.display)
    borg_baby.inputs = Inputs()

    fps = 30
    clock = pygame.time.Clock()

    initial_screen = True

    in_game = False
    his_dudeness = Player(50, 50, borg_baby.SCREEN_SIZE)
    coins = Coins()

    params_screen = ParamsScreen()
    params = False
    background = pygame.transform.scale(pygame.image.load("assets/backgrounds/" + Params.background).convert(),
                                        borg_baby.SCREEN_SIZE)

    while not (borg_baby.inputs['alt']['is pressed'] and borg_baby.inputs['F4']['is pressed'])\
            and not borg_baby.inputs['close']['is pressed'] or borg_baby.inputs['escape']['is pressed']:
        borg_baby.display.blit(background, (0, 0))

        screen.resize(borg_baby.display, borg_baby.inputs)
        borg_baby.inputs.update()
        if initial_screen:
            play_button = Text("Play", (0.4, 0.4, 0.2, 0.1, (0, 120, 255, 128), ROUNDED, 0.2),
                               Font(Calibri, 1), WHITE, ('cc', 0, 0))
            play_button.render()
            borg_baby.display.blit(play_button, play_button.real_topleft)

            if play_button.mouse_click_area(1):
                initial_screen = False
                in_game = True
                coins.coins_timer()
                params = False

        elif in_game:
            his_dudeness.update(borg_baby.inputs)
            coins.update((his_dudeness.x + 40), (his_dudeness.y + 30))
            his_dudeness.render(borg_baby.display)
            coins.render(borg_baby.display)
        elif params:
            params_screen.render(borg_baby.display)
            background = pygame.transform.scale(pygame.image.load("assets/backgrounds/" + Params.background).convert(),
                                                borg_baby.SCREEN_SIZE)

            if borg_baby.inputs['escape']['is pressed']:
                initial_screen = True
                in_game = False
                params = False

        params_screen.update(borg_baby.inputs)

        score = Text("Coins : {}".format(borg_baby.score), (0.65, 0.01, 0.2, 0.05, (0, 0, 0, 128), ROUNDED, 0.2),
                     Font(Calibri, 1), get_rainbow(), ('tl', 0, 0))
        score.render()
        borg_baby.display.blit(score, score.real_topleft)

        settings_button = Text("Settings", (0.87, 0.01, 0.1, 0.05, (0, 120, 255, 128), ROUNDED, 0.2),
                               Font(Calibri, 0.8), WHITE, anchor=('cc', 0, 0))
        settings_button.render()
        borg_baby.display.blit(settings_button, settings_button.real_topleft)

        if settings_button.mouse_click_area(1):
            initial_screen = False
            in_game = False
            params = True

        clock.tick(fps)
        pygame.display.flip()

    his_dudeness.quit()
    coins.quit()
    Params.save()


if __name__ == "__main__":
    main()
