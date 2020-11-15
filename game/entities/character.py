import pygame
import math
from .abstract_sprite import AbstractSprite
from .animated_text import AnimatedText
from game import ResourceManager
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

    DASH_CD = 2
    DASH_DUR = 0.15
    DASH_TEXT = "Dash!"
    DASH_COLOR = (138, 43, 226)

    def __init__(self, level, data, position, invert, velocity_x = 0, velocity_y = 0):
        AbstractSprite.__init__(self)
        self._coords = ResourceManager.load_coords(level, data)
        self._sheet = ResourceManager.load_sheet(level, data, colorkey=-1)
        self._level = level
        self._data = data
        if invert:
            self._sheet = pygame.transform.flip(self._sheet, True, False)

        self._left = False
        self._animation_idx = 0
        self._animation_dur = -1

        self._text = ResourceManager.get_text_repository()

        self._set_sprite("STILL")
        self.rect = self.image.get_rect()

        self.set_global_position(position)

        self._is_jumping = False
        self._jump = Character.JUMPING_DELAY
        self._velocity = (0, 0)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

        self._dash = Character.DASH_CD
        self._end_dash = True

        self._movement_x = Character.STILL
        self._movement_y = Character.STILL

        self._momentum = 0

        self._orientation = Character.RIGHT

    def update(self, elapsed_time):
        step_over = False
        self._jump += elapsed_time
        self._dash += elapsed_time

        res = ResourceManager.load_config().get_resolution()
        vel_x, vel_y = self._velocity_x, self._velocity_y
        vel_px, vel_py = ResourceManager.load_config().get_pixels((vel_x, vel_y))

        if self._dash > Character.DASH_DUR and not self._end_dash:
            self._end_dash = True
            self._velocity = vel_px * elapsed_time * (-1 if self._left else 1), self._velocity[1]

        # update horizontal movement
        if self._movement_x == Character.LEFT:
            self._momentum = 0
            self._velocity = (-vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.RIGHT:
            self._momentum = 0
            self._velocity = (vel_px * elapsed_time, self._velocity[1])
        if self._movement_x == Character.STILL and not self._is_jumping and self._dash >= Character.DASH_DUR:
            self._momentum += (-vel_px if self._velocity[0] >= 0 else vel_px) * elapsed_time * 0.02
            v_x = max(0, self._momentum + self._velocity[0]) if self._velocity[0] >= 0 else min(0, self._momentum + self._velocity[0])
            self._momentum = self._momentum if v_x != 0 else 0
            self._velocity = (v_x, self._velocity[1])
        if self._movement_y == Character.UP and self._jump >= Character.JUMPING_DELAY and not self._is_jumping:
            self._jump = 0
            self._is_jumping = True
            self._velocity = (self._velocity[0], -vel_py * 0.018)
        if self._dash < Character.DASH_DUR:
            direction = -1 if self._left else 1
            self._velocity = ((vel_px + 300) * elapsed_time * direction, 0)
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
                if self._is_jumping and self._velocity[1] > 0 and self.rect.left - platform.rect.left - platform.rect.height > 10:
                    self._dash = Character.DASH_CD
                self._is_jumping = False
                self._velocity = (self._velocity[0], 0)
                self.set_global_position((self._position[0], platform._position[1] - platform.rect.height + 1))
            elif self._velocity[1] < 0:
                self._velocity = (self._velocity[0], 0.04 * vel_py * elapsed_time)
                self.set_global_position((self._position[0], platform._position[1] + self.rect.height))
        else:
            # check y axis boundaries
            if self.rect.bottom >= res[1]:
                if self._is_jumping and self._velocity[1] > 0 and self.rect.left > 10:
                    self._dash = Character.DASH_CD
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

    def do_dash(self):
        if self._dash > Character.DASH_CD:
            self._dash = 0
            self._end_dash = False
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Character.DASH_TEXT, self._scroll, Character.DASH_COLOR))

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
        if scale[0] > -1:
            self.image = pygame.transform.scale(image, target_dims)
        else:
            self.image = pygame.transform.scale(image, (self._coords["DEST_W"], self._coords["DEST_H"]))

        if self._left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

        self._animation_idx = (idx + 1) % len(animations)
