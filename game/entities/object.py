#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
from ..util.log import Clog
import pygame

class Object(AbstractPlatform):
    def __init__(self, level, kind, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0,0)), invert)
        self.log = Clog(__name__)
        self._kind = kind
        self._connector = []

    def set_item_connector(self, connector):
        self._connector = connector

    def remove(self):
        if self._connector != []:
            self._connector.remove(self)

    def collect(self):
        self.log.debug("Collected item")
        self.remove()
