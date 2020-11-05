#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
from ..util.log import Clog
import pygame

class Object(AbstractPlatform):
    MASK = "mask"

    def __init__(self, level, kind, sprite, collision, coord, invert):
        AbstractPlatform.__init__(self, level, sprite, collision, pygame.Rect(coord, (0,0)), invert)
        self.log = Clog(__name__)
        self._kind = kind
        self._connector = []
        self._player = None

    def set_item_connector(self, connector):
        self._connector = connector

    def remove(self):
        if self._connector != []:
            self._connector.remove(self)

    def set_player_connector(self, player):
        self._player = player

    def collect(self):
        if self._kind == Object.MASK:
            self.log.debug("Collected mask")
            self._player._picked_item(Object.MASK)
        self.remove()
