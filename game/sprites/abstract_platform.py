import pygame
from .abstract_sprite import AbstractSprite

class AbstractPlatform(AbstractSprite):
    def __init__(self, rect):
        AbstractSprite.__init__(self)

        self.rect = rect
        self.set_global_position((rect.left, rect.bottom))
