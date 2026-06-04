#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Urban Futures.
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

profiles = pd.read_csv(DATA / "urban_system_profiles.csv")
scenarios = pd.read_csv(DATA / "urban_scenarios.csv")
strategies = pd.read_csv(DATA / "urban_strategy_options.csv")
risks = pd.read_csv(DATA / "urban_risk_indicators.csv")
governance = pd.read_csv(DATA / "urban_governance_records.csv")
pathways = pd.read_csv(DATA / "urban_stress_pathways.csv")

profiles["urban_viability_score"] = (
    0.17 * profiles["infrastructure_strength"]
    + 0.16 * profiles["governance_capacity"]
    + 0.14 * profiles["housing_affordability"]
    - 0.14 * profiles["climate_exposure"]
    - 0.14 * profiles["inequality"]
    + 0.09 * profiles["digital_integration"]
    + 0.12 * profiles["public_finance_capacity"]
    + 0.14 * profiles["social_cohesion"]
    - 0.08 * profiles["maintenance_backlog"]
)

profiles["urban_fragility_score"] = (
    0.15 * profiles["climate_exposure"]
    + 0.15 * profiles["inequality"]
    + 0.14 * profiles["maintenance_backlog"]
    + 0.13 * (1 - profiles["infrastructure_strength"])
    + 0.13 * (1 - profiles["governance_capacity"])
    + 0.12 * (1 - profiles["housing_affordability"])
    + 0.10 * (1 - profiles["public_finance_capacity"])
    + 0.10 * (1 - profiles["social_cohesion"])
    + 0.08 * profiles["digital_integration"]
)

scenarios["urban_stress_score"] = (
    0.15 * scenarios["infrastructure_stress"]
    + 0.16 * scenarios["housing_pressure"]
    + 0.15 * scenarios["climate_pressure"]
    + 0.12 * scenarios["fiscal_pressure"]
    + 0.10 * scenarios["digital_dependency"]
    + 0.10 * scenarios["migration_pressure"]
    + 0.12 * scenarios["governance_fragmentation"]
    + 0.10 * scenarios["social_fragmentation"]
)

strategies["urban_strategy_value_score"] = (
    0.16 * strategies["infrastructure_gain"]
    + 0.16 * strategies["housing_stability_gain"]
    + 0.14 * strategies["climate_resilience_gain"]
    + 0.14 * strategies["governance_gain"]
    + 0.12 * strategies["finance_gain"]
    + 0.10 * strategies["digital_accountability_gain"]
    + 0.14 * strategies["social_cohesion_gain"]
    + 0.04 * strategies["implementation_capacity"]
)

risks["urban_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["urban_governance_capacity_score"] = (
    0.16 * governance["coordination"]
    + 0.14 * governance["participation"]
    + 0.14 * governance["public_finance"]
    + 0.14 * governance["maintenance_capacity"]
    + 0.12 * governance["digital_accountability"]
    + 0.15 * governance["housing_governance"]
    + 0.15 * governance["climate_governance"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    load = (
        0.18 * row["climate_exposure"]
        + 0.14 * row["maintenance_backlog"]
        + 0.14 * (1 - row["infrastructure"])
        + 0.14 * (1 - row["housing_stability"])
        + 0.12 * (1 - row["public_finance"])
        + 0.12 * (1 - row["governance"])
        + 0.10 * (1 - row["social_cohesion"])
        + 0.06 * row["digital_dependency"]
    )
    capacity = (
        0.20 * row["infrastructure"]
        + 0.22 * row["governance"]
        + 0.18 * row["public_finance"]
        + 0.16 * row["housing_stability"]
        + 0.16 * row["social_cohesion"]
        + 0.08 * (1 - row["climate_exposure"])
    )
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.18 if t % 8 == 0 else 0.07

            response_gain = (
                0.18 * row["infrastructure"]
                + 0.22 * row["governance"]
                + 0.18 * row["public_finance"]
                + 0.16 * row["housing_stability"]
                + 0.16 * row["social_cohesion"]
                + 0.10 * (1 - row["climate_exposure"])
            )

            load = np.clip(
                load
                + 0.05 * shock
                + 0.03 * row["climate_exposure"]
                + 0.03 * row["maintenance_backlog"]
                + 0.02 * row["digital_dependency"]
                - 0.03 * row["infrastructure"]
                - 0.03 * row["governance"]
                - 0.02 * row["housing_stability"],
                0,
                1.5,
            )

            capacity = np.clip(
                capacity
                + 0.03 * row["governance"]
                + 0.03 * row["public_finance"]
                + 0.02 * row["social_cohesion"]
                + 0.02 * row["infrastructure"]
                - 0.03 * shock,
                0,
                1.6,
            )

            viability = np.clip(
                viability
                + 0.07 * response_gain
                + 0.04 * capacity
                - shock
                - 0.06 * load
                - 0.02 * row["maintenance_backlog"],
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "urban_viability": viability,
            "system_load": load,
            "adaptive_capacity": capacity,
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
        final_urban_viability=("urban_viability", "last"),
        mean_urban_viability=("urban_viability", "mean"),
        mean_system_load=("system_load", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_urban_viability", ascending=False)
)

profiles.sort_values("urban_viability_score", ascending=False).to_csv(OUTPUTS / "advanced_urban_profile_scores.csv", index=False)
scenarios.sort_values("urban_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_urban_scenario_scores.csv", index=False)
strategies.sort_values("urban_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_urban_strategy_scores.csv", index=False)
risks.sort_values("urban_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_urban_risk_priority_scores.csv", index=False)
governance.sort_values("urban_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_urban_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_urban_stress_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_urban_stress_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("urban_viability_score")
plt.barh(ranked["city_future_name"], ranked["urban_viability_score"])
plt.xlabel("Urban Viability Score")
plt.title(f"Urban Viability — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "urban_viability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["urban_viability_score"], profiles["urban_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["urban_viability_score"], row["urban_fragility_score"], row["city_future_name"], fontsize=7)
plt.xlabel("Urban Viability")
plt.ylabel("Urban Fragility")
plt.title("Urban Viability vs Urban Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "urban_viability_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["urban_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Urban Viability")
plt.title("Urban Stress and Adaptive Response")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "urban_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["system_load"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("System Load")
plt.title("Urban System Load Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "urban_system_load_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
