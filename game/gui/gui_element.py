class GUIElement:
    def __init__(self, screen, rect):
        self._screen = screen
        self.rect = rect

    def set_pos(self, pos):
        self.rect.left = pos[0]
        self.rect.bottom = pos[1]

    def pos_in_element(self, pos):
        (pos_x, pos_y) = pos
        return (pos_x >= self.rect.left and pos_x <= self.rect.right
                and pos_y >= self.rect.top and pos_y <= self.rect.bottom)

    def draw(self, screen):
        raise NotImplemented()

    def callback(self):
        raise NotImplemented()
