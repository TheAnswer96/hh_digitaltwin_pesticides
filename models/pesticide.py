import numpy as np


class Pesticide:
    def __init__(self, id, name, position, initial_radius, quantity):
        self.id = id
        self.name = name
        self.position = np.array(position)  # Use NumPy for easier vector calculations
        self.radius = initial_radius
        self.quantity = quantity  # Total amount of pesticide released (g)

        # Fenpropathrin-specific properties (values derived from literature)
        self.decay_factor = 0.0025  # Decay rate per second
        self.mortality_probability = 0.8  # Probability of killing an insect upon exposure
        self.repulsion_probability = 0.6  # Probability of repelling an insect upon exposure
        # self.density = 1.2  # Approximate density in g/m³ (assumed)

    def spread(self, wind_direction, wind_speed, temperature, humidity, time_step):
        """Simulates Fenpropathrin dispersion over a given time step based on wind, diffusion, temperature, and humidity effects."""
        if self.quantity > 0:
            # Wind-driven movement (m)
            # wind_vector = np.array([np.cos(wind_direction), np.sin(wind_direction)])
            # delta = np.array(wind_direction) * wind_speed * time_step
            # self.position = np.ndarray.tolist(np.array(self.position) + delta)

            # Turbulent diffusion effect (m)
            diffusion_factor = np.sqrt(time_step)  # Approximate turbulent diffusion behavior

            # Temperature and humidity influence on spread
            temp_factor = 1 + 0.02 * (temperature - 25)  # Warmer temperatures increase spread
            humidity_factor = 1 - 0.004 * humidity  # High humidity slows dispersion
            spread_rate = wind_speed * time_step * 0.15 * temp_factor * humidity_factor + diffusion_factor
            self.radius += spread_rate

            # decay based on environmental factors
            self.quantity *= np.exp(-self.decay_factor * time_step * temp_factor * humidity_factor)

            # End of effect condition: If quantity is too low, consider pesticide dissipated
            if self.quantity < 0.01:
                self.quantity = 0

    def get_concentration(self, point):
        """Computes Fenpropathrin concentration at a given point based on a Gaussian model."""
        if self.quantity == 0:
            return 0  # No effect if the pesticide has dissipated

        distance = np.linalg.norm(np.array(point) - np.array(self.position))
        if distance > self.radius:
            return 0  # No effect outside dispersion radius

        sigma = self.radius / 2  # Spread factor (m)
        return (self.quantity / (2 * np.pi * sigma ** 2)) * np.exp(-distance ** 2 / (2 * sigma ** 2))  # g/m³

    def affects_bug(self, bug):
        """Determines if a bug is affected based on the pesticide concentration."""
        concentration = self.get_concentration(bug.position)
        mortalty_rate = concentration * self.mortality_probability
        outcome = mortalty_rate > np.random.rand()
        # print(f"concentration: {mortalty_rate}, outcome: {outcome}")
        return outcome

