#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Thinking and Sustainability.
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

profiles = pd.read_csv(DATA / "sustainability_future_profiles.csv")
scenarios = pd.read_csv(DATA / "sustainability_scenarios.csv")
strategies = pd.read_csv(DATA / "transition_strategies.csv")
risks = pd.read_csv(DATA / "sustainability_risk_indicators.csv")
governance = pd.read_csv(DATA / "governance_capacity_records.csv")
pathways = pd.read_csv(DATA / "transition_pathways.csv")

profiles["sustainability_viability_score"] = (
    0.17 * profiles["ecological_integrity"]
    + 0.15 * profiles["social_equity"]
    + 0.14 * profiles["adaptive_capacity"]
    + 0.10 * profiles["technological_responsibility"]
    + 0.14 * profiles["governance_coordination"]
    + 0.10 * profiles["public_finance_capacity"]
    + 0.10 * profiles["resilience_capacity"]
    + 0.10 * profiles["justice_legitimacy"]
    - 0.08 * profiles["degradation_pressure"]
)

profiles["sustainability_fragility_score"] = (
    0.16 * profiles["degradation_pressure"]
    + 0.15 * (1 - profiles["ecological_integrity"])
    + 0.14 * (1 - profiles["social_equity"])
    + 0.13 * (1 - profiles["governance_coordination"])
    + 0.12 * (1 - profiles["adaptive_capacity"])
    + 0.11 * (1 - profiles["public_finance_capacity"])
    + 0.10 * (1 - profiles["resilience_capacity"])
    + 0.09 * (1 - profiles["justice_legitimacy"])
)

scenarios["sustainability_stress_score"] = (
    0.17 * scenarios["climate_stress"]
    + 0.15 * scenarios["biodiversity_pressure"]
    + 0.13 * scenarios["resource_constraint"]
    + 0.15 * scenarios["inequality_pressure"]
    + 0.12 * scenarios["governance_fragmentation"]
    + 0.12 * scenarios["public_finance_stress"]
    + 0.08 * (1 - scenarios["transition_momentum"])
    + 0.08 * scenarios["technology_change"]
)

scenarios["transition_opportunity_score"] = (
    0.20 * scenarios["transition_momentum"]
    + 0.14 * scenarios["technology_change"]
    + 0.12 * (1 - scenarios["governance_fragmentation"])
    + 0.12 * (1 - scenarios["public_finance_stress"])
    + 0.12 * (1 - scenarios["inequality_pressure"])
    + 0.10 * (1 - scenarios["climate_stress"])
    + 0.10 * (1 - scenarios["biodiversity_pressure"])
    + 0.10 * (1 - scenarios["resource_constraint"])
)

strategies["sustainability_gain_score"] = (
    0.16 * strategies["ecological_gain"]
    + 0.16 * strategies["equity_gain"]
    + 0.14 * strategies["adaptive_capacity_gain"]
    + 0.14 * strategies["governance_gain"]
    + 0.12 * strategies["finance_gain"]
    + 0.12 * strategies["resilience_gain"]
    + 0.12 * strategies["justice_gain"]
    + 0.04 * strategies["implementation_capacity"]
)

risks["sustainability_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["irreversibility"]
    + 0.16 * risks["systemic_reach"]
    + 0.12 * risks["visibility_gap"]
    + 0.15 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["governance_capacity_score"] = (
    0.14 * governance["participation"]
    + 0.14 * governance["accountability"]
    + 0.16 * governance["coordination"]
    + 0.14 * governance["monitoring_capacity"]
    + 0.16 * governance["adaptive_learning"]
    + 0.12 * governance["public_investment"]
    + 0.14 * governance["justice_safeguards"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    exposure = (
        0.22 * row["degradation_pressure"]
        + 0.18 * (1 - row["ecology"])
        + 0.16 * (1 - row["resilience"])
        + 0.16 * (1 - row["governance"])
        + 0.12 * (1 - row["public_finance"])
        + 0.08 * (1 - row["adaptation"])
        + 0.08 * (1 - row["justice"])
    )
    capacity = (
        0.24 * row["governance"]
        + 0.22 * row["adaptation"]
        + 0.18 * row["public_finance"]
        + 0.18 * row["resilience"]
        + 0.18 * row["justice"]
    )
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            stress = 0.16 if t % 9 == 0 else 0.06

            response_gain = (
                0.20 * row["ecology"]
                + 0.18 * row["governance"]
                + 0.18 * row["adaptation"]
                + 0.14 * row["public_finance"]
                + 0.16 * row["resilience"]
                + 0.14 * row["justice"]
            )

            exposure = np.clip(
                exposure
                + 0.05 * stress
                + 0.03 * row["degradation_pressure"]
                - 0.03 * row["ecology"]
                - 0.03 * row["resilience"]
                - 0.02 * row["governance"]
                - 0.02 * row["justice"],
                0,
                1.4,
            )

            capacity = np.clip(
                capacity
                + 0.03 * row["governance"]
                + 0.03 * row["adaptation"]
                + 0.02 * row["public_finance"]
                + 0.02 * row["justice"]
                - 0.04 * stress,
                0,
                1.5,
            )

            viability = np.clip(
                viability
                + 0.07 * response_gain
                + 0.04 * capacity
                - stress
                - 0.05 * exposure
                - 0.03 * row["degradation_pressure"],
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "sustainability_viability": viability,
            "stress_exposure": exposure,
            "institutional_capacity": capacity,
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
        final_viability=("sustainability_viability", "last"),
        mean_viability=("sustainability_viability", "mean"),
        mean_stress_exposure=("stress_exposure", "mean"),
        final_institutional_capacity=("institutional_capacity", "last")
    )
    .reset_index()
    .sort_values("final_viability", ascending=False)
)

profiles.sort_values("sustainability_viability_score", ascending=False).to_csv(OUTPUTS / "advanced_sustainability_profile_scores.csv", index=False)
scenarios.sort_values("sustainability_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_sustainability_scenario_scores.csv", index=False)
strategies.sort_values("sustainability_gain_score", ascending=False).to_csv(OUTPUTS / "advanced_transition_strategy_scores.csv", index=False)
risks.sort_values("sustainability_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_sustainability_risk_priority_scores.csv", index=False)
governance.sort_values("governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_transition_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_transition_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("sustainability_viability_score")
plt.barh(ranked["future_name"], ranked["sustainability_viability_score"])
plt.xlabel("Sustainability Viability Score")
plt.title(f"Sustainability Viability — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "sustainability_viability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["sustainability_viability_score"], profiles["sustainability_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["sustainability_viability_score"], row["sustainability_fragility_score"], row["future_name"], fontsize=7)
plt.xlabel("Sustainability Viability")
plt.ylabel("Sustainability Fragility")
plt.title("Sustainability Viability vs Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "sustainability_viability_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["sustainability_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Sustainability Viability")
plt.title("Sustainability Transition Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "sustainability_transition_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["stress_exposure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Stress Exposure")
plt.title("Sustainability Stress Exposure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "sustainability_stress_exposure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
