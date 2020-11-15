import pygame
from .abstract_scene import AbstractScene
from game.entities import Platform, Player
from .backgrounds import MainBackground
from game import ResourceManager
from .pause_menu import PauseMenu
from .end_menu import EndMenu
from ..entities.hud import *
from ..entities.hud.hud_elements import *
from ..player_repository import PlayerRepository
from ..util.log import Clog
from ..farm import Farm
from pygame.locals import *

class AbstractHorizontalScene(AbstractScene):
    MIN_X = 150
    MAX_X = 350

    # Main layout
    # CONTROL_JUMP_BINDING    = (K_w, K_SPACE)
    # CONTROL_DOWN_BINDING    = K_s
    # CONTROL_RIGHT_BINDING   = K_d
    # CONTROL_LEFT_BINDING    = K_a
    # CONTROL_PARRY_BINDING   = K_k
    # CONTROL_DASH_BINDING    = K_j

    # Alternative layout
    CONTROL_RELOAD_BINDING  = K_r
    CONTROL_JUMP_BINDING    = (K_UP, K_SPACE)
    CONTROL_DOWN_BINDING    = K_DOWN
    CONTROL_RIGHT_BINDING   = K_RIGHT
    CONTROL_LEFT_BINDING    = K_LEFT
    CONTROL_PARRY_BINDING   = K_d
    CONTROL_DASH_BINDING    = K_f
    CONTROL_INTERACT_BINDING = K_e

    CONTROL_PAUSE_BINDING   = (K_ESCAPE, K_p)

    def __init__(self):
        AbstractScene.__init__(self)
        self._scroll_x = 0
        self._hud = Hud()
        self._hud.create_hud_group(PlayerRepository.ATTR_HEALTH, HudHeart, (0, 0), Hud.GROW_RIGHT, 100)
        self._hud.create_hud_group(PlayerRepository.ATTR_MASKS, HudMask, (0, 6), Hud.GROW_RIGHT, 110)
        self._hud.create_hud_group(PlayerRepository.ATTR_TOILET_PAPER, HudToiletPaper, (80, 0), Hud.GROW_LEFT, 100)

        self._text_repo = ResourceManager.get_text_repository()
        self._player_repo = ResourceManager.get_player_repository()

        self._background = None
        self._sky = None

        self._last_scroll = self._scroll_x

    def update(self, elapsed_time):
        Farm.update_ponds(elapsed_time)

        self._text_repo.update(elapsed_time)
        self._hud.update()

        if self._update_scroll() or (self._last_scroll != self._scroll_x):
            self._last_scroll = self._scroll_x
            self._background.update(self._scroll_x)
            Farm.set_pond_position(self._scroll_x, 0)
            self._text_repo.set_position((self._scroll_x, 0))

        if self._player_repo.get_parameter(PlayerRepository.ATTR_HEALTH) <= 0:
            self._director.push_scene(EndMenu())

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._director.quit_game()
            elif event.type == KEYDOWN and (event.key in self.CONTROL_PAUSE_BINDING):
                self._director.push_scene(PauseMenu(self.CONTROL_PAUSE_BINDING))
            elif event.type == KEYDOWN and (event.key == self.CONTROL_RELOAD_BINDING):
                pass
        keys_pressed = pygame.key.get_pressed()

        Farm.get_player().move(keys_pressed, up=self.CONTROL_JUMP_BINDING,
                down=self.CONTROL_DOWN_BINDING, left=self.CONTROL_LEFT_BINDING,
                right=self.CONTROL_RIGHT_BINDING, parry=self.CONTROL_PARRY_BINDING,
                dash=self.CONTROL_DASH_BINDING, interact=self.CONTROL_INTERACT_BINDING)

    def draw(self):
        self._sky.draw(self._screen)
        self._background.draw(self._screen)
        Farm.draw_pond(self._screen)
        self._text_repo.draw(self._screen)
        self._hud.draw(self._screen)

    def _update_scroll(self):
        player = Farm.get_player()
        resolution = ResourceManager.load_config().get_resolution()

        if player.rect.right > AbstractHorizontalScene.MAX_X:
            displ = player.rect.right - AbstractHorizontalScene.MAX_X

            if self._scroll_x + resolution[0] >= self._background.rect.right:
                if player.rect.right >= resolution[0]:
                    player.set_global_position((self._background.rect.right - player.rect.width, player._position[1]))
                return False

            self._scroll_x = min(self._scroll_x + displ, self._background.rect.right - resolution[0])
            return True

        if player.rect.left < AbstractHorizontalScene.MIN_X:
            displ = AbstractHorizontalScene.MIN_X - player.rect.left
            self._scroll_x = max(self._scroll_x - displ, 0)
       
            if self._scroll_x == 0 and player.rect.left < 0:
                player.set_global_position((0, player._position[1]))
                return False
            else:
                return True

        return False
