import json
import os


class SimulationLoader:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.environment = None
        self.bugs = []
        self.trees = []
        self.pesticides = []

    def load_json(self, filename):
        """Helper function to load JSON files."""
        file_path = os.path.join(self.data_folder, filename)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {filename} not found in {self.data_folder}.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Failed to parse {filename}. Ensure valid JSON format.")
            return None

    def load_environment(self):
        """Loads the environment configuration from JSON."""
        data = self.load_json("environment.json")
        if data:
            self.environment = {
                "size": tuple(data["size"]),
                "climate_data": data["climate_data"],
                "time_of_day": data["time_of_day"],
                "season": data["season"],
                "simulation_days": data["simulation_days"],
                "seconds_per_step": data["seconds_per_step"]
            }
            print("Environment loaded successfully.")

    def load_bugs(self):
        """Loads bugs data from JSON."""
        data = self.load_json("bugs.json")
        if data:
            self.bugs = [{
                "id": bug["id"],
                "seed": bug["seed"],
                "lifetime": bug["lifetime"],
                "stage": bug["stage"],
                "position": tuple(bug["position"])
            } for bug in data]
            print(f"Loaded {len(self.bugs)} bugs.")

    def load_trees(self):
        """Loads trees and fruits from JSON."""
        data = self.load_json("trees.json")
        if data:
            for tree in data:
                tree_obj = {
                    "id": tree["id"],
                    "position": tuple(tree["position"]),
                    "shade_factor": tree["shade_factor"],
                    "fruits": [{
                        "id": fruit["id"],
                        "seed": fruit["seed"],
                        "ripe_lifetime": fruit["ripe_lifetime"],
                        "bite_tolerance": fruit["bite_tolerance"]
                    } for fruit in tree["fruits"]]
                }
                self.trees.append(tree_obj)
            print(f"Loaded {len(self.trees)} trees.")

    def load_pesticides(self):
        """Loads pesticide data from JSON."""
        data = self.load_json("pesticides.json")
        if data:
            self.pesticides = [{
                "id": pesticide["id"],
                "position": tuple(pesticide["position"]),
                "initial_radius": pesticide["initial_radius"],
                "max_radius": pesticide["max_radius"],
                "decay_factor": pesticide["decay_factor"],
                "mortality_probability": pesticide["mortality_probability"],
                "repulsion_probability": pesticide["repulsion_probability"],
            } for pesticide in data]
            print(f"Loaded {len(self.pesticides)} pesticides.")

    def load_all(self):
        """Loads all simulation data."""
        print("\nLoading simulation data...")
        self.load_environment()
        self.load_bugs()
        self.load_trees()
        self.load_pesticides()
        print("All data loaded successfully.\n")

    def get_simulation_data(self):
        """Returns all loaded data."""
        return {
            "environment": self.environment,
            "bugs": self.bugs,
            "trees": self.trees,
            "pesticides": self.pesticides
        }
