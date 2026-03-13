import pandas as pd
import os


def load_flight_data():
    """
    Loads the BLR arrivals dataset.
    """

    file_path = os.path.join("data", "blr_arrivals.csv")

    df = pd.read_csv(file_path)

    return df


def validate_dataset(df):
    """
    Basic validation to ensure dataset integrity.
    """

    required_columns = [
        "flight_id",
        "callsign",
        "origin_airport",
        "destination_airport",
        "aircraft_type",
        "weight_class",
        "eta_minutes",
        "priority"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    return True
