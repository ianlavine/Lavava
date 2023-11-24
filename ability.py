from constants import *

class Ability:

    def __init__(self, key, validation_func, click_count, box, return_func=None, click_type=NODE):
        self.key = key
        self.validation_func = validation_func
        self.click_count = click_count
        self.box = box
        self.return_func = return_func
        self.click_type = click_type
        self.clicks = []

    def wipe(self):
        self.clicks = []

    def complete_check(self):
        return len(self.clicks) == self.click_count

    def validate(self, item):
        return self.validation_func(self.clicks + [item])

    def complete(self, item):
        self.clicks.append(item)
        if self.complete_check():
            clicks = self.clicks
            self.wipe()
            if self.return_func:
                return self.return_func(clicks)
            return clicks
        return False