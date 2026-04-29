import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from src.ml.features import encode_aircraft_type, encode_traffic_level


# -------------------------------
# 🔧 Convert time to minutes
# -------------------------------
def convert_to_minutes(time_val):
    try:
        if isinstance(time_val, (int, float)):
            return int(time_val)

        if ":" in str(time_val):
            h, m = map(int, str(time_val).split(":"))
            return h * 60 + m

        return int(time_val)
    except:
        return 0


print("📥 Loading dataset...")
df = pd.read_csv("data/final_schedule.csv")

print("🔧 Preprocessing...")
df["eta_minutes"] = df["arrival_time"].apply(convert_to_minutes)

# -------------------------------
# 🧠 Feature Engineering
# -------------------------------

df["traffic_encoded"] = encode_traffic_level(df["traffic_level"])

# Encode aircraft type (simple encoding)
df["aircraft_encoded"] = encode_aircraft_type(df["aircraft_type"])

# -------------------------------
# 🎯 Features & Target
# -------------------------------
features = ["eta_minutes", "traffic_encoded", "aircraft_encoded"]
# Create better target (controlled delay)
df["target_delay"] = df["landing_time"] - df["arrival_time"]

# Remove negative values
df["target_delay"] = df["target_delay"].clip(lower=0, upper=60)

target = "target_delay"

X = df[features]
y = df[target]

# -------------------------------
# ✂️ Train-test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🧠 Training model...")
model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# 📊 Evaluate
# -------------------------------
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)

print(f"✅ Model trained | MAE: {mae:.2f}")

# -------------------------------
# 💾 Save model
# -------------------------------
joblib.dump(model, "src/ml/model.pkl")
print("💾 Model saved at src/ml/model.pkl")
