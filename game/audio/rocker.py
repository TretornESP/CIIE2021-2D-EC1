from .. import ResourceManager
import os
import pygame

class Rocker:
    AUD_HIT = "hit.wav"
    AUD_WIN = "victory.wav"
    AUD_DEFEAT = "defeat.wav"
    AUD_PICK = "pick.wav"
    AUD_HEART = "heart.wav"
    AUD_TALK = "talk.wav"
    AUD_JUMP = "jump.wav"
    AUD_DASH = "dash.wav"
    AUD_PARRY = "shield.wav"

    INIT = False

    @classmethod
    def background(cls, song):
        if not cls.INIT:
            pygame.mixer.init()
            cls.INIT = True
        path = os.path.abspath(os.getcwd()) #THIS FORBIDS YOU TO DO CD DURING THE CODE FLOW: BEWARE
        path = os.path.join(path, "game", "assets", "music", song)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(e)

    @classmethod
    def action(cls, action):
        ResourceManager.play_sound(os.path.join("sfx",str(action)))
