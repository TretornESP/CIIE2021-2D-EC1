import copy
import pygame

class Director:
    def __init__(self):
        self._scene_stack = []
        self._end_scene = False
        self._clock = pygame.time.Clock()

    def set_checkpoint(self):
        if (len(self._scene_stack) > 0):
            try:
                self._scene_stack[len(self._scene_stack) - 1].set_checkpoint()
            except Exception:
                pass

    def run_checkpoint(self):
        if (len(self._scene_stack) > 1):
            if self._scene_stack[len(self._scene_stack) - 2].run_checkpoint():
                self.end_scene()

    def execute(self):
        pygame.init()
        pygame.mixer.init()
        while (len(self._scene_stack) > 0):
            scene = self._scene_stack[len(self._scene_stack) - 1]
            self._game_loop(scene)
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
        else:
            self.push_scene(scene)
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

    def debug(self, level):
        current = self._scene_stack[len(self._scene_stack) - 1]
        for scene in level.get_scenes():
            if scene.get_id() == current.get_id():
                scr = current.get_scroll_x()
                scene.set_checkpoint(scr)
                self.push_scene(scene)
                self.run_checkpoint()

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
            scene.draw_fps(self._clock.get_fps())


            pygame.display.flip()
