import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# =========================
# LOAD CLEAN DATA
# =========================
df = pd.read_csv("data/clean_ml_dataset.csv")

print("\n📥 Loaded clean dataset:", df.shape)


# =========================
# SELECT FEATURES & TARGET
# =========================

features = [
    "ROT",
    "traffic_density",
    "runway_congestion"
]

X = df[features]
y = df["delay_minutes"]


# =========================
# TRAIN-TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# TRAIN MODEL
# =========================

model = XGBRegressor()

model.fit(X_train, y_train)

print("\n✅ Model trained!")


# =========================
# EVALUATE MODEL
# =========================

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

print(f"\n📊 MAE (error): {mae:.2f} minutes")


# =========================
# SAVE MODEL
# =========================

joblib.dump(model, "src/ml/delay_model.pkl")

print("\n💾 Model saved at src/ml/delay_model.pkl")