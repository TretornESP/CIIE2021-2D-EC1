class DialogOption:
    def __init__(self, text, valid):
        self._text = text
        self._valid = valid
    def get_text(self):
        return self._text
    def is_valid(self):
        return self._valid
