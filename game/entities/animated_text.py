import pygame
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite

class AnimatedText(AbstractSprite):
    DUR = 0.5

    def __init__(self, position, text):
        AbstractSprite.__init__(self)

        font = ResourceManager.load_font_asset("8bit.ttf", 16)

        self.image = font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()

        self._dur = 0

        self.set_global_position(position)

    def update(self, elapsed_time):
        self._dur += elapsed_time

        _, vel_y = Configuration().get_pixels((0, -5))
        self._increase_position((0, vel_y * elapsed_time))

        if self._dur > AnimatedText.DUR:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
