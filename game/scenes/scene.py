from . import AbstractHorizontalScene
from .. import Configuration, ResourceManager
from .backgrounds import MainBackground
from ..player_repository import PlayerRepository #This is only for debug and can be deleted
from ..checkpoint_repository import CheckpointRepository
from ..entities.hud import Hud
from .skies import AbstractSky
import pygame

class Scene(AbstractHorizontalScene):
    def __init__(self, level, director, id, background, size, sky):
        AbstractHorizontalScene.__init__(self, director)
        resolution = Configuration().get_resolution()

        self._id = id
        self._background = MainBackground(level, background)
        self._scroll_size = size

        self._sky = AbstractSky(level, sky)

        self._player = None

        self._objects   = pygame.sprite.Group()
        self._enemies   = pygame.sprite.Group()
        self._platforms = pygame.sprite.Group()
        self._triggers  = pygame.sprite.Group()

        self._dynamic_sprites = pygame.sprite.Group()
        self._static_sprites  = pygame.sprite.Group()
        self._overlay_sprites = pygame.sprite.Group()

        self._checkpoint = ResourceManager.get_checkpoint_repository()

    def set_checkpoint(self):
        print(f"Im at {self._player.get_global_position()}")
        self._checkpoint.set_player(self._player)

    def run_checkpoint(self):
        print(f"Position was: {self._player.get_global_position()}")
        print(f"i had {self._player.get_repository().get_parameter(PlayerRepository.ATTR_MASKS)} masks")
        print(f"i had {self._player.get_repository().get_parameter(PlayerRepository.ATTR_HEALTH)} hearths")

        pos, repo = self._checkpoint.get_player()
        repo.set_parameter(PlayerRepository.ATTR_HEALTH, 3)
        self._player.get_repository().load_checkpoint_status(repo)
        self._player.teleport(pos)
        print(f"Pos is: {pos}")

        print(f"Position is: {self._player.get_global_position()}")
        print(f"i have {self._player.get_repository().get_parameter(PlayerRepository.ATTR_MASKS)} masks")
        print(f"i have {self._player.get_repository().get_parameter(PlayerRepository.ATTR_HEALTH)} hearths")


    def set_player(self, player):
        self._player = player
        self._dynamic_sprites.add(player)

    def add_platform(self, platform):
        self._platforms.add(platform)
        self._static_sprites.add(platform)
        self._player.set_platform_group(self._platforms)
        for enemy in self._enemies:
            enemy.set_platform_group(self._platforms)
    def add_object(self, object):
        object.set_item_connector(self._static_sprites)
        object.set_player_connector(self._player)
        self._objects.add(object)
        self._static_sprites.add(object)
        self._player.set_item_group(self._objects)
        self._player.set_item_group(self._objects)
    def add_enemy(self, enemy):
        self._enemies.add(enemy)
        self._dynamic_sprites.add(enemy)
        self._player.set_enemy_group(self._enemies)
    def add_trigger(self, trigger):
        trigger.set_overlay_connector(self._static_sprites) #this is kinda wrong!
        self._triggers.add(trigger)
        self._static_sprites.add(trigger)
        self._player.set_trigger_group(self._triggers)

    # # TODO ELIMINAR ESTA MIERDA
    # def add_overlay_sprite(self, sprite):
    #     self._overlay_sprites.add(sprite)
    #
    # def del_overlay_sprite(self, sprite):
    #     self._overlay_sprites.remove(sprite)
