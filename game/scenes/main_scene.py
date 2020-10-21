import pygame
from .abstract_horizontal_scene import AbstractHorizontalScene
from game.sprites import Platform, Player
from .backgrounds import MainBackground
from game import Configuration
from pygame.locals import *

class MainScene(AbstractHorizontalScene):
    def __init__(self, director):
        AbstractHorizontalScene.__init__(self, director)

        resolution = Configuration().get_resolution()

        self._player = Player()
        self._background = MainBackground()

        # platforms
        platform = Platform(pygame.Rect((0, resolution[1] - 20), (resolution[0], 20)))
        self._platforms = pygame.sprite.Group(platform)

        # sprites
        self._dynamic_sprites = pygame.sprite.Group(self._player)
        self._static_sprites = pygame.sprite.Group(platform)

        # delegate collision handling
        self._player.set_platform_group(self._platforms)
