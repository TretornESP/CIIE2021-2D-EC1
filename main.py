import pygame
from pygame.locals import *
import sys

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    window.fill((0, 0, 0))
    pygame.draw.circle(window, (255, 255, 255), (400, 300), 20, 0)
    pygame.display.update()
