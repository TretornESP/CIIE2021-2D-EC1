#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
import pygame

class Object(AbstractPlatform):
    def __init__(self, level, kind, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0,0)), invert)
        self._kind = kind
