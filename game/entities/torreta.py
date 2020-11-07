from .. import Configuration
from ..util.log import Clog
from .enemy import Enemy
from .character import Character


class Torreta(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

        self._count = 0

    def move_cpu(self, player):
        (xright, _) = Configuration().get_resolution()
        if self.rect.left > 0 and self.rect.right < xright:

            distance = player._position[0] - self._position[0]

            if distance < -5:
                direction_x = Character.LEFT
            elif -5 < distance < 5:
                direction_x = Character.STILL
            else:
                direction_x = Character.RIGHT

        else:
            direction_x = Character.STILL

        Character.move(self, (direction_x, Character.STILL))
