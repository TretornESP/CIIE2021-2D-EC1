import pygame
from .configuration import Configuration

class Director:
    def __init__(self):
        self._scene_stack = []
        self._end_scene = False
        self._clock = pygame.time.Clock()

    def execute(self):
        pygame.init()

        self._screen = pygame.display.set_mode(Configuration().get_resolution())
        pygame.display.set_caption(Configuration().get_name())

        while (len(self._scene_stack) > 0):
            scene = self._scene_stack[len(self._scene_stack) - 1]
            self._game_loop(scene)

        pygame.quit()

    def end_scene(self):
        self._end_scene = True

        if (len(self._scene_stack) > 0):
            self._scene_stack.pop()

    def change_scene(self, scene):
        self.end_scene()
        self._scene_stack.append(scene)

    def push_scene(self, scene):
        self._end_scene = True
        self._scene_stack.append(scene)

    def quit_game(self):
        self._end_scene = True
        self._scene_stack = []

    def _game_loop(self, scene):
        pygame.event.clear()

        self._end_scene = False
        while not self._end_scene:
            elapsed_time = self._clock.tick(60)
            elapsed_time = elapsed_time / 1000

            scene.events(pygame.event.get())
            scene.update(elapsed_time)
            scene.draw()

            pygame.display.flip() 
