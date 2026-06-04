#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Migration, Demography, and Future Societies.
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

profiles = pd.read_csv(DATA / "demographic_profiles.csv")
scenarios = pd.read_csv(DATA / "migration_demography_scenarios.csv")
strategies = pd.read_csv(DATA / "demographic_strategy_options.csv")
risks = pd.read_csv(DATA / "demographic_risk_indicators.csv")
care_records = pd.read_csv(DATA / "care_urban_records.csv")
pathways = pd.read_csv(DATA / "adaptive_demographic_pathways.csv")

profiles["demographic_stress_score"] = (
    0.13 * profiles["aging_pressure"]
    + 0.13 * profiles["youth_opportunity_gap"]
    + 0.12 * profiles["migration_pressure"]
    + 0.13 * (1 - profiles["care_capacity"])
    + 0.12 * profiles["housing_pressure"]
    + 0.10 * (1 - profiles["labor_adaptation"])
    + 0.11 * profiles["climate_mobility_exposure"]
    + 0.08 * (1 - profiles["social_cohesion"])
    + 0.05 * (1 - profiles["gender_equity"])
    + 0.03 * (1 - profiles["public_health_capacity"])
)

profiles["adaptive_capacity_score"] = (
    0.18 * profiles["care_capacity"]
    + 0.16 * profiles["labor_adaptation"]
    + 0.16 * profiles["social_cohesion"]
    + 0.13 * profiles["gender_equity"]
    + 0.13 * profiles["public_health_capacity"]
    + 0.10 * (1 - profiles["housing_pressure"])
    + 0.08 * (1 - profiles["youth_opportunity_gap"])
    + 0.06 * (1 - profiles["climate_mobility_exposure"])
)

profiles["adaptation_gap_score"] = (profiles["demographic_stress_score"] - profiles["adaptive_capacity_score"]).clip(lower=0)

scenarios["demographic_pressure_score"] = (
    0.12 * scenarios["aging_shock"]
    + 0.12 * scenarios["youth_employment_shock"]
    + 0.12 * scenarios["housing_shock"]
    + 0.12 * scenarios["care_shock"]
    + 0.13 * scenarios["climate_mobility_shock"]
    + 0.10 * scenarios["border_restriction_pressure"]
    + 0.09 * scenarios["labor_shortage_pressure"]
    + 0.08 * scenarios["public_health_shock"]
    + 0.07 * scenarios["social_cohesion_stress"]
    + 0.05 * scenarios["rights_protection_gap"]
)

strategies["demographic_strategy_value_score"] = (
    0.13 * strategies["care_investment_gain"]
    + 0.12 * strategies["housing_affordability_gain"]
    + 0.12 * strategies["youth_opportunity_gain"]
    + 0.12 * strategies["legal_mobility_gain"]
    + 0.11 * strategies["labor_protection_gain"]
    + 0.10 * strategies["climate_adaptation_gain"]
    + 0.09 * strategies["reproductive_health_gain"]
    + 0.08 * strategies["gender_equity_gain"]
    + 0.07 * strategies["public_health_gain"]
    + 0.04 * strategies["social_cohesion_gain"]
    + 0.02 * strategies["implementation_capacity"]
)

risks["demographic_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.15 * risks["cascade_potential"]
    + 0.10 * risks["visibility_gap"]
    + 0.13 * risks["recovery_difficulty"]
    + 0.20 * risks["distributional_harm"]
    + 0.10 * (1 - risks["preparedness"])
)

care_records["care_stress_score"] = (
    0.28 * care_records["eldercare_demand"]
    + 0.20 * care_records["childcare_demand"]
    + 0.20 * care_records["unpaid_care_burden"]
    + 0.14 * (1 - care_records["care_workforce_capacity"])
    + 0.10 * (1 - care_records["public_health_capacity"])
    + 0.08 * (1 - care_records["integration_capacity"])
)

care_records["urban_absorption_capacity_score"] = (
    0.24 * care_records["affordable_housing_supply"]
    + 0.20 * care_records["urban_service_capacity"]
    + 0.18 * care_records["integration_capacity"]
    + 0.16 * care_records["public_health_capacity"]
    + 0.14 * care_records["care_workforce_capacity"]
    + 0.08 * (1 - care_records["unpaid_care_burden"])
)

