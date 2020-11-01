from .gui_element import GUIElement

class TextGUI(GUIElement):
    def __init__(self, screen, font, color, text, pos):
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()

        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        
        GUIElement.__init__(self, screen, self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
