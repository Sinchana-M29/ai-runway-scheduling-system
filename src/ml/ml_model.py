import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


# ===== LOAD DATA =====
def load_data():
    df = pd.read_csv("data/generated_schedule_1000.csv")
    print("Dataset loaded successfully\n")
    return df


# ===== PREPROCESS =====
def preprocess_data(df):

    df = df.copy()

    df["aircraft_type"] = df["aircraft_type"].astype("category").cat.codes
    df["wake_category"] = df["wake_category"].astype("category").cat.codes
    df["weather_condition"] = df["weather_condition"].astype("category").cat.codes
    df["runway"] = df["runway"].astype("category").cat.codes

    return df


# ===== FEATURE SELECTION =====
def split_features(df):

    X = df[[
        "eta",
        "aircraft_type",
        "wake_category",
        "weather_condition",
        "ROT",
        "traffic_density"
    ]]

    y = df["delay_minutes"]

    return X, y


# ===== TRAIN MODEL =====
def train_model(X, y):

    print("Training XGBoost model...\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(y_test, predictions)

    print("Model Performance:")
    print("Mean Absolute Error:", round(error, 2), "minutes\n")

    return model


# ===== MAIN EXECUTION =====
if __name__ == "__main__":

    print("=== ML PIPELINE STARTED ===\n")

    df_raw = load_data()

    df_processed = preprocess_data(df_raw)

    X, y = split_features(df_processed)

    model = train_model(X, y)

    print("=== SAMPLE PREDICTIONS ===")
    sample_df = df_raw.head(5)
    sample_X = X.head(5)
    predictions = model.predict(sample_X)
    
    for i in range(5):
        print(f"Flight {sample_df['flight_id'].iloc[i]} ({sample_df['callsign'].iloc[i]}):")
        print(f"  Aircraft Type       : {sample_df['aircraft_type'].iloc[i]}")
        print(f"  Arrival Time (ETA)  : {sample_df['eta'].iloc[i]:.2f}")
        print(f"  Traffic Density     : {sample_df['traffic_density'].iloc[i]}")
        print(f"  Weather             : {sample_df['weather_condition'].iloc[i].capitalize()}")
        print(f"  Runway Availability : {sample_df['runway'].iloc[i]}")
        print(f"  ==> PREDICTED DELAY : {predictions[i]:.2f} minutes\n")

    print("=== ML PIPELINE COMPLETED ===")
    