def simulate_pathway(row):
    population = float(row["population_base"])
    birth_rate = float(row["birth_rate"])
    death_rate = float(row["death_rate"])
    net_migration_rate = float(row["net_migration_rate"])
    aging = float(row["aging_pressure"])
    youth = float(row["youth_opportunity_gap"])
    care = float(row["care_capacity"])
    housing = float(row["housing_pressure"])
    labor = float(row["labor_adaptation"])
    climate = float(row["climate_mobility_exposure"])
    cohesion = float(row["social_cohesion"])
    adaptive = float(row["initial_adaptive_capacity"])
    horizon = int(row["time_horizon"])

    demographic_stress = (
        0.16 * aging
        + 0.14 * youth
        + 0.14 * housing
        + 0.14 * climate
        + 0.12 * (1 - care)
        + 0.12 * (1 - labor)
        + 0.10 * (1 - cohesion)
        + 0.08 * min(1, abs(net_migration_rate) * 100)
    )

    care_stress = (
        0.36 * aging
        + 0.18 * youth
        + 0.16 * (1 - care)
        + 0.12 * (1 - labor)
        + 0.10 * housing
        + 0.08 * (1 - cohesion)
    )

    mobility = (
        0.34 * climate
        + 0.18 * housing
        + 0.16 * youth
        + 0.14 * (1 - labor)
        + 0.10 * (1 - cohesion)
        + 0.08 * aging
    )

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            climate_shock = 0.004 if t % 10 == 0 else 0.0
            housing_shock = 0.003 if t % 8 == 0 else 0.0
            care_shock = 0.003 if t % 12 == 0 else 0.0

            births = population * birth_rate
            deaths = population * death_rate
            net_migration = population * (net_migration_rate + climate_shock * climate - housing_shock * housing)
            population = max(0, population + births - deaths + net_migration)

            care_stress = np.clip(
                care_stress + 0.04 * aging + care_shock + 0.03 * housing - 0.05 * care - 0.03 * labor,
                0,
                1.8,
            )

            mobility = np.clip(
                mobility + 0.04 * climate + 0.03 * housing + climate_shock - 0.03 * labor - 0.03 * cohesion,
                0,
                1.8,
            )

            demographic_stress = np.clip(
                demographic_stress + 0.03 * care_stress + 0.03 * mobility + 0.02 * youth + 0.02 * aging - 0.04 * adaptive,
                0,
                1.8,
            )

            adaptive = np.clip(
                adaptive + 0.03 * care + 0.03 * labor + 0.02 * cohesion - 0.03 * demographic_stress - 0.02 * care_stress,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "population": population,
            "demographic_stress": demographic_stress,
            "care_stress": care_stress,
            "mobility_pressure": mobility,
            "adaptive_capacity": adaptive,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_population=("population", "last"),
        final_demographic_stress=("demographic_stress", "last"),
        mean_care_stress=("care_stress", "mean"),
        mean_mobility_pressure=("mobility_pressure", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last"),
    )
    .reset_index()
    .sort_values("final_adaptive_capacity", ascending=False)
)

profiles.sort_values("demographic_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_demographic_profile_scores.csv", index=False)
scenarios.sort_values("demographic_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_migration_demography_scenario_scores.csv", index=False)
strategies.sort_values("demographic_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_demographic_strategy_scores.csv", index=False)
risks.sort_values("demographic_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_demographic_risk_priority_scores.csv", index=False)
care_records.sort_values("care_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_care_urban_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_demographic_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_demographic_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("demographic_stress_score")
plt.barh(ranked["future_name"], ranked["demographic_stress_score"])
plt.xlabel("Demographic Stress Score")
plt.title(f"Demographic Stress — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "demographic_stress_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["demographic_stress_score"], profiles["adaptive_capacity_score"])
for _, row in profiles.iterrows():
    plt.text(row["demographic_stress_score"], row["adaptive_capacity_score"], row["future_name"], fontsize=7)
plt.xlabel("Demographic Stress")
plt.ylabel("Adaptive Capacity")
plt.title("Demographic Stress vs Adaptive Capacity")
plt.tight_layout()
plt.savefig(OUTPUTS / "demographic_stress_vs_adaptive_capacity.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["demographic_stress"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Demographic Stress")
plt.title("Adaptive Demographic Stress Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_demographic_stress_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["adaptive_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Adaptive Capacity")
plt.title("Adaptive Demographic Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_demographic_capacity_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
