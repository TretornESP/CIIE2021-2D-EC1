from .character import Character
from game import Configuration, ResourceManager
from ..player_repository import PlayerRepository
from ..util.log import Clog
from .object import Object
import pygame


class Player(Character):
    INVULNERABILITY_LAPSE = 2

    def __init__(self, level, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self.log = Clog(__name__)

        self.player_repo = ResourceManager.get_player_repository()
        self.player_repo.set_parameter(PlayerRepository.ATTR_HEALTH, 3)
        self.player_repo.set_parameter(PlayerRepository.ATTR_MASKS, 1)

        self._hp = 3
        self._masks = 0
        self._last_hit = 0

    def hit(self):
        self._hp = self._hp - 1
        #if self._hud != None:
            #self._hud.remove_heart()
        #TODO: Update animation as untouchable

    def picked_item(self, item):
        if item==Object.MASK:
            self._masks = self._masks + 1 # revisar si esto es necesario

            self.player_repo.set_parameter(PlayerRepository.ATTR_MASKS, self.player_repo.get_parameter(PlayerRepository.ATTR_MASKS) + 1)
            self.player_repo.set_parameter(PlayerRepository.ATTR_MASKS, self.player_repo.get_parameter(PlayerRepository.ATTR_MASKS) + 1)
            self.player_repo.set_parameter(PlayerRepository.ATTR_MASKS, self.player_repo.get_parameter(PlayerRepository.ATTR_MASKS) + 1)

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        self._last_hit = self._last_hit + elapsed_time

        if (self._enemies != None):
            enemy = pygame.sprite.spritecollideany(self, self._enemies) #TODO
            if (enemy != None):
                if self._last_hit > Player.INVULNERABILITY_LAPSE:
                    self.log.debug("Player hit!")
                    self.hit()
                    self._last_hit = 0

        if (self._items != None):
            item = pygame.sprite.spritecollideany(self, self._items) #TODO
            if (item != None):
                self._items.remove(item)
                item.collect()

        if (self._triggers != None):
            trigger = pygame.sprite.spritecollideany(self, self._triggers) #TODO
            if (trigger != None):
                 trigger.event()
                 self._triggers.remove(trigger)

    def move(self, keys_pressed, up, down, left, right):
        if keys_pressed[up]:
            y = Character.UP
        elif keys_pressed[down]:
            y = Character.DOWN
        else:
            y = Character.STILL

        if keys_pressed[left]:
            x = Character.LEFT
        elif keys_pressed[right]:
            x = Character.RIGHT
        else:
            x = Character.STILL
        Character.move(self, (x,y))
