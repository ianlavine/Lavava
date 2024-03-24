# from abc import ABC, abstractmethod

class AbstractAbilityManager():
    def __init__(self, abilities, default_color):
        self.abilities = abilities
        self.default_color = default_color
        self.mode = None
        self.clicks = set()
        self.hovering = None

    def set_hover(self, item):
        self.hovering = item

    def use_ability(self, item, color):
        if not self.ability:
            return False
        if self.ability.click_type == item.type and self.box_col == color:
            self.clicks.add(item)
            if self.complete_check():
                clicks = self.clicks
                self.wipe()
                return clicks
            return False
        return False
    
    def wipe(self):
        self.clicks = set()

    def switch_to(self, key):
        self.mode = key
        return self.complete_check()
    
    def complete_check(self):
        return self.ability.click_count == len(self.clicks)

    def select(self, key):
        if self.ability:
            self.abilities[self.mode].wipe()
        if self.mode == key:
            self.mode = None
        elif self.abilities[key].selectable:
            return self.switch_to(key)
        return False
    
    def validate(self, item):
        if item.type == self.ability.click_type:
            if self.ability.validation_func(self.clicks.union({item})):
                return item, self.ability.visual.color
        return False

    @property
    def ability(self):
        if not self.mode:
            return None
        return self.abilities[self.mode]
 
    @property
    def box_col(self):
        if not self.ability:
            return self.default_color
        return self.ability.box.color

 
# class MoneyAbilityManager(AbstractAbilityManager):

#     def select(self, key):
#         if self.ability:
#             self.abilities[self.mode].wipe()
#         if self.mode == key:
#             self.mode = None
#         elif CONTEXT["main_player"].money >= self.costs[key]:
#             return self.switch_to(key)
#         return False

#     def update_ability(self):
#         CONTEXT["main_player"].money -= self.costs[self.mode]
#         if (
#             self.costs[self.mode] > CONTEXT["main_player"].money
#             or self.mode == RAGE_CODE
#         ):
#             self.mode = None

#     @property
#     def display_nums(self):
#         return self.costs


# class ReloadAbilityManager(AbstractAbilityManager):



#     def update_ability(self):
#         self.load_count[self.mode] = 0
#         self.remaining_usage[self.mode] -= 1
#         self.mode = None

#     def full(self, key):
#         return self.load_count[key] >= self.full_reload[key]
    
#     def percent_complete(self, key): 
#         return min(1, self.load_count[key] / self.full_reload[key])
        
#     @property
#     def display_nums(self):
#         return self.remaining_usage
