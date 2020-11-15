import pygame
from game.levels import Level
from game import ResourceManager
from .menu_screen import MenuScreen
from .abstract_menu import AbstractMenu

class MainMenu(AbstractMenu):
    def __init__(self, hacks=False):
        AbstractMenu.__init__(self)
        self._hacks = hacks
        self._screen_list.append(MenuScreen(self))
        self._show_first_screen()

    def update(self, *args):
        pass

    def play_game(self):
        # stop music
        pygame.mixer.music.stop()

        # init repo
        repo = ResourceManager.get_player_repository()
        repo.reset_attr()

        level1 = Level("Level1", self._hacks)
        level0 = Level("Level0", self._hacks)

        for level in [level1, level0]:
            for scene in level.get_scenes():
                self._director.push_scene(scene)

    def quit_game(self):
        self._director.quit_game()
