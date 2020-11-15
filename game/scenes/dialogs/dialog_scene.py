from .. import AbstractHorizontalScene
from ..skies import AbstractSky
import pygame

class DialogScene(AbstractHorizontalScene):

    _DEFAULT_DUR = 0.3
    _DEFAULT_SPD = 5

    _COLOR = (255, 0, 0)
    _SCALE = 0.3

    def __init__(self, director, index, title, text, background, options):
        AbstractHorizontalScene.__init__(self, director)

        self._id = -1
        self._background = background
        self._scroll_size = 0

        self._index = index
        self._title = title
        self._text = text

        self._options = options
        self._director = director

        self._sky = AbstractSky(level, self._sky)
        self._player = None
        self._objects   = pygame.sprite.Group()
        self._enemies   = pygame.sprite.Group()
        self._platforms = pygame.sprite.Group()
        self._triggers  = pygame.sprite.Group()

        self._dynamic_sprites = pygame.sprite.Group()
        self._static_sprites  = pygame.sprite.Group()
        self._overlay_sprites = pygame.sprite.Group()
