#Este approach no permite items animados!!
from .abstract_platform import AbstractPlatform
import pygame
from ..util.log import Clog


class Trigger(AbstractPlatform):
    MUSIC_START = 0x0
    CHECKPOINT  = 0x1
    DIALOG      = 0x2
    SCENE_END   = 0x3

    def __init__(self, director, level, id, indic, once, coord, size, invert, action_data=None):
        AbstractPlatform.__init__(self, level, None, True, pygame.Rect(coord, size), invert, not indic)
        self.log = Clog(__name__)
        self._id = id
        self._once = once
        self._active = True
        self._overlay_connector = []
        self._action_data=action_data
        self._director = director

    def get_pos(self):
        return self.rect

    def event(self, override=False):
        if not self._active and not override:
            return self._once

        if self._id == Trigger.MUSIC_START:
            self.log.debug("PLAYING SOME SICK SOUNDS")
        if self._id == Trigger.CHECKPOINT:
            self.log.debug("CHECKPOINT REACHED")
        if self._id == Trigger.DIALOG:
            self._director.push_scene(self._action_data)
            self.log.debug("BLABLABLA")
        if self._id == Trigger.SCENE_END:
            self.log.debug("SCNE ENDED!")

        self.event_deactivate()
        self._active = False

        return self._once

    def can_interact(self):
        return (self._id == Trigger.DIALOG)

    def revive(self):
        self.event_activate()
        self._active = True

    def set_overlay_connector(self, connector):
        self._overlay_connector = connector
