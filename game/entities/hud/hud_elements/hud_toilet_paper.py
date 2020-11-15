from game.entities.hud.hud_element import HudElement


class HudToiletPaper(HudElement):
    X_SIZE = 46

    SPRITE_NAME = "hud_toilet_paper.png"

    def __init__(self, coords):
        HudElement.__init__(self, self.SPRITE_NAME, coords, self.X_SIZE, -1)
