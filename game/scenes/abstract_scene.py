import pygame
from game import ResourceManager

class AbstractScene:
    def __init__(self):
        pygame.init()

        configuration = ResourceManager.load_config()
        self._screen = pygame.display.set_mode(configuration.get_resolution())
        pygame.display.set_caption(configuration.get_name())

        self._director = ResourceManager.load_director()

    def update(self, *args):
        raise NotImplemented()

    def events(self, *args):
        raise NotImplemented()

    def draw(self, *args):
        raise NotImplemented()

    def start_scene(self):
        pass
