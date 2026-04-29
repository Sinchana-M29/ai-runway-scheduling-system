import pandas as pd


class PerformanceAnalyzer:

    def __init__(self):
        pass

    def analyze_fcfs_vs_ai(self, fcfs_df: pd.DataFrame, ai_df: pd.DataFrame):
        """
        Compare FCFS schedule vs AI schedule
        """

        results = {}

        # =========================
        # 1. Average Delay
        # =========================

        fcfs_avg_delay = fcfs_df["delay"].mean() if "delay" in fcfs_df else 0
        ai_avg_delay = ai_df["delay"].mean()

        results["fcfs_avg_delay"] = fcfs_avg_delay
        results["ai_avg_delay"] = ai_avg_delay

        # =========================
        # 2. Max Delay
        # =========================

        fcfs_max_delay = fcfs_df["delay"].max() if "delay" in fcfs_df else 0
        ai_max_delay = ai_df["delay"].max()

        results["fcfs_max_delay"] = fcfs_max_delay
        results["ai_max_delay"] = ai_max_delay

        # =========================
        # 3. Improvement %
        # =========================

        if fcfs_avg_delay > 0:
            improvement = ((fcfs_avg_delay - ai_avg_delay) / fcfs_avg_delay) * 100
        else:
            improvement = 0

        results["delay_reduction_percent"] = improvement

        # =========================
        # 4. Runway Utilization
        # =========================

        def utilization(df):
            if "runway" not in df:
                return 0
            return len(df) / max(df["runway"].nunique(), 1)

        results["fcfs_utilization"] = utilization(fcfs_df)
        results["ai_utilization"] = utilization(ai_df)

        return results

    def print_report(self, results: dict):
        """
        Clean output for project/report
        """

        print("\n" + "=" * 50)
        print("📊 RUNWAY PERFORMANCE REPORT")
        print("=" * 50)

        print(f"\n✈ FCFS Average Delay : {results['fcfs_avg_delay']:.2f}")
        print(f"🧠 AI Average Delay   : {results['ai_avg_delay']:.2f}")

        print(f"\n🚨 FCFS Max Delay     : {results['fcfs_max_delay']:.2f}")
        print(f"⚡ AI Max Delay       : {results['ai_max_delay']:.2f}")

        print(f"\n📉 Delay Reduction    : {results['delay_reduction_percent']:.2f}%")

        print(f"\n🛫 FCFS Utilization   : {results['fcfs_utilization']:.2f}")
        print(f"🧠 AI Utilization     : {results['ai_utilization']:.2f}")

        print("\n" + "=" * 50)