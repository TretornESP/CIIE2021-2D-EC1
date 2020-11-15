import pygame
from .abstract_platform import AbstractPlatform
from .animated_text import AnimatedText
from game import ResourceManager
from ..farm import Farm
from ..audio.rocker import Rocker

class Trigger(AbstractPlatform):
    DIALOG_TEXT = "Press E to interact!"

    MUSIC_START = 0x0
    CHECKPOINT  = 0x1
    DIALOG      = 0x2
    SCENE_END   = 0x3

    def __init__(self, level, id, indic, once, coord, size, invert, action_data=None, locking=True):
        AbstractPlatform.__init__(self, level, None, True, pygame.Rect(coord, size), invert, not indic)
        self._id = id
        self._locking = locking
        self._once = once
        self._action_data = action_data
        self._director = ResourceManager.load_director()

        self._text = ResourceManager.get_text_repository()
        self._last = 0

        self._has_interacted = False

    def update(self, elapsed_time):
        AbstractPlatform.update(self, elapsed_time)
        self._last += elapsed_time
        player = Farm.get_player()

        if pygame.sprite.collide_rect(player, self):
            if self._id == Trigger.MUSIC_START:
                print("Playing music")
                Rocker.background(self._action_data)
                pass
            elif self._id == Trigger.CHECKPOINT:
                print("Checkpoint reached")
                self._director.set_checkpoint()
            elif self._id == Trigger.DIALOG:
                if self._last >= AnimatedText.get_duration():
                    self._last = 0
                    pos = self._position[0], self._position[1] - self.rect.height
                    self._text.add_sprite(AnimatedText(pos, Trigger.DIALOG_TEXT, self._scroll))
                if player.is_interacting() or (self._locking and not self._has_interacted):
                    self._has_interacted = True
                    Rocker.action(Rocker.AUD_TALK)
                    self._director.push_scene(self._action_data)
            elif self._id == Trigger.SCENE_END:
                Rocker.action(Rocker.AUD_WIN)
                self._director.end_scene()
            else:
                raise NotImplemented("This trigger does not exist")

            if self._once:
                self.kill()
