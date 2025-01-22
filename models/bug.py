import random
import math

class Bug:
    def __init__(self, id, seed, lifetime, stage, position):
        self.id = id
        self.seed = seed
        self.lifetime = lifetime
        self.stage = stage
        self.position = tuple(position)

    def move(self, environment, trees):
        # Bug attracted by warm temperature, light, and fruit
        # Bug repelled by pesticides

        fruit_attraction = 0

        temp_effect = environment.get_temperature_at(self.position[0], self.position[1]) / 30 # Normalize to 0-1 -- put maximum temperature
        light_effect = environment.get_light_at(self.position[0], self.position[1]) / 100 # Normalize to 0-1 -- put maximum light intensity

        for tree in trees:
            for fruit in tree.fruits:
                distance = self.get_distance(tree.position)
                if distance < 10:
                    fruit_attraction += 1 / (distance + 1)

        dx = random.randint(-1, 1) * (1 + temp_effect + light_effect + fruit_attraction)
        dy = random.randint(-1, 1) * (1 + temp_effect + light_effect + fruit_attraction)
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def is_near(self, point, threshold):
        return self.get_distance(point) < threshold

    def get_distance(self, point):
        return math.sqrt((self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2)