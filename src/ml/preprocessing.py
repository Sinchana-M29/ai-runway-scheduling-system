import pandas as pd


def preprocess_data(df):

    print("\n⚙️ Preprocessing dataset...")

    df = df.copy()

    # -----------------------------
    # CLEAN MISSING VALUES
    # -----------------------------
    df = df.fillna({
        "arrival_time": 0,
        "scheduled_time": 0,
        "aircraft_type": "MEDIUM",
        "traffic_level": 1
    })

    # -----------------------------
    # TIME NORMALIZATION (minutes → seconds)
    # -----------------------------
    df["arrival_time"] = df["arrival_time"] * 60
    df["scheduled_time"] = df["scheduled_time"] * 60

    # -----------------------------
    # ENCODE AIRCRAFT TYPE
    # -----------------------------
    df["aircraft_type"] = df["aircraft_type"].astype(str).str.upper()

    mapping = {
        "HEAVY": 2,
        "MEDIUM": 1,
        "LIGHT": 0
    }

    df["aircraft_type_encoded"] = df["aircraft_type"].map(mapping)
    df["aircraft_type_encoded"] = df["aircraft_type_encoded"].fillna(1)

    # -----------------------------
    # CLEAN TRAFFIC LEVEL
    # -----------------------------
    df["traffic_level"] = pd.to_numeric(df["traffic_level"], errors="coerce").fillna(1)

    print("\n✅ Preprocessing complete")
    print(df.head())

    return df
