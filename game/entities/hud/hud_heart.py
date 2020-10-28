from .hud_element import HudElement

class HudHeart(HudElement):
    X_SIZE = 50
    def __init__(self, parent, offset):
        print(f"{offset[0]} + {len(parent._hearts)} * {HudHeart.X_SIZE}")
        x = offset[0] + len(parent._hearts)*HudHeart.X_SIZE
        HudElement.__init__(self, parent._player._level, "heart_hud.png", (x, offset[1]))
