from pygame.locals import *
import copy
class CheckpointRepository:

    PLAYER_POSITION = "player_position"
    PLAYER_REPOSITORY = "player_repository"

    def __init__(self):
        self._data = {}
        self.updated = []
        self._player_pos = None
        self._player_repo = None
        self._scroll = 0

    def reset_attr(self):
        pass

    def set_player(self, player):
        self.set_parameter(CheckpointRepository.PLAYER_REPOSITORY, player.get_repository())
        self.set_parameter(CheckpointRepository.PLAYER_POSITION, player._position)

    def get_player(self):
        if CheckpointRepository.PLAYER_POSITION not in self._data or CheckpointRepository.PLAYER_REPOSITORY not in self._data:
            return None
        else:
            return (self._data[CheckpointRepository.PLAYER_POSITION], self._data[CheckpointRepository.PLAYER_REPOSITORY])


    def set_parameter(self, param_name, value):
        self.updated.append(param_name)
        self._data[param_name] = copy.deepcopy(value)

    def get_parameter(self, param_name):
        if param_name not in self._data:
            return None
        else:
            return self._data[param_name]

    def set_scroll(self, scroll):
        self._scroll = scroll

    def get_scroll(self):
        return self._scroll
