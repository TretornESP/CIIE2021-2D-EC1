from .hud_element import HudElement

class HudMask(HudElement):
    X_SIZE = 50
    X_OFFSET = 100
    Y_OFFSET = 40
    def __init__(self, parent, offset):
        print(f"{offset[0]} + {len(parent._masks)} * {HudMask.X_SIZE}")
        x = offset[0] + len(parent._masks)*HudMask.X_SIZE
        HudElement.__init__(self, parent._player._level, "mask_hud.png", (x+HudMask.X_OFFSET, offset[1]+HudMask.Y_OFFSET))
