import joblib
import pandas as pd

from src.ml.features import encode_aircraft_type, encode_traffic_level


# -------------------------------
# 🧠 Load model
# -------------------------------
def load_model():
    model = joblib.load("src/ml/model.pkl")
    print("✅ ML model loaded successfully")
    return model


# -------------------------------
# 🔧 Feature Engineering (MUST MATCH TRAINING)
# -------------------------------
def preprocess_features(df):
    df = df.copy()
    df["traffic_encoded"] = encode_traffic_level(df["traffic_level"])
    df["aircraft_encoded"] = encode_aircraft_type(df["aircraft_type"])

    return df


# -------------------------------
# 🔮 Predict delay
# -------------------------------
def predict_delay(model, df):

    df = preprocess_features(df)

    features = [
        "eta_minutes",
        "traffic_encoded",
        "aircraft_encoded"
    ]

    df["predicted_delay"] = model.predict(df[features])

    print("🔮 Delay prediction completed")

    return df
