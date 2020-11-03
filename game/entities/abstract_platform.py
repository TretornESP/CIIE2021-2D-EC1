import pygame
from .abstract_sprite import AbstractSprite
from ..resource_manager import ResourceManager

class AbstractPlatform(AbstractSprite):
    ACTIVE = (255, 0, 255, 255)
    RESIDE = (0, 255, 0, 255)
    ACTIVE_A = (255, 0, 255, 0)
    RESIDE_A = (0, 255, 0, 0)

    def __init__(self, level, sprite, collision, coord, invert, invisible=False):
        AbstractSprite.__init__(self)
        self._invisible = invisible

        if sprite == None:
            self.image = pygame.Surface((coord.width, coord.height), pygame.SRCALPHA)
            if not self._invisible:
                self.image.fill(self.ACTIVE)
            self.rect = coord
        else:
            self.image = ResourceManager.load_sprite(level, sprite)
            self.rect = self.image.get_rect()

        if (invert):
            self.image = pygame.transform.flip(self.image, 1, 0)

        self.set_global_position(coord)
        self.set_collision(collision)

    def event_deactivate(self):
        self._active = AbstractPlatform.RESIDE
        if not self._invisible:
            self.image.fill(self.RESIDE)