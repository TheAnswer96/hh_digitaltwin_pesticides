class Fruit:
    def __init__(self, id, seed, ripe_lifetime, bite_tolerance):
        self.id = id
        self.seed = seed
        self.ripe_lifetime = ripe_lifetime
        self.bite_tolerance = bite_tolerance

    def update_ripeness(self):
        self.ripe_lifetime -= 1

    def bite(self):
        self.bite_tolerance -= 1

    def is_rotten(self):
        return self.ripe_lifetime <= 0 or self.bite_tolerance <= 0