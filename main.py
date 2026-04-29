import pandas as pd
import sys

from src.data_loader import load_data
from src.ml.predict import load_model, predict_delay
from src.scheduling.scheduler_fcfs import multi_runway_schedule
from src.ml.train_rl import train_rl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# -------------------------------
# 🔧 Convert time → minutes
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


# -------------------------------
# 🔧 Preprocessing
# -------------------------------
def preprocess_data(df):
    print("\n🔧 Standardizing dataset...")

    df["eta_minutes"] = df["arrival_time"].apply(convert_to_minutes)

    print("\n🔍 DATA COLUMNS AFTER STANDARDIZATION:")
    print(df.columns)

    return df


# -------------------------------
# 🚀 MAIN PIPELINE
# -------------------------------
def main():

    # -------------------------------
    # 📥 Load data
    # -------------------------------
    print("📥 Loading dataset...")
    df = load_data("data/final_schedule.csv")

    print("📊 Shape:", df.shape)

    # -------------------------------
    # 🔧 Preprocess
    # -------------------------------
    df = preprocess_data(df)

    # -------------------------------
    # 🧠 ML MODEL
    # -------------------------------
    print("\n🧠 Loading ML model...")
    model = load_model()

    print("🔮 Predicting delays...")
    df = predict_delay(model, df)

    # -------------------------------
    # 🤖 RL TRAINING
    # -------------------------------
    print("\n🤖 Training RL Agent...")
    rl_agent = train_rl(df, episodes=1)

    # -------------------------------
    # 🛫 SCHEDULING (RL CONTROLLED)
    # -------------------------------
    print("\n🛫 Running Scheduler...")
    result = multi_runway_schedule(df, rl_agent=rl_agent)

    # -------------------------------
    # 📊 OUTPUT
    # -------------------------------
    print("\n✅ Scheduling completed\n")
    print(result.head())

    # -------------------------------
    # 💾 SAVE OUTPUT
    # -------------------------------
    result.to_csv("data/output_final.csv", index=False)
    print("\n💾 Output saved to data/output_final.csv")


# -------------------------------
# ▶️ RUN
# -------------------------------
if __name__ == "__main__":
    main()
