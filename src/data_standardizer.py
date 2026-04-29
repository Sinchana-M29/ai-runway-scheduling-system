import pandas as pd


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes flight dataset for runway scheduling system.
    Fixes column names, missing values, and ensures consistency.
    """

    # Make a copy to avoid modifying original
    df = df.copy()

    # 1. Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2. Remove completely empty rows
    df = df.dropna(how="all")

    # 3. Fill missing values (safe defaults for scheduling)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("UNKNOWN")
        else:
            df[col] = df[col].fillna(0)

    # 4. If flight time columns exist, ensure numeric format
    time_cols = ["eta", "etd", "arrival_time", "departure_time", "eta_minutes"]

    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 5. Remove duplicate flights if any
    if "flight_id" in df.columns:
        df = df.drop_duplicates(subset=["flight_id"])
    elif "callsign" in df.columns:
        df = df.drop_duplicates(subset=["callsign"])

    # 6. Reset index
    df = df.reset_index(drop=True)

    return df