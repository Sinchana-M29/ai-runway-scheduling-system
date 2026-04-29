import pandas as pd


def encode_traffic_level(series: pd.Series) -> pd.Series:
    """
    Convert traffic_level values into a numeric priority/feature.
    Supports both labels (LOW/MEDIUM/HIGH) and numeric levels such as 1-9.
    """
    labels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }

    normalized = series.astype(str).str.strip().str.upper()
    mapped = normalized.map(labels)
    numeric = pd.to_numeric(series, errors="coerce")

    return mapped.fillna(numeric).fillna(1)


def encode_aircraft_type(series: pd.Series) -> pd.Series:
    return series.astype("category").cat.codes
