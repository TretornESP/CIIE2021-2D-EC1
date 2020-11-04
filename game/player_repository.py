from pygame.locals import *


class PlayerRepository:

    # Default names (for not fucking up with typos)
    ATTR_HEALTH = "attr_health"
    ATTR_MASKS = "attr_masks"

    def __init__(self):
        self._data = {}

    def set_parameter(self, param_name, value):
        self._data[param_name] = value

    def get_parameter(self, param_name):
        if param_name not in self._data:
            return None
        else:
            return self._data[param_name]
