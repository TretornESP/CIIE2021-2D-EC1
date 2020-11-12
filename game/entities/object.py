import pygame
from .abstract_platform import AbstractPlatform
from ..farm import Farm

class Object(AbstractPlatform):
    MASK = "mask"

    def __init__(self, level, kind, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0, 0)), invert)
        self._kind = kind

    def update(self, elapsed_time):
        AbstractPlatform.update(self, elapsed_time)
        player = Farm.get_player()
        if pygame.sprite.collide_rect(player, self):
            self.kill()
            self._collect(player)

    def _collect(self, player):
        if self._kind == Object.MASK:
            player.pick_mask()
