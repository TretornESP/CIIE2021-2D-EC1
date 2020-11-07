from .. import Configuration
from ..util.log import Clog
from .enemy import Enemy
from .character import Character

class Corredor(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

        self._count = 0

    def move_cpu(self, player):
        (xleft, xright) = Configuration.get_resolution()
        if self.rect.left > xleft and self.rect.right < xright:
            Character.move(self, (Character.LEFT, Character.STILL))
