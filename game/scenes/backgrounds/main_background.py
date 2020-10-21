import pygame
from .abstract_background import AbstractBackground
from game import ResourceManager, Configuration

class MainBackground(AbstractBackground):
    def __init__(self, scroll_x=0):
        AbstractBackground.__init__(self, scroll_x)

        resolution = Configuration().get_resolution()
        image = ResourceManager.load_image("main_background.png")

        dest_resolution = (image.get_rect().width, resolution[1])
        self.image = pygame.transform.scale(image, dest_resolution)

        self.rect = self.image.get_rect()
        self.rect.bottom = resolution[1]

        self.subimage_rect = pygame.Rect((0, 0), resolution)
        self.subimage_rect.left = scroll_x
