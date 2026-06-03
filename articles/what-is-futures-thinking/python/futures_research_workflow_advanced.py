#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Thinking article directories.

Gracefully exits if pandas or matplotlib are missing.
"""

from pathlib import Path
import json
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

config = json.loads((ROOT / "article_config.json").read_text(encoding="utf-8"))

performance = pd.read_csv(DATA / "strategy_performance.csv")
strategies = pd.read_csv(DATA / "strategies.csv")
scenarios = pd.read_csv(DATA / "scenarios.csv")
signals = pd.read_csv(DATA / "signals.csv")
drivers = pd.read_csv(DATA / "drivers.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")

perf = (
    performance
    .merge(strategies, on="strategy_id")
    .merge(scenarios, on="scenario_id")
)

summary = (
    perf.groupby(["strategy_id", "strategy_name", "strategy_type"], as_index=False)
    .agg(
        mean_performance=("performance", "mean"),
        worst_case=("performance", "min"),
        best_case=("performance", "max"),
        volatility=("performance", "std"),
        adaptability=("adaptability", "mean"),
        equity_sensitivity=("equity_sensitivity", "mean"),
        implementation_difficulty=("implementation_difficulty", "mean"),
    )
)

summary["volatility"] = summary["volatility"].fillna(0)
summary["robustness_score"] = (
    0.45 * summary["worst_case"]
    + 0.30 * summary["mean_performance"]
    + 0.15 * summary["adaptability"]
    + 0.10 * summary["equity_sensitivity"]
    - 0.15 * summary["volatility"]
    - 0.05 * summary["implementation_difficulty"]
)

best_by_scenario = perf.groupby("scenario_id", as_index=False)["performance"].max()
best_by_scenario = best_by_scenario.rename(columns={"performance": "best_scenario_performance"})

regret = perf.merge(best_by_scenario, on="scenario_id")
regret["regret"] = regret["best_scenario_performance"] - regret["performance"]

signals["watch_score"] = 0.35 * signals["uncertainty"] + 0.40 * signals["impact"] + 0.25 * signals["novelty"]
drivers["driver_priority"] = drivers["uncertainty"] * drivers["impact"] * drivers["velocity"]
assumptions["vulnerability_score"] = (
    assumptions["exposure"] * (1 - assumptions["confidence"]) * (1 + (1 - assumptions["reversibility"]))
)

summary = summary.sort_values("robustness_score", ascending=False)
signals = signals.sort_values("watch_score", ascending=False)
drivers = drivers.sort_values("driver_priority", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)

summary.to_csv(OUTPUTS / "advanced_strategy_robustness_summary.csv", index=False)
regret.to_csv(OUTPUTS / "advanced_regret_analysis.csv", index=False)
signals.to_csv(OUTPUTS / "advanced_signal_watch_scores.csv", index=False)
drivers.to_csv(OUTPUTS / "advanced_driver_priority_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(summary["strategy_name"], summary["robustness_score"])
plt.xlabel("Robustness score")
plt.title(f"Strategy Robustness — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_robustness.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(signals.head(8)["signal_id"], signals.head(8)["watch_score"])
plt.xlabel("Watch score")
plt.title("Signal Watch Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_watch_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(drivers.head(8)["driver_name"], drivers.head(8)["driver_priority"])
plt.xlabel("Driver priority")
plt.title("Driver Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(assumptions.head(6)["assumption_id"], assumptions.head(6)["vulnerability_score"])
plt.xlabel("Vulnerability score")
plt.title("Assumption Vulnerability Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "assumption_vulnerability_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
