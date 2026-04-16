import pandas as pd
import numpy as np

df = pd.read_csv("data/converted_real_dataset.csv")
print("\n📥 Original Shape:", df.shape)

# clean
df = df.dropna()
df = df[df["callsign"] != "unknown"]

print("\n🧹 After cleaning:", df.shape)

# FIXED GROUPBY (based on your dataset)
df = df.groupby("callsign").agg({
    "ROT": "mean",
    "delay_minutes": "mean"
}).reset_index()

print("\n📊 After grouping:", df.shape)

# features
df["traffic_density"] = np.random.randint(1, 20, len(df))
df["runway_congestion"] = np.random.randint(1, 5, len(df))

print("\n✅ Sample:")
print(df.head())

df.to_csv("data/clean_ml_dataset.csv", index=False)

print("\n🎯 DONE: Clean dataset created!")