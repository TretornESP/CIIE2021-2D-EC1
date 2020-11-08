import pygame
from game import ResourceManager
from .dialog_screen import DialogScreen
from ..abstract_menu import AbstractMenu

class DialogMenu(AbstractMenu):
    def __init__(self, director, background, title, text, options):
        AbstractMenu.__init__(self, director)

        self._title = title
        self._text = text
        self._options = options

        self._screen_list.append(DialogScreen(self, background, title, text, options))
        self._show_first_screen()

    def choose_option(self, valid):
        print(f"pressed a {valid} button")
        self._director.end_scene()
    def update(self, *args):
        pass

    def play_game(self):
        pass

    def quit_game(self):
        pass
