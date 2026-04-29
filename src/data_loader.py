import pandas as pd
import os


def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads flight scheduling dataset safely.
    Supports CSV and checks file existence.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")

    try:
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully from {file_path}")
        print(f"📊 Shape: {df.shape}")
        return df

    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")