import math
import random


class Bug:
    def __init__(self, id, lifetime, stage, position, maximum_step):
        self.id = id
        self.lifetime = lifetime #currently not employed since no lifecycle is considered
        self.stage = stage #currently not employed since no lifecycle is considered
        self.position = tuple(position)
        # Maximum movement length in meters
        self.L_max = maximum_step # meter
        # Small constant to avoid division by zero
        self.epsilon = 1e-6

        # Parameters for temperature-based movement probability
        self.p_max = 0.9  # Maximum probability at optimal temperature
        self.p_min = 0.2  # Minimum probability far from optimal
        self.T_opt = 22  # Optimal temperature (°C)
        self.sigma = 3  # Spread of the temperature response

    def temperature_movement_probability(self, environment):
        # Get the temperature at the bug's current position
        T = environment.get_temperature_at(self.position[0], self.position[1])
        # Compute movement probability using a Gaussian function
        p_move = self.p_min + (self.p_max - self.p_min) * math.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2))
        return p_move

    def move(self, environment, trees, other_bugs, sensors, pesticides):
        # Initialize the net movement vector (Mx, My)
        Mx, My = 0, 0

        # --- Attractors ---
        # Fruit attraction: iterate over trees and fruits
        for tree in trees:
            for fruit in tree.fruits:
                # Each fruit has a ripeness factor (e.g., 0 to 1)
                ripeness = fruit.ripe_lifetime
                fruit_pos = fruit.position
                dx = fruit_pos[0] - self.position[0]
                dy = fruit_pos[1] - self.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                weight = ripeness / (distance + self.epsilon)
                Mx += weight * dx
                My += weight * dy

        # Attraction to other bugs
        for other in other_bugs:
            if other.id != self.id:
                dx = other.position[0] - self.position[0]
                dy = other.position[1] - self.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                weight = 0.5 / (distance + self.epsilon)
                Mx += weight * dx
                My += weight * dy

        # Attraction to sensors with higher temperature
        for sensor in sensors:
            sensor_pos = sensor.position
            temp = sensor.temperature  # Sensor temperature
            dx = sensor_pos[0] - self.position[0]
            dy = sensor_pos[1] - self.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            weight = (temp / 30) / (distance + self.epsilon)  # Normalize with a max temp assumption (e.g., 30°C)
            Mx += weight * dx
            My += weight * dy

        # --- Repellents ---
        # Pesticide repulsion
        for pesticide in pesticides:
            pesticide_pos = pesticide.position
            strength = pesticide.strength
            dx = pesticide_pos[0] - self.position[0]
            dy = pesticide_pos[1] - self.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            weight = strength / (distance + self.epsilon)
            Mx -= weight * dx
            My -= weight * dy

        # Compute the net movement vector's magnitude
        M_norm = math.sqrt(Mx ** 2 + My ** 2)
        if M_norm > 0:
            # Normalize the net movement vector
            unit_Mx = Mx / M_norm
            unit_My = My / M_norm

            # Get the temperature-dependent movement probability
            move_prob = self.temperature_movement_probability(environment)
            if random.random() < move_prob:
                # The bug moves up to L_max centimeters along the computed direction.
                dx_move = self.L_max * unit_Mx
                dy_move = self.L_max * unit_My
                self.position = (self.position[0] + dx_move, self.position[1] + dy_move)
        # If no net vector is computed, the bug stays in place

    def get_distance(self, point):
        return math.sqrt((self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2)
