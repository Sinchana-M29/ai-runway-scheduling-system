# `ml_model.py` Explanation

The `ml_model.py` file contains a Machine Learning pipeline designed to predict flight delays (`delay_minutes`) based on various flight and environmental features. It uses the popular XGBoost library for regression.

Here is a breakdown of the code by function:

## 1. `load_data()`
Loads the training dataset from `data/generated_schedule_1000.csv` using pandas and returns it as a DataFrame.

## 2. `preprocess_data(df)`
Prepares the data for the machine learning model. It converts categorical text columns into numerical codes so the model can understand them:
- `aircraft_type` (e.g., Boeing 747, Airbus A320)
- `wake_category` (e.g., Light, Medium, Heavy)
- `weather_condition` (e.g., Clear, Rain, Fog)
- `runway` (The specific runway assigned)

## 3. `split_features(df)`
Separates the dataset into input features (`X`) and the target variable to be predicted (`y`).
- **Input Features (`X`)**: `eta` (Estimated Time of Arrival), `aircraft_type`, `wake_category`, `weather_condition`, `ROT` (Runway Occupancy Time), and `traffic_density`.
- **Target Variable (`y`)**: `delay_minutes` (The amount of delay in minutes).

## 4. `train_model(X, y)`
Trains and evaluates the Machine Learning model:
- Splits the data into a training set (80%) and a testing set (20%).
- Initializes an **XGBRegressor** (XGBoost regression model) with specific hyperparameters (`n_estimators=200`, `learning_rate=0.05`, `max_depth=6`).
- Trains the model on the training data.
- Makes predictions on the test data and calculates the **Mean Absolute Error (MAE)** to measure how far off the predictions are on average from the actual delays.

## 5. Main Execution Block (`if __name__ == "__main_":`)
This is the entry point that runs the pipeline step by step: it loads the data, preprocesses it, splits the features, and trains the model. *(Note: There is a typo in the original code—`"__main_"` is missing an underscore at the end, so this block won't execute automatically when running the file).*
