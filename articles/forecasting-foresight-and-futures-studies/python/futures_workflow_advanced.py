#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for forecasting and foresight.

Run after:
    pip install -r requirements-advanced.txt
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Advanced dependencies are missing.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r requirements-advanced.txt")
    print(f"Original error: {exc}")
    sys.exit(0)

df = pd.read_csv(DATA / "strategy_performance.csv")

summary = (
    df.groupby("strategy")["performance"]
    .agg(mean_performance="mean", worst_case="min", best_case="max", volatility="std")
    .reset_index()
)

summary["robustness_score"] = (
    0.45 * summary["worst_case"] +
    0.35 * summary["mean_performance"] -
    0.20 * summary["volatility"].fillna(0)
)

best_by_future = (
    df.groupby("future")["performance"]
    .max()
    .reset_index()
    .rename(columns={"performance": "best_future_performance"})
)

regret_df = df.merge(best_by_future, on="future")
regret_df["regret"] = regret_df["best_future_performance"] - regret_df["performance"]

regret_summary = (
    regret_df.groupby("strategy")["regret"]
    .agg(mean_regret="mean", max_regret="max")
    .reset_index()
)

summary = summary.merge(regret_summary, on="strategy")
summary = summary.sort_values("robustness_score", ascending=False)

plt.figure(figsize=(11, 6))
for strategy in df["strategy"].unique():
    subset = df[df["strategy"] == strategy]
    plt.plot(subset["future"], subset["performance"], marker="o", label=strategy)

plt.xticks(rotation=25, ha="right")
plt.ylabel("Performance")
plt.title("Strategy Performance Across Plausible Futures")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_performance_across_futures.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 5))
plt.barh(summary["strategy"], summary["robustness_score"])
plt.xlabel("Robustness score")
plt.title("Robustness-Oriented Strategy Comparison")
plt.tight_layout()
plt.savefig(OUTPUTS / "robustness_strategy_comparison.png", dpi=150)
plt.close()

practice = pd.read_csv(DATA / "practice_profiles.csv")
practice_long = practice.melt(id_vars="practice", var_name="dimension", value_name="value")
pivot = practice_long.pivot(index="dimension", columns="practice", values="value")

pivot.plot(kind="barh", figsize=(11, 7))
plt.xlabel("Relative emphasis")
plt.title("Comparing Future-Oriented Practices")
plt.tight_layout()
plt.savefig(OUTPUTS / "practice_profile_comparison.png", dpi=150)
plt.close()

df.to_csv(OUTPUTS / "strategy_performance_advanced.csv", index=False)
summary.to_csv(OUTPUTS / "strategy_summary_advanced.csv", index=False)
regret_df.to_csv(OUTPUTS / "strategy_regret_advanced.csv", index=False)
practice_long.to_csv(OUTPUTS / "practice_profiles_long_advanced.csv", index=False)

print("Advanced workflow complete.")
print(f"Outputs written to: {OUTPUTS}")
