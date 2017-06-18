import pygame
from graphalama import Borg
from params import Params
import math as m
borg_baby = Borg()

UP = [0, -8]
DOWN = [0, 8]
RIGHT = [8, 0]
LEFT = [-8, 0]
UP_LEFT = [-4*m.sqrt(2), -4*m.sqrt(2)]
UP_RIGHT = 0
DOWN_RIGHT = 0
DOWN_LEFT = 0


class Player:
    def __init__(self, x, y, screensize):
        self.x = x
        self.y = y
        self.max_x = screensize[0]-80
        self.max_y = screensize[1]-60
        self.score = 0
        self.image = pygame.transform.scale(pygame.image.load("assets/"
                                                              "players/" + Params.player), (80, 60)).convert_alpha()

    def update(self, inputs):
        if inputs['left arrow']['is pressed'] and inputs['up arrow']['is pressed']:
            self.move(UP_LEFT)
        elif inputs['up arrow']['is pressed']:
            self.move(UP)
        elif inputs['down arrow']['is pressed']:
            self.move(DOWN)
        elif inputs['right arrow']['is pressed']:
            self.move(RIGHT)
        elif inputs['left arrow']['is pressed']:
            self.move(LEFT)

    def render(self, display):
        display.blit(self.image, (self.x, self.y))

    def move(self, direction):
        if not ((self.x < 0 and direction == LEFT) or (self.y < 0 and direction == UP) or
                    (self.x > self.max_x and direction == RIGHT) or (self.y > self.max_y and direction == DOWN)):
            self.x += direction[0]
            self.y += direction[1]

    def quit(self):
        pass
