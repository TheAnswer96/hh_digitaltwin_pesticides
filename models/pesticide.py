class Pesticide:
    def __init__(self, id, position, initial_radius, max_radius, decay_factor, mortality_probability, repulsion_probability):
        self.id = id
        self.position = tuple(position)
        self.radius = initial_radius
        self.max_radius = max_radius
        self.decay_factor = decay_factor
        self.mortality_probability = mortality_probability
        self.repulsion_probability = repulsion_probability


    def spread(self, wind_direction, wind_speed):
        if self.radius < self.max_radius:
            self.radius += self.wind_influence["speed"]

    def affects_bug(self, bug):
        return bug.get_distance(self.position) < self.radius