import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


def main():
    # 1. Load dataset
    df = pd.read_csv("data/generated_schedule_1000.csv")

    # 2. Clean dataset
    df = df.drop_duplicates()
    df.fillna(0, inplace=True)

    # 3. Encode wake category
    wake_map = {"Light": 0, "Medium": 1, "Heavy": 2}
    df["wake_category_encoded"] = df["wake_category"].map(wake_map)

    # 4. One-hot encode categorical columns
    df = pd.get_dummies(df, columns=[
        "aircraft_type",
        "weather_condition",
        "runway"
    ])

    # 5. Define features and target
    feature_cols = [
        "eta",
        "scheduled_landing",
        "ROT",
        "traffic_density",
        "wake_category_encoded"
    ] + [
        col for col in df.columns
        if col.startswith("aircraft_type_")
        or col.startswith("weather_condition_")
        or col.startswith("runway_")
    ]

    X = df[feature_cols]
    y = df["delay_minutes"]

    # 6. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 7. XGBoost model
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=4,
        min_child_weight=1,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0,
        reg_lambda=1,
        objective="reg:squarederror",
        random_state=42
    )

    # 8. Train
    model.fit(X_train, y_train)

    # 9. Predict
    preds = model.predict(X_test)

    # 10. Prevent negative predictions
    preds = [max(0, pred) for pred in preds]

    # 11. Evaluate
    mae = mean_absolute_error(y_test, preds)

    print("Improved XGBoost Model trained successfully!")
    print("MAE:", mae)

    # 12. Save model
    joblib.dump(model, "src/ml/delay_model.pkl")
    print("Saved model to src/ml/delay_model.pkl")

if __name__ == "__main__":
    main()