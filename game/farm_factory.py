from .farm import Farm

class FarmFactory:
    def __init__(self):
        self._player = None
        self._enemies = []
        self._platforms = []
        self._items = []
        self._triggers = []

    def set_player(self, player):
        self._player = player

    def add_enemy(self, enemy):
        self._enemies.append(enemy)
    def add_object(self, object):
        self._items.append(object)
    def add_trigger(self, trigger):
        self._triggers.append(trigger)
    def add_platform(self, platform):
        self._platforms.append(platform)

    def push_to_charge(self): #https://imgur.com/a/QsoIxuz
        Farm.push_to_close()

        Farm.spawn_player(self._player)
        for enemy in self._enemies:
            Farm.add_enemy(enemy)
        for item in self._items:
            Farm.add_object(item)
        for trigger in self._triggers:
            Farm.add_trigger(trigger)
        for platform in self._platforms:
            Farm.add_platform(platform)
