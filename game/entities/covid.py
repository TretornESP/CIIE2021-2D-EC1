from .. import Configuration
from ..util.log import Clog
from .enemy import Enemy
from .character import Character
from ..resource_manager import ResourceManager
from ..player_repository import PlayerRepository
class Covid(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)
        self._player = ResourceManager.get_player_repository()

        self._count = 0

    def move_cpu(self, elapsed_time):
        (xright, _) = Configuration().get_resolution()
        xpos, ypos = self._player.get_parameter(PlayerRepository.ATTR_POS)

        if self.rect.left > 0 and self.rect.right < xright:

            distance = xpos - self._position[0]

            if distance < -5:
                direction_x = Character.LEFT
            elif -5 < distance < 5:
                direction_x = Character.STILL
            else:
                direction_x = Character.RIGHT

            if ypos < self._position[1]:
                direction_y = Character.UP
            else:
                direction_y = Character.STILL

        else:
            direction_x = Character.STILL
            direction_y = Character.STILL

        Character.move(self, (direction_x, direction_y))

    def update(self, elapsed_time):
        Enemy.update(self, elapsed_time)
        self.move_cpu(elapsed_time)
