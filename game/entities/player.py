from .character import Character

class Player(Character):
    def __init__(self, level, data, coord, speedx = 25, speedy = 40, invert = False):
        Character.__init__(self, level, data, coord, invert, speedx, speedy)

    def move(self, keys_pressed, up, down, left, right):
        if keys_pressed[up]:
            Character.move(self, Character.UP)
        elif keys_pressed[down]:
            Character.move(self, Character.DOWN)
        elif keys_pressed[left]:
            Character.move(self, Character.LEFT)
        elif keys_pressed[right]:
            Character.move(self, Character.RIGHT)
        else:
            Character.move(self, Character.STILL)
