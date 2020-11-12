from . import AbstractHorizontalScene
from .. import ResourceManager
from .backgrounds import MainBackground
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
        self._farm_factory.push_to_charge()

    def set_checkpoint(self):
        self._checkpoint.set_player(Farm.get_player())
        self._checkpoint.set_scroll(self._scroll_x)

    def run_checkpoint(self):
        if self._checkpoint.get_player() == None:
            return False
        pos, repo = self._checkpoint.get_player()
        repo.set_parameter(PlayerRepository.ATTR_HEALTH, PlayerRepository.DEFAULT_HEALTH)
        Farm.get_player().get_repository().load_checkpoint_status(repo)
        Farm.get_player().teleport(pos)
        self._scroll_x = self._checkpoint.get_scroll()
        return True
