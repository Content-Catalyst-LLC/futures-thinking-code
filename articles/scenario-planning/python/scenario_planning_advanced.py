#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Scenario Planning.
Gracefully exits if dependencies are missing.
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
drivers = pd.read_csv(DATA / "drivers_uncertainties.csv")
signals = pd.read_csv(DATA / "signals.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")

perf = (
    performance
    .merge(strategies, on="strategy_id")
    .merge(scenarios, on="scenario_id")
)

summary = (
    perf.groupby(["strategy_id", "strategy", "strategy_type"], as_index=False)
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

best_by_scenario = perf.groupby("scenario_id", as_index=False)["performance"].max()
best_by_scenario = best_by_scenario.rename(columns={"performance": "best_scenario_performance"})

regret = perf.merge(best_by_scenario, on="scenario_id")
regret["regret"] = regret["best_scenario_performance"] - regret["performance"]

regret_summary = (
    regret.groupby("strategy_id", as_index=False)
    .agg(mean_regret=("regret", "mean"), max_regret=("regret", "max"))
)

summary = summary.merge(regret_summary, on="strategy_id")

summary["robustness_score"] = (
    0.45 * summary["worst_case"]
    + 0.30 * summary["mean_performance"]
    + 0.15 * summary["adaptability"]
    + 0.10 * summary["equity_sensitivity"]
    - 0.15 * summary["volatility"]
    - 0.05 * summary["implementation_difficulty"]
)

drivers["criticality_score"] = drivers["uncertainty"] * drivers["impact"] * drivers["velocity"]
signals["watch_score"] = 0.35 * signals["uncertainty"] + 0.40 * signals["impact"] + 0.25 * signals["novelty"]
assumptions["vulnerability_score"] = (
    assumptions["exposure"] *
    (1 - assumptions["confidence"]) *
    (1 + (1 - assumptions["reversibility"]))
)

summary = summary.sort_values("robustness_score", ascending=False)
drivers = drivers.sort_values("criticality_score", ascending=False)
signals = signals.sort_values("watch_score", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)

summary.to_csv(OUTPUTS / "advanced_strategy_robustness_summary.csv", index=False)
regret.to_csv(OUTPUTS / "advanced_strategy_regret_analysis.csv", index=False)
drivers.to_csv(OUTPUTS / "advanced_driver_uncertainty_scores.csv", index=False)
signals.to_csv(OUTPUTS / "advanced_signal_watch_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(summary["strategy"], summary["robustness_score"])
plt.xlabel("Robustness score")
plt.title(f"Strategy Robustness — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_robustness.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(drivers.head(8)["driver_or_uncertainty"], drivers.head(8)["criticality_score"])
plt.xlabel("Criticality score")
plt.title("Drivers and Critical Uncertainties")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_uncertainty_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(signals.head(8)["signal_id"], signals.head(8)["watch_score"])
plt.xlabel("Watch score")
plt.title("Scenario Monitoring Signals")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_watch_scores.png", dpi=150)
plt.close()

pivot = perf.pivot(index="strategy", columns="scenario_name", values="performance")
pivot.to_csv(OUTPUTS / "advanced_strategy_scenario_matrix.csv")

plt.figure(figsize=(10, 6))
for strategy in perf["strategy"].unique():
    subset = perf[perf["strategy"] == strategy]
    plt.plot(subset["scenario_name"], subset["performance"], marker="o", label=strategy)

plt.xticks(rotation=25, ha="right")
plt.ylabel("Performance")
plt.title("Strategy Performance Across Scenarios")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_performance_across_scenarios.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
