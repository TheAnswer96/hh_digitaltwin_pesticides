# Pesticide Development Simulator - Documentation

## 1. How to Execute

### Prerequisites
Ensure you have Python 3 installed and required dependencies:
```bash
pip install numpy matplotlib scipy json
```

Run the simulation:
```bash
python main.py
```

## 2. Description of the Input

The simulator reads JSON files stored inside the `data/` folder.

### Example: `environment.json`
```json
{
  "size": [100, 100],
  "climate_centroids": {
    "temperature": [{"position": [20, 30], "value": 25}],
    "humidity": [{"position": [15, 40], "value": 60}],
    "light_intensity": [{"position": [10, 50], "value": 80}]
  },
  "time_of_day": 12,
  "season": "summer",
  "simulation_days": 10,
  "seconds_per_step": 60
}
```

## 3. Explanation of the Code

The project is structured using Object-Oriented Programming (OOP). Key components:

- **`SimulationLoader.py`** - Loads JSON data dynamically.
- **`Environment.py`** - Generates grid-based heatmaps and interpolates values.
- **`Bug.py`** - Models insect behavior and movement.
- **`Tree.py & Fruit.py`** - Handles fruit ripening and shading effects.
- **`Pesticide.py`** - Simulates pesticide diffusion and mortality effects.
- **`Simulation.py`** - Manages simulation flow and records execution.

## 4. Contact Us

**Email:** [lorenzo.palazzetti@unipg.it](mailto:lorenzo.palazzetti@unipg.it)
**Email:** [federico.coro@unipd.it](mailto:federico.coro@unipd.it)
