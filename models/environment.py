import numpy as np
import os
import matplotlib.pyplot as plt
import keras
from sklearn.preprocessing import MinMaxScaler
import joblib
from datetime import datetime, timedelta

class Environment:
    def __init__(self, size, sensors_pos, temperatures, humidities, wind):

        # known things of the environment
        self.size = size  # (width, height)
        self.positions = sensors_pos
        self.temperature_X = temperatures
        self.humidity_X = humidities
        self.wind_speed = wind["speed"]
        self.wind_direction = wind["direction"]

        #models
        self.temp_model = keras.saving.load_model(os.path.join("models", "ai", "lstm_temperature_model.keras"))
        self.hum_model = keras.saving.load_model(os.path.join("models", "ai", "lstm_humidity_model.keras"))
        self.temp_scaler = joblib.load(os.path.join("models", "ai", "scaler_temperature.save"))
        self.hum_scaler = joblib.load(os.path.join("models", "ai", "scaler_humidity.save"))
        self.current_temperature, self.current_humidity, self.current_date = self.update_conditions()
        self.temperature_map = self.generate_heatmap(self.positions, self.current_temperature)
        self.humidity_map = self.generate_heatmap(self.positions, self.current_humidity)
        # self.light_map = self.generate_heatmap(lights["light_intensity"])


    def generate_heatmap(self, positions, values):
        width, height = self.size
        grid = np.zeros((width, height))

        centroid_positions = np.array(positions)
        centroid_values = np.array(values[0])

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

    def update_conditions(self):
        # TODO: make the position of the centroids parametric
        # WARNING: The centroid positions are hard coded for the moment to accelerate production

        last_row = self.temperature_X[-1]
        #take the last row date
        last_date = datetime(
            int(last_row[-4]),  # year
            int(last_row[-3]),  # month
            int(last_row[-2]),  # day
            int(last_row[-1])  # hour
        )
        #compute the next date
        next_date = last_date + timedelta(hours=1)
        date_features = np.array([
            next_date.year,
            next_date.month,
            next_date.day,
            next_date.hour
        ])

        # Get the number of columns in each array
        n1 = self.temperature_X.shape[1]
        n2 = self.humidity_X.shape[1]

        # Normalize all columns except the last 4
        temp_to_normalize = self.temperature_X[:, :n1 - 4]
        temp_unnormalized = self.temperature_X[:, n1 - 4:]
        normalized_temp = self.temp_scaler.transform(temp_to_normalize)
        temp_X = np.hstack((normalized_temp, temp_unnormalized))
        r, c = temp_X.shape
        temp_y = self.temp_model.predict(temp_X[-r:].reshape(1, r, c), verbose=0)
        new_temp = temp_y[:, :n1 - 4]
        new_temp = self.temp_scaler.inverse_transform(new_temp)
        # recover the new window for temperature
        new_row = np.concatenate([new_temp[0], date_features])
        self.temperature_X = np.vstack([self.temperature_X, new_row])[1:]

        hum_to_normalize = self.humidity_X[:, :n2 - 4]
        hum_unnormalized = self.humidity_X[:, n2 - 4:]
        normalized_hum = self.hum_scaler.transform(hum_to_normalize)
        hum_X = np.hstack((normalized_hum, hum_unnormalized))
        r, c = temp_X.shape
        hum_y = self.hum_model.predict(hum_X[-r:].reshape(1, r, c), verbose=0)
        new_hum = hum_y[:, :n2 - 4]
        new_hum = self.temp_scaler.inverse_transform(new_hum)
        new_row = np.concatenate([new_hum[0], date_features])
        self.humidity_X = np.vstack([self.humidity_X, new_row])[1:]
        return new_temp, new_hum, date_features

    def save_heatmap(self, heatmap, filename, cmap='viridis', vmin=None, vmax=None):
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        # Set up figure
        fig, ax = plt.subplots(figsize=(6, 6), dpi=600)

        # Plot heatmap
        cax = ax.imshow(
            heatmap.T,
            cmap=cmap,
            origin="lower",
            vmin=vmin,
            vmax=vmax,
            interpolation='none',
            aspect='equal',
            alpha=0.95
        )


        # Add colorbar
        cbar = fig.colorbar(cax, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label(filename.replace("_", " ").capitalize(), fontsize=16)
        cbar.ax.tick_params(labelsize=12)

        # Fonts and style
        plt.rcParams.update({
            "font.size": 16,
            "font.family": "serif",  # or "sans-serif"
        })

        # Save to file
        file_path = os.path.join(output_folder, f"{filename}.png")
        plt.savefig(file_path, bbox_inches='tight', transparent=True)
        plt.close()

    def save_all_heatmaps(self):
        temp_min, temp_max = np.min(self.temperature_map), np.max(self.temperature_map)
        humidity_min, humidity_max = np.min(self.humidity_map), np.max(self.humidity_map)
        # light_min, light_max = np.min(self.light_map), np.max(self.light_map)

        self.save_heatmap(self.temperature_map, "temperature", cmap="Reds", vmin=temp_min, vmax=temp_max)
        self.save_heatmap(self.humidity_map, "humidity", cmap="Blues", vmin=humidity_min, vmax=humidity_max)
        # self.save_heatmap(self.light_map, "light_intensity", cmap="YlOrBr", vmin=light_min, vmax=light_max)

        print("Heatmaps saved in the output/ folder.")

    def get_temperature_at(self, x, y):
        return self.temperature_map[int(x), int(y)]

    # def get_light_at(self, x, y):
    #     return self.light_map[int(x), int(y)]

    def get_humidity_at(self, x, y):
        return self.humidity_map[int(x), int(y)]

    def get_wind_speed(self):
        return self.wind_speed

    def get_wind_direction(self):
        return self.wind_direction

    def get_size(self):
        return self.size

    def get_info(self):
        print(f"Env: temps: {self.current_temperature}\nhums: {self.current_humidity}")
        return