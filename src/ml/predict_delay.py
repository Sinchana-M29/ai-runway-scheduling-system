import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def predict_delay(df: pd.DataFrame):
    """
    Final improved ML model:
    Predicts delay potential BEFORE scheduling
    """

    df = df.copy()

    # -------------------------------
    # 🔥 TARGET ENGINEERING (IMPORTANT)
    # -------------------------------
    df["delay_potential"] = df["scheduled_time"] - df["arrival_time"]
    df["delay_potential"] = df["delay_potential"].clip(lower=0)

    # -------------------------------
    # ✅ CLEAN FEATURES (NO NOISE)
    # -------------------------------
    features = [
        "arrival_time",
        "scheduled_time",
        "traffic_level"
    ]

    X = df[features]
    y = df["delay_potential"]

    # -------------------------------
    # TRAIN MODEL
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    # -------------------------------
    # EVALUATION
    # -------------------------------
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    print(f"✅ FINAL ML Model (Delay Potential) | MAE: {mae:.2f}")

    # Predict for full dataset
    return model.predict(X)