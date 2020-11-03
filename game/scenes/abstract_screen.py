import pygame
from pygame.locals import *
from game import ResourceManager, Configuration

class AbstractScreen:
    def __init__(self, menu, image, song=None, transform=False):
        res = Configuration().get_resolution()

        self._menu = menu

        self.image = ResourceManager.load_image_asset(image)
        if transform:
            self.image = pygame.transform.scale(self.image, res)

        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = res[1]

        if song != None:
            channel = ResourceManager.load_music_channel()
            song = ResourceManager.load_music_asset(song)
            channel.play(song, loops=-1)

        self._clicked = None
        self._gui_elements = []

    def events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self._clicked = None
                for element in self._gui_elements:
                    if element.pos_in_element(event.pos):
                        self._clicked = element
                        break
            if event.type == MOUSEBUTTONUP:
                for element in self._gui_elements:
                    if element.pos_in_element(event.pos):
                        if self._clicked != None and element == self._clicked:
                            self._clicked.callback()
                            break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for element in self._gui_elements:
            element.draw(screen)
