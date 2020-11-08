from .animated_text import AnimatedText
from .shots import Shots
from .. import Configuration, ResourceManager
from ..util.log import Clog
from .enemy import Enemy
from .character import Character


class Torreta(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)
        self._text = ResourceManager.get_text_repository()
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

        self._disparo()
        Character.move(self, (direction_x, Character.STILL))

    def _disparo(self):
        x, y = self.rect.center
        projectile = Shots(x, y)
