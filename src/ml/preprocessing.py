import pandas as pd

def preprocess_data(path="data/generated_schedule_1000.csv"):
    df = pd.read_csv(path)

    # Remove duplicates
    df = df.drop_duplicates()

    # Drop missing rows
    df = df.dropna()

    # Normalize time columns if needed
    # Here eta and scheduled_landing are already numeric.
    # If you want, scale them to 0-1 for ML consistency.
    df["eta"] = (df["eta"] - df["eta"].min()) / (df["eta"].max() - df["eta"].min())
    df["scheduled_landing"] = (
        (df["scheduled_landing"] - df["scheduled_landing"].min()) /
        (df["scheduled_landing"].max() - df["scheduled_landing"].min())
    )

    # Encode wake category using roadmap style
    wake_map = {
        "Light": 0,
        "Medium": 1,
        "Heavy": 2
    }
    df["wake_category_encoded"] = df["wake_category"].map(wake_map)

    # One-hot encode other categorical columns
    df = pd.get_dummies(df, columns=[
        "aircraft_type",
        "weather_condition",
        "runway"
    ])

    print("Preprocessing complete!")
    print("Shape:", df.shape)
    print(df.head())

    return df

if __name__ == "__main__":
    preprocess_data()