import pygame
from game.levels import Level
from game import ResourceManager
from .menu_screen import MenuScreen
from .abstract_menu import AbstractMenu

class MainMenu(AbstractMenu):
    def __init__(self, director):
        AbstractMenu.__init__(self, director)

        self._screen_list.append(MenuScreen(self))
        self._show_first_screen()

    def update(self, *args):
        pass

    def play_game(self):
        # stop music
        pygame.mixer.music.stop()

        level = Level("Level0", self._director)
        for scene in level.get_scenes():
            self._director.push_scene(scene)

    def quit_game(self):
        self._director.quit_game()
