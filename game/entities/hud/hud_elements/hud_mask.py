from game.entities.hud.hud_element import HudElement

class HudMask(HudElement):
    X_SIZE = 30

    SPRITE_NAME = "mask_hud.png"

    # def __init__(self, parent, offset):
    #     print(f"{offset[0]} + {len(parent._masks)} * {HudMask.X_SIZE}")
    #     x = offset[0] + len(parent._masks)*HudMask.X_SIZE
    #     HudElement.__init__(self, parent._player._level, "mask_hud.png", (x+HudMask.X_OFFSET, offset[1]+HudMask.Y_OFFSET))

    def __init__(self, coords):
        #print(f"[HudMask] at {coords}")
        # TODO De-hardcodear el nivel (o no) (es que que los sprites del HUD cambien dependiendo del nivel, en nuestro caso es un poco innecesario)
        HudElement.__init__(self, "Level0", self.SPRITE_NAME, coords, self.X_SIZE, -1)
