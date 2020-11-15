import pygame

from .character import Character
from game import ResourceManager, Farm
from .enemy import Enemy
from ..player_repository import PlayerRepository


class Spikes(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        player = Farm.get_player()

        if pygame.sprite.collide_rect(self, player):
            player.insta_kill()

    def move_cpu(self):
        pass
