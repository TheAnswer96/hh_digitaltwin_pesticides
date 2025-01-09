from mesa import Model

from .agents import PearTree
import mesa

class Simulation(Model):
    def __init__(self, environment, pesticides):
        super().__init__()
        self.environment = environment
        self.pesticides = pesticides
        # self.schedule = RandomActivation(self)

        # Add pear trees
        for position in environment.pear_positions:
            tree = PearTree(position)
            self.environment.grid.place_agent(tree, position)

    def add_bug(self, bug):
        """Add an HH bug to the environment."""
        self.schedule.add(bug)
        self.environment.grid.place_agent(bug, bug.position)

    def step(self):
        """Advance the simulation by one step."""
        self.schedule.step()
        for pesticide in self.pesticides:
            pesticide.decay_effect()
