from .character import Character
from ..player_repository import PlayerRepository
from .animated_text import AnimatedText
from game import ResourceManager
from ..farm import Farm
from .shot import Shot
import pygame


class Player(Character):
    PARRY_CD = 2
    PARRY_DUR = 0.5

    PARRY_ON = "Parry ON!"
    PARRY_OFF = "Parry OFF!"
    PARRY_TEXT = "Parry!"
    MASK_TEXT = "Mask!"
    HEART_TEXT = "Heart!"
    HIT_TEXT = "Damage!"

    MASK_COLOR = (0, 206, 209)
    PARRY_COLOR = (255, 165, 0)
    HIT_COLOR = (255, 0, 0)

    INVULNERABILITY_LAPSE = 2

    TRIGGER_HYST = 0.125

    def __init__(self, level, data, coord, speedx=25, speedy=40, invert=False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

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
        # Diría que no hace falta, ya que en ninguna parte del código se lee de este atributo del repositorio
        #self._repo.set_parameter(PlayerRepository.ATTR_POS, self._position, False)
        self._last_hit += elapsed_time
        self._parry += elapsed_time

        # DEBUG PRINT POSITION
        print(f"{self._position}")

        if self._parry >= Player.PARRY_DUR and not self._end_parry:
            self._end_parry = True
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_OFF, self._scroll, Player.PARRY_COLOR))

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

        self._interact = keys_pressed[interact]

    # esto no es responsabilidad del player
    def reset_hearts(self):
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, PlayerRepository.DEFAULT_HEALTH)

    def teleport(self, position):
        self.set_global_position(position)

    def hit(self):
        self._last_hit = 0
        current_health = self._repo.get_parameter(PlayerRepository.ATTR_HEALTH)
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, current_health - 1)

        pos = self._position[0], self._position[1] - self.rect.height
        self._text.add_sprite(AnimatedText(pos, Player.HIT_TEXT, self._scroll, Player.HIT_COLOR))

    def insta_kill(self):
        self._repo.set_parameter(PlayerRepository.ATTR_HEALTH, 0)

    def is_interacting(self):
        return self._interact

    def is_parrying(self):
        return self._parry < Player.PARRY_DUR

    def is_invulnerable(self):
        return self._last_hit < Player.INVULNERABILITY_LAPSE

    def end_parry(self):
        self._parry = Player.PARRY_DUR
        self._end_parry = True
        pos = self._position[0], self._position[1] - self.rect.height
        self._text.add_sprite(AnimatedText(pos, Player.PARRY_TEXT, self._scroll, Player.PARRY_COLOR))

    def pick_mask(self):
        pos = (self._position[0], self._position[1] - self.rect.height)
        self._text.add_sprite(AnimatedText(pos, Player.MASK_TEXT, self._scroll, Player.MASK_COLOR))
        current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
        self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks + 1)

    def do_parry(self):
        current_masks = self._repo.get_parameter(PlayerRepository.ATTR_MASKS)
        if self._parry >= Player.PARRY_CD and current_masks > 0:
            pos = self._position[0], self._position[1] - self.rect.height
            self._text.add_sprite(AnimatedText(pos, Player.PARRY_ON, self._scroll, Player.PARRY_COLOR))
            self._parry = 0
            self._end_parry = False
            self._repo.set_parameter(PlayerRepository.ATTR_MASKS, current_masks - 1)
