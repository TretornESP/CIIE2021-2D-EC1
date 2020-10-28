from .character import Character
from game import Configuration
from ..util.log import Clog
import pygame

class Player(Character):

    INVULNERABILITY_LAPSE = 2

    def __init__(self, level, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self.log = Clog(__name__)

        self._hp = 3
        self._last_hit = 0

    def hit(self):
        self._hp = self._hp - 1
        #TODO: Update animation as untouchable

    def update(self, elapsed_time):
        res = Configuration().get_resolution()
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = Configuration().get_pixels((vel_x, vel_y))
        self._last_hit = self._last_hit + elapsed_time

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
            if self._velocity[0] > 0:
                self.set_global_position((platform._position[0] - self.rect.width, self._position[1]))
            elif self._velocity[0] < 0:
                self.set_global_position((platform._position[0] + platform.rect.width, self._position[1]))

        if (self._enemies != None):
            enemy = pygame.sprite.spritecollideany(self, self._enemies) #TODO
            if (enemy != None):
                #self.log.debug("Elapsed: "+str(self._last_hit))
                if self._last_hit > Player.INVULNERABILITY_LAPSE:
                    self.log.debug("Player hit!")
                    self.hit()
                    self._last_hit = 0

        if (self._items != None):
            item = pygame.sprite.spritecollideany(self, self._items) #TODO
            if (item != None):
                self._items.remove(item)
                item.collect()

        if (self._triggers != None):
            trigger = pygame.sprite.spritecollideany(self, self._triggers) #TODO
            if (trigger != None):
                 trigger.event()
                 self._triggers.remove(trigger)

        # check vertical collisions
        self._increase_position((0, self._velocity[1]))
        platform = pygame.sprite.spritecollideany(self, self._platforms)
        if platform != None and platform._collides:
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

        if (self._enemies != None):
            enemy = pygame.sprite.spritecollideany(self, self._enemies) #TODO
            if (enemy != None):
                #self.log.debug("Colliding with enemy")
                if (elapsed_time - self._last_hit) > Player.INVULNERABILITY_LAPSE:
                    self.log.debug("Player hit!")
                    self._hp = self._hp - 1
                    self._last_hit = elapsed_time

        if (self._items != None):
            item = pygame.sprite.spritecollideany(self, self._items) #TODO
            if (item != None):
                self._items.remove(item)
                item.collect()

        if (self._triggers != None):
            trigger = pygame.sprite.spritecollideany(self, self._triggers) #TODO
            if (trigger != None):
                 trigger.event()
                 self._triggers.remove(trigger)

    def move(self, keys_pressed, up, down, left, right):
        if keys_pressed[up]:
            y = Character.UP
        elif keys_pressed[down]:
            y = Character.DOWN
        else:
            y = Character.STILL

        if keys_pressed[left]:
            x = Character.LEFT
        elif keys_pressed[right]:
            x = Character.RIGHT
        else:
            x = Character.STILL

        Character.move(self, (x,y))
