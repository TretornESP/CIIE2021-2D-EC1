import pygame
from .configuration import Configuration
from .resource_manager import ResourceManager
from .memory_manager import MemoryManager
from .util import Clog
import copy
class Director:
    def __init__(self):
        self._log = Clog(__name__)
        self._scene_stack = []
        self._end_scene = False
        self._clock = pygame.time.Clock()


    def set_checkpoint(self):
        if (len(self._scene_stack) > 0):
            self._scene_stack[len(self._scene_stack) - 1].set_checkpoint()

    def run_checkpoint(self):
        if (len(self._scene_stack) > 1):
            if self._scene_stack[len(self._scene_stack) - 2].run_checkpoint():
                self.end_scene()

    def execute(self):
        pygame.init()
        pygame.mixer.init()
        mm = MemoryManager(10)
        mm.start()
        while (len(self._scene_stack) > 0):
            scene = self._scene_stack[len(self._scene_stack) - 1]
            self._game_loop(scene)
        mm.stop()
        pygame.quit()

    def end_scene(self):
        self._end_scene = True

        if (len(self._scene_stack) > 0):
            self._scene_stack.pop()

    def insert_scene(self, scene):
        if (len(self._scene_stack) > 0):
            context = self._scene_stack[len(self._scene_stack) - 1]
            self._scene_stack[len(self._scene_stack) - 1] = scene
            self.push_scene(context)

            self._log.debug(f"Size is {len(self._scene_stack)}")

        else:
            self._log.info("Incorrect use of insert_scene")
            self.push_scene(scene)

        self._log.debug("You'll all hail hitler")
        self._end_scene = True

    def pop_scene(self):
        if (len(self._scene_stack) > 0):
            return self._scene_stack.pop()
        return None

    def change_scene(self, scene):
        self.end_scene()
        self._scene_stack.append(scene)

    def push_scene(self, scene):
        self._end_scene = True
        self._scene_stack.append(scene)

    def quit_game(self):
        self._end_scene = True
        self._scene_stack = []

    def flush_scene(self):
        while (len(self._scene_stack) > 1):
            self._scene_stack.pop()
        self._end_scene = True

    def _game_loop(self, scene):
        pygame.event.clear()

        self._end_scene = False
        scene.start_scene()
        while not self._end_scene:
            elapsed_time = self._clock.tick(60)
            elapsed_time /= 1000

            scene.events(pygame.event.get())
            scene.update(elapsed_time)
            scene.draw()

            pygame.display.flip()
