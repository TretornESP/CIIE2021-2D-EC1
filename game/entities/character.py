import pygame
import math
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite
from ..util.log import Clog

class Character(AbstractSprite):
    STILL = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __init__(self, level, data, position, invert, velocity_x = 0, velocity_y = 0):
        AbstractSprite.__init__(self)
        self._log = Clog(__name__)
        self._coords = ResourceManager.load_coords(level, data)
        self._sheet = ResourceManager.load_sheet(level, data, colorkey=-1)

        if (invert):
            self._sheet = pygame.transform.flip(self._sheet, 1, 0) #Tal vez invierta controles??

        self._left = False #Comentario de arriba
        self._animation_idx = 0
        self._animation_dur = -1

        self._set_sprite("STILL")
        self.rect = self.image.get_rect()

        self.set_global_position(position)

        self._velocity = (0, 0)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

        self._movement = Character.STILL
        self._orientation = Character.RIGHT

        _, self._limit_y = Configuration().get_resolution()

        self._platforms = None
        self._enemies = None
        self._items = None
        self._triggers = None

    def update(self, elapsed_time):
        res = Configuration().get_resolution()
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = Configuration().get_pixels((vel_x, vel_y))

        # update horizontal movement
        if self._movement == Character.LEFT:
            self._velocity = (-vel_px * elapsed_time, self._velocity[1])
        if self._movement == Character.RIGHT:
            self._velocity = (vel_px * elapsed_time, self._velocity[1])
        if self._movement == Character.STILL:
            self._velocity = (0, self._velocity[1])
        if self._movement == Character.UP and self._velocity[1] == 0:
            self._velocity = (self._velocity[0], -vel_py * elapsed_time)
        self._update_sprite()

        self._increase_position(self._velocity)

    def _is_on_ground(self, offset=0):
        return self.rect.bottom < (self._limit_y - offset - 20)

    def _update_collisions(self, elapsed_time):
        has_collided = False
        (xvel, yvel) = self._velocity
        on_ground =  self._is_on_ground()

        if (self._platforms != None):
            platform = pygame.sprite.spritecollideany(self, self._platforms)
            if (platform != None and platform._collides): #No tengo claro esto
                self._log.debug("XVEL: " + str(xvel) + " YVEL: " + str(yvel))
                if (xvel < 0):
                    self.set_global_position((platform._position[0] + platform.rect.width, self._position[1]))
                if (xvel > 0):
                    self.set_global_position((platform._position[0] - self.rect.width, self._position[1]))
                if (yvel > 0):
                    self.set_global_position((self._position[0], platform._position[1] - platform.rect.height))
                if (yvel < 0):
                    self.set_global_position((self._position[0], platform._position[1]))

                has_collided = True

        if (self._enemies != None):
            enemy = pygame.sprite.spritecollideany(self, self._enemies) #TODO
        if (self._items != None):
            item = pygame.sprite.spritecollideany(self, self._items) #TODO
        if (self._triggers != None):
            trigger = pygame.sprite.spritecollideany(self, self._triggers) #TODO
            if (trigger != None):
                 trigger.event()
                 self._triggers.remove(trigger)

        if not has_collided:
            _, vel_py = Configuration().get_pixels((0, self._velocity_y))
            #self._log.debug("limit_y: "+ str(limit_y) + " bottom: " + str(self.rect.bottom))

            vely = (self._velocity[1] + 0.08 * vel_py * elapsed_time) * on_ground
            self._velocity = (self._velocity[0], vely)


    def _update_sprite(self):
        if self._velocity[0] < 0:
            self._left = True
        elif self._velocity[0] > 0:
            self._left = False

        if self._velocity[1] != 0:
            self._set_sprite("MOV_Y")
        elif self._velocity[0] == 0:
            self._set_sprite("STILL")
        else:
            self._set_sprite("MOV_X")

    def move(self, direction):
        self._movement = direction

    def set_platform_group(self, platforms):
        self._platforms = platforms

    def set_enemy_group(self, enemies):
        self._enemies = enemies

    def set_item_group(self, items):
        self._items = items

    def set_trigger_group(self, trigger):
        self._triggers = trigger

    def _set_sprite(self, posture):
        idx = self._animation_idx
        animations = self._coords[posture]

        if len(animations) == 1:
            idx = 0
        else:
            self._animation_dur = (self._animation_dur + 1) % 6
            if self._animation_dur > 0:
                return

        info = animations[idx]

        pos = (info["POS"][0], info["POS"][1])
        dims = (info["W"], info["H"])
        scale = (self._coords["SCALE_W"], self._coords["SCALE_H"])
        target_dims = (dims[0] * scale[0], dims[1] * scale[1])

        rect = pygame.Rect(pos, dims)
        image = self._sheet.subsurface(rect)
        self.image = pygame.transform.scale(image, target_dims)

        if self._left:
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()

        self._animation_idx = (idx + 1) % len(animations)
