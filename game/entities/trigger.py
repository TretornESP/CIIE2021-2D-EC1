#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
import pygame

class Trigger(AbstractPlatform):
    def __init__(self, level, id, indic, coord, size, invert):
        AbstractPlatform.__init__(self, level, None, True, pygame.Rect(coord, size), invert)
        self._id = id
