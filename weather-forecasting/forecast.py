import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os
import joblib

# Prepare input sequences and labels
def create_sequences(data, sequence_length=24):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

def process_files_humidity():
    lst_files = os.listdir(os.path.join("data", "humidity"))

    for idx, file in enumerate(lst_files):
        print(f"Processing: {file}")

        csv_path = os.path.join("data", "humidity", file)
        df = pd.read_csv(csv_path)

        df_file = pd.DataFrame()
        df_file["value"] = df["_value"]
        df_file["time"] = pd.to_datetime(df["_time"])

        # Compute timestamp including year, month, day, and hour
        df_file["year"] = df_file["time"].dt.year
        df_file["month"] = df_file["time"].dt.month
        df_file["day"] = df_file["time"].dt.day
        df_file["hour"] = df_file["time"].dt.hour
        df_file["timestamp"] = (df_file["year"] * 10 ** 10 +
                                df_file["month"] * 10 ** 8 +
                                df_file["day"] * 10 ** 6 +
                                df_file["hour"] * 10 ** 4 +
                                (df_file["time"].astype(np.int64) // 10 ** 9 % 10 ** 4))

        # Save the processed file
        output_path = os.path.join("data", "dest", "humidity", f"humidity_{idx}.csv")
        df_file.drop(columns=["time"], inplace=True)  # Drop original time column if not needed
        df_file.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

def process_files_temperature():
    lst_files = os.listdir(os.path.join("data", "temperature"))
    for idx, file in enumerate(lst_files):
        print(f"Processing: {file}")

        csv_path = os.path.join("data", "temperature", file)
        df = pd.read_csv(csv_path)

        df_file = pd.DataFrame()
        df_file["value"] = df["_value"]
        df_file["time"] = pd.to_datetime(df["_time"])

        # Compute timestamp including year, month, day, and hour
        df_file["year"] = df_file["time"].dt.year
        df_file["month"] = df_file["time"].dt.month
        df_file["day"] = df_file["time"].dt.day
        df_file["hour"] = df_file["time"].dt.hour
        df_file["timestamp"] = (df_file["year"] * 10 ** 10 +
                                df_file["month"] * 10 ** 8 +
                                df_file["day"] * 10 ** 6 +
                                df_file["hour"] * 10 ** 4 +
                                (df_file["time"].astype(np.int64) // 10 ** 9 % 10 ** 4))

        # Save the processed file
        output_path = os.path.join("data", "dest", "temperature", f"temperature_{idx}.csv")
        df_file.drop(columns=["time"], inplace=True)  # Drop original time column if not needed
        df_file.to_csv(output_path, index=False)

        print(f"Saved: {output_path}")

if __name__ == '__main__':
    values = ["temperature", "humidity"]
    sensors = ["fritz", "emil", "heinz", "igor"]

    ## Humidity Modeling
    process_files_humidity()
    humidity_files = os.listdir(os.path.join("data", "dest", "humidity"))
    dfs_humidity = [pd.read_csv(os.path.join("data", "dest", "humidity", file)) for file in humidity_files]
    largest_df = max(dfs_humidity, key=len)
    final_df = largest_df[["timestamp", "year", "month", "day", "hour"]].copy()
    for idx, df in enumerate(dfs_humidity):
        final_df = final_df.merge(df[["timestamp", "value"]], on="timestamp", how="left", suffixes=("", f"_{idx}"))
    final_df.rename(columns={"value": "value_0"}, inplace=True)
    value_columns = [col for col in final_df.columns if col.startswith("value_")]
    final_df[value_columns] = final_df[value_columns].apply(lambda row: row.fillna(row.mean()), axis=1)
    final_df.to_csv(os.path.join("data", "humidity_all.csv"))

    scaler = MinMaxScaler()
    final_df[value_columns] = scaler.fit_transform(final_df[value_columns])
    joblib.dump(scaler, os.path.join("..", "data","scaler_humidity.save"))
    final_df["year"] = final_df["year"] - 2000
    features = final_df[value_columns + ["year", "month", "day", "hour"]].values
    target = final_df[value_columns].values
    X, y = create_sequences(features)
    print(X.shape, y.shape)

    # Train-validation-test split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, shuffle=False)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)

    # Build LSTM Model
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(24, X.shape[2])),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(y.shape[1])
    ])

    model.compile(optimizer='adam', loss='mse')
    # print(model.summary())

    # Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val))

    # Save training history to CSV
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(os.path.join("data", "training_history_hum.csv"), index=False)

    # Plot training loss
    plt.figure()
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training vs Validation Loss')
    plt.savefig(os.path.join("data", "training_loss_plot_hum.png"))
    plt.show()

    # Evaluate on test set
    y_pred = model.predict(X_test)
    test_rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    print(f"Test RMSE: {test_rmse:.4f}")

    # Save the model
    model.save(os.path.join("data", "lstm_humidity_model.keras"))
    print("Model saved as 'data/lstm_humidity_model.keras'")


    ## Temperature Modeling
    process_files_temperature()

    # Get all temperature file names
    temperature_files = os.listdir(os.path.join("data", "dest", "temperature"))

    # Read all temperature CSVs into a list of DataFrames
    dfs_temperature = [pd.read_csv(os.path.join("data", "dest", "temperature", file)) for file in temperature_files]

    # Identify the largest DataFrame based on row count
    largest_df = max(dfs_temperature, key=len)

    # Create the base DataFrame with timestamps from the largest dataset
    final_df = largest_df[["timestamp", "year", "month", "day", "hour"]].copy()

    # Merge each dataset with the largest one based on timestamp
    for idx, df in enumerate(dfs_temperature):
        final_df = final_df.merge(df[["timestamp", "value"]], on="timestamp", how="left", suffixes=("", f"_{idx}"))

    # Rename the first "value" column to avoid confusion
    final_df.rename(columns={"value": "value_0"}, inplace=True)

    # Fill empty values with the average of the same row
    value_columns = [col for col in final_df.columns if col.startswith("value_")]
    final_df[value_columns] = final_df[value_columns].apply(lambda row: row.fillna(row.mean()), axis=1)

    final_df.to_csv(os.path.join("data", "temperature_all.csv"))
    # Normalize the dataset
    scaler = MinMaxScaler()
    final_df[value_columns] = scaler.fit_transform(final_df[value_columns])

    joblib.dump(scaler, os.path.join("..", "data", "scaler_temperature.save"))

    final_df["year"] = final_df["year"] - 2000
    features = final_df[value_columns + ["year", "month", "day", "hour"]].values
    target = final_df[value_columns].values
    X, y = create_sequences(features)
    print(X.shape, y.shape)

    # Train-validation-test split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, shuffle=False)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)

    # Build LSTM Model
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(24, X.shape[2])),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(y.shape[1])
    ])

    model.compile(optimizer='adam', loss='mse')

    # Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val))

    # Save training history to CSV
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(os.path.join("data", "training_history_temp.csv"), index=False)

    # Plot training loss
    plt.figure()
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training vs Validation Loss')
    plt.savefig(os.path.join("data", "training_loss_plot_temp.png"))
    plt.show()

    # Evaluate on test set
    y_pred = model.predict(X_test)
    test_rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    print(f"Test RMSE: {test_rmse:.4f}")

    # Save the model
    model.save(os.path.join("data", "lstm_temperature_model.keras"))
    print("Model saved as 'data/lstm_temperature_model.keras'")

    # # Visualizing the 13 temperature columns
    # time_series_data = final_df[value_columns]
    # plt.figure(figsize=(12, 6))
    # for col in value_columns:
    #     plt.plot(final_df["timestamp"], final_df[col], label=col, alpha=0.7)
    # plt.xlabel("Timestamp")
    # plt.ylabel("Temperature")
    # plt.title("Temperature Trends Over Time")
    # plt.legend()
    # plt.savefig(os.path.join("data", "temperature_trends.png"))
    # plt.show()

    # # Save dataset for future visualization
    # final_df.to_csv(os.path.join("data", "processed_temperature_data.csv"), index=False)
    # print("Processed data saved as 'data/processed_temperature_data.csv'")




