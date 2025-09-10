import os.path

from .fruit import Fruit
from .pesticide import Pesticide
from .tree import Tree
from .environment import Environment
from .bug import Bug
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')
#######################################################################################################################
# The measurements are in meters, and grams
# everytime you invoke a map reader you will obtain the cell of the grid with indexes [int(x), int(y)]
#######################################################################################################################

class Twin:
    def __init__(self, env_params, bug_params, tree_params, pesticide_params):
        # index of the date
        self.idx = env_params['starting_date']
        self.sequence_length = env_params['sequence_length']
        self.time_step = env_params['time_step']
        #input data for the environment
        self.temp_csv = pd.read_csv(os.path.join("weather-forecasting", "data", "temperature_all.csv"))
        self.hum_csv = pd.read_csv(os.path.join("weather-forecasting", "data", "humidity_all.csv"))
        temperatures, humidities = self.get_climate()
        # Current date and time is inside environment; for changes consider to port here such field
        self.env = Environment((100, 100),
                               [[1, 3], [1, 30], [1, 60], [1, 90],
                                [30, 3], [30, 30], [30, 60], [30, 90],
                                [60, 3], [60, 30], [60, 60], [60, 90], [90, 3]],
                               temperatures,
                               humidities,
                               env_params['wind']
                               )
        #env ==========================================================================

        #input pesticides
        # Pesticidi in posizione alberi
        # alternatani
        # 
        self.n_pesticide = pesticide_params['number']
        # quantity of 1 KG partitioned by n_pesticide
        self.pesticides = []
        for idx in range(len(pesticide_params['positions'])):
            x = pesticide_params['positions'][idx][0]
            y = pesticide_params['positions'][idx][0]
            pest = Pesticide(idx, "Fenpropathrin", [x, y], pesticide_params['initial_radius'], pesticide_params['quantity'])
            self.pesticides.append(pest)
        #pesticide ========================================================================

        # bug =============================================================================
        #def __init__(self, id, lifetime, stage, position, maximum_step):
        #input bugs
        self.n_bugs = bug_params['number']
        self.bugs = []
        for i in range(self.n_bugs):
            x = np.random.uniform(0, self.env.get_size()[0])
            y = np.random.uniform(0, self.env.get_size()[1])
            bug = Bug(i, 100, 2, [x,y], 1)
            self.bugs.append(bug)
        # bug =============================================================================

        # tree ============================================================================
        # Each plant is 4 meters far from its next
        self.n_tres = tree_params['number']
        self.trees = []
        for idx in range(len(tree_params['positions'])):
            x = tree_params['positions'][idx][0]
            y = tree_params['positions'][idx][1]
            #TODO: generatio semi-real on the base of the season for the fruits
            n_fruits = np.random.randint(0, tree_params['max_pears'])
            pears = []
            for j in range(n_fruits):
                pear = Fruit(j * tree_params['max_pears']^i, 1, np.random.uniform(0, 1), 5)
                pears.append(pear)
            tree = Tree(i, [x, y], 1, pears)
            self.trees.append(tree)
        # tree ============================================================================

    def get_climate(self):
        temp = []
        hum = []
        self.temp_csv["year"] = self.temp_csv["year"] - 2000
        self.hum_csv["year"] = self.hum_csv["year"] - 2000
        v_col = [f"value_{i}" for i in range(0, 13)]
        if self.idx >= self.sequence_length:
            # data series from temp
            temp = self.temp_csv[v_col + ["year", "month", "day", "hour"]].values
            temp = temp[self.idx - self.sequence_length:self.idx]
            #data series hum
            hum = self.hum_csv[v_col + ["year", "month", "day", "hour"]].values
            hum = hum[self.idx - self.sequence_length:self.idx]
        return np.array(temp), np.array(hum)

    def check_pesticide(self):
        state = False
        idx = 0
        while not state and idx < self.n_pesticide:
            state = state or (self.pesticides[idx].quantity != 0)
            idx = idx + 1
        return state

    def run(self):
        instants = 60 // self.time_step # tune it to have more steps

        hours = 0
        deads = 0
        lefts = 0
        max_rad = 0

        while (self.check_pesticide() and self.n_bugs > 0): #regular condition
        # while (self.check_pesticide()): #for pesticide evaluation
            # timestep per bugs
            for i in range(instants):
                # print(f"instant: {i}")
                print(f"Time [hh:mm]: {hours}:{i * self.time_step}")
                # print(f"--- Pesticides ---")

                for pesticide in self.pesticides:
                    # print(pesticide.position)
                    pesticide.spread(self.env.get_wind_direction(), self.env.get_wind_speed(),
                                     self.env.get_temperature_at(pesticide.position[0], pesticide.position[1]),
                                     self.env.get_humidity_at(pesticide.position[0], pesticide.position[1]),
                                     self.time_step
                                     )
                    # add here info on pesticide
                    # add here code for saving results
                    max_rad = max(max_rad, pesticide.radius)
                    # print(f"pesticide {pesticide.id} -> position: {pesticide.position}, quantity: {pesticide.quantity} g, rad: {pesticide.radius}")
                    bug2delete = []
                    for idx in range(len(self.bugs)):
                        if pesticide.affects_bug(self.bugs[idx]):
                            bug2delete.append(idx)
                            deads = deads + 1
                            # print(f"HH {idx} is dead. We are safer.")
                    self.bugs = [i for j, i in enumerate(self.bugs) if j not in bug2delete]
                    self.n_bugs = len(self.bugs)
                bug2delete = []
                # print(f"--- Bugs ---")
                for idx in range(len(self.bugs)):
                    self.bugs[idx].move(self.env, self.trees, self.bugs, self.pesticides)
                    # add here info on bugs
                    # add here code for saving results
                    # print(f"bug {self.bugs[idx].id}-> position {self.bugs[idx].position}")
                    if self.bugs[idx].position[0] > self.env.size[0] or self.bugs[idx].position[0] < 0 or self.bugs[idx].position[1] > self.env.size[1] or self.bugs[idx].position[1] < 0:
                        bug2delete.append(idx)
                        lefts = lefts + 1
                        # print(f"HH {idx} outside the field. We are safer.")
                self.bugs = [i for j, i in enumerate(self.bugs) if j not in bug2delete]
                self.n_bugs = len(self.bugs)
                # print(f"Bugs alive: {self.n_bugs}")
            # one hour is passed-> update environment
            # print(f"hour done.")
            self.env.update_conditions()
            # print("--- Environment ---")
            # self.env.get_info()
            # self.env.save_all_heatmaps()
            hours += 1

        results = {
            'bugs_survived': self.n_bugs,
            'bugs_escaped': lefts,
            'bug_deads': deads,
            'pesticide_decay': hours,
            'pesticide_radius': max_rad
        }
        return results