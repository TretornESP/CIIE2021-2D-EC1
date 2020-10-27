import pygame
from .abstract_horizontal_scene import AbstractHorizontalScene
from game.entities import Platform, Player, Enemy
from .backgrounds import MainBackground
from game import Configuration
from pygame.locals import *

class MainScene(AbstractHorizontalScene):
    def __init__(self, director):
        AbstractHorizontalScene.__init__(self, director)

        resolution = Configuration().get_resolution()
        self._scroll_size = 2000

        self._player = Player()
        self._background = MainBackground()
        self._enemies = []
        for i in range(0, 10):
            self._enemies.append(Enemy((100+i*10, 300), 0, 0))

        # platforms
        platform = Platform("Level0", None, None, pygame.Rect((0, resolution[1] - 20), (self._scroll_size, 20)), False)
        self._platforms = pygame.sprite.Group(platform)

        # sprites
        self._dynamic_sprites = pygame.sprite.Group(self._player)
        self._dynamic_sprites.add(self._enemies)
        self._static_sprites = pygame.sprite.Group(platform)

        # delegate collision handling
        self._player.set_platform_group(self._platforms)
        for enemy in self._enemies:
            enemy.set_platform_group(self._platforms)
