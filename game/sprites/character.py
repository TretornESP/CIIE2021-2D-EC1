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

    def __init__(self, image, position, velocity_x, velocity_y):
        AbstractSprite.__init__(self)

        self.image = ResourceManager.load_image(image)
        self.rect = self.image.get_rect()

        self.set_global_position(position)

        self._velocity = (0, 0)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

        self._movement = Character.STILL
        self._orientation = Character.RIGHT

        self._platforms = None

    def update(self, elapsed_time):
        self._update_orientation()
        self._update_movement(elapsed_time)
        self._update_collisions(elapsed_time)

    def move(self, direction):
        self._movement = direction

    def set_platform_group(self, platforms):
        self._platforms = platforms

    def _update_image(self):
        self.image = pygame.transform.flip(self.image, 1, 0)

    def _update_orientation(self):
        next_orientation = None

        if self._movement == Character.LEFT:
            next_orientation = Character.LEFT
        elif self._movement == Character.RIGHT:
            next_orientation = Character.RIGHT

        if next_orientation != None and next_orientation != self._orientation:
            self._update_image()
            self._orientation = next_orientation

    def _update_movement(self, elapsed_time):
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = Configuration().get_pixels((vel_x, vel_y))

        if self._movement == Character.LEFT:
            self._velocity = (-vel_px * elapsed_time, self._velocity[1])
        if self._movement == Character.RIGHT:
            self._velocity = (vel_px * elapsed_time, self._velocity[1])
        if self._movement == Character.STILL:
            self._velocity = (0, self._velocity[1])
        if self._velocity[1] == 0 and self._movement == Character.UP:
            self._velocity = (self._velocity[0], -vel_py * elapsed_time)

        self._increase_position(self._velocity)

    def _update_collisions(self, elapsed_time):
        platform = pygame.sprite.spritecollideany(self, self._platforms)

        if platform != None:
            self.set_global_position((self._position[0], platform._position[1] - platform.rect.height))
            self._velocity = (self._velocity[0], 0)
        else:
            _, vel_py = Configuration().get_pixels((0, self._velocity_y))
            self._velocity = (self._velocity[0], self._velocity[1] + 0.07 * vel_py * elapsed_time)
