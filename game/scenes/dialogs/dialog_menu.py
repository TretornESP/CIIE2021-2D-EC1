import pygame
from game import ResourceManager
from .dialog_screen import DialogScreen
from ..abstract_menu import AbstractMenu
from ...farm import Farm
import time
class DialogMenu(AbstractMenu):
    def __init__(self, background, title, text, options, spawn_v, spawn_vt, spawn_i, spawn_it):
        AbstractMenu.__init__(self)

        self._title = title
        self._text = text
        self._options = options
        self._spawn_v = spawn_v
        self._spawn_vt = spawn_vt
        self._spawn_i = spawn_i
        self._spawn_it = spawn_it
        self._scroll = (0, 0)

        self._screen_list.append(DialogScreen(self, background, title, text, options))
        self._show_first_screen()

    def choose_option(self, valid):
        self._director.end_dialog()

        if valid:
            i = 0
            while i < len(self._spawn_v):
                sprite = self._spawn_v[i]
                sprite._scroll = self._scroll
                if self._spawn_vt[i] == "object":
                    Farm.add_object(sprite)
                elif self._spawn_vt[i] == "platform":
                    Farm.add_platform(sprite)
                i += 1
        else:
            i = 0
            while i < len(self._spawn_i):
                sprite = self._spawn_i[i]
                sprite._scroll = self._scroll
                if self._spawn_it[i] == "object":
                    Farm.add_object(sprite)
                elif self._spawn_it[i] == "platform":
                    Farm.add_platform(sprite)
                i += 1

    def update(self, *args):
        pass

    def play_game(self):
        pass

    def quit_game(self):
        pass
