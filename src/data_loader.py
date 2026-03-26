import pandas as pd


def load_flight_data(file_path):
    """
    Loads aircraft arrival data and prepares priority sorting
    """

    flights = pd.read_csv(file_path)

    priority_map = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    flights["priority_value"] = flights["priority"].map(priority_map)

    flights = flights.sort_values(by=["priority_value", "eta_minutes"])

    return flights


def load_weather_data(file_path):

    return pd.read_csv(file_path)


def load_training_data(file_path):

    return pd.read_csv(file_path)
