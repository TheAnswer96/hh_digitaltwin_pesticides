from models.twin import Simulation
from models.twin_exp import Twin

if __name__ == "__main__":
    # sim = Simulation()
    # sim.run()
    # TODO: randomize the wind
    # TODO: add a cycle for generating instances
    wind = {"direction": [1,0], "speed":5}
    DT = Twin(25, 24, 3, 5, wind)
