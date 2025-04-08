import os.path

from .fruit import Fruit
from .pesticide import Pesticide
from .tree import Tree
from .environment import Environment
from .bug import Bug
import pandas as pd
import numpy as np

#######################################################################################################################
# The measurements are in meters, and grams
# everytime you invoke a map reader you will obtain the cell of the grid with indexes [int(x), int(y)]
#######################################################################################################################

class Twin:
    def __init__(self, idx, sequence_length, n_bugs, n_pesticide, n_trees, max_n_pears, wind):
        # index of the date
        self.idx = idx
        self.sequence_length = sequence_length
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
                               wind
                               )
        #env ==========================================================================

        #input pesticides
        self.n_pesticide = n_pesticide
        self.pesticides = []
        for i in range(self.n_pesticide):
            x = np.random.uniform(0, self.env.get_size()[0])
            y = np.random.uniform(0, self.env.get_size()[1])
            pest = Pesticide(i, "Fenpropathrin", [x, y], 1, 200)
            self.pesticides.append(pest)
        #pesticide ========================================================================

        # bug =============================================================================
        #def __init__(self, id, lifetime, stage, position, maximum_step):
        #input bugs
        self.n_bugs = n_bugs
        self.bugs = []
        for i in range(self.n_bugs):
            x = np.random.uniform(0, self.env.get_size()[0])
            y = np.random.uniform(0, self.env.get_size()[1])
            bug = Bug(i, 100, 2, [x,y], 1)
            self.bugs.append(bug)
        # bug =============================================================================

        # tree ============================================================================
        self.n_tres = n_trees
        self.trees = []
        for i in range(self.n_tres):
            x = np.random.uniform(0, self.env.get_size()[0])
            y = np.random.uniform(0, self.env.get_size()[1])
            #TODO: generatio semi-real on the base of the season for the fruits
            n_fruits = np.random.uniform(0, max_n_pears)
            pears = []
            for j in range(n_fruits):
                pear = Fruit(j*max_n_pears^i, 1, np.random.uniform(0, 1), 5)
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

    def run(self):
        #TODO: for loop to move bug every X minutes and update the climate everyhour + save results
        return