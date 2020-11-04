import pygame

from ... import ResourceManager
from ...util.log import Clog


class Hud:

    # Alignments (it is important not changing these values)
    # REALLY, DO *NOT* CHANGE THESE
    GROW_LEFT = -1
    GROW_RIGHT = 1
    GROW_UP = -2
    GROW_DOWN = 2

    # Relative offsets in %
    X_RELATIVE_LEFT_OFFSET = 6
    X_RELATIVE_RIGHT_OFFSET = 0 # To be changed if necessary
    Y_RELATIVE_TOP_OFFSET = 8
    Y_RELATIVE_BOTTOM_OFFSET = 0 # TBC

    def __init__(self):
        # Get screen res
        self._X_TOTAL = pygame.display.Info().current_w
        self._Y_TOTAL = pygame.display.Info().current_h

        # Init log and so
        self.log = Clog(__name__)

        # wth this bullshit
        # self._player = player
        # self._player.attach(self)

        # We store here the sprite groups
        self._sprite_groups = {}
        self._sprite_group = pygame.sprite.Group()

        # Set hud offsets
        self._x_min_offset = self._X_TOTAL*self.X_RELATIVE_LEFT_OFFSET/100
        self._y_min_offset = self._Y_TOTAL*self.Y_RELATIVE_TOP_OFFSET/100
        self._x_max_offset = self._X_TOTAL - self._X_TOTAL*self.X_RELATIVE_RIGHT_OFFSET/100
        self._y_max_offset = self._Y_TOTAL - self._Y_TOTAL*self.Y_RELATIVE_BOTTOM_OFFSET/100

        # DEBUG print(f"{self._x_min_offset} {self._y_min_offset} {self._x_max_offset} {self._y_max_offset}")

    # Attach HUD to scene
    # def attach(self, scene):
    #     self._scene = scene

    # Create zone
    #  hud_element: Hud element component of the group
    #  coords: Relative to the HUD offset: (x_%_start, y_%_start)
    #  spacing: Spacing from starting side of drawing
    def create_hud_group(self, param_name, hud_element, coords, alignment, spacing):
        self._sprite_groups[param_name] = {
            "hud_element": hud_element,
            "coords": coords,
            "alignment": alignment,
            "spacing": spacing,
            "count": 0
        }

    def update(self):
        pl_repo = ResourceManager.get_player_repository()
        for param_name in pl_repo.updated:
            pl_repo.updated.remove(param_name)
            self._sprite_groups[param_name]["count"] = pl_repo.get_parameter(param_name)

    def draw(self, screen):
        for key in self._sprite_groups:
            for local_offset in range(0, self._sprite_groups[key]["count"]):
                if abs(self._sprite_groups[key]["alignment"]) < 2:
                    coord_x = self._x_min_offset + (
                                (abs(self._x_min_offset - self._x_max_offset)) * self._sprite_groups[key]["coords"][0] / 100) + \
                              self._sprite_groups[key]["spacing"] * self._sprite_groups[key]["alignment"] * local_offset

                    coord_y = self._y_min_offset + (
                                (abs(self._y_min_offset - self._y_max_offset)) * self._sprite_groups[key]["coords"][1] / 100)
                else:
                    coord_x = self._x_min_offset + (
                                (abs(self._x_min_offset - self._x_max_offset)) * self._sprite_groups[key]["coords"][0] / 100)

                    coord_y = self._y_min_offset + (
                                (abs(self._y_min_offset - self._y_max_offset)) * self._sprite_groups[key]["coords"][1] / 100) + \
                              self._sprite_groups[key]["spacing"] * (self._sprite_groups[key]["alignment"] >> 1) * local_offset

                element = self._sprite_groups[key]["hud_element"]((coord_x, coord_y))
                element.draw(screen)
