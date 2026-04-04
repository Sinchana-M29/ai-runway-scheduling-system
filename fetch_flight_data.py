import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

# =========================
# YOUR CREDENTIALS (TEMP)
# =========================
CLIENT_ID = "mansigowda095@gmail.com-api-client"
CLIENT_SECRET = "OHFDxqSDaToXXDQQEDJZmHM8gduUKyLW"

# =========================
# CONFIG
# =========================
AIRPORT_ICAO = "VOBL"   # Bangalore airport
OUTPUT_FILE = "data/converted_real_dataset.csv"

TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
ARRIVAL_URL = "https://opensky-network.org/api/flights/arrival"
DEPARTURE_URL = "https://opensky-network.org/api/flights/departure"

# Fetch last 1 hour (IMPORTANT)
END_TIME = int(time.time())
START_TIME = END_TIME - 86400

IST = timezone(timedelta(hours=5, minutes=30))


# =========================
# STEP 1: GET TOKEN
# =========================
def get_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        print("❌ Token error:", response.text)
        exit()

    return response.json()["access_token"]


# =========================
# STEP 2: FETCH DATA
# =========================
def fetch_data(url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "airport": AIRPORT_ICAO,
        "begin": START_TIME,
        "end": END_TIME
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return []
    else:
        print("❌ API error:", response.text)
        return []


# =========================
# STEP 3: CONVERT TIME
# =========================
def convert_time(ts):
    if ts is None:
        return ""
    return datetime.fromtimestamp(ts, tz=IST).strftime("%Y-%m-%d %H:%M:%S")


# =========================
# STEP 4: BUILD CSV FORMAT
# =========================
def build_rows(arrivals, departures):
    rows = []
    flight_id = 1

    total = len(arrivals) + len(departures)

    if total < 5:
        density = "Low"
    elif total < 15:
        density = "Medium"
    else:
        density = "High"

    # ARRIVALS
    for f in arrivals:
        ts = f.get("lastSeen")

        rows.append({
            "flight_id": flight_id,
            "callsign": (f.get("callsign") or "N/A").strip(),
            "aircraft_type": "Unknown",
            "wake_category": "Unknown",
            "weather_condition": "Clear",
            "traffic_density": density,
            "runway": "RWY-09",
            "eta": convert_time(ts),
            "scheduled_landing": convert_time(ts),
            "ROT": 3.0,
            "delay_minutes": 0.0
        })

        flight_id += 1

    # DEPARTURES
    for f in departures:
        ts = f.get("firstSeen")

        rows.append({
            "flight_id": flight_id,
            "callsign": (f.get("callsign") or "N/A").strip(),
            "aircraft_type": "Unknown",
            "wake_category": "Unknown",
            "weather_condition": "Clear",
            "traffic_density": density,
            "runway": "RWY-27",
            "eta": convert_time(ts),
            "scheduled_landing": convert_time(ts),
            "ROT": 3.0,
            "delay_minutes": 0.0
        })

        flight_id += 1

    return rows


# =========================
# MAIN FUNCTION
# =========================
def main():
    print("🔐 Getting token...")
    token = get_token()

    print("✈️ Fetching arrivals...")
    arrivals = fetch_data(ARRIVAL_URL, token)

    print("✈️ Fetching departures...")
    departures = fetch_data(DEPARTURE_URL, token)

    print(f"Arrivals: {len(arrivals)}, Departures: {len(departures)}")

    rows = build_rows(arrivals, departures)

    df = pd.DataFrame(rows)

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Saved to {OUTPUT_FILE}")
    print(df.head())


if __name__ == "__main__":
    main()