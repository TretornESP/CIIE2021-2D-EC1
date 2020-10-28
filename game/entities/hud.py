class hud():
    def __init__(self, player):
        self._player = player
        self._elements = []
        for i in player._hp:
            self.add_heart()

    def add_heart(self):
        pass
    def remove_heart(self):
        pass

    def attach(self, group):
        for element int self._elements:
            if element not in group:
                group.add(element)
