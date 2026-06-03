#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Anticipatory Governance.
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

profiles = pd.read_csv(DATA / "governance_profiles.csv")
signals = pd.read_csv(DATA / "weak_signal_register.csv")
risks = pd.read_csv(DATA / "emerging_risk_register.csv")
scenarios = pd.read_csv(DATA / "scenario_profiles.csv")
pathways = pd.read_csv(DATA / "adaptive_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

profiles["anticipatory_capacity_score"] = (
    0.12 * profiles["detection_capacity"]
    + 0.12 * profiles["interpretation_capacity"]
    + 0.12 * profiles["scenario_capacity"]
    + 0.12 * profiles["preparedness_capacity"]
    + 0.12 * profiles["legitimacy"]
    + 0.10 * profiles["coordination_capacity"]
    + 0.10 * profiles["adaptive_authority"]
    + 0.08 * profiles["equity_safeguards"]
    + 0.07 * profiles["learning_capacity"]
    + 0.05 * profiles["implementation_connection"]
)

profiles["anticipatory_fragility_pressure_score"] = (
    0.16 * (1 - profiles["detection_capacity"])
    + 0.14 * (1 - profiles["preparedness_capacity"])
    + 0.14 * (1 - profiles["adaptive_authority"])
    + 0.14 * (1 - profiles["coordination_capacity"])
    + 0.14 * (1 - profiles["legitimacy"])
    + 0.12 * (1 - profiles["equity_safeguards"])
    + 0.08 * (1 - profiles["learning_capacity"])
    + 0.08 * (1 - profiles["implementation_connection"])
)

signals["weak_signal_priority_score"] = (
    0.16 * signals["signal_strength"]
    + 0.14 * signals["novelty"]
    + 0.12 * signals["uncertainty"]
    + 0.18 * signals["system_relevance"]
    + 0.16 * signals["justice_relevance"]
    + 0.12 * signals["detection_difficulty"]
    + 0.12 * (1 - signals["response_readiness"])
)
signals["response_gap_score"] = 1 - signals["response_readiness"]

risks["emerging_risk_priority_score"] = (
    0.16 * risks["probability"]
    + 0.18 * risks["severity"]
    + 0.14 * risks["uncertainty"]
    + 0.14 * risks["detection_difficulty"]
    + 0.14 * risks["justice_exposure"]
    + 0.14 * risks["governance_gap"]
    + 0.10 * (1 - risks["mitigation_capacity"])
)

scenarios["future_stress_pressure_score"] = (
    0.16 * scenarios["technology_acceleration"]
    + 0.18 * scenarios["climate_stress"]
    + 0.14 * (1 - scenarios["public_trust"])
    + 0.14 * scenarios["geopolitical_volatility"]
    + 0.12 * scenarios["fiscal_pressure"]
    + 0.10 * (1 - scenarios["institutional_capacity"])
    + 0.08 * (1 - scenarios["participation_quality"])
    + 0.08 * scenarios["crisis_frequency"]
)

scenarios["democratic_anticipatory_opportunity_score"] = (
    0.22 * scenarios["institutional_capacity"]
    + 0.22 * scenarios["participation_quality"]
    + 0.20 * scenarios["public_trust"]
    + 0.12 * (1 - scenarios["fiscal_pressure"])
    + 0.10 * (1 - scenarios["crisis_frequency"])
    + 0.08 * (1 - scenarios["geopolitical_volatility"])
    + 0.06 * (1 - scenarios["climate_stress"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    capacity = float(row["initial_capacity"])
    legitimacy_state = float(row["legitimacy"])
    learning_state = 0.5 * float(row["interpretation"]) + 0.5 * float(row["adaptive_authority"])
    risk_pressure = 0.55
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.16 if t % 8 == 0 else 0.06
            warning_effect = 0.22 * row["detection"] + 0.18 * row["interpretation"]
            response_effect = 0.20 * row["preparedness"] + 0.18 * row["coordination"] + 0.16 * row["adaptive_authority"]
            democratic_effect = 0.14 * legitimacy_state + 0.12 * row["equity"]
            learning_effect = 0.12 * learning_state

            risk_pressure = np.clip(risk_pressure + shock - 0.10 * warning_effect - 0.08 * response_effect, 0, 1.5)

            learning_state = np.clip(
                learning_state + 0.04 * row["interpretation"] + 0.04 * row["adaptive_authority"] + 0.02 * row["coordination"] + 0.02 * row["learning"] - 0.03 * shock,
                0,
                1.4,
            )

            legitimacy_state = np.clip(
                legitimacy_state + 0.04 * row["legitimacy"] + 0.03 * row["equity"] + 0.02 * row["preparedness"] - 0.04 * risk_pressure,
                0,
                1.4,
            )

            capacity = np.clip(
                capacity + warning_effect / 5 + response_effect / 5 + democratic_effect / 6 + learning_effect / 6 - 0.10 * risk_pressure,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "governance_id": row["governance_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "anticipatory_capacity": capacity,
            "legitimacy_score": legitimacy_state,
            "learning_score": learning_state,
            "risk_pressure": risk_pressure,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "governance_id", "scenario_id", "pathway_name"])
    .agg(
        final_anticipatory_capacity=("anticipatory_capacity", "last"),
        mean_anticipatory_capacity=("anticipatory_capacity", "mean"),
        final_legitimacy_score=("legitimacy_score", "last"),
        final_learning_score=("learning_score", "last"),
        mean_risk_pressure=("risk_pressure", "mean")
    )
    .reset_index()
    .sort_values("final_anticipatory_capacity", ascending=False)
)

strategies["anticipatory_governance_strategy_score"] = (
    0.12 * strategies["horizon_scanning"]
    + 0.12 * strategies["scenario_planning"]
    + 0.14 * strategies["early_warning"]
    + 0.14 * strategies["adaptive_regulation"]
    + 0.14 * strategies["public_participation"]
    + 0.12 * strategies["budget_alignment"]
    + 0.10 * strategies["evaluation_capacity"]
    + 0.08 * strategies["equity_safeguards"]
    + 0.04 * strategies["implementation_authority"]
)

strategies["operational_authority_strategy_score"] = (
    0.18 * strategies["implementation_authority"]
    + 0.16 * strategies["budget_alignment"]
    + 0.14 * strategies["early_warning"]
    + 0.14 * strategies["adaptive_regulation"]
    + 0.12 * strategies["evaluation_capacity"]
    + 0.10 * strategies["horizon_scanning"]
    + 0.08 * strategies["scenario_planning"]
    + 0.08 * strategies["public_participation"]
)

profiles.sort_values("anticipatory_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_profile_scores.csv", index=False)
signals.sort_values("weak_signal_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_weak_signal_scores.csv", index=False)
risks.sort_values("emerging_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_emerging_risk_scores.csv", index=False)
scenarios.sort_values("future_stress_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_scenario_profile_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_anticipatory_governance_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_anticipatory_governance_pathway_summary.csv", index=False)
strategies.sort_values("anticipatory_governance_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("anticipatory_capacity_score")
plt.barh(ranked["governance_strategy"], ranked["anticipatory_capacity_score"])
plt.xlabel("Anticipatory Capacity")
plt.title(f"Anticipatory Governance Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "anticipatory_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_signal = signals.sort_values("weak_signal_priority_score")
plt.barh(ranked_signal["signal_name"], ranked_signal["weak_signal_priority_score"])
plt.xlabel("Weak Signal Priority")
plt.title("Weak Signal Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "weak_signal_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["anticipatory_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Anticipatory Capacity")
plt.title("Anticipatory Governance Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "anticipatory_capacity_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["risk_pressure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Risk Pressure")
plt.title("Risk Pressure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "anticipatory_risk_pressure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
