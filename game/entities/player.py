from .character import Character

class Player(Character):
    def __init__(self, level, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

    def move(self, keys_pressed, up, down, left, right):
        if keys_pressed[up]:
            y = Character.UP
        elif keys_pressed[down]:
            y = Character.DOWN
        else:
            y = Character.STILL

        if keys_pressed[left]:
            x = Character.LEFT
        elif keys_pressed[right]:
            x = Character.RIGHT
        else:
            x = Character.STILL

        Character.move(self, (x,y))
