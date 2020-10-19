from .abstract_platform import AbstractPlatform
from game import ResourceManager

class Platform(AbstractPlatform):
    def __init__(self, rect):
        AbstractPlatform.__init__(self, rect)

        self.image = ResourceManager.load_image("platform.png")
