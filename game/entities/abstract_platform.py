import pygame
from .abstract_sprite import AbstractSprite
from ..resource_manager import ResourceManager

class AbstractPlatform(AbstractSprite):
    def __init__(self, level, sprite, collision, coord, invert):
        AbstractSprite.__init__(self)

        if sprite == None:
            self.image = pygame.Rect(coord)
            self.rect = self.image
        else:
            self.image = ResourceManager.load_sprite(level, sprite)
            self.rect = self.image.get_rect() #No estoy nada seguro de esto

        if (invert):
            self.image = pygame.transform.flip(self.image, 1, 0)


        self.set_global_position((coord.left, coord.bottom))
        self.set_collision(collision)
