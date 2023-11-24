from constants import LETTER_TO_CODE, BREAKDOWNS
class PowerBox:

    def __init__(self, name, color, shape, letter=None):
        self.name = name
        self.color = color
        self.shape = shape
        self.letter = letter
        if letter is None:
            self.letter = name[0]
        self.stat_func = None

    def set_stat_func(self, stat_func):
        self.stat_func = stat_func

    @property
    def display_num(self):
        if self.stat_func is None:
            return BREAKDOWNS[LETTER_TO_CODE[self.letter]]['cost']
        return self.stat_func()