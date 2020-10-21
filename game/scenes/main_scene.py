import pygame
from .abstract_scene import AbstractScene
from game.sprites import Platform, Player
from .backgrounds import MainBackground
from game import Configuration
from pygame.locals import *

# estaria bien que esta escena acabese siendo abstracta para que todas las
# escenas con scroll horizontal hereden de ellas
class MainScene(AbstractScene):
    MIN_X = 100
    MAX_X = 300

    def __init__(self, director):
        AbstractScene.__init__(self, director)

        resolution = Configuration().get_resolution()

        self._scroll_x = 0

        self._player = Player()
        self._background = MainBackground()
        
        # platforms
        platform = Platform(pygame.Rect((0, resolution[1] - 20), (resolution[0], 20)))
        self._platforms = pygame.sprite.Group(platform)

        self._player.set_platform_group(self._platforms)

        # sprites
        self._dynamic_sprites = pygame.sprite.Group(self._player)
        self._static_sprites = pygame.sprite.Group(platform)

    def update(self, elapsed_time):
        self._dynamic_sprites.update(elapsed_time)

        if self._update_scroll():
            for sprite in iter(self._dynamic_sprites):
                sprite.set_position((self._scroll_x, 0))

            for sprite in iter(self._static_sprites):
                sprite.set_position((self._scroll_x, 0))

            self._background.update(self._scroll_x)

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._director.end_scene()

        keys_pressed = pygame.key.get_pressed()
        self._player.move(keys_pressed, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    def draw(self):
        self._background.draw(self._screen)
        self._dynamic_sprites.draw(self._screen)
        self._static_sprites.draw(self._screen)

    def _update_scroll(self):
        player = self._player
        resolution = Configuration().get_resolution()

        if player.rect.right > MainScene.MAX_X:
            displ = player.rect.right - MainScene.MAX_X

            if self._scroll_x + resolution[0] >= self._background.rect.right:
                if player.rect.right >= resolution[0]:
                    player.set_global_position((self._background.rect.right - player.rect.width, player._position[1]))
                return False

            self._scroll_x = min(self._scroll_x + displ, self._background.rect.right - resolution[0])
            return True

        if player.rect.left < MainScene.MIN_X:
            displ = MainScene.MIN_X - player.rect.left
            self._scroll_x = max(self._scroll_x - displ, 0)

            if self._scroll_x == 0 and player.rect.left < 0:
                player.set_global_position((0, player._position[1]))
                return False

            return True

        return False
