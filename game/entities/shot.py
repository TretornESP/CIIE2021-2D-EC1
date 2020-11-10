import pygame
from game import ResourceManager, Configuration
from .enemy import Enemy
from .character import Character
from ..farm import Farm
from ..util.log import Clog
from ..player_repository import PlayerRepository

class Shot(Enemy):
    SPEEDX = 5
    SPEEDY = 0

    def __init__(self, level, data, coord, left):
        self.log = Clog(__name__)
        Enemy.__init__(self, level, data, coord, Shot.SPEEDX, Shot.SPEEDY, False)

        self._left = left
        self._count = 0
        self._player = ResourceManager.get_player_repository()

    def move_cpu(self, elapsed_time):
        (xright, _) = Configuration().get_resolution()
        xpos, ypos = self._player.get_parameter(PlayerRepository.ATTR_POS)
        if self.rect.left > 0 and self.rect.right < xright:

            distance = xpos - self._position[0]

            if self._left:
                direction_x = Character.LEFT
            else:
                direction_x = Character.RIGHT

        else:
            self.kill()
            direction_x = Character.STILL

        direction_y = Character.STILL

        Character.move(self, (direction_x, direction_y))

    def update(self, elapsed_time):
        if Farm.touches_anything_visible(self):
            self.kill()
        Enemy.update(self, elapsed_time)
        self.move_cpu(elapsed_time)
