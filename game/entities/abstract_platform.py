import pygame
from .abstract_sprite import AbstractSprite
from ..resource_manager import ResourceManager

class AbstractPlatform(AbstractSprite):
    def __init__(self, level, sprite, collision, coord, invert):
        AbstractSprite.__init__(self)

        if sprite == None:
            self.image = pygame.Surface((150, 10))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect()
        else:
            self.image = ResourceManager.load_sprite(level, sprite)
            self.rect = self.image.get_rect()

        if (invert):
            self.image = pygame.transform.flip(self.image, 1, 0)

        self.set_global_position(coord)
        self.set_collision(collision)
