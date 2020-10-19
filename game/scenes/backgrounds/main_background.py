import pygame
from game import ResourceManager, Configuration

class MainBackground:
    def __init__(self, scroll_x=0):
        resolution = Configuration().get_resolution()
        image = ResourceManager.load_image("main_background.png")

        dest_resolution = (image.get_rect().width, resolution[0])
        self.image = pygame.transform.scale(image, dest_resolution)

        self.rect = self.image.get_rect()
        self.rect.bottom = resolution[0]

        self.subimage_rect = pygame.Rect((0, 0), resolution)
        self.subimage_rect.left = scroll_x

    def update(self, scroll_x):
        self.subimage_rect.left = scroll_x

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.subimage_rect)
