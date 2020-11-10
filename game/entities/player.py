from .character import Character
from game import Configuration, ResourceManager
from ..player_repository import PlayerRepository
from ..util.log import Clog
from .object import Object
from .animated_text import AnimatedText
from ..farm import Farm
import pygame


class Player(Character):
    PARRY_CD = 2
    PARRY_DUR = 0.5
    PARRY_ON = "Parry ON!"
    PARRY_OFF = "Parry OFF!"

    PARRY_TEXT = "Parry!"
    MASK_TEXT = "Mask!"
    HEART_TEXT = "Heart!"
    INTERACT_TEXT = "Press E to interact!"

    INVULNERABILITY_LAPSE = 2

    TRIGGER_HYST = 0.125

    def __init__(self, level, data, coord, speedx=25, speedy=40, invert=False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)
        self.log = Clog(__name__)

        self._repo = ResourceManager.get_player_repository()
        self._text = ResourceManager.get_text_repository()

        self._last_hit = Player.INVULNERABILITY_LAPSE
        self._parry = Player.PARRY_CD

        self._end_parry = True

        self._pending_trigger = None
        self._last_triggered = Player.TRIGGER_HYST
        self._interact_last_displayed = AnimatedText.get_duration()
        self._interact = False

    def get_repository(self):
        return self._repo

    def set_repository(self, repo):
        self._repo = repo

    def update(self, elapsed_time):
        Character.update(self, elapsed_time)
        self._repo.set_parameter(PlayerRepository.ATTR_POS, self._position, False)
        self._last_hit += elapsed_time
        self._parry += elapsed_time

        if self._parry >= Player.PARRY_DUR and not self._end_parry:
            self._end_parry = True
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_OFF, self._scroll))

        enemy = Farm.enemy_collision(self)
        if (enemy != None):
            if self._parry < Player.PARRY_DUR:
                enemy.kill()
                self._parry = Player.PARRY_DUR
                self._end_parry = True
                pos = self._position[0], self._position[1] - self.rect.height
                self._text.add_sprite(AnimatedText(pos, Player.PARRY_TEXT, self._scroll))
            elif self._last_hit > Player.INVULNERABILITY_LAPSE:
                self.hit()
                self._last_hit = 0

        item = Farm.item_collision(self)
        if (item != None):
            item.collect()

        trigger = Farm.trigger_collision(self) #TODO
        if (trigger != None):
            if trigger.can_interact():
                if self._interact:
                    if not trigger.event(True):
                        self._last_triggered = 0
                        self._pending_trigger = trigger
                elif self._interact_last_displayed > AnimatedText.get_duration():
                    pos = (trigger._position[0], trigger._position[1] - trigger.rect.height)
                    self._text.add_sprite(AnimatedText(pos, Player.INTERACT_TEXT, self._scroll))
                    self._interact_last_displayed = 0
                else:
                    self._interact_last_displayed += elapsed_time
            else:
                if not trigger.event():
                    self._last_triggered = 0
                    self._pending_trigger = trigger
        else:
            if self._pending_trigger != None and self._last_triggered > Player.TRIGGER_HYST:
                self._pending_trigger.revive()
                self._pending_trigger = None
                self._last_triggered = 0
            else:
                self._last_triggered += elapsed_time

    def move(self, keys_pressed, up, down, left, right, parry, dash, interact):
        if keys_pressed[up[0]] or keys_pressed[up[1]]:
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
        Character.move(self, (x, y))

        if keys_pressed[parry]:
            self.do_parry()

        if keys_pressed[dash]:
            Character.do_dash(self)

        self._interact = keys_pressed[interact] #maybe this belongs inside a function, i dont really care

    def reset_hearts(self):
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, PlayerRepository.DEFAULT_HEALTH)

    def teleport(self, position):
        self.set_global_position(position) # This doesnt work!

    def hit(self):
        current_health = self._repo.get_parameter(PlayerRepository.ATTR_HEALTH)
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, current_health - 1)

    def picked_item(self, item):
        if item == Object.MASK:
            pos = (self._position[0], self._position[1] - self.rect.height)
            self._text.add_sprite(AnimatedText(pos, Player.MASK_TEXT, self._scroll))
            current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
            self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks + 1)

    def do_parry(self):
        current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
        if self._parry >= Player.PARRY_CD and current_masks > 0:
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_ON, self._scroll))
            self._parry = 0
            self._end_parry = False
            self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks - 1)
