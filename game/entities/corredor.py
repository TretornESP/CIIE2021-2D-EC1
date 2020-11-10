from .character import Character
from .. import Configuration
from .enemy import Enemy

class Corredor(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

    def move_cpu(self):
        width, _ = Configuration().get_resolution()
        if self.rect.left >= -150 and self.rect.right <= width + 150:
            Character.move(self, (Character.LEFT, Character.STILL))
