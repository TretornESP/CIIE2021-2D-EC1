from .character import Character
from ..util.log import Clog
from game import Configuration
import pygame

class Enemy(Character):
    ROTATOR = [Character.LEFT, Character.RIGHT]
    X_COLLISION = 0
    Y_COLLISION = 1
    NO_COLLISION = 2

    def __init__(self, level, data, coord, speedx = 10, speedy = 20, invert = False):
        self.log = Clog(__name__)
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self._kind = data
        self._dir = 0

    def move(self, keys_pressed, up, down, left, right):
        Character.move(self, (Enemy.ROTATOR[self._dir],0))

    def update(self, elapsed_time):
        res = Configuration().get_resolution()
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = Configuration().get_pixels((vel_x, vel_y))

        # update horizontal movement
        if self._movement_x == Character.LEFT:
            self._velocity = (-vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.RIGHT:
            self._velocity = (vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.STILL and self._movement_y == Character.STILL:
            self._velocity = (0, self._velocity[1])
        if self._movement_y == Character.UP and self._velocity[1] == 0:
            self._velocity = (self._velocity[0], -vel_py * elapsed_time)
        self._update_sprite()

        # check horizontal collisions
        self._increase_position((self._velocity[0], 0))
        platform = pygame.sprite.spritecollideany(self, self._platforms)
        if platform != None and platform._collides and self.rect.bottom > platform.rect.top + 1:
            print("Enemy collided with h platform")
            self._dir = not self._dir
            if self._velocity[0] > 0:
                self.set_global_position((platform._position[0] - self.rect.width, self._position[1]))
            elif self._velocity[0] < 0:
                self.set_global_position((platform._position[0] + platform.rect.width, self._position[1]))

        # check vertical collisions
        self._increase_position((0, self._velocity[1]))
        platform = pygame.sprite.spritecollideany(self, self._platforms)
        if platform != None and platform._collides:
            print("Enemy collided with yplatform")
            if self._velocity[1] > 0:
                self._velocity = (self._velocity[0], 0)
                self.set_global_position((self._position[0], platform._position[1] - platform.rect.height + 1))
            elif self._velocity[1] < 0:
                self._velocity = (self._velocity[0], 0.04 * vel_py * elapsed_time)
                self.set_global_position((self._position[0], platform._position[1] + self.rect.height))
        else:
            # check y axis boundaries
            if self.rect.bottom >= res[1]:
                self._velocity = (self._velocity[0], 0)
                self.set_global_position((self._position[0], res[1]))
            else:
                self._velocity = (self._velocity[0], self._velocity[1] + 0.08 * vel_py * elapsed_time)
