from game.entities.hud.hud_element import HudElement


class HudHeart(HudElement):
    X_SIZE = 30

    SPRITE_NAME = "hud_heart.png"

    def __init__(self, coords):
        HudElement.__init__(self, "shared", self.SPRITE_NAME, coords, self.X_SIZE, -1)
