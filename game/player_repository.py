from pygame.locals import *


class PlayerRepository:
    DEFAULT_HEALTH = 3
    DEFAULT_MASKS = 2

    ATTR_HEALTH = "attr_health"
    ATTR_MASKS = "attr_masks"
    ATTR_TOILET_PAPER = "attr_toilet_paper"
    ATTR_POS = "attr_position" #TODO, los checkpoints deberían sacar de aqui la posicion!
    ATTR_TOTAL_TIME = "attr_total_time"

    def __init__(self):
        self._data = {}
        self.updated = []

    def reset_attr(self):
        self.set_parameter(PlayerRepository.ATTR_HEALTH, PlayerRepository.DEFAULT_HEALTH)
        self.set_parameter(PlayerRepository.ATTR_MASKS, PlayerRepository.DEFAULT_MASKS)
        self.set_parameter(PlayerRepository.ATTR_TOILET_PAPER, 0)

    def load_checkpoint_status(self, checkpoint):
        self.set_parameter(PlayerRepository.ATTR_HEALTH, checkpoint.get_parameter(PlayerRepository.ATTR_HEALTH))
        self.set_parameter(PlayerRepository.ATTR_MASKS, checkpoint.get_parameter(PlayerRepository.ATTR_MASKS))

    def set_parameter(self, param_name, value, accounted = True):
        if accounted:
            self.updated.append(param_name)
        self._data[param_name] = value

    def get_parameter(self, param_name):
        if param_name not in self._data:
            return None
        else:
            return self._data[param_name]
