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

    def __init__(self, level, data, position, invert, velocity_x = 0, velocity_y = 0):
        AbstractSprite.__init__(self)

        self._coords = ResourceManager.load_coords(level, data)
        self._sheet = ResourceManager.load_sheet(level, data, colorkey=-1)

        if (invert):
            self._sheet =  pygame.transform.flip(self._sheet, 1, 0) #Tal vez invierta controles??

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

        self._platforms = None
        self._enemies = None
        self._items = None
        self._triggers = None

    def update(self, elapsed_time):
        self._update_movement(elapsed_time)
        self._update_collisions(elapsed_time)
        self._update_sprite()

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
        if (self._platforms != None):
            platform = pygame.sprite.spritecollideany(self, self._platforms)
            if (platform != None and platform._collides): #No tengo claro esto
                self.set_global_position((self._position[0], platform._position[1] - platform.rect.height + 1))
                self._velocity = (self._velocity[0], 0)
            else:
                _, vel_py = Configuration().get_pixels((0, self._velocity_y))
                self._velocity = (self._velocity[0], self._velocity[1] + 0.08 * vel_py * elapsed_time)
        if (self._enemies != None):
            enemy = pygame.sprite.spritecollideany(self, self._enemies) #TODO
        if (self._items != None):
            item = pygame.sprite.spritecollideany(self, self._items) #TODO
        if (self._triggers != None):
            trigger = pygame.sprite.spritecollideany(self, self._triggers) #TODO

    def _update_sprite(self):
        vel = self._velocity

        if vel[0] < 0:
            self._left = True
        elif vel[0] > 0:
            self._left = False

        if vel[1] != 0:
            self._set_sprite("MOV_Y")
        elif vel[0] == 0:
            self._set_sprite("STILL")
        else:
            self._set_sprite("MOV_X")

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
        target_dims = (self._coords["TARGET_W"], self._coords["TARGET_H"])

        rect = pygame.Rect(pos, dims)
        image = self._sheet.subsurface(rect)
        self.image = pygame.transform.scale(image, target_dims)

        if self._left:
            self.image = pygame.transform.flip(self.image, 1, 0)

        self._animation_idx = (idx + 1) % len(animations)
