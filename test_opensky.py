import requests

# 🔐 YOUR LOGIN DETAILS (PUT YOURS HERE)
username = "mansigowda095@gmail.com"
password = "Mansigowda@007"

# 🌐 OpenSky API URL
url = "https://opensky-network.org/api/states/all"

# 📡 API Request
response = requests.get(url, auth=(username, password))

# 📊 Output
print("Status:", response.status_code)

data = response.json()
print("Total flights:", len(data.get("states", [])))