import random
import time
from .io.loader import SimulationLoader
from .bug import Bug
from .tree import Tree
from .pesticide import Pesticide
from .environment import Environment
import numpy as np

class Simulation:

    def __init__(self, data_folder="data"):
        self.loader = SimulationLoader(data_folder)
        self.loader.load_all()

        self.environment = Environment(
            size=self.loader.environment["size"],
            climate_data=self.loader.environment["climate_data"],
            time_of_day=self.loader.environment["time_of_day"],
            month=self.loader.environment["month"],
            year=self.loader.environment["year"],
            simulation_days=self.loader.environment["simulation_days"],
            seconds_per_step=self.loader.environment["seconds_per_step"]
        )

        # Initialize agents dynamically
        self.bugs = [Bug(**bug_data) for bug_data in self.loader.bugs]
        self.trees = [Tree(**tree_data) for tree_data in self.loader.trees]
        self.pesticides = [Pesticide(**pest_data) for pest_data in self.loader.pesticides]

        # All objects
        self.objects = self.bugs + self.trees + self.pesticides
        self.num_objects = len(self.objects)

        # Initialize simulation clock
        self.current_time = 0
        self.day_count = 0
        self.history = {"bug_deaths": 0, "bug_positions": [], "fruit_decay": []}

        # position and distance
        self.positions = np.array([obj.position for obj in self.objects])
        self.distance_matrix = self.compute_distance_matrix()

        # Encode mapping
        self.name2idx_dict = {f"{obj.__class__.__name__.lower()}{obj.id}": idx for idx, obj in enumerate(self.objects)}
        self.idx2name_dict = {idx: f"{obj.__class__.__name__.lower()}{obj.id}" for idx, obj in enumerate(self.objects)}

    def compute_distance_matrix(self):
        dists = np.linalg.norm(self.positions[:, np.newaxis] - self.positions, axis=2)
        return dists

    def update_environment(self):
        self.environment.update_conditions(self.current_time)

    def move_bugs(self):
        for bug in self.bugs:
            bug.move(self.environment, self.trees)
            self.history["bug_positions"].append((self.current_time, bug.id, bug.position))

    def update_fruits(self):
        for tree in self.trees:
            for fruit in tree.fruits[:]:
                fruit.update_ripeness()

                for bug in self.bugs:
                    fruit.puncture_by_bug(bug.position[0], bug.position[1], tree.position[0], tree.position[1], 2)
                # print results here on a CSV

                if fruit.is_rotten():
                    self.history["fruit_decay"].append((self.current_time, fruit.id))
                    tree.fruits.remove(fruit)  # Remove decayed fruit

    def spread_pesticides(self):
        for pesticide in self.pesticides:
            pesticide.spread(self.environment.get_wind_direction(), self.environment.get_wind_speed())

            for bug in self.bugs[:]:
                if pesticide.affects_bug(bug):
                    self.history["bug_deaths"] += 1
                    self.bugs.remove(bug)

    def run(self):
        total_seconds = self.environment.simulation_days * 24
        print("Simulation started...")

        while self.current_time < total_seconds:
            self.update_environment()
            self.move_bugs()
            self.update_fruits()
            self.spread_pesticides()

            self.current_time += self.environment.seconds_per_step

            if self.current_time % 86400 == 0:
                self.day_count += 1
                print(f"Day {self.day_count} completed.")

        print("Simulation completed.")
        print(f"Total bugs died: {self.history['bug_deaths']}")
        print(f"Fruit decay events: {len(self.history['fruit_decay'])}")

