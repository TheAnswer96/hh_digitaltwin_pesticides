import random
import time
from .io.loader import SimulationLoader
from .bug import Bug
from .tree import Tree
from .pesticide import Pesticide
from .environment import Environment

class Simulation:

    def __init__(self, data_folder="data"):
        self.loader = SimulationLoader(data_folder)
        self.loader.load_all()

        self.environment = Environment(
            size=self.loader.environment["size"],
            climate_data=self.loader.environment["climate_data"],
            time_of_day=self.loader.environment["time_of_day"],
            season=self.loader.environment["season"],
            simulation_days=self.loader.environment["simulation_days"],
            seconds_per_step=self.loader.environment["seconds_per_step"]
        )

        # Initialize agents dynamically
        self.bugs = [Bug(**bug_data) for bug_data in self.loader.bugs]
        self.trees = [Tree(**tree_data) for tree_data in self.loader.trees]
        self.pesticides = [Pesticide(**pest_data) for pest_data in self.loader.pesticides]

        # Initialize simulation clock
        self.current_time = 0
        self.day_count = 0
        self.history = {"bug_deaths": 0, "bug_positions": [], "fruit_decay": []}

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
                    if bug.is_near(tree.position, 2):  # 2 unit distance threshold
                        if random.random() < 0.3:  # 30% chance bug eats fruit
                            fruit.bite()

                if fruit.is_rotten():
                    self.history["fruit_decay"].append((self.current_time, fruit.id))
                    tree.fruits.remove(fruit)  # Remove decayed fruit

    def spread_pesticides(self):
        for pesticide in self.pesticides:
            pesticide.spread()

            for bug in self.bugs[:]:
                if pesticide.affects_bug(bug):
                    if random.random() < pesticide.mortality_probability:
                        self.history["bug_deaths"] += 1
                        self.bugs.remove(bug)

    def run(self):
        total_seconds = self.environment.simulation_days * 86400
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

