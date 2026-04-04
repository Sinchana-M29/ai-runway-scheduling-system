import pandas as pd
import joblib

MODEL_PATH = "src/ml/delay_model.pkl"


def prepare_features(df):
    df = df.copy()

    # Fill missing values
    df.fillna(0, inplace=True)

    # Encode wake category
    wake_map = {"Light": 0, "Medium": 1, "Heavy": 2}
    df["wake_category_encoded"] = df["wake_category"].map(wake_map)

    # One-hot encode categorical columns
    df = pd.get_dummies(df, columns=[
        "aircraft_type",
        "weather_condition",
        "runway"
    ])

    return df


def predict_delay_for_batch(batch_df):
    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Prepare batch
    batch_processed = prepare_features(batch_df)

    # Match training feature columns exactly
    trained_feature_cols = list(model.feature_names_in_)

    for col in trained_feature_cols:
        if col not in batch_processed.columns:
            batch_processed[col] = 0

    X = batch_processed[trained_feature_cols]

    # Predict
    predictions = model.predict(X)

    # Prevent negative delays
    predictions = [max(0, pred) for pred in predictions]

    # Add predictions back
    result_df = batch_df.copy()
    result_df["predicted_delay"] = predictions

    return result_df


if __name__ == "__main__":
    df = pd.read_csv("data/generated_schedule_1000.csv")

    result = predict_delay_for_batch(df)

    print(result[["flight_id", "predicted_delay"]].head())

    result.to_csv("data/predicted_delays.csv", index=False)
    print("Predictions saved to data/predicted_delays.csv")