#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Public-Sector Foresight Capacity.
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
    import numpy as np
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

profiles = pd.read_csv(DATA / "foresight_capacity_profiles.csv")
signals = pd.read_csv(DATA / "scanning_signals.csv")
uptake = pd.read_csv(DATA / "decision_uptake_register.csv")
scenarios = pd.read_csv(DATA / "scenario_cycle_profiles.csv")
pathways = pd.read_csv(DATA / "adaptive_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

profiles["foresight_capacity_score"] = (
    0.12 * profiles["scanning_capacity"]
    + 0.12 * profiles["scenario_capacity"]
    + 0.14 * profiles["decision_uptake"]
    + 0.12 * profiles["participation_capacity"]
    + 0.12 * profiles["budget_connection"]
    + 0.10 * profiles["evaluation_capacity"]
    + 0.10 * profiles["institutional_learning"]
    + 0.10 * profiles["implementation_authority"]
    + 0.05 * profiles["knowledge_infrastructure"]
    + 0.03 * profiles["legitimacy"]
)

profiles["capacity_gap_score"] = (
    0.16 * (1 - profiles["decision_uptake"])
    + 0.14 * (1 - profiles["budget_connection"])
    + 0.14 * (1 - profiles["implementation_authority"])
    + 0.12 * (1 - profiles["scanning_capacity"])
    + 0.12 * (1 - profiles["scenario_capacity"])
    + 0.10 * (1 - profiles["participation_capacity"])
    + 0.10 * (1 - profiles["evaluation_capacity"])
    + 0.08 * (1 - profiles["institutional_learning"])
    + 0.04 * (1 - profiles["knowledge_infrastructure"])
)

signals["scanning_signal_priority_score"] = (
    0.16 * signals["signal_strength"]
    + 0.12 * signals["novelty"]
    + 0.12 * signals["uncertainty"]
    + 0.18 * signals["policy_relevance"]
    + 0.16 * signals["equity_relevance"]
    + 0.12 * signals["detection_difficulty"]
    + 0.14 * (1 - signals["response_readiness"])
)
signals["response_gap_score"] = 1 - signals["response_readiness"]

uptake["decision_uptake_score"] = (
    0.20 * uptake["uptake_strength"]
    + 0.18 * uptake["budget_influence"]
    + 0.14 * uptake["regulatory_influence"]
    + 0.12 * uptake["procurement_influence"]
    + 0.14 * uptake["implementation_influence"]
    + 0.12 * uptake["evaluation_influence"]
    + 0.10 * uptake["participation_influence"]
)

scenarios["foresight_stress_pressure_score"] = (
    0.16 * scenarios["technology_disruption"]
    + 0.18 * scenarios["climate_stress"]
    + 0.14 * scenarios["fiscal_pressure"]
    + 0.12 * (1 - scenarios["public_trust"])
    + 0.12 * (1 - scenarios["institutional_capacity"])
    + 0.10 * (1 - scenarios["participation_quality"])
    + 0.08 * (1 - scenarios["review_frequency"])
    + 0.10 * scenarios["implementation_pressure"]
)

scenarios["foresight_opportunity_score"] = (
    0.22 * scenarios["institutional_capacity"]
    + 0.20 * scenarios["participation_quality"]
    + 0.18 * scenarios["public_trust"]
    + 0.14 * scenarios["review_frequency"]
    + 0.10 * (1 - scenarios["fiscal_pressure"])
    + 0.08 * (1 - scenarios["technology_disruption"])
    + 0.08 * (1 - scenarios["climate_stress"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    capacity = float(row["initial_capacity"])
    uptake_state = 0.5 * float(row["budget"]) + 0.5 * float(row["authority"])
    legitimacy = float(row["legitimacy"])
    learning_state = float(row["learning"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            pressure = 0.16 if t % 8 == 0 else 0.06
            analytic_gain = 0.22 * row["scanning"] + 0.22 * row["scenarios"]
            institutional_gain = 0.20 * row["budget"] + 0.18 * row["authority"] + 0.16 * row["evaluation"]
            democratic_gain = 0.16 * row["participation"] + 0.10 * legitimacy
            learning_gain = 0.14 * learning_state

            uptake_state = np.clip(
                uptake_state + 0.05 * row["budget"] + 0.05 * row["authority"] + 0.03 * row["evaluation"] - 0.04 * pressure,
                0,
                1.4,
            )

            legitimacy = np.clip(
                legitimacy + 0.05 * row["participation"] + 0.03 * row["evaluation"] + 0.02 * row["legitimacy"] - 0.03 * pressure,
                0,
                1.4,
            )

            learning_state = np.clip(
                learning_state + 0.04 * row["learning"] + 0.03 * row["evaluation"] + 0.02 * uptake_state - 0.02 * pressure,
                0,
                1.4,
            )

            capacity = np.clip(
                capacity + analytic_gain / 6 + institutional_gain / 6 + democratic_gain / 7 + learning_gain / 7 - 0.08 * pressure + 0.04 * uptake_state,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "capacity_id": row["capacity_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "foresight_capacity": capacity,
            "decision_uptake": uptake_state,
            "legitimacy_score": legitimacy,
            "learning_score": learning_state,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "capacity_id", "scenario_id", "pathway_name"])
    .agg(
        final_foresight_capacity=("foresight_capacity", "last"),
        mean_foresight_capacity=("foresight_capacity", "mean"),
        final_decision_uptake=("decision_uptake", "last"),
        final_legitimacy_score=("legitimacy_score", "last"),
        final_learning_score=("learning_score", "last")
    )
    .reset_index()
    .sort_values("final_foresight_capacity", ascending=False)
)

strategies["foresight_capacity_strategy_score"] = (
    0.12 * strategies["foresight_mandate"]
    + 0.12 * strategies["horizon_scanning"]
    + 0.13 * strategies["scenario_cycles"]
    + 0.13 * strategies["decision_pathways"]
    + 0.12 * strategies["participatory_foresight"]
    + 0.12 * strategies["budget_alignment"]
    + 0.10 * strategies["evaluation_capacity"]
    + 0.08 * strategies["knowledge_infrastructure"]
    + 0.08 * strategies["implementation_authority"]
)

strategies["implementation_authority_strategy_score"] = (
    0.18 * strategies["implementation_authority"]
    + 0.18 * strategies["budget_alignment"]
    + 0.14 * strategies["decision_pathways"]
    + 0.12 * strategies["evaluation_capacity"]
    + 0.10 * strategies["foresight_mandate"]
    + 0.10 * strategies["scenario_cycles"]
    + 0.09 * strategies["horizon_scanning"]
    + 0.09 * strategies["knowledge_infrastructure"]
)

profiles.sort_values("foresight_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_capacity_scores.csv", index=False)
signals.sort_values("scanning_signal_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_scanning_signal_scores.csv", index=False)
uptake.sort_values("decision_uptake_score", ascending=False).to_csv(OUTPUTS / "advanced_decision_uptake_scores.csv", index=False)
scenarios.sort_values("foresight_stress_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_scenario_cycle_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_foresight_capacity_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_foresight_capacity_pathway_summary.csv", index=False)
strategies.sort_values("foresight_capacity_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("foresight_capacity_score")
plt.barh(ranked["foresight_model"], ranked["foresight_capacity_score"])
plt.xlabel("Foresight Capacity")
plt.title(f"Public-Sector Foresight Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "foresight_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_signal = signals.sort_values("scanning_signal_priority_score")
plt.barh(ranked_signal["signal_name"], ranked_signal["scanning_signal_priority_score"])
plt.xlabel("Signal Priority")
plt.title("Scanning Signal Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "scanning_signal_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["foresight_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Foresight Capacity")
plt.title("Foresight Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "foresight_capacity_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["decision_uptake"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Decision Uptake")
plt.title("Foresight Decision Uptake Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "foresight_decision_uptake_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
