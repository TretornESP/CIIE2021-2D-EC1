from .character import Character

class Player(Character):
    def __init__(self):
        Character.__init__(self, "player.png", (0, 300), 25, 40)

    def move(self, keys_pressed, up, down, left, right):
        if keys_pressed[up]:
            Character.move(self, Character.UP)
        elif keys_pressed[left]:
            Character.move(self, Character.LEFT)
        elif keys_pressed[right]:
            Character.move(self, Character.RIGHT)
        else:
            Character.move(self, Character.STILL)
