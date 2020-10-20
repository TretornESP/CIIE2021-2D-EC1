import pygame
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

    def update(self, elapsed_time):
        next_orientation = None

        if self._movement in [Character.LEFT, Character.UP_LEFT, Character.DOWN_LEFT]:
            next_orientation = Character.LEFT
        elif self._movement in [Character.RIGHT, Character.UP_RIGHT, Character.DOWN_RIGHT]:
            next_orientation = Character.RIGHT

        if next_orientation != None and next_orientation != self._orientation:
            self._update_image()
            self._orientation = next_orientation

        increase = Configuration().get_pixels(self._velocity)
        if self._movement == Character.RIGHT:
            inc_x = increase[0] * self._velocity[0]
            self._increase_position((inc_x, 0))
        elif self._movement == Character.LEFT:
            inc_x = increase[0] * self._velocity[0]
            self._increase_position((-inc_x, 0))

    def move(self, direction):
        self._movement = direction

    def _update_image(self):
        self.image = pygame.transform.flip(self.image, 1, 0)
