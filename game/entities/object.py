#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
from ..util.log import Clog
from ..farm import Farm
import pygame

class Object(AbstractPlatform):
    MASK = "mask"

    def __init__(self, level, kind, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0,0)), invert)
        self.log = Clog(__name__)
        self._kind = kind


    def collect(self):
        if self._kind == Object.MASK:
            self.log.debug("Collected mask")
            Farm.get_player().picked_item(Object.MASK)
        self.kill()
