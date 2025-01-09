from models.environment import Environment
from models.pesticides import Pesticide
from models.agents import HHBug
from models.simulation import Simulation

def main():
    # Load environment and pesticides
    environment = Environment.from_json("json/field.json", "json/environment.json")
    pesticides = Pesticide.load_from_json("json/pesticides.json")

    # Initialize simulation
    # simulation = Simulation(environment, pesticides)
    #
    # # Add HH bugs
    # for i, position in enumerate(environment.load_json("json/environment.json")['HH_positions']):
    #     bug = HHBug(unique_id=i, model=simulation, position=tuple(position))
    #     simulation.add_bug(bug)
    #
    # # Run simulation
    # print("Running simulation...")
    # for _ in range(10):  # Run for 10 steps
    #     simulation.step()
    # print("Simulation complete.")

if __name__ == "__main__":
    main()
