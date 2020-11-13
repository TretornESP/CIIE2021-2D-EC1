from .character import Character
from game import ResourceManager
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
        width, _ = ResourceManager.load_config().get_resolution()
        x_pos, _ = Farm.get_player()._position

        if self._delay >= Covid.DELAY:
            self._delay = 0
            if self.rect.left >= -150 and self.rect.right <= width + 150:
                dist_x = x_pos - self._position[0]

                if dist_x <= 0:
                    direction_x = Character.LEFT
                else:
                    direction_x = Character.RIGHT

                inc = self.rect.width / 2 * (1 if direction_x == Character.RIGHT else -1)
                self.rect.left += inc
                platform = Farm.platform_collision(self)
                self.rect.left -= inc
                if platform != None and platform._collides:
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
        Enemy.update(self, elapsed_time)
        self._delay += elapsed_time
