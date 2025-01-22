import json

class SimulationLogger:
    """Logs important events during the simulation."""

    def __init__(self):
        self.logs = []

    def record(self, message):
        self.logs.append(message)

    def save_to_file(self, filename="simulation_log.json"):
        with open(filename, "w") as file:
            json.dump(self.logs, file, indent=4)