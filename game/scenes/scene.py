from . import AbstractHorizontalScene
from .. import ResourceManager
from .backgrounds import MainBackground
from ..entities import Player
from ..entities.character import Character
from ..player_repository import PlayerRepository #This is only for debug and can be deleted
from ..checkpoint_repository import CheckpointRepository
from ..entities.hud import Hud
from .skies import AbstractSky
from ..farm import Farm
from ..farm_factory import FarmFactory
import pygame

class Scene(AbstractHorizontalScene):
    def __init__(self, level, farm_factory, id, background, size, sky):
        AbstractHorizontalScene.__init__(self)
        resolution = ResourceManager.load_config().get_resolution()

        self._id = id
        self._background = MainBackground(level, background)
        self._scroll_size = size
        self._sky = AbstractSky(level, sky)
        self._checkpoint = ResourceManager.get_checkpoint_repository()

        self._farm_factory = farm_factory

    def get_id(self):
        return self._id

    def get_scroll_x(self):
        return self._scroll_x

    def start_scene(self):
        AbstractHorizontalScene.start_scene(self)
        Farm.get_player().reset_hearts()
        Farm.get_player().reset_masks()
        
    def set_checkpoint(self, _scroll_x=None):
        self._checkpoint.set_player(Farm.get_player())
        if _scroll_x != None:
            self._checkpoint.set_scroll(_scroll_x)
        else:
            self._checkpoint.set_scroll(self._scroll_x)

    def run_checkpoint(self):
        if self._checkpoint.get_player() == None:
            return False
        pos, repo = self._checkpoint.get_player()
        repo.set_parameter(PlayerRepository.ATTR_HEALTH, PlayerRepository.DEFAULT_HEALTH)

        # Reset dash and jump
        Farm.get_player()._velocity = (0, 0)
        Farm.get_player()._dash = Character.DASH_DUR + 1
        Farm.get_player()._end_dash = True

        # Reset invulnerability
        Farm.get_player()._last_hit = Player.INVULNERABILITY_LAPSE + 1

        Farm.get_player().get_repository().load_checkpoint_status(repo)
        Farm.get_player().teleport(pos)
        self._scroll_x = self._checkpoint.get_scroll()

        return True
