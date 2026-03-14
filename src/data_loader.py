import pandas as pd


def load_flight_data(file_path):
    """
    Loads aircraft arrival data from CSV
    """
    flights = pd.read_csv(file_path)

    # sort flights by ETA
    flights = flights.sort_values(by="eta_minutes")

    return flights


def load_weather_data(file_path):
    """
    Loads weather conditions dataset
    """
    weather = pd.read_csv(file_path)

    return weather


def load_training_data(file_path):
    """
    Loads ML training dataset
    """
    training_data = pd.read_csv(file_path)

    return training_data
