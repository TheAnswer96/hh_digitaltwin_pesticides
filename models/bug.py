import random
import math

class Bug:
    def __init__(self, id, position, attraction_range=10, lifespan=30):
        self.id = id
        self.position = position  # (x, y) tuple
        self.lifespan = lifespan  # days left to live
        self.attraction_range = attraction_range
        self.alive = True

    def move_towards(self, target_position):
        if not self.alive:
            return
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.position = (
                self.position[0] + dx / distance,
                self.position[1] + dy / distance,
            )

    def interact_with_fruit(self, fruit):
        if not self.alive or not fruit.is_ripe:
            return
        fruit.degrade()
        if random.random() < 0.1:  # 10% chance of dying after eating
            self.alive = False

    def interact_with_pesticide(self, pesticide_effect):
        if not self.alive:
            return
        if random.random() < pesticide_effect["fatality_rate"]:
            self.alive = False
        else:
            self.position = (
                self.position[0] + pesticide_effect["repulsion_force"][0],
                self.position[1] + pesticide_effect["repulsion_force"][1],
            )

    def age(self):
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.alive = False