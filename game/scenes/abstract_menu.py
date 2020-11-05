import pygame
from .abstract_scene import AbstractScene

class AbstractMenu(AbstractScene):
    def __init__(self, director):
        AbstractScene.__init__(self, director)
        self._screen_list = [] 

    def update(self, *args):
        pass

    def start_scene(self):
        AbstractScene.start_scene(self)
        self._screen_list[self._current_screen].start_scene()

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._director.quit_game()
        self._screen_list[self._current_screen].events(events)

    def draw(self):
        self._screen_list[self._current_screen].draw(self._screen)

    def play_game(self):
        pass

    def quit_game(self):
        pass

    def _show_first_screen(self):
        self._current_screen = 0
