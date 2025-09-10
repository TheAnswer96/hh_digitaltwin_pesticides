from models.twin import Simulation
from models.twin_exp import Twin
import pandas as pd
import random
import math
import numpy as np
import os
import time

def generate_wind_conditions():
    """
    Generate realistic random wind conditions.
    Returns:
        direction (tuple): Unit vector (x, y) representing wind direction.
        speed (float): Wind speed in m/s.
    """
    # Random direction in 2D (angle in radians)
    angle = random.uniform(0, 2 * math.pi)
    direction = [math.cos(angle), math.sin(angle)]  # Unit vector

    # Realistic wind speed: most often between 1 and 15 m/s
    # We'll use a Weibull distribution to simulate typical wind speed distribution
    k = 2.0  # Shape parameter (typical for many locations)
    lam = 6.0  # Scale parameter (mean wind speed around 5-7 m/s)

    speed = random.weibullvariate(lam, k)

    return direction, speed

def pesticide_test():
    save_path = os.path.join('output', 'pesticide_exp.csv')  # Change this path accordingly

    # === Prepare the results DataFrame ===
    df = pd.DataFrame(columns=['index', 'quantity', 'radius_mean', 'radius_std', 'hours_mean', 'hours_std'])

    # === Fixed parameters ===
    tree_parameters = {'number': 1, 'max_pears': 10, 'positions': [[50, 50]]}
    bugs_parameters = {'number': 1}

    # === List of quantities to test ===
    quantities = [1, 100, 200, 300, 500, 800, 1000]
    indexes = [0, 1, 2, 3, 4, 5, 6]
    for quantity in quantities:
        print(f"================== TEST PESTICIDE: quantity = {quantity} ==================")
        pesticide_parameters = {'quantity': quantity, 'initial_radius': 1, 'number': 1, 'positions': [[50, 50]]}

        radius_list = []
        hours_list = []

        for i in range(13):
            np.random.seed(i)
            random.seed(i)
            print(f"Iteration {i} starting...")
            d, s = generate_wind_conditions()
            wind = {"direction": d, "speed": s}
            environment_parameters = {'starting_date': 25, 'sequence_length': 24, 'time_step': 10, 'wind': wind}

            DT = Twin(environment_parameters, bugs_parameters, tree_parameters, pesticide_parameters)
            results = DT.run()

            radius_list.append(results['pesticide_radius']/1000)
            hours_list.append(results['pesticide_decay'])
            print(f"Iteration {i} ended.")
        # Compute stats
        radius_mean = np.mean(radius_list)
        radius_std = np.std(radius_list)
        hours_mean = np.mean(hours_list)
        hours_std = np.std(hours_list)

        # Append to DataFrame
        df.loc[len(df)] = [quantity, radius_mean, radius_std, hours_mean, hours_std]

    # === Save DataFrame to CSV ===
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)

# === Helper to index into grid ===
def get_grid_index(row, col, total_cols):
    return row * total_cols + col

# === Function to construct pesticide parameters based on layout ===
def make_pesticide_parameters(layout, quantity, rows, cols, grid):
    pos_layout = []
    if layout == 0:
        # === Layout 1: Checkerboard (even rows AND odd columns) ===
        pos_layout = []
        for r in range(rows):
            for c in range(cols):
                if r % 2 == 0 and c % 2 == 1:
                    idx = get_grid_index(r, c, cols)
                    pos_layout.append(grid[idx])
    if layout == 1:
        # === Layout 2: Alternate Full Rows (e.g., rows 0, 2, 4...) ===
        pos_layout = []
        for r in range(rows):
            if r % 2 == 0:
                for c in range(cols):
                    idx = get_grid_index(r, c, cols)
                    pos_layout.append(grid[idx])
    if layout == 2:
        # === Layout 3: Alternate Full Columns (e.g., columns 0, 2, 4...) ===
        pos_layout = []
        for r in range(rows):
            for c in range(cols):
                if c % 2 == 0:
                    idx = get_grid_index(r, c, cols)
                    pos_layout.append(grid[idx])

    return {
        'quantity': quantity / len(pos_layout),
        'initial_radius': 1,
        'number': len(pos_layout),
        'positions': pos_layout
    }

