import pygame

from ..abstract_sprite import AbstractSprite
from ...resource_manager import ResourceManager


class HudElement(AbstractSprite):
    def __init__(self, level, sprite, coord, x_size, y_size):
        AbstractSprite.__init__(self)

        self.image = ResourceManager.load_sprite(level, sprite)
        curr_res = self.image.get_rect().size
        if x_size != curr_res[0]:
            if y_size <= 0:
                self.image = pygame.transform.scale(self.image, (x_size, int(float(x_size/curr_res[0])*curr_res[1])))
            else:
                self.image = pygame.transform.scale(self.image, (x_size, y_size))
        self.rect = coord

    def update(self, elapsed_time):
        pass

    def set_collision(self, coll):
        pass

    def _increase_position(self, increment):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
