from .character import Character
from ..util.log import Clog
from game import Configuration
import pygame

class Enemy(Character):
    def __init__(self, level, data, coord, speedx=10, speedy=20, invert=False):
        self.log = Clog(__name__)
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

    def move_cpu(self, player):
        pass
