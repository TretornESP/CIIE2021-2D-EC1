import pygame
from game.levels import Level
from game import ResourceManager
from .highscores_screen import HighscoresScreen
from .menu_screen import MenuScreen
from .abstract_menu import AbstractMenu
from ..player_repository import PlayerRepository


class MainMenu(AbstractMenu):
    def __init__(self, hacks=False):
        AbstractMenu.__init__(self)
        self._hacks = hacks
        self._screen_list.append(MenuScreen(self))
        self._screen_list.append(HighscoresScreen(self))
        self._show_first_screen()

    def update(self, *args):
        pass

    def play_game(self):
        # stop music
        pygame.mixer.music.stop()

        # init repo
        repo = ResourceManager.get_player_repository()
        repo.reset_attr()
        repo.set_parameter(PlayerRepository.ATTR_TOTAL_TIME, None, accounted=False)

        level0 = Level("Level0", self._hacks)
        level1 = Level("Level1", self._hacks)
        level2 = Level("Level2", self._hacks)

        for level in [level2, level1, level0]:
            for scene in level.get_scenes():
                self._director.push_scene(scene)

    def quit_game(self):
        self._director.quit_game()

    def play_highscores(self):
        self._current_screen = 1

    def populate_highscores(self):
        self._screen_list[1].populate_hs_list(ResourceManager.load_hs())
