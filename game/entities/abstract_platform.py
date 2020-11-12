import pygame
from .abstract_sprite import AbstractSprite
from ..resource_manager import ResourceManager


class AbstractPlatform(AbstractSprite):
    ACTIVE = (255, 0, 255, 255)
    RESIDE = (0, 255, 0, 255)
    ACTIVE_A = (255, 0, 255, 0)
    RESIDE_A = (0, 255, 0, 0)

    def __init__(self, level, sprite, collision, coord, invert, invisible=False, scale=None):
        AbstractSprite.__init__(self)
        self._invisible = invisible

        if sprite is None:
            self.image = pygame.Surface((coord.width, coord.height), pygame.SRCALPHA)
            if not self._invisible:
                self.image.fill(self.ACTIVE)
            coord.top -= coord.height #Pygame defines rect as: left, top, w, h. We want left, bottom, w, h
            self.rect = coord
            pos = (coord.left, coord.bottom)
        else:
            self.image = ResourceManager.load_sprite(sprite, level)
            if scale is not None:
                (_, _, x_size, y_size) = self.image.get_rect()
                x_size = int(float(x_size * scale))
                y_size = int(float(y_size * scale))
                self.image = pygame.transform.scale(self.image, (x_size, y_size))
            self.rect = self.image.get_rect()
            pos = coord

        if invert:
            self.image = pygame.transform.flip(self.image, True, False)

        self.set_global_position(pos)
        self.set_collision(collision)
