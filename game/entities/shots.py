import pygame
from game import ResourceManager, Configuration
from .abstract_sprite import AbstractSprite


class Shots(AbstractSprite):

    def __init__(self, posx, posy):
        AbstractSprite.__init__(self)
        self.image = ResourceManager.load_sprite("laserBullet.png")
        self.rect = self.image.get_rect()

        self.velocity = 10
        self.rect.top = posy
        self.rect.left = posx

    def update(self, elapsed_time):
        self.rect.left = self.rect.left + self.velocity * elapsed_time

    def draw(self, screen):
        screen.blit(self.image, self.rect)
