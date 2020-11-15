from threading import Timer
from .farm import Farm

class MemoryManager(object):
    def __init__(self, interval):
        self._timer     = None
        self.interval   = interval
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        Farm.free_killed_sprites()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
