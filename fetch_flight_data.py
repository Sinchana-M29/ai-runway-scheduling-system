import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

def safe_get(data, *keys, default=None):
    """Safely get nested dictionary values."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current

def parse_datetime(dt_str):
    """Parse API datetime string safely."""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None

def minutes_from_midnight(dt_obj):
    """Convert datetime to minutes from midnight."""
    if dt_obj is None:
        return 0.0
    return float(dt_obj.hour * 60 + dt_obj.minute + dt_obj.second / 60)

def infer_wake_category(aircraft_code):
    """
    Simple wake category inference.
    You can improve this later with a better aircraft mapping table.
    """
    if not aircraft_code:
        return "Medium"

    code = str(aircraft_code).upper()

    heavy_list = ["B77", "B78", "B74", "A33", "A34", "A35", "A38", "B767", "B777", "B787", "A330", "A340", "A350", "A380"]
    light_list = ["C15", "C17", "SR2", "PA2", "DA4", "BE2"]

    if any(x in code for x in heavy_list):
        return "Heavy"
    if any(x in code for x in light_list):
        return "Light"
    return "Medium"

def infer_weather_condition():
    """
    Placeholder because aviationstack flight endpoint does not return weather.
    Change later if you integrate a weather API.
    """
    return "clear"

def infer_traffic_density(total_flights):
    """
    Simple traffic density score based on total filtered flights.
    You can replace this with a better airport congestion calculation later.
    """
    if total_flights <= 5:
        return 2
    if total_flights <= 10:
        return 4
    if total_flights <= 20:
        return 6
    return 8

def pick_runway(index):
    """
    Placeholder runway assignment for dataset storage.
    RL scheduler will optimize this later.
    """
    return "R1" if index % 2 == 0 else "R2"

def download_flight_schedule():
    # 1. API details
    url = "http://api.aviationstack.com/v1/flights"
    api_key = "c6040a6a1ef1898174e0f8628f5f144f"

    params = {
        "access_key": api_key,
        "iata_code": "LHR",
        "flight_status": "scheduled"
    }

    # 2. Next 1 hour window in UTC
    now_utc = datetime.now(timezone.utc)
    next_one_hour_utc = now_utc + timedelta(hours=1)

    print(f"Searching flights between {now_utc.isoformat()} and {next_one_hour_utc.isoformat()}")

    try:
        # 3. Fetch API data
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        api_data = response.json().get("data", [])

        # 4. Filter flights where departure OR arrival scheduled time is in next 1 hour
        filtered_flights = []
        for flight in api_data:
            dep_scheduled_raw = safe_get(flight, "departure", "scheduled")
            arr_scheduled_raw = safe_get(flight, "arrival", "scheduled")

            dep_dt = parse_datetime(dep_scheduled_raw)
            arr_dt = parse_datetime(arr_scheduled_raw)

            dep_in_range = dep_dt is not None and now_utc <= dep_dt <= next_one_hour_utc
            arr_in_range = arr_dt is not None and now_utc <= arr_dt <= next_one_hour_utc

            if dep_in_range or arr_in_range:
                filtered_flights.append(flight)

        if not filtered_flights:
            print("No flights found in the next 1 hour window.")
            # Still save empty CSV with correct headers
            empty_df = pd.DataFrame(columns=[
                "flight_id",
                "callsign",
                "aircraft_type",
                "wake_category",
                "weather_condition",
                "traffic_density",
                "runway",
                "eta",
                "scheduled_landing",
                "ROT",
                "delay_minutes"
            ])
            output_path = os.path.join("data", "converted_real_dataset.csv")
            empty_df.to_csv(output_path, index=False)
            print(f"Empty file saved to {output_path}")
            return

        traffic_density_value = infer_traffic_density(len(filtered_flights))
        rows = []

        # 5. Convert to same CSV format as your attached file
        for idx, flight in enumerate(filtered_flights, start=1):
            flight_id = idx

            callsign = (
                safe_get(flight, "flight", "iata")
                or safe_get(flight, "flight", "icao")
                or safe_get(flight, "airline", "iata")
                or "UNKNOWN"
            )

            aircraft_type = (
                safe_get(flight, "aircraft", "icao24")
                or safe_get(flight, "aircraft", "registration")
                or safe_get(flight, "flight", "icao")
                or "UNKNOWN"
            )

            wake_category = infer_wake_category(aircraft_type)
            weather_condition = infer_weather_condition()
            runway = pick_runway(idx)

            dep_scheduled_raw = safe_get(flight, "departure", "scheduled")
            arr_scheduled_raw = safe_get(flight, "arrival", "scheduled")

            dep_dt = parse_datetime(dep_scheduled_raw)
            arr_dt = parse_datetime(arr_scheduled_raw)

            # For runway scheduling, prefer arrival as landing time if available
            # Otherwise fall back to departure
            eta_dt = arr_dt if arr_dt is not None else dep_dt
            eta = minutes_from_midnight(eta_dt)

            # Since API doesn't provide actual landing delay/ROT directly here,
            # we store safe placeholders for now.
            delay_minutes = 0.0
            rot = 3.0

            scheduled_landing = eta + delay_minutes

            rows.append({
                "flight_id": flight_id,
                "callsign": callsign,
                "aircraft_type": aircraft_type,
                "wake_category": wake_category,
                "weather_condition": weather_condition,
                "traffic_density": traffic_density_value,
                "runway": runway,
                "eta": eta,
                "scheduled_landing": scheduled_landing,
                "ROT": rot,
                "delay_minutes": delay_minutes
            })

        # 6. Save to SAME filename
        df = pd.DataFrame(rows, columns=[
            "flight_id",
            "callsign",
            "aircraft_type",
            "wake_category",
            "weather_condition",
            "traffic_density",
            "runway",
            "eta",
            "scheduled_landing",
            "ROT",
            "delay_minutes"
        ])

        output_path = os.path.join("data", "converted_real_dataset.csv")
        df.to_csv(output_path, index=False)

        print(f"Success! Saved {len(df)} flights to {output_path}")
        print(df.head())

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    download_flight_schedule()