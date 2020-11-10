from .character import Character
from .. import Configuration
from .enemy import Enemy
from .. import Farm

class Covid(Enemy):
    DELAY = 0.15

    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

        self._last_x = Character.STILL
        self._last_y = Character.STILL

        self._delay = Covid.DELAY

    def move_cpu(self):
        width, _ = Configuration().get_resolution()
        x_pos, y_pos = Farm.get_player()._position

        if self._delay >= Covid.DELAY:
            self._delay = 0
            if self.rect.left >= -150 and self.rect.right <= width + 150:
                dist_x = x_pos - self._position[0]

                if dist_x <= 0:
                    direction_x = Character.LEFT
                else:
                    direction_x = Character.RIGHT

                if y_pos < self._position[1]:
                    direction_y = Character.UP
                else:
                    direction_y = Character.STILL
            else:
                direction_x = Character.STILL
                direction_y = Character.STILL
            self._last_x = direction_x
            self._last_y = direction_y
        Character.move(self, (self._last_x, self._last_y))

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        self._delay += elapsed_time
