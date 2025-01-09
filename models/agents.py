from mesa import Agent

class HHBug(Agent):
    def __init__(self, unique_id, model, position):
        super().__init__(unique_id, model)
        self.position = position
        self.state = "alive"

    def move(self):
        """Move randomly within the grid."""
        possible_moves = self.model.grid.get_neighborhood(
            self.position, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)

    def apply_pesticide_effect(self, pesticides):
        """Apply the effects of pesticides."""
        for pesticide in pesticides:
            if pesticide.in_range(self.position):
                if pesticide.effect == "death":
                    self.state = "dead"
                elif pesticide.effect == "repulsion":
                    self.move()

    def step(self):
        """Single step behavior."""
        if self.state == "alive":
            self.move()
            self.apply_pesticide_effect(self.model.pesticides)

class PearTree(Agent):
    def __init__(self, position):
        super().__init__(unique_id=None, model=None)
        self.position = position
