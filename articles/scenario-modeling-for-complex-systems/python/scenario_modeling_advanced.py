#!/usr/bin/env python3
"""
Advanced pandas/numpy/matplotlib workflow for Scenario Modeling for Complex Systems.
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
    import numpy as np
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

scenarios = pd.read_csv(DATA / "scenario_assumptions.csv")
strategies = pd.read_csv(DATA / "strategy_portfolio.csv")
drivers = pd.read_csv(DATA / "driver_register.csv")
monitoring = pd.read_csv(DATA / "monitoring_indicators.csv")

time_steps = np.arange(1, 41)

def simulate_path(scenario, strategy):
    state = np.zeros(len(time_steps))
    capacity = np.zeros(len(time_steps))

    state[0] = 1.0 + strategy.baseline_boost
    capacity[0] = scenario.adaptation_gain + strategy.adaptation_boost

    governance_effect = scenario.governance_capacity * strategy.governance_dependency * 0.015
    legitimacy_effect = scenario.public_trust * 0.010
    equity_penalty = max(0.0, scenario.distributional_pressure - strategy.equity_weight) * 0.035
    complexity_penalty = strategy.implementation_complexity * 0.006

    for idx in range(1, len(time_steps)):
        t = idx + 1
        periodic_shock = scenario.shock_level if t % 8 == 0 else scenario.shock_level / 3.0
        absorbed_shock = max(0.0, periodic_shock - strategy.shock_absorption)
        stress = max(0.0, 1.0 - state[idx - 1])
        stress_feedback = scenario.feedback_strength * stress

        capacity[idx] = min(
            0.30,
            capacity[idx - 1]
            + scenario.learning_gain * stress
            + 0.002 * strategy.adaptation_boost
            + governance_effect
        )

        state[idx] = np.clip(
            state[idx - 1]
            + scenario.growth_rate
            - absorbed_shock
            - stress_feedback
            + capacity[idx]
            + legitimacy_effect
            - equity_penalty
            - complexity_penalty,
            0,
            2
        )

    return state, capacity

rows = []

for scenario in scenarios.itertuples(index=False):
    for strategy in strategies.itertuples(index=False):
        state, capacity = simulate_path(scenario, strategy)
        for t, value, adaptive_value in zip(time_steps, state, capacity):
            rows.append({
                "scenario_id": scenario.scenario_id,
                "scenario_name": scenario.scenario_name,
                "strategy_id": strategy.strategy_id,
                "strategy_name": strategy.strategy_name,
                "time_step": t,
                "system_state": value,
                "adaptive_capacity": adaptive_value
            })

paths = pd.DataFrame(rows)

summary = (
    paths.groupby(["scenario_id", "scenario_name", "strategy_id", "strategy_name"])
    .agg(
        final_state=("system_state", "last"),
        min_state=("system_state", "min"),
        mean_state=("system_state", "mean"),
        max_state=("system_state", "max"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
)

summary["viability_score"] = (
    0.35 * summary["final_state"]
    + 0.30 * summary["min_state"]
    + 0.20 * summary["mean_state"]
    + 0.15 * summary["final_adaptive_capacity"]
)

robustness = (
    summary.groupby(["strategy_id", "strategy_name"])
    .agg(
        worst_case_viability=("viability_score", "min"),
        mean_viability=("viability_score", "mean"),
        best_case_viability=("viability_score", "max")
    )
    .reset_index()
)

robustness["viability_range"] = robustness["best_case_viability"] - robustness["worst_case_viability"]
robustness = robustness.sort_values(["worst_case_viability", "mean_viability"], ascending=False)

best_by_scenario = summary.groupby("scenario_id")["viability_score"].transform("max")
summary["regret"] = best_by_scenario - summary["viability_score"]

drivers["driver_priority_score"] = (
    0.25 * drivers["impact_level"]
    + 0.25 * drivers["uncertainty_level"]
    + 0.20 * drivers["interaction_strength"]
    + 0.15 * drivers["time_sensitivity"]
    + 0.15 * drivers["monitoring_need"]
)

frequency = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
monitoring["monitoring_gap"] = (monitoring["target_or_threshold"] - monitoring["baseline"]).abs()
monitoring["review_weight"] = monitoring["review_frequency"].map(frequency).fillna(0.50)
monitoring["monitoring_priority"] = 0.70 * monitoring["monitoring_gap"] + 0.30 * monitoring["review_weight"]

paths.to_csv(OUTPUTS / "advanced_scenario_strategy_paths.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_scenario_strategy_summary.csv", index=False)
robustness.to_csv(OUTPUTS / "advanced_scenario_strategy_robustness.csv", index=False)
drivers.sort_values("driver_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_driver_priority_scores.csv", index=False)
monitoring.sort_values("monitoring_priority", ascending=False).to_csv(OUTPUTS / "advanced_monitoring_trigger_scores.csv", index=False)

plt.figure(figsize=(10, 6))
target_strategy = "Robust Resilience Portfolio"
for scenario_name in paths["scenario_name"].unique():
    subset = paths[(paths["strategy_name"] == target_strategy) & (paths["scenario_name"] == scenario_name)]
    plt.plot(subset["time_step"], subset["system_state"], label=scenario_name)
plt.xlabel("Time Step")
plt.ylabel("System State")
plt.title(f"Scenario Pathways — {target_strategy}")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "robust_resilience_portfolio_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked = robustness.sort_values("worst_case_viability")
plt.barh(ranked["strategy_name"], ranked["worst_case_viability"])
plt.xlabel("Worst-Case Viability")
plt.title("Strategy Robustness Across Scenarios")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_robustness_scores.png", dpi=150)
plt.close()

driver_ranked = drivers.sort_values("driver_priority_score")
plt.figure(figsize=(10, 6))
plt.barh(driver_ranked["driver_name"], driver_ranked["driver_priority_score"])
plt.xlabel("Driver Priority")
plt.title("Scenario Driver Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_priority_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
