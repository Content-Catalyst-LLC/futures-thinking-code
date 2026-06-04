#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Climate Futures and Environmental Change.
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

profiles = pd.read_csv(DATA / "climate_future_profiles.csv")
scenarios = pd.read_csv(DATA / "climate_scenarios.csv")
strategies = pd.read_csv(DATA / "mitigation_adaptation_strategies.csv")
risks = pd.read_csv(DATA / "climate_risk_indicators.csv")
governance = pd.read_csv(DATA / "climate_governance_records.csv")
pathways = pd.read_csv(DATA / "climate_pathways.csv")

profiles["climate_readiness_score"] = (
    -0.16 * profiles["emissions_intensity"]
    + 0.15 * profiles["adaptation_capacity"]
    - 0.15 * profiles["ecosystem_stress"]
    + 0.14 * profiles["governance_coordination"]
    - 0.12 * profiles["social_vulnerability"]
    + 0.10 * profiles["technology_deployment"]
    + 0.14 * profiles["transition_speed"]
    + 0.12 * profiles["justice_capacity"]
    - 0.10 * profiles["residual_loss"]
)

profiles["climate_fragility_score"] = (
    0.16 * profiles["emissions_intensity"]
    + 0.15 * profiles["ecosystem_stress"]
    + 0.14 * profiles["social_vulnerability"]
    + 0.13 * profiles["residual_loss"]
    + 0.12 * (1 - profiles["adaptation_capacity"])
    + 0.12 * (1 - profiles["governance_coordination"])
    + 0.10 * (1 - profiles["transition_speed"])
    + 0.08 * (1 - profiles["justice_capacity"])
)

scenarios["climate_stress_score"] = (
    0.15 * scenarios["emissions_pressure"]
    + 0.15 * scenarios["feedback_pressure"]
    + 0.15 * scenarios["physical_hazard_pressure"]
    + 0.13 * scenarios["ecological_degradation"]
    + 0.14 * scenarios["social_vulnerability_pressure"]
    + 0.12 * scenarios["governance_fragmentation"]
    + 0.10 * scenarios["adaptation_finance_gap"]
    + 0.06 * (1 - scenarios["transition_momentum"])
)

scenarios["transition_opportunity_score"] = (
    0.22 * scenarios["transition_momentum"]
    + 0.14 * (1 - scenarios["emissions_pressure"])
    + 0.12 * (1 - scenarios["governance_fragmentation"])
    + 0.12 * (1 - scenarios["adaptation_finance_gap"])
    + 0.12 * (1 - scenarios["social_vulnerability_pressure"])
    + 0.10 * (1 - scenarios["ecological_degradation"])
    + 0.09 * (1 - scenarios["feedback_pressure"])
    + 0.09 * (1 - scenarios["physical_hazard_pressure"])
)

strategies["climate_strategy_value_score"] = (
    0.17 * strategies["mitigation_effect"]
    + 0.16 * strategies["adaptation_gain"]
    + 0.15 * strategies["vulnerability_reduction"]
    + 0.14 * strategies["ecosystem_protection"]
    + 0.13 * strategies["governance_gain"]
    + 0.11 * strategies["finance_capacity"]
    + 0.10 * strategies["justice_gain"]
    + 0.04 * strategies["implementation_capacity"]
)

risks["climate_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["irreversibility"]
    + 0.16 * risks["systemic_reach"]
    + 0.12 * risks["visibility_gap"]
    + 0.15 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["climate_governance_capacity_score"] = (
    0.16 * governance["mitigation_governance"]
    + 0.16 * governance["adaptation_governance"]
    + 0.14 * governance["public_finance"]
    + 0.14 * governance["monitoring_capacity"]
    + 0.16 * governance["coordination"]
    + 0.10 * governance["participation"]
    + 0.14 * governance["justice_safeguards"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    stress = float(row["initial_climate_stress"])
    vulnerability = 0.70 - 0.35 * row["vulnerability_reduction"] + 0.10 * (1 - row["justice_capacity"])
    capacity = 0.30 + 0.35 * row["adaptation"] + 0.25 * row["governance_capacity"] + 0.15 * row["justice_capacity"]
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            feedback_event = row["feedback_pressure"] if t % 10 == 0 else row["feedback_pressure"] * 0.45

            capacity = np.clip(
                capacity
                + 0.03 * row["governance_capacity"]
                + 0.03 * row["adaptation"]
                + 0.02 * row["justice_capacity"]
                - 0.02 * feedback_event,
                0,
                1.5,
            )

            vulnerability = np.clip(
                vulnerability
                - 0.03 * row["vulnerability_reduction"]
                - 0.02 * row["governance_capacity"]
                - 0.02 * row["justice_capacity"]
                + 0.02 * stress,
                0,
                1.2,
            )

            stress = np.clip(
                stress
                + row["emissions"]
                - row["sink_strength"]
                + feedback_event
                - 0.18 * row["adaptation"]
                - 0.08 * row["governance_capacity"]
                - 0.05 * row["justice_capacity"],
                0,
                3.0,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "climate_stress_index": stress,
            "social_vulnerability_index": vulnerability,
            "adaptive_capacity_index": capacity,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths
    .groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_climate_stress=("climate_stress_index", "last"),
        mean_climate_stress=("climate_stress_index", "mean"),
        final_social_vulnerability=("social_vulnerability_index", "last"),
        final_adaptive_capacity=("adaptive_capacity_index", "last")
    )
    .reset_index()
    .sort_values("final_climate_stress")
)

profiles.sort_values("climate_readiness_score", ascending=False).to_csv(OUTPUTS / "advanced_climate_profile_scores.csv", index=False)
scenarios.sort_values("climate_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_climate_scenario_scores.csv", index=False)
strategies.sort_values("climate_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_mitigation_adaptation_strategy_scores.csv", index=False)
risks.sort_values("climate_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_climate_risk_priority_scores.csv", index=False)
governance.sort_values("climate_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_climate_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_climate_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_climate_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("climate_readiness_score")
plt.barh(ranked["future_name"], ranked["climate_readiness_score"])
plt.xlabel("Climate Readiness Score")
plt.title(f"Climate Readiness — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "climate_readiness_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["climate_readiness_score"], profiles["climate_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["climate_readiness_score"], row["climate_fragility_score"], row["future_name"], fontsize=7)
plt.xlabel("Climate Readiness")
plt.ylabel("Climate Fragility")
plt.title("Climate Readiness vs Climate Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "climate_readiness_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["climate_stress_index"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Climate Stress Index")
plt.title("Climate Stress Pathways")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "climate_stress_pathways.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["social_vulnerability_index"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Social Vulnerability Index")
plt.title("Social Vulnerability Across Climate Futures")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "climate_social_vulnerability_pathways.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
