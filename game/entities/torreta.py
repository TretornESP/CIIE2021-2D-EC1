from .character import Character
from .. import Configuration
from .enemy import Enemy
from ..farm import Farm
from .shot import Shot

class Torreta(Enemy):
    DELAY = 0.15
    SHOOT_RATIO = 0.75

    def __init__(self, level, data, shot, coord, speedx, speedy, invert=False):
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

        self._shot = shot

        self._delay = Torreta.DELAY
        self._last_shot = Torreta.SHOOT_RATIO

        self._last_x = Character.STILL

    def move_cpu(self):
        width, _ = Configuration().get_resolution()
        x_pos, y_pos = Farm.get_player()._position

        if self._delay >= Torreta.DELAY:
            self._delay = 0
            if self.rect.left >= -150 and self.rect.right <= width + 150:
                dist_x = x_pos - self._position[0]

                if self._last_shot >= Torreta.SHOOT_RATIO:
                    self._last_shot = 0
                    Farm.add_enemy(Shot(self._level, self._shot, self._position, dist_x < 0, self._scroll))

                if dist_x <= 0:
                    direction_x = Character.LEFT
                else:
                    direction_x = Character.RIGHT
            else:
                direction_x = Character.STILL
            self._last_x = direction_x
        Character.move(self, (self._last_x, Character.STILL))

    def update(self, elapsed_time):
        Enemy.update(self, elapsed_time)
        self._delay += elapsed_time
        self._last_shot += elapsed_time
