class Rocker:
    AUD_HIT = 0x0
    AUD_WIN = 0x1
    AUD_LOST = 0x2
    AUD_PICK = 0x3
    AUD_HEART = 0x4
    AUD_TALK = 0x5
    AUD_JUMP = 0x6
    AUD_DASH = 0x7
    AUD_PARRY = 0x8

    def __init__(self):
        self._background = None

    def set_background(self, song):
        pass

    def add_effect(self, song):
        pass

    def stop_effects(self, song):
