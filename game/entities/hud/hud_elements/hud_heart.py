from game.entities.hud.hud_element import HudElement

class HudHeart(HudElement):
    X_SIZE = 30

    SPRITE_NAME = "heart_hud.png"

    def __init__(self, coords):
        #print(f"[HudHeart] at {coords}")
        # TODO De-hardcodear el nivel (o no) (es que que los sprites del HUD cambien dependiendo del nivel, en nuestro caso es un poco innecesario)
        HudElement.__init__(self, "Level0", self.SPRITE_NAME, coords, self.X_SIZE, -1)
