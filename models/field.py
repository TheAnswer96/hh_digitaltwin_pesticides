from .fruit import Fruit

class Field:
    def __init__(self, size, trees, weather):
        self.size = size  # (width, height)
        self.trees = trees  # List of tree objects
        self.weather = weather  # Dictionary with temperature, humidity, wind

    def get_fruits(self):
        fruits = []
        for tree in self.trees:
            fruits.extend(tree.fruits)
        return fruits

class Tree:
    def __init__(self, id, position, num_fruits):
        self.id = id
        self.position = position
        self.fruits = [Fruit(i, position) for i in range(num_fruits)]