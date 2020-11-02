import pygame

from ...util.log import Clog


class Hud:

    # Alignments (it is important not changing these values)
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

        # Ok we might need this later
        self._sprite_groups = []
        self._hearts = []
        self._masks = []
        self._scene = None

        # Set hud offsets
        self._x_min_offset = self._X_TOTAL*self.X_RELATIVE_LEFT_OFFSET/100
        self._y_min_offset = self._Y_TOTAL*self.Y_RELATIVE_TOP_OFFSET/100
        self._x_max_offset = self._X_TOTAL - self._X_TOTAL*self.X_RELATIVE_RIGHT_OFFSET/100
        self._y_max_offset = self._Y_TOTAL - self._Y_TOTAL*self.Y_RELATIVE_BOTTOM_OFFSET/100

        # DEBUG print(f"{self._x_min_offset} {self._y_min_offset} {self._x_max_offset} {self._y_max_offset}")

    # Attach HUD to scene
    def attach(self, scene):
        self._scene = scene

    # Create zone
    #  hud_element: Hud element component of the group
    #  coords: Relative to the HUD offset: (x_%_start, y_%_start)
    #  spacing: Spacing from starting side of drawing
    # Returns:
    #  identifier: identifier given to the sprite group
    def create_hud_group(self, hud_element, coords, alignment, spacing):
        my_dict = {
            "hud_element": hud_element,
            "coords": coords,
            "alignment": alignment,
            "spacing": spacing,
            "count": 0
        }
        self._sprite_groups.append(my_dict)
        return len(self._sprite_groups)-1

    # # Returns MUTABLE sprite group
    # def get_sprite_group(self, identifier):
    #     if not self._sprite_groups:
    #         return self._sprite_groups[identifier]
    #     else:
    #         return None

    def add_element(self, identifier):
        if not self._sprite_groups:
            raise RuntimeError("Sprite list is empty")

        my_element = self._sprite_groups[identifier]

        self.log.debug(f'[NEW] Adding {my_element["hud_element"].__name__}!')
        my_element["count"] += 1

        # Horizontal alignment
        if abs(my_element["alignment"]) < 2:
            coord_x = self._x_min_offset+((abs(self._x_min_offset-self._x_max_offset))*my_element["coords"][0]/100) + my_element["spacing"]*my_element["alignment"]*my_element["count"]
            coord_y = self._y_min_offset+((abs(self._y_min_offset-self._y_max_offset))*my_element["coords"][1]/100)
        else:
            coord_x = self._x_min_offset+((abs(self._x_min_offset-self._x_max_offset))*my_element["coords"][0]/100)
            coord_y = self._y_min_offset+((abs(self._y_min_offset-self._y_max_offset))*my_element["coords"][1]/100) + my_element["spacing"]*(my_element["alignment"]>>1)*my_element["count"]

        element = self._sprite_groups[identifier]["hud_element"]((coord_x, coord_y))

        self._scene.add_overlay_sprite(element)




    #
    # def add_mask(self):
    #     self.log.debug("adding mask")
    #     mask = HudMask(self, (self._x_offset, self._y_offset))
    #     self._masks.append(mask)
    #     self._scene._overlay_sprites.add(mask)
    #
    # def remove_mask(self):
    #     self.log.debug("removing mask")
    #     if len(self._mask) > 0:
    #         element = self._masks.pop()
    #         self._scene._overlay_sprites.remove(element)
    #
    # def add_heart(self):
    #     self.log.debug("adding heart")
    #     heart = HudHeart(self, (self._x_offset, self._y_offset))
    #     self._hearts.append(heart)
    #     self._scene._overlay_sprites.add(heart)
    #
    # def remove_heart(self):
    #     self.log.debug("removing heart")
    #     if len(self._hearts) > 0:
    #         element = self._hearts.pop()
    #         self._scene._overlay_sprites.remove(element)
    #
    # def attach(self, scene):
    #     self._scene = scene
    #     for i in range(0, self._player._hp):
    #         self.add_heart()
    #     for i in range(0, self._player._masks):
    #         self.add_mask()

    # def move(self, offset):
    #     for heart in self._hearts:
    #         pos = heart.get_global_position()
    #         #heart.set_global_position((pos.left + offset[0], pos.bottom + offset[1]))
    #     for mask in self._masks:
    #         pos = mask.get_global_position()
    #         #mask.set_global_position((pos.left + offset[0], pos.bottom + offset[1]))
