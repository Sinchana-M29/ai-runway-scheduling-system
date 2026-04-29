def calculate_metrics(df):

    if "final_delay" not in df.columns:
        df["final_delay"] = 0

    avg_delay = df["final_delay"].mean()
    max_delay = df["final_delay"].max()
    total = len(df)

    print("\n📈 PERFORMANCE METRICS:")
    print(f"Average Delay: {avg_delay:.2f}")
    print(f"Max Delay: {max_delay:.2f}")
    print(f"Total Flights: {total}")