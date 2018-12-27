import pygame
from graphalama import Borg
from threading import Timer, Thread
import random
import pickle
import time
borg_baby = Borg()


class Coins:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("assets/coin.png"), (30, 40)).convert_alpha()
        self.coins_list = []
        borg_baby.score = 0
        self.all = dict()
        self.all['coins_list'] = self.coins_list
        self.all['collected'] = borg_baby.score
        self.timestamp = time.time()
        self.load()

    def load(self):
        try:
            with open('save/score.set', 'rb') as file:
                self.all = pickle.load(file)
                self.coins_list = self.all['coins_list']
                borg_baby.score = self.all['collected']

        except KeyError:  # TODO : add other errors
            print('KeyError in save/score.set : Loading default scores.')
        except FileNotFoundError:
            print('FileNotFoundError for save/score.set : Loading default scores.')

    def update(self, x, y):
        for coin in self.coins_list:
            if abs((coin.x + 15) - x) < 40 and abs((coin.y + 20) - y) < 30:
                self.coins_list.remove(coin)
                borg_baby.score += 1
        if time.time() >= self.timestamp + 300:
            t = Thread(target=self.save)
            t.daemon = True
            t.start()
            self.timestamp = time.time()

    def render(self, display):
        for coin in self.coins_list:
            display.blit(self.image, (coin.x, coin.y))

    def coins_timer(self):
        spawn_speed = 5 - (0.05 * borg_baby.score)
        if spawn_speed < 0.5:
            spawn_speed = 0.5
        t = Timer(spawn_speed, self.coins_timer)
        t.setDaemon(t)
        t.start()
        print("coin spawn")
        self.coins_list.append(Coin(borg_baby.SCREEN_SIZE))

    def save(self):
        with open('save/score.set', 'wb') as file:
            self.all['coins_list'] = self.coins_list
            self.all['collected'] = borg_baby.score
            pickle.dump(self.all, file)

    def quit(self):
        self.save()


class Coin:
    def __init__(self, screensize):
        self.x = random.randrange(0, (screensize[0] - 30))
        self.y = random.randrange(0, (screensize[1] - 40))
