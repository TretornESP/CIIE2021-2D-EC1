from .abstract_platform import AbstractPlatform
from game import ResourceManager
import pygame
class Platform(AbstractPlatform):
    def __init__(self, level, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0,0)), invert)
