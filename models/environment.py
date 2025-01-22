import numpy as np
import os
import matplotlib.pyplot as plt


class Environment:
    def __init__(self, size, climate_data, time_of_day, season, simulation_days, seconds_per_step):
        self.size = size  # (width, height)
        self.climate_data = climate_data
        self.time_of_day = time_of_day
        self.season = season
        self.simulation_days = simulation_days
        self.seconds_per_step = seconds_per_step

        self.temperature_map = self.generate_heatmap(self.climate_data["temperature"])
        self.humidity_map = self.generate_heatmap(self.climate_data["humidity"])
        self.light_map = self.generate_heatmap(self.climate_data["light_intensity"])
        self.save_all_heatmaps()

        self.wind_speed = self.climate_data["wind"]["speed"]
        self.wind_direction = self.climate_data["wind"]["direction"]

    def generate_heatmap(self, centroids):
        width, height = self.size
        grid = np.zeros((width, height))

        centroid_positions = np.array([c["position"] for c in centroids])
        centroid_values = np.array([c["value"] for c in centroids])

        for x in range(width):
            for y in range(height):
                grid[x, y] = self.inverse_distance_weighting(x, y, centroid_positions, centroid_values)

        return grid

    def inverse_distance_weighting(self, x, y, points, values, power=2):
        # interpolation technique to estimate values at unknown points --> https://en.wikipedia.org/wiki/Inverse_distance_weighting
        distances = np.sqrt((points[:, 0] - x) ** 2 + (points[:, 1] - y) ** 2)

        if np.any(distances == 0):
            return values[np.argmin(distances)]

        weights = 1 / (distances ** power)
        return np.sum(weights * values) / np.sum(weights)

    def update_conditions(self, current_time):
        hour = (current_time // 3600) % 24

        if 6 <= hour < 12:  # Morning
            temp_factor = 1.1
            light_factor = 1.3
        elif 12 <= hour < 18:  # Afternoon
            temp_factor = 1.3
            light_factor = 1.1
        elif 18 <= hour < 24:  # Evening
            temp_factor = 0.9
            light_factor = 0.6
        else:  # Night
            temp_factor = 0.7
            light_factor = 0.2

        self.temperature_map *= temp_factor
        self.light_map *= light_factor

    def save_heatmap(self, heatmap, filename, cmap, vmin=None, vmax=None):
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        plt.figure(figsize=(8, 8))
        plt.imshow(heatmap.T, cmap=cmap, origin="lower", vmin=vmin, vmax=vmax, alpha=0.9)
        plt.colorbar(label=filename.replace("_", " ").capitalize())
        plt.title(f"{filename.replace('_', ' ').capitalize()} Heatmap")
        plt.axis("off")

        file_path = os.path.join(output_folder, f"{filename}.png")
        plt.savefig(file_path, dpi=300)
        plt.close()

    def save_all_heatmaps(self):
        temp_min, temp_max = np.min(self.temperature_map), np.max(self.temperature_map)
        humidity_min, humidity_max = np.min(self.humidity_map), np.max(self.humidity_map)
        light_min, light_max = np.min(self.light_map), np.max(self.light_map)

        self.save_heatmap(self.temperature_map, "temperature", cmap="Reds", vmin=temp_min, vmax=temp_max)
        self.save_heatmap(self.humidity_map, "humidity", cmap="Blues", vmin=humidity_min, vmax=humidity_max)
        self.save_heatmap(self.light_map, "light_intensity", cmap="YlOrBr", vmin=light_min, vmax=light_max)

        print("Heatmaps saved in the output/ folder.")

    def get_temperature_at(self, x, y):
        return self.temperature_map[int(x), int(y)]

    def get_light_at(self, x, y):
        return self.light_map[int(x), int(y)]

    def get_humidity_at(self, x, y):
        return self.humidity_map[int(x), int(y)]

    def get_wind_speed(self):
        return self.wind_speed

    def get_wind_direction(self):
        return self.wind_direction