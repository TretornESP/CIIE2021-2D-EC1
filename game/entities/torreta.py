from .. import Configuration
from ..util.log import Clog
from .enemy import Enemy
from .character import Character
from .shot import Shot
from ..farm import Farm
from ..resource_manager import ResourceManager
from ..player_repository import PlayerRepository

class Torreta(Enemy):

    SHOT_RATIO = 1 #Shots per sec

    def __init__(self, level, data, shot, coord, speedx, speedy, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)
        self._count = 0
        self._shot = shot
        self._last_shot = 1
        self._player = ResourceManager.get_player_repository()

    def move_cpu(self, elapsed_time):
        xpos, ypos = self._player.get_parameter(PlayerRepository.ATTR_POS)
        (xright, _) = Configuration().get_resolution()
        if self.rect.left > 0 and self.rect.right < xright:

            distance = xpos - self._position[0]

            if self._last_shot > Torreta.SHOT_RATIO:
                Farm.add_enemy(Shot(self._level, self._shot, self.get_absolute_position(), (distance < 0)))
                self._last_shot = 0
            else:
                self._last_shot += elapsed_time

            if distance < -5:
                direction_x = Character.LEFT
            elif -5 < distance < 5:
                direction_x = Character.STILL
            else:
                direction_x = Character.RIGHT

        else:
            direction_x = Character.STILL

        Character.move(self, (direction_x, Character.STILL))

    def update(self, elapsed_time):
        Enemy.update(self, elapsed_time)
        self.move_cpu(elapsed_time)
