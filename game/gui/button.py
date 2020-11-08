import pygame
from game import ResourceManager
from .gui_element import GUIElement

class Button(GUIElement):
    def __init__(self, screen, pos, image=None, x_size=None, y_size=None):
        if image != None:
            self.image = ResourceManager.load_image_asset(image)
            self.image = pygame.transform.scale(self.image, (x_size, y_size))
        else:
            if x_size != None and y_size != None:
                self.image = pygame.Surface((x_size, y_size))
            else:
                self.image = pygame.Surface((300, 40))

            self.image.fill((160, 160, 160))

        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        GUIElement.__init__(self, screen, self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class EmptyButton(Button):
    def __init__(self, screen, pos, x_size, y_size, image):
        Button.__init__(self, screen, pos, x_size=x_size, y_size=y_size, image=image) #dirty nasty hack

    def callback(self):
        pass

class OptionButton(Button):
    def __init__(self, screen, pos, x_size, y_size, valid):
        Button.__init__(self, screen, pos, x_size=x_size, y_size=y_size) #dirty nasty hack
        self._valid = valid

    def callback(self):
        self._screen._menu.choose_option(self._valid)

class RetryButton(Button):
    def __init__(self, screen, pos):
        Button.__init__(self, screen, pos)

    def callback(self):
        self._screen._menu.retry()

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
