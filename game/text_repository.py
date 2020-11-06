import pygame

class TextRepository:
    def __init__(self):
        self._sprites = pygame.sprite.Group()

    def add_sprite(self, sprite):
        self._sprites.add(sprite)

    def update(self, elapsed_time):
        for sprite in self._sprites:
            sprite.update(elapsed_time)

    def draw(self, screen):
        for sprite in self._sprites:
            sprite.draw(screen)

    def set_position(self, pos):
        for sprite in self._sprites:
            sprite.set_position(pos)