def pesticide_layout():
    rows, cols = 12, 15

    # === Prepare the results DataFrame ===
    df = pd.DataFrame(columns=[
        'index', 'quantity',
        'radius_mean', 'radius_std',
        'hours_mean', 'hours_std',
        'time_mean', 'time_std',
        'dead_mean', 'dead_std',
        'alive_mean', 'alive_std',
        'left_mean', 'left_std'
    ])

    # === Fixed parameters ===
    grid = []  # 12x15 --> distanza fra filari è 3 metri, la distanza tra le piante è 1.5
    for r in range(rows):
        for c in range(cols):
            grid.append([r * 3 + 33, c * 1.5 + 45])
    tree_parameters = {'number': 1, 'max_pears': 10, 'positions': grid}
    quantity = 1800  # grams

    bugs_parameters = {'number': 400}


    # === List of bug counts to test ===
    indexes = [0, 1, 2]

    for idx in indexes:
        print(f"================== TEST LAYOUT: Number = {idx} ==================")
        save_path = os.path.join('output', f'layout_exp_{idx}.csv')  # Change this path accordingly
        pesticide_parameters = make_pesticide_parameters(idx, quantity, rows, cols, grid)
        radius_list = []
        hours_list = []
        time_list = []
        dead_list = []
        alive_list = []
        left_list = []

        for i in range(13):
            np.random.seed(i)
            random.seed(i)
            print(f"Iteration {i} starting...")

            d, s = generate_wind_conditions()
            wind = {"direction": d, "speed": s}
            environment_parameters = {
                'starting_date': 25,
                'sequence_length': 24,
                'time_step': 10,
                'wind': wind
            }

            start_time = time.time()

            DT = Twin(environment_parameters, bugs_parameters, tree_parameters, pesticide_parameters)
            results = DT.run()

            elapsed = time.time() - start_time

            radius_list.append(results['pesticide_radius'] / 1000)
            hours_list.append(results['pesticide_decay'])
            time_list.append(elapsed)
            dead_list.append(results['bug_deads'])
            alive_list.append(results['bugs_survived'])
            left_list.append(results['bugs_escaped'])

            print(f"Iteration {i} ended in {elapsed:.2f} seconds.")

        # Compute stats
        radius_mean = np.mean(radius_list)
        radius_std = np.std(radius_list)
        hours_mean = np.mean(hours_list)
        hours_std = np.std(hours_list)
        time_mean = np.mean(time_list)
        time_std = np.std(time_list)
        dead_mean = np.mean(dead_list)
        dead_std = np.std(dead_list)
        alive_mean = np.mean(alive_list)
        alive_std = np.std(alive_list)
        left_mean = np.mean(left_list)
        left_std = np.std(left_list)

        # Append to DataFrame
        df.loc[len(df)] = [
            idx, quantity,
            radius_mean, radius_std,
            hours_mean, hours_std,
            time_mean, time_std,
            dead_mean, dead_std,
            alive_mean, alive_std,
            left_mean, left_std
        ]

        # === Save DataFrame to CSV ===
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)


def pesticide_efficiency():
    save_path = os.path.join('output', 'efficiency_exp.csv')  # Change this path accordingly

    # === Prepare the results DataFrame ===
    df = pd.DataFrame(columns=[
        'index', 'quantity',
        'radius_mean', 'radius_std',
        'hours_mean', 'hours_std',
        'time_mean', 'time_std',
        'dead_mean', 'dead_std',
        'alive_mean', 'alive_std',
        'left_mean', 'left_std'
    ])

    # === Fixed parameters ===
    grid = []  # 12x15 --> distanza fra filari è 3 metri, la distanza tra le piante è 1.5
    for r in range(12):
        for c in range(15):
            grid.append([r * 3 + 33, c * 1.5 + 45])
    tree_parameters = {'number': 1, 'max_pears': 10, 'positions': grid}
    quantity = 1800  # grams
    pesticide_parameters = {
        'quantity': quantity / len(grid),
        'initial_radius': 1,
        'number': len(grid),
        'positions': grid
    }

    # === List of bug counts to test ===
    bugs = [1, 20, 50, 100, 200, 400, 600, 1000]
    indexes = [0, 1, 2, 3, 4, 5, 6, 7]

    for idx, n in zip(indexes, bugs):
        print(f"================== TEST BUGS: Number = {n} ==================")
        bugs_parameters = {'number': n}

        radius_list = []
        hours_list = []
        time_list = []
        dead_list = []
        alive_list = []
        left_list = []

        for i in range(13):
            np.random.seed(i)
            random.seed(i)
            print(f"Iteration {i} starting...")

            d, s = generate_wind_conditions()
            wind = {"direction": d, "speed": s}
            environment_parameters = {
                'starting_date': 25,
                'sequence_length': 24,
                'time_step': 10,
                'wind': wind
            }

            start_time = time.time()

            DT = Twin(environment_parameters, bugs_parameters, tree_parameters, pesticide_parameters)
            results = DT.run()

            elapsed = time.time() - start_time

            radius_list.append(results['pesticide_radius'] / 1000)
            hours_list.append(results['pesticide_decay'])
            time_list.append(elapsed)
            dead_list.append(results['bug_deads'])
            alive_list.append(results['bugs_survived'])
            left_list.append(results['bugs_escaped'])

            print(f"Iteration {i} ended in {elapsed:.2f} seconds.")

        # Compute stats
        radius_mean = np.mean(radius_list)
        radius_std = np.std(radius_list)
        hours_mean = np.mean(hours_list)
        hours_std = np.std(hours_list)
        time_mean = np.mean(time_list)
        time_std = np.std(time_list)
        dead_mean = np.mean(dead_list)
        dead_std = np.std(dead_list)
        alive_mean = np.mean(alive_list)
        alive_std = np.std(alive_list)
        left_mean = np.mean(left_list)
        left_std = np.std(left_list)

        # Append to DataFrame
        df.loc[len(df)] = [
            idx, quantity,
            radius_mean, radius_std,
            hours_mean, hours_std,
            time_mean, time_std,
            dead_mean, dead_std,
            alive_mean, alive_std,
            left_mean, left_std
        ]

    # === Save DataFrame to CSV ===
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)





if __name__ == "__main__":
    # pesticide_test()
    # pesticide_efficiency()
    pesticide_layout()
