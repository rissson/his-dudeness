import time
import pickle
from graphalama.buttons import StatesButton
from graphalama.CONSTANTS import *
from graphalama.color import get_rainbow


class ParamsScreen:
    def __init__(self):
        self.timestamp = time.time()
        background_states = [{'txt': 'Walter', 'clr': RED, 'value': 'background_walter.jpg'},
                             {'txt': 'Astronaut', 'clr': GREY_BLUE, 'value': 'background_astronaut.jpg'},
                             {'txt': 'Autumn', 'clr': ORANGE, 'value': 'background_autumn.jpg'},
                             {'txt': 'Over the clouds', 'clr': L_YELLOW, 'value': 'background_clouds.jpg'},
                             {'txt': 'Lake & Mountains', 'clr': L_BLUE, 'value': 'background_mountains.jpg'},
                             {'txt': 'On / Off', 'clr': DARK_GREEN, 'value': 'background_on.jpg'},
                             {'txt': 'Rainbow', 'clr': get_rainbow(), 'value': 'background_rainbow.jpg'},
                             {'txt': 'Relax', 'clr': DARK_RED, 'value': 'background_relax.jpg'},
                             {'txt': 'Sexy', 'clr': get_rainbow(1), 'value': 'background_sexy.jpg'},
                             {'txt': 'Skyscrapers', 'clr': BLUE, 'value': 'background_skyscrapers.jpg'}]
        self.background_button = StatesButton(0.42, 0.3, 0.15, 'Background', background_states, WHITE + (128,))
        self.background_button.go_to_value(Params.background)  # we go at the saved value

        player_states = [{'txt': 'Platypus', 'clr': BLUE, 'value': 'his-dudeness.png'},
                         {'txt': 'Llama', 'clr': get_rainbow(1), 'value': 'llama.png'}]
        self.player_button = StatesButton(0.42, 0.6, 0.15, 'Character', player_states, WHITE + (128,), hint='Reboot'
                                                                                                            ' needed')
        self.player_button.go_to_value(Params.player)  # we go at the saved value

    def update(self, inputs):
        Params.background = self.background_button.update(inputs)
        Params.player = self.player_button.update(inputs)
        if time.time() >= self.timestamp + 600:
            Params.save()
            self.timestamp = time.time()

    def render(self, display):
        self.player_button.render()
        self.background_button.render()

        display.blit(self.player_button, self.player_button.real_topleft)
        display.blit(self.background_button, self.background_button.real_topleft)


class Params:

    all_params = dict()
    background = 'background_walter.jpg'
    player = 'his-dudeness.png'

    @classmethod
    def save(cls):
        with open('assets/params.set', 'wb') as file:
            cls.all_params['background'] = cls.background
            cls.all_params['player'] = cls.player
            pickle.dump(cls.all_params, file)

    @classmethod
    def load(cls):
        try:
            with open('assets/params.set', 'rb') as file:
                cls.all_params = pickle.load(file)
                cls.background = cls.all_params['background']
                cls.player = cls.all_params['player']

        except KeyError:  # TODO : add other errors
            print('KeyError in params.set : Loading default params.')
            # keep the default
        except FileNotFoundError:
            print('FileNotFoundError for params.set : Loading default params.')
