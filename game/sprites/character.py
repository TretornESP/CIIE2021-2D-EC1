import pygame
import math
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite

class Character(AbstractSprite):
    STILL = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

    def __init__(self, image, position, velocity):
        AbstractSprite.__init__(self)

        self.image = ResourceManager.load_image(image)
        self.rect = self.image.get_rect()

        self.set_global_position(position)
        self._velocity = velocity

        self._movement = Character.STILL
        self._orientation = Character.RIGHT

        self._platforms = None

    def update(self, elapsed_time):
        self._update_orientation()
        self._update_movement(elapsed_time)
        self._update_collisions()

    def move(self, direction):
        self._movement = direction

    def set_platform_group(self, platforms):
        self._platforms = platforms

    def _update_image(self):
        self.image = pygame.transform.flip(self.image, 1, 0)

    def _update_orientation(self):
        next_orientation = None

        if self._movement in [Character.LEFT, Character.UP_LEFT, Character.DOWN_LEFT]:
            next_orientation = Character.LEFT
        elif self._movement in [Character.RIGHT, Character.UP_RIGHT, Character.DOWN_RIGHT]:
            next_orientation = Character.RIGHT

        if next_orientation != None and next_orientation != self._orientation:
            self._update_image()
            self._orientation = next_orientation

    def _update_movement(self, elapsed_time):
        increase = Configuration().get_pixels(self._velocity)

        if self._movement == Character.UP:
            inc_y = -increase[1] * elapsed_time
            self._increase_position((0, inc_y))

        if self._movement == Character.RIGHT:
            inc_x = increase[0] * elapsed_time
            self._increase_position((inc_x, 0))

        if self._movement == Character.LEFT:
            inc_x = -increase[0] * elapsed_time
            self._increase_position((inc_x, 0))

    def _update_collisions(self):
        platform = pygame.sprite.spritecollideany(self, self._platforms)

        if platform != None and platform.rect.bottom > self.rect.bottom:
            self.set_global_position((self._position[0], platform._position[1] - platform.rect.height))
