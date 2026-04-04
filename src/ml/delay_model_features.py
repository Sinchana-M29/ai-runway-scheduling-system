import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def train_delay_model(path="data/generated_schedule_1000.csv"):
    df = pd.read_csv(path)

    df = df.drop_duplicates().dropna()

    # Encode wake category
    wake_map = {"Light": 0, "Medium": 1, "Heavy": 2}
    df["wake_category_encoded"] = df["wake_category"].map(wake_map)

    # Encode other categoricals
    df = pd.get_dummies(df, columns=[
        "aircraft_type",
        "weather_condition",
        "runway"
    ])

    # Choose features
    drop_cols = ["delay_minutes", "flight_id", "callsign", "wake_category"]
    X = df.drop(columns=drop_cols, errors="ignore")

    # Remove leakage-heavy column if needed
    if "scheduled_landing" in X.columns:
        X = X.drop(columns=["scheduled_landing"], errors="ignore")

    y = df["delay_minutes"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Model trained successfully!")
    print("MAE:", mae)
    print("R2 Score:", r2)

    joblib.dump(model, "src/ml/delay_model.pkl")
    joblib.dump(list(X.columns), "src/ml/delay_model_features.pkl")

    print("Saved model to src/ml/delay_model.pkl")
    return model

if __name__ == "__main__":
    train_delay_model()