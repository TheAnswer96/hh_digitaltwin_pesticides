class Pesticide:
    def __init__(self, diffusion_rate, decay_rate, fatality_rate, repulsion_force):
        self.id = 0
        self.diffusion_rate = diffusion_rate
        self.decay_rate = decay_rate
        self.fatality_rate = fatality_rate
        self.repulsion_force = repulsion_force  # (dx, dy)

    def decay(self):
        self.diffusion_rate *= (1 - self.decay_rate)
        self.fatality_rate *= (1 - self.decay_rate)