from .fruit import Fruit

class Tree:
    def __init__(self, id, position, shade_factor, fruits):
        self.id = id
        self.position = tuple(position)
        self.shade_factor = shade_factor
        self.fruits = [Fruit(**fruit) for fruit in fruits]