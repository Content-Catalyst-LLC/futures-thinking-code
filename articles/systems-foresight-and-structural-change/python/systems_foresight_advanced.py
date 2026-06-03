#!/usr/bin/env python3
"""
Advanced pandas/numpy/matplotlib workflow for Systems Foresight and Structural Change.
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

systems = pd.read_csv(DATA / "system_domains.csv")
feedback = pd.read_csv(DATA / "feedback_loops.csv")
leverage = pd.read_csv(DATA / "leverage_points.csv")
signals = pd.read_csv(DATA / "signals_pressure.csv")
strategies = pd.read_csv(DATA / "strategy_pathways.csv")
monitoring = pd.read_csv(DATA / "monitoring_triggers.csv")

systems["structural_pressure_score"] = (
    0.22 * systems["system_stress"]
    + 0.16 * (1 - systems["adaptive_capacity"])
    + 0.14 * (1 - systems["public_trust"])
    + 0.16 * systems["interdependence"]
    + 0.14 * systems["distributional_vulnerability"]
    + 0.09 * systems["institutional_fragmentation"]
    + 0.09 * systems["structural_lock_in"]
)

feedback["feedback_priority_score"] = feedback["feedback_strength"] * (
    0.40 * feedback["delay_risk"]
    + 0.30 * (1 - feedback["visibility"])
    + 0.30 * (1 - feedback["institutional_control"])
)

leverage["leverage_score"] = (
    leverage["intervention_depth"]
    * leverage["system_reach"]
    * leverage["political_feasibility"]
    * leverage["legitimacy_quality"]
    * leverage["equity_quality"]
    * leverage["implementation_readiness"]
)

signals["signal_priority_score"] = (
    0.15 * signals["novelty"]
    + 0.30 * signals["structural_relevance"]
    + 0.25 * signals["urgency"]
    + 0.15 * signals["visibility"]
    + 0.15 * signals["affected_voice"]
)

frequency = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
monitoring["monitoring_gap"] = (monitoring["threshold"] - monitoring["baseline"]).abs()
monitoring["review_weight"] = monitoring["review_frequency"].map(frequency).fillna(0.50)
monitoring["monitoring_priority"] = 0.70 * monitoring["monitoring_gap"] + 0.30 * monitoring["review_weight"]

time_steps = np.arange(1, 41)
paths = []

def structural_pressure(stress, capacity, trust, interdependence, vulnerability):
    return (
        0.26 * stress
        + 0.22 * (1 - capacity)
        + 0.18 * (1 - trust)
        + 0.18 * interdependence
        + 0.16 * vulnerability
    )

for strategy in strategies.itertuples(index=False):
    stress = 0.84
    capacity = 0.42
    trust = 0.46
    interdependence = 0.86
    vulnerability = 0.88

    for t in time_steps:
        shock = 0.08 if t % 10 == 0 else 0.02
        learning_effect = strategy.structural_depth * max(0, 0.75 - capacity) * 0.010
        implementation_drag = strategy.implementation_complexity * 0.002
        coordination_bonus = strategy.governance_dependency * strategy.structural_depth * 0.0015

        stress = np.clip(stress + shock - strategy.stress_reduction - learning_effect - coordination_bonus, 0, 1)
        capacity = np.clip(capacity + strategy.capacity_gain + learning_effect - implementation_drag, 0, 1)
        trust = np.clip(trust + strategy.trust_gain - 0.020 * shock + 0.003 * strategy.structural_depth, 0, 1)
        vulnerability = np.clip(vulnerability - strategy.vulnerability_reduction + 0.010 * shock - 0.002 * strategy.structural_depth, 0, 1)

        pressure = structural_pressure(stress, capacity, trust, interdependence, vulnerability)

        paths.append({
            "strategy_id": strategy.strategy_id,
            "strategy_name": strategy.strategy_name,
            "strategy_type": strategy.strategy_type,
            "time_step": t,
            "stress": stress,
            "adaptive_capacity": capacity,
            "trust": trust,
            "interdependence": interdependence,
            "distributional_vulnerability": vulnerability,
            "structural_depth": strategy.structural_depth,
            "structural_pressure": pressure
        })

pathways = pd.DataFrame(paths)

summary = (
    pathways.groupby(["strategy_id", "strategy_name", "strategy_type"])
    .agg(
        final_pressure=("structural_pressure", "last"),
        mean_pressure=("structural_pressure", "mean"),
        max_pressure=("structural_pressure", "max"),
        final_capacity=("adaptive_capacity", "last"),
        final_trust=("trust", "last"),
        final_vulnerability=("distributional_vulnerability", "last")
    )
    .reset_index()
)

summary["structural_change_score"] = (
    0.30 * (1 - summary["final_pressure"])
    + 0.25 * summary["final_capacity"]
    + 0.20 * summary["final_trust"]
    + 0.25 * (1 - summary["final_vulnerability"])
)

systems.sort_values("structural_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_structural_pressure_scores.csv", index=False)
feedback.sort_values("feedback_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_feedback_loop_priority_scores.csv", index=False)
leverage.sort_values("leverage_score", ascending=False).to_csv(OUTPUTS / "advanced_leverage_point_scores.csv", index=False)
signals.sort_values("signal_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_signal_pressure_scores.csv", index=False)
pathways.to_csv(OUTPUTS / "advanced_structural_change_pathways.csv", index=False)
summary.sort_values("structural_change_score", ascending=False).to_csv(OUTPUTS / "advanced_structural_change_summary.csv", index=False)
monitoring.sort_values("monitoring_priority", ascending=False).to_csv(OUTPUTS / "advanced_monitoring_trigger_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked_systems = systems.sort_values("structural_pressure_score")
plt.barh(ranked_systems["system_domain"], ranked_systems["structural_pressure_score"])
plt.xlabel("Structural Pressure Score")
plt.title(f"Structural Pressure by System Domain — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "structural_pressure_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_leverage = leverage.sort_values("leverage_score")
plt.barh(ranked_leverage["intervention"], ranked_leverage["leverage_score"])
plt.xlabel("Leverage Score")
plt.title("Leverage Point Scores for Structural Change")
plt.tight_layout()
plt.savefig(OUTPUTS / "leverage_point_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for strategy_name in pathways["strategy_name"].unique():
    subset = pathways[pathways["strategy_name"] == strategy_name]
    plt.plot(subset["time_step"], subset["structural_pressure"], label=strategy_name)
plt.xlabel("Time Step")
plt.ylabel("Structural Pressure")
plt.title("Structural Pressure Across Strategy Pathways")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "structural_pressure_pathways.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_summary = summary.sort_values("structural_change_score")
plt.barh(ranked_summary["strategy_name"], ranked_summary["structural_change_score"])
plt.xlabel("Structural Change Score")
plt.title("Structural Change Strategy Comparison")
plt.tight_layout()
plt.savefig(OUTPUTS / "structural_change_strategy_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
