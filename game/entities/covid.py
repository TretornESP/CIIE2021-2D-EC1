from ..util.log import Clog
from .enemy import Enemy
from .character import Character

class Covid(Enemy):
    def __init__(self, level, data, coord, speedx=10, speedy=20, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

        self._count = 0

    def move_cpu(self):
        if self._count < 20:
            direction = Character.LEFT
        else:
            direction = Character.RIGHT
        self._count = (self._count + 1) % 41

        Character.move(self, (direction, Character.UP))
