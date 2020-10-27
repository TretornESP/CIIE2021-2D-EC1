#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
import pygame
from ..util.log import Clog

class Trigger(AbstractPlatform):
    MUSIC_START = 0x0
    CHECKPOINT  = 0x1
    DIALOG      = 0x2
    SCENE_END   = 0x3

    def __init__(self, level, id, indic, coord, size, invert):
        AbstractPlatform.__init__(self, level, None, True, pygame.Rect(coord, size), invert, not indic)
        self.log = Clog(__name__)
        self._id = id

    def event(self):
        if self._id == Trigger.MUSIC_START:
            self.log.debug("PLAYING SOME SICK SOUNDS")
        if self._id == Trigger.CHECKPOINT:
            self.log.debug("CHECKPOINT REACHED")
        if self._id == Trigger.DIALOG:
            self.log.debug("BLABLABLA")
        if self._id == Trigger.SCENE_END:
            self.log.debug("SCNE ENDED!")

        self.event_deactivate()
