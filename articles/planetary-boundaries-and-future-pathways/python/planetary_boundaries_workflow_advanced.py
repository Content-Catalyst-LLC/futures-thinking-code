#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Planetary Boundaries and Future Pathways.
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

profiles = pd.read_csv(DATA / "planetary_pathway_profiles.csv")
scenarios = pd.read_csv(DATA / "boundary_scenarios.csv")
strategies = pd.read_csv(DATA / "pathway_strategy_options.csv")
risks = pd.read_csv(DATA / "planetary_risk_indicators.csv")
governance = pd.read_csv(DATA / "planetary_governance_records.csv")
simulations = pd.read_csv(DATA / "planetary_pathway_simulations.csv")

profiles["total_boundary_pressure_score"] = (
    0.16 * profiles["climate_pressure"]
    + 0.16 * profiles["biosphere_pressure"]
    + 0.12 * profiles["land_pressure"]
    + 0.12 * profiles["freshwater_pressure"]
    + 0.10 * profiles["nutrient_pressure"]
    + 0.10 * profiles["ocean_pressure"]
    + 0.08 * profiles["aerosol_pressure"]
    + 0.10 * profiles["novel_entity_pressure"]
    + 0.06 * profiles["technology_dependence"]
)

profiles["safe_and_just_pathway_score"] = (
    0.22 * profiles["social_foundation_security"]
    + 0.20 * profiles["governance_capacity"]
    + 0.20 * profiles["justice_capacity"]
    + 0.14 * profiles["regeneration_capacity"]
    - 0.20 * profiles["total_boundary_pressure_score"]
    + 0.04 * (1 - profiles["technology_dependence"])
)

scenarios["planetary_stress_score"] = (
    0.16 * scenarios["climate_stress"]
    + 0.16 * scenarios["biosphere_stress"]
    + 0.12 * scenarios["land_stress"]
    + 0.12 * scenarios["freshwater_stress"]
    + 0.10 * scenarios["nutrient_stress"]
    + 0.10 * scenarios["ocean_stress"]
    + 0.08 * scenarios["aerosol_stress"]
    + 0.10 * scenarios["novel_entity_stress"]
    + 0.08 * scenarios["social_stress"]
    + 0.08 * scenarios["governance_fragmentation"]
)

strategies["pathway_strategy_value_score"] = (
    0.14 * strategies["climate_reduction"]
    + 0.14 * strategies["biosphere_recovery"]
    + 0.11 * strategies["land_restoration"]
    + 0.11 * strategies["water_security"]
    + 0.09 * strategies["nutrient_circularity"]
    + 0.09 * strategies["novel_entity_control"]
    + 0.12 * strategies["social_foundation_gain"]
    + 0.10 * strategies["governance_gain"]
    + 0.08 * strategies["justice_gain"]
    + 0.02 * strategies["implementation_capacity"]
)

risks["planetary_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["planetary_governance_capacity_score"] = (
    0.16 * governance["monitoring_capacity"]
    + 0.17 * governance["policy_coordination"]
    + 0.15 * governance["public_finance"]
    + 0.14 * governance["participation"]
    + 0.15 * governance["justice_safeguards"]
    + 0.12 * governance["international_cooperation"]
    + 0.11 * governance["implementation_capacity"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    pressure = float(row["boundary_pressure"])
    social = float(row["social_foundations"])
    governance_capacity = float(row["governance"])
    justice = float(row["justice"])
    technology = float(row["technology_dependence"])
    regeneration = float(row["regeneration"])

    adaptive_capacity = (
        0.26 * governance_capacity
        + 0.24 * justice
        + 0.22 * social
        + 0.18 * regeneration
        + 0.10 * (1 - technology)
    )

    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.16 if t % 8 == 0 else 0.06
            technology_risk = 0.06 * technology if t % 11 == 0 else 0.0

            pressure = np.clip(
                pressure
                + 0.04 * shock
                + 0.03 * technology
                + 0.02 * technology_risk
                - 0.04 * regeneration
                - 0.03 * governance_capacity
                - 0.02 * justice,
                0,
                1.5,
            )

            adaptive_capacity = np.clip(
                adaptive_capacity
                + 0.03 * governance_capacity
                + 0.03 * justice
                + 0.02 * social
                + 0.02 * regeneration
                - 0.03 * shock
                - 0.02 * pressure,
                0,
                1.6,
            )

            viability = np.clip(
                viability
                + 0.05 * adaptive_capacity
                + 0.04 * social
                + 0.03 * regeneration
                - shock
                - technology_risk
                - 0.07 * pressure,
                0,
                1.8,
            )

        rows.append({
            "simulation_id": row["simulation_id"],
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "simulation_name": row["simulation_name"],
            "time_step": t,
            "pathway_viability": viability,
            "boundary_pressure": pressure,
            "adaptive_capacity": adaptive_capacity,
        })

    return rows

trajectory_rows = []
for _, row in simulations.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths
    .groupby(["simulation_id", "pathway_id", "scenario_id", "simulation_name"])
    .agg(
        final_pathway_viability=("pathway_viability", "last"),
        mean_pathway_viability=("pathway_viability", "mean"),
        mean_boundary_pressure=("boundary_pressure", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_pathway_viability", ascending=False)
)

profiles.sort_values("safe_and_just_pathway_score", ascending=False).to_csv(OUTPUTS / "advanced_planetary_pathway_scores.csv", index=False)
scenarios.sort_values("planetary_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_boundary_scenario_scores.csv", index=False)
strategies.sort_values("pathway_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_pathway_strategy_scores.csv", index=False)
risks.sort_values("planetary_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_planetary_risk_priority_scores.csv", index=False)
governance.sort_values("planetary_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_planetary_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_planetary_pathway_simulation_paths.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_planetary_pathway_simulation_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("safe_and_just_pathway_score")
plt.barh(ranked["pathway_name"], ranked["safe_and_just_pathway_score"])
plt.xlabel("Safe-and-Just Pathway Score")
plt.title(f"Safe-and-Just Pathway Score — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "safe_and_just_pathway_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["total_boundary_pressure_score"], profiles["safe_and_just_pathway_score"])
for _, row in profiles.iterrows():
    plt.text(row["total_boundary_pressure_score"], row["safe_and_just_pathway_score"], row["pathway_name"], fontsize=7)
plt.xlabel("Total Boundary Pressure")
plt.ylabel("Safe-and-Just Pathway Score")
plt.title("Boundary Pressure vs Safe-and-Just Pathway Performance")
plt.tight_layout()
plt.savefig(OUTPUTS / "boundary_pressure_vs_safe_just_score.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for simulation_name in paths["simulation_name"].unique():
    subset = paths[paths["simulation_name"] == simulation_name]
    plt.plot(subset["time_step"], subset["pathway_viability"], label=simulation_name)

plt.xlabel("Time Step")
plt.ylabel("Pathway Viability")
plt.title("Planetary Pathway Viability Under Repeated Stress")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "planetary_pathway_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for simulation_name in paths["simulation_name"].unique():
    subset = paths[paths["simulation_name"] == simulation_name]
    plt.plot(subset["time_step"], subset["boundary_pressure"], label=simulation_name)

plt.xlabel("Time Step")
plt.ylabel("Boundary Pressure")
plt.title("Boundary Pressure Across Planetary Pathways")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "planetary_boundary_pressure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
