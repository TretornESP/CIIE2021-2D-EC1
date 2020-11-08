import pygame
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite


class AnimatedText(AbstractSprite):

    _DEFAULT_DUR = 0.3
    _DEFAULT_SPD = 5

    def __init__(self, position=(0, 0), text="dummy", scroll=(0, 0), custom_duration=None, custom_speed=None):
        AbstractSprite.__init__(self)

        font = ResourceManager.load_font_asset("8bit.ttf", 16)

        self.image = font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self._text = text
        self.duration = self._DEFAULT_DUR
        self.speed = self._DEFAULT_SPD

        if custom_duration is not None:
            self.cust_dur = custom_duration

        if custom_speed is not None:
            self.speed = custom_speed

        self._dur = 0
        self._scroll = scroll

        self.set_global_position(position)
        self.set_position(self._scroll)

    @classmethod
    def get_duration(self):
        return AnimatedText._DEFAULT_DUR

    def set_pos(self, position):
        self.set_global_position(position)

    def update(self, elapsed_time):
        self._dur += elapsed_time

        _, vel_y = Configuration().get_pixels((0, -self.speed))
        self._increase_position((0, vel_y * elapsed_time))

        if self._dur > self.duration:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
