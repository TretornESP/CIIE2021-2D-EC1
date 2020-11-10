from .character import Character
from .. import Configuration
from .enemy import Enemy
from .. import Farm

class Shot(Enemy):
    SPEEDX = 10
    SPEEDY = 0

    def __init__(self, level, data, coord, left, scroll):
        Enemy.__init__(self, level, data, coord, Shot.SPEEDX, Shot.SPEEDY, False)

        self._scroll = scroll
        self._left = left

    def move_cpu(self):
        direction_x = Character.LEFT if self._left else Character.RIGHT
        Character.move(self, (direction_x, Character.STILL))

    def update(self, elapsed_time):
        vel_px, _ = Configuration().get_pixels((Shot.SPEEDX, Shot.SPEEDY))

        self._velocity = vel_px * elapsed_time * (-1 if self._movement_x == Character.LEFT else 1), 0
        self._increase_position(self._velocity)

        if Farm.touches_anything_visible(self):
            self.kill()
