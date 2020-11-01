import pygame
from game import ResourceManager
from .gui_element import GUIElement

class Button(GUIElement):
    def __init__(self, screen, pos, image=None):
        if image != None:
            self.image = ResourceManager.load_image_asset(image)
        else:
            self.image = pygame.Surface((300, 40))
            self.image.fill((160, 160, 160))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        GUIElement.__init__(self, screen, self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PlayButton(Button):
    def __init__(self, screen, pos):
        Button.__init__(self, screen, pos)

    def callback(self):
        self._screen._menu.play_game()

class ExitButton(Button):
    def __init__(self, screen, pos):
        Button.__init__(self, screen, pos)

    def callback(self):
        self._screen._menu.quit_game()
