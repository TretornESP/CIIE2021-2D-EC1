from game.entities.hud.hud_element import HudElement


class HudMask(HudElement):
    X_SIZE = 30

    SPRITE_NAME = "hud_mask.png"

    def __init__(self, coords):
        HudElement.__init__(self, self.SPRITE_NAME, coords, self.X_SIZE, -1)
