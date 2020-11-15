import pygame
from game import ResourceManager

class AbstractScene:
    def __init__(self):
        pygame.init()
        self._font = pygame.font.Font(None, 30)

        configuration = ResourceManager.load_config()
        self._screen = pygame.display.set_mode(configuration.get_resolution())
        pygame.display.set_caption(configuration.get_name())

        self._director = ResourceManager.load_director()
        self._farm_factory = None

    def draw_fps(self, fps):
        f = self._font.render(str(int(fps)), True, pygame.Color('white'))
        self._screen.blit(f, (10, 10))

    def update(self, *args):
        raise NotImplemented()

    def events(self, *args):
        raise NotImplemented()

    def draw(self, *args):
        raise NotImplemented()

    def start_scene(self):
        if self._farm_factory != None:
            self._farm_factory.push_to_charge()
