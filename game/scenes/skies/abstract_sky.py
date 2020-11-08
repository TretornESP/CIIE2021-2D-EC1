import pygame
from game import ResourceManager, Configuration

class AbstractSky:
    def __init__(self, level, filename):
        res = Configuration().get_resolution()
        image = ResourceManager.load_sprite(filename, level)

        self.image = pygame.transform.scale(image, res)
        self.rect = self.image.get_rect()

        self.rect.left = 0
        self.rect.bottom = res[1] - 100

    def update(self, elapsed_time):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
