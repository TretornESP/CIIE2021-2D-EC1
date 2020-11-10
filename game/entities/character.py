import pygame
import math
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite
from ..util.log import Clog
from ..farm import Farm

class Character(AbstractSprite):
    STILL = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    DASH = 5

    STEP_OVER = 3
    JUMPING_DELAY = 0.07

    def __init__(self, level, data, position, invert, velocity_x = 0, velocity_y = 0):
        AbstractSprite.__init__(self)
        self._log = Clog(__name__)
        if data != "shot":
            self._log.info("loading character "+data)
        self._coords = ResourceManager.load_coords(level, data)
        self._sheet = ResourceManager.load_sheet(level, data, colorkey=-1)
        self._level = level
        self._data = data
        if (invert):
            self._sheet = pygame.transform.flip(self._sheet, 1, 0)

        self._left = False
        self._animation_idx = 0
        self._animation_dur = -1

        self._set_sprite("STILL")
        self.rect = self.image.get_rect()

        self.set_global_position(position)

        self._is_jumping = False
        self._jump = Character.JUMPING_DELAY
        self._velocity = (0, 0)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

        self._movement_x = Character.STILL
        self._movement_y = Character.STILL

        self._orientation = Character.RIGHT

    def update(self, elapsed_time):
        step_over = False
        self._jump += elapsed_time

        res = Configuration().get_resolution()
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = Configuration().get_pixels((vel_x, vel_y))

        # update horizontal movement
        if self._movement_x == Character.LEFT:
            self._velocity = (-vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.RIGHT:
            self._velocity = (vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.STILL:
            self._velocity = (0, self._velocity[1])
        if self._movement_y == Character.UP and self._jump >= Character.JUMPING_DELAY and not self._is_jumping:
            self._jump = 0
            self._is_jumping = True
            self._velocity = (self._velocity[0], -vel_py * 0.018)
        self._update_sprite()

        # check horizontal collisions
        self._increase_position((self._velocity[0], 0))
        platform = Farm.platform_collision(self)
        if platform != None and platform._collides and self.rect.bottom > platform.rect.top + 1:
            dist_l = abs(platform.rect.centerx - self.rect.left)
            dist_r = abs(platform.rect.centerx - self.rect.right)

            if self.rect.bottom - Character.STEP_OVER < platform.rect.top + 1:
                step_over = True
            elif self._velocity[0] > 0 or dist_l >= dist_r:
                self.set_global_position((platform._position[0] - self.rect.width, self._position[1]))
            elif self._velocity[0] < 0 or dist_r > dist_l:
                self.set_global_position((platform._position[0] + platform.rect.width, self._position[1]))

        # check vertical collisions
        self._increase_position((0, self._velocity[1]))
        platform = Farm.platform_collision(self)
        if platform != None and platform._collides:
            if self._velocity[1] > 0 or step_over:
                self._is_jumping = False
                self._velocity = (self._velocity[0], 0)
                self.set_global_position((self._position[0], platform._position[1] - platform.rect.height + 1))
            elif self._velocity[1] < 0:
                self._velocity = (self._velocity[0], 0.04 * vel_py * elapsed_time)
                self.set_global_position((self._position[0], platform._position[1] + self.rect.height))
        else:
            # check y axis boundaries
            if self.rect.bottom >= res[1]:
                self._is_jumping = False
                self._velocity = (self._velocity[0], 0)
                self.set_global_position((self._position[0], res[1]))
            else:
                self._is_jumping = True
                self._jump -= elapsed_time
                self._velocity = (self._velocity[0], self._velocity[1] + 0.08 * vel_py * elapsed_time)

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
        self._movement_x = direction[0]
        self._movement_y = direction[1]

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
        target_dims = (int(dims[0] * scale[0]), int(dims[1] * scale[1]))

        rect = pygame.Rect(pos, dims)
        try:
            image = self._sheet.subsurface(rect)
        except Exception:
            print(f"Coords JSON is invalid! (X,Y)(H,W) are bigger than image: ! {self._sheet.get_width()}, {self._sheet.get_height()}")
            raise SystemExit
        self.image = pygame.transform.scale(image, target_dims)

        if self._left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

        self._animation_idx = (idx + 1) % len(animations)
