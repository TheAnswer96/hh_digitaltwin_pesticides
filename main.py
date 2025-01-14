from models.bug import Bug
from models.fruit import Fruit
from models.field import Field, Tree
from models.pesticide import Pesticide
import json
import logging
import time


class Simulation:
    def __init__(self, config_path, field_path, pesticide_path):
        self.config_path = config_path
        self.field_path = field_path
        self.pesticide_path = pesticide_path
        self.load_simulation()

        # Clock initialization
        self.current_hour = 0
        self.current_minute = 0

        # Set up logging
        logging.basicConfig(filename="simulation.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        logging.info("Simulation initialized.")

    def load_simulation(self):
        """Load the initial configuration for the simulation."""
        # Load configurations
        config = self.load_config(self.config_path)
        field_data = self.load_config(self.field_path)
        pesticide_data = self.load_config(self.pesticide_path)

        # Create field, bugs, and pesticides
        self.field = Field(field_data["size"], [Tree(**tree) for tree in field_data["trees"]], field_data["weather"])
        self.bugs = [Bug(**bug) for bug in config["bugs"]]
        self.pesticides = [Pesticide(**pesticide) for pesticide in pesticide_data]
        self.simulation_days = config["simulation_days"]
        self.running = True

    @staticmethod
    def load_config(file_path):
        """Load configuration JSON from a file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def advance_time(self):
        """Advance the clock by one minute."""
        self.current_minute += 1
        if self.current_minute >= 60:
            self.current_minute = 0
            self.current_hour += 1
        if self.current_hour >= 24:
            self.current_hour = 0

    def get_formatted_time(self):
        """Get the current time as a formatted string."""
        return f"{self.current_hour:02}:{self.current_minute:02}"

    def print_summary(self):
        """Print a summary of the simulation status."""
        alive_bugs = [bug for bug in self.bugs if bug.alive]
        fruits = self.field.get_fruits()
        ripe_fruits = [fruit for fruit in fruits if fruit.is_ripe and not fruit.is_eaten]
        unripe_fruits = [fruit for fruit in fruits if not fruit.is_ripe and not fruit.is_eaten]
        eaten_fruits = [fruit for fruit in fruits if fruit.is_eaten]

        current_time = self.get_formatted_time()
        print(f"Time: {current_time}")
        print("=" * 20)
        print(f"Environment: Temperature={self.field.weather['temperature']}°C, "
              f"Humidity={self.field.weather['humidity'] * 100}%, Wind={self.field.weather['wind']} km/h")
        print(f"Bugs: Alive={len(alive_bugs)}, Positions={[bug.position for bug in alive_bugs]}")
        print(f"Fruits: Ripe={len(ripe_fruits)}, Unripe={len(unripe_fruits)}, Eaten={len(eaten_fruits)}")
        print(f"Pesticides: Remaining={len(self.pesticides)} (effectiveness varies)")
        print("=" * 20)

    def log_agent_status(self):
        """Log the status of each agent to the log file."""
        current_time = self.get_formatted_time()
        logging.info(f"Time {current_time}: Simulation status update.")

        # Log bugs
        for bug in self.bugs:
            status = "alive" if bug.alive else "dead"
            logging.info(f"Bug {bug.id}: Position={bug.position}, Status={status}")

        # Log fruits
        for fruit in self.field.get_fruits():
            status = "ripe" if fruit.is_ripe else "unripe"
            status += ", eaten" if fruit.is_eaten else ", uneaten"
            logging.info(f"Fruit {fruit.id}: Position={fruit.position}, Status={status}")

        # Log pesticides
        for pesticide in self.pesticides:
            logging.info(f"Pesticide {pesticide.id}: Repulsion force={pesticide.repulsion_force}, "
                         f"Remaining effect={pesticide.remaining_effect}")

    def simulate_minute(self):
        """Simulate a single minute of activity."""
        if not self.running:
            return

        # Update fruits
        for fruit in self.field.get_fruits():
            fruit.ripen()

        # Update bugs
        for bug in self.bugs:
            if not bug.alive:
                continue
            fruits = self.field.get_fruits()
            if fruits:
                closest_fruit = min(fruits, key=lambda f: (f.position[0] - bug.position[0]) ** 2 + (f.position[1] - bug.position[1]) ** 2)
                bug.move_towards(closest_fruit.position)
                bug.interact_with_fruit(closest_fruit)

            # Check if the bug is out of the field bounds
            if not (0 <= bug.position[0] < self.field.size[0] and 0 <= bug.position[1] < self.field.size[1]):
                bug.alive = False

        # Apply pesticides
        for bug in self.bugs:
            for pesticide in self.pesticides:
                bug.interact_with_pesticide({"fatality_rate": pesticide.fatality_rate, "repulsion_force": pesticide.repulsion_force})

        # Update pesticide state
        for pesticide in self.pesticides:
            pesticide.decay()

        # Print and log status
        self.print_summary()
        self.log_agent_status()

        # Advance the clock
        self.advance_time()

    def run(self):
        """Run the simulation."""
        while True:
            alive_bugs = [bug for bug in self.bugs if bug.alive]
            if not alive_bugs:
                print(f"Simulation ended at {self.get_formatted_time()} as all bugs are dead or have exited the field.")
                logging.info(f"Simulation ended at {self.get_formatted_time()} as all bugs are dead or have exited the field.")
                break
            self.simulate_minute()
            time.sleep(1)  # Simulate real time

        print("Simulation completed.")
        logging.info("Simulation completed.")


if __name__ == "__main__":
    sim = Simulation("data/config.json", "data/field.json", "data/pesticides.json")
    sim.run()
