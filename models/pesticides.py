class Pesticide:
    def __init__(self, name, range, decay_rate, effect):
        self.name = name
        self.range = range
        self.decay_rate = decay_rate
        self.effect = effect
        self.current_effectiveness = 1.0

    def decay_effect(self):
        """Decay the pesticide's effectiveness over time."""
        self.current_effectiveness = max(0, self.current_effectiveness - self.decay_rate)

    def in_range(self, position):
        """Check if a position is within the pesticide's range."""
        # Example implementation: Define distance logic
        # For simplicity, assume (0,0) is the pesticide's source
        x, y = position
        distance = (x**2 + y**2)**0.5
        return distance <= self.range * self.current_effectiveness

    @staticmethod
    def load_from_json(file_path):
        """Load pesticides from a JSON file."""
        import json
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return [Pesticide(**p) for p in data]
        except Exception as e:
            raise RuntimeError(f"Error loading pesticides: {e}")
