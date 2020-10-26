import pygame

class AbstractBackground:
    def __init__(self, scroll_x):
        pass

    def update(self, scroll_x):
        self.subimage_rect.left = scroll_x

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.image, self.rect, self.subimage_rect)
