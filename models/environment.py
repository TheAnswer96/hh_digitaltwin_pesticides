import json
from mesa.space import MultiGrid

class Environment:
    def __init__(self, field_size, pear_positions, meteorological_data):
        self.grid = MultiGrid(field_size[0], field_size[1], torus=False)
        self.field_size = field_size
        self.pear_positions = pear_positions
        self.meteorological_data = meteorological_data

    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            raise RuntimeError(f"Error loading {file_path}: {e}")

    @classmethod
    def from_json(cls, field_path, env_path):
        """Create an environment from JSON files."""
        field_data = cls.load_json(field_path)
        env_data = cls.load_json(env_path)

        return cls(
            field_size=field_data['size'],
            pear_positions=field_data['pear_positions'],
            meteorological_data=env_data['meteorological_data']
        )
