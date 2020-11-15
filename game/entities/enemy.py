import pygame
from .character import Character
from ..farm import Farm

class Enemy(Character):
    def __init__(self, level, data, coord, speedx=10, speedy=20, invert=False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        player = Farm.get_player()

        if pygame.sprite.collide_rect(self, player):
            if player.is_parrying():
                self.kill()
                player.end_parry()
            elif not player.is_invulnerable():
                player.hit()

    def move_cpu(self):
        pass
