from .character import Character
from game import ResourceManager
from .enemy import Enemy

class Corredor(Enemy):
    def __init__(self, level, data, coord, speedx, speedy, invert=False):
        Enemy.__init__(self, level, data, coord, speedx, speedy, invert)

    def move_cpu(self):
        width, _ = ResourceManager.load_config().get_resolution()
        if self.rect.left >= -50 and self.rect.right <= width + 50:
            Character.move(self, (Character.LEFT, Character.STILL))
