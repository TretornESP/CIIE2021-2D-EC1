from ...util.log import Clog
from .hud_heart import HudHeart
from .hud_mask import HudMask

class Hud():

    X_OFFSET = 150
    Y_OFFSET = 80

    def __init__(self, player):
        self.log = Clog(__name__)
        self._player = player
        self._player.attach(self)
        self._hearts = []
        self._masks = []
        self._scene = None
        self._x_offset = Hud.X_OFFSET
        self._y_offset = Hud.Y_OFFSET

    def add_mask(self):
        self.log.debug("adding mask")
        mask = HudMask(self, (self._x_offset, self._y_offset))
        self._masks.append(mask)
        self._scene._overlay_sprites.add(mask)

    def remove_mask(self):
        self.log.debug("removing mask")
        if len(self._mask) > 0:
            element = self._masks.pop()
            self._scene._overlay_sprites.remove(element)

    def add_heart(self):
        self.log.debug("adding heart")
        heart = HudHeart(self, (self._x_offset, self._y_offset))
        self._hearts.append(heart)
        self._scene._overlay_sprites.add(heart)

    def remove_heart(self):
        self.log.debug("removing heart")
        if len(self._hearts) > 0:
            element = self._hearts.pop()
            self._scene._overlay_sprites.remove(element)

    def attach(self, scene):
        self._scene = scene
        for i in range(0, self._player._hp):
            self.add_heart()
        for i in range(0, self._player._masks):
            self.add_mask()

    # def move(self, offset):
    #     for heart in self._hearts:
    #         pos = heart.get_global_position()
    #         #heart.set_global_position((pos.left + offset[0], pos.bottom + offset[1]))
    #     for mask in self._masks:
    #         pos = mask.get_global_position()
    #         #mask.set_global_position((pos.left + offset[0], pos.bottom + offset[1]))
