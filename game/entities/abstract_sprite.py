import pygame
import uuid
from game import Configuration

class AbstractSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self._position = (0, 0)
        self._velocity = (0, 0)
        self._scroll = (0, 0)

        self._collides = True
        self._uuid = uuid.uuid1()

    def set_global_position(self, position):
        self._position = position
        self.rect.left = position[0] - self._scroll[0]
        self.rect.bottom = position[1] - self._scroll[1]

    def get_global_position(self):
        return self.rect

    def get_absolute_position(self):
        return self._position

    def set_position(self, scroll):
        (scroll_x, scroll_y) = scroll
        (pos_x, pos_y) = self._position

        self.rect.left = pos_x - scroll_x
        self.rect.bottom = pos_y - scroll_y

        self._scroll = scroll

    def set_collision(self, coll):
        self._collides = coll

    def update(self, elapsed_time):
        increment = Configuration().get_pixels(self._velocity)
        new_x = increment[0] * elapsed_time
        new_y = increment[1] * elapsed_time
        self._increase_position((new_x, new_y))

    def _increase_position(self, increment):
        new_x = self._position[0] + increment[0]
        new_y = self._position[1] + increment[1]
        self.set_global_position((new_x, new_y))

    def get_uuid(self):
        return self._uuid

    def is_same(self, other):
        return (self._uuid == other.get_uuid)
