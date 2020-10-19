import pygame
from game import Configuration

class AbstractScene:
    def __init__(self, director):
        pygame.init()

        self._screen = pygame.display.set_mode(Configuration().get_resolution())
        pygame.display.set_caption(Configuration().get_name())

        self._director = director

    def update(self, *args):
        raise NotImplemented()

    def events(self, *args):
        raise NotImplemented()

    def draw(self, *args):
        raise NotImplemented()
