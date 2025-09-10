import random
import math


class Fruit:
    def __init__(self, id, ripe_lifetime, ripeness, bite_tolerance):
        self.id = id
        self.ripeness = ripeness
        self.ripe_lifetime = ripe_lifetime  # Days until overripe
        self.bite_tolerance = bite_tolerance  # How many bites before inedible
        self.bug_punctures = 0  # Track punctures
        self.bug_positions = []  # Store bug positions
        self.rotten = False  # Initial state

    def update_ripeness(self, temperature, humidity):
        if temperature > 30:  # High temperatures speed up ripening
            self.ripe_lifetime -= 2
        elif temperature < 10:  # Cold slows down ripening
            self.ripe_lifetime -= 0.5
        else:
            self.ripe_lifetime -= 1

        if humidity > 80:  # High humidity increases bug activity
            self.bug_punctures += 1

            # If too many punctures or ripe lifetime is over, pear rots
        if self.ripe_lifetime <= 0 or self.bug_punctures > self.bite_tolerance:
            self.rotten = True

    def puncture_by_bug(self, bug_x, bug_y, pear_x, pear_y, range_radius=2):
        """
        Checks if a bug is close enough to puncture the pear.
        If within range, it has a probability (60%) of puncturing.
        """
        distance = math.sqrt((bug_x - pear_x) ** 2 + (bug_y - pear_y) ** 2)

        if distance <= range_radius:  # Bug is close enough
            if random.random() < 0.6:  # 60% chance to puncture
                self.bug_punctures += 1
                self.bug_positions.append((bug_x, bug_y))


    def is_rotten(self):
        """Checks if the pear is rotten."""
        return self.rotten

    def __str__(self):
        return (f"Pear {self.id}: Ripe lifetime {self.ripe_lifetime}, "
                f"Bite tolerance {self.bite_tolerance}, Bug punctures {self.bug_punctures}, "
                f"Rotten: {self.rotten}, Bug Positions: {self.bug_positions}")

    def get_csv_row(self):
        return [self.id, self.ripe_lifetime, self.bite_tolerance, self.bug_punctures, self.rotten]
