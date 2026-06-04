#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Food, Water, and Land-Use Futures.
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

profiles = pd.read_csv(DATA / "food_water_land_profiles.csv")
scenarios = pd.read_csv(DATA / "resource_scenarios.csv")
strategies = pd.read_csv(DATA / "adaptation_strategy_options.csv")
risks = pd.read_csv(DATA / "resource_risk_indicators.csv")
governance = pd.read_csv(DATA / "resource_governance_records.csv")
pathways = pd.read_csv(DATA / "resource_stress_pathways.csv")

profiles["food_water_land_resilience_score"] = (
    0.13 * profiles["production_capacity"]
    + 0.16 * profiles["water_security"]
    + 0.15 * profiles["soil_health"]
    + 0.14 * profiles["biodiversity_integrity"]
    + 0.14 * profiles["governance_capacity"]
    - 0.12 * profiles["climate_exposure"]
    - 0.08 * profiles["market_vulnerability"]
    + 0.14 * profiles["justice_capacity"]
    + 0.12 * profiles["livelihood_resilience"]
)

profiles["food_water_land_fragility_score"] = (
    0.16 * profiles["climate_exposure"]
    + 0.14 * profiles["market_vulnerability"]
    + 0.14 * (1 - profiles["water_security"])
    + 0.13 * (1 - profiles["soil_health"])
    + 0.12 * (1 - profiles["biodiversity_integrity"])
    + 0.12 * (1 - profiles["governance_capacity"])
    + 0.10 * (1 - profiles["justice_capacity"])
    + 0.06 * (1 - profiles["livelihood_resilience"])
    + 0.03 * (1 - profiles["production_capacity"])
)

scenarios["resource_stress_score"] = (
    0.13 * scenarios["food_pressure"]
    + 0.15 * scenarios["water_pressure"]
    + 0.13 * scenarios["land_pressure"]
    + 0.13 * scenarios["soil_degradation_pressure"]
    + 0.12 * scenarios["biodiversity_pressure"]
    + 0.14 * scenarios["climate_pressure"]
    + 0.09 * scenarios["market_pressure"]
    + 0.06 * scenarios["governance_fragmentation"]
    + 0.05 * scenarios["rights_conflict_pressure"]
)

strategies["resource_strategy_value_score"] = (
    0.12 * strategies["production_gain"]
    + 0.16 * strategies["water_gain"]
    + 0.16 * strategies["soil_gain"]
    + 0.15 * strategies["biodiversity_gain"]
    + 0.14 * strategies["governance_gain"]
    + 0.15 * strategies["justice_gain"]
    + 0.08 * strategies["livelihood_gain"]
    + 0.04 * strategies["implementation_capacity"]
)

risks["resource_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["resource_governance_capacity_score"] = (
    0.15 * governance["land_rights"]
    + 0.17 * governance["water_governance"]
    + 0.15 * governance["food_security_institutions"]
    + 0.13 * governance["soil_monitoring"]
    + 0.14 * governance["biodiversity_governance"]
    + 0.14 * governance["participation"]
    + 0.12 * governance["public_finance"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    resilience = float(row["initial_resilience"])
    stress = (
        0.18 * row["climate_exposure"]
        + 0.15 * row["market_vulnerability"]
        + 0.15 * (1 - row["water_security"])
        + 0.13 * (1 - row["soil_health"])
        + 0.12 * (1 - row["biodiversity"])
        + 0.12 * (1 - row["governance"])
        + 0.10 * (1 - row["justice"])
        + 0.05 * (1 - row["livelihood_resilience"])
    )
    capacity = (
        0.18 * row["governance"]
        + 0.18 * row["justice"]
        + 0.16 * row["water_security"]
        + 0.16 * row["soil_health"]
        + 0.14 * row["biodiversity"]
        + 0.10 * row["production"]
        + 0.08 * row["livelihood_resilience"]
    )

    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.18 if t % 8 == 0 else 0.06
            regeneration = (
                0.18 * row["soil_health"]
                + 0.18 * row["water_security"]
                + 0.16 * row["biodiversity"]
                + 0.16 * row["governance"]
                + 0.14 * row["justice"]
                + 0.10 * row["production"]
                + 0.08 * row["livelihood_resilience"]
            )

            stress = np.clip(
                stress
                + 0.05 * shock
                + 0.04 * row["climate_exposure"]
                + 0.03 * row["market_vulnerability"]
                - 0.04 * row["water_security"]
                - 0.03 * row["soil_health"]
                - 0.03 * row["governance"]
                - 0.02 * row["justice"],
                0,
                1.6,
            )

            capacity = np.clip(
                capacity
                + 0.03 * row["governance"]
                + 0.03 * row["justice"]
                + 0.02 * row["soil_health"]
                + 0.02 * row["biodiversity"]
                + 0.02 * row["livelihood_resilience"]
                - 0.03 * shock,
                0,
                1.6,
            )

            resilience = np.clip(
                resilience
                + 0.06 * regeneration
                + 0.04 * capacity
                - shock
                - 0.06 * stress,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "food_water_land_resilience": resilience,
            "resource_stress": stress,
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
        final_resilience=("food_water_land_resilience", "last"),
        mean_resilience=("food_water_land_resilience", "mean"),
        mean_resource_stress=("resource_stress", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_resilience", ascending=False)
)

profiles.sort_values("food_water_land_resilience_score", ascending=False).to_csv(OUTPUTS / "advanced_food_water_land_profile_scores.csv", index=False)
scenarios.sort_values("resource_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_resource_scenario_scores.csv", index=False)
strategies.sort_values("resource_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_adaptation_strategy_scores.csv", index=False)
risks.sort_values("resource_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_resource_risk_priority_scores.csv", index=False)
governance.sort_values("resource_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_resource_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_resource_stress_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_resource_stress_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("food_water_land_resilience_score")
plt.barh(ranked["future_name"], ranked["food_water_land_resilience_score"])
plt.xlabel("Food-Water-Land Resilience Score")
plt.title(f"Food-Water-Land Resilience — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "food_water_land_resilience_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["food_water_land_resilience_score"], profiles["food_water_land_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["food_water_land_resilience_score"], row["food_water_land_fragility_score"], row["future_name"], fontsize=7)
plt.xlabel("Resilience")
plt.ylabel("Fragility")
plt.title("Food-Water-Land Resilience vs Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "food_water_land_resilience_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["food_water_land_resilience"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Food-Water-Land Resilience")
plt.title("Food-Water-Land Resilience Under Repeated Stress")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "food_water_land_resilience_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["resource_stress"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Resource Stress")
plt.title("Resource Stress Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "food_water_land_resource_stress_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
