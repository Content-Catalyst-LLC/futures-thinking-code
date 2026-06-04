#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Infrastructure Futures.
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

profiles = pd.read_csv(DATA / "infrastructure_system_profiles.csv")
scenarios = pd.read_csv(DATA / "infrastructure_scenarios.csv")
strategies = pd.read_csv(DATA / "infrastructure_strategy_options.csv")
risks = pd.read_csv(DATA / "infrastructure_risk_indicators.csv")
governance = pd.read_csv(DATA / "infrastructure_governance_records.csv")
pathways = pd.read_csv(DATA / "infrastructure_cascade_pathways.csv")

profiles["infrastructure_viability_score"] = (
    0.14 * (1 - profiles["centralization"])
    + 0.18 * profiles["redundancy"]
    - 0.12 * profiles["digital_dependence"]
    - 0.16 * profiles["climate_exposure"]
    + 0.16 * profiles["coordination_quality"]
    + 0.12 * profiles["public_finance_capacity"]
    + 0.12 * profiles["maintenance_integrity"]
    + 0.10 * profiles["equity_of_access"]
    - 0.08 * profiles["geopolitical_dependency"]
)

profiles["infrastructure_fragility_score"] = (
    0.14 * profiles["centralization"]
    + 0.14 * (1 - profiles["redundancy"])
    + 0.12 * profiles["digital_dependence"]
    + 0.17 * profiles["climate_exposure"]
    + 0.13 * (1 - profiles["coordination_quality"])
    + 0.11 * (1 - profiles["public_finance_capacity"])
    + 0.10 * (1 - profiles["maintenance_integrity"])
    + 0.08 * (1 - profiles["equity_of_access"])
    + 0.11 * profiles["geopolitical_dependency"]
)

scenarios["infrastructure_stress_score"] = (
    0.15 * scenarios["physical_load"]
    + 0.16 * scenarios["climate_pressure"]
    + 0.13 * scenarios["digital_control_risk"]
    + 0.13 * scenarios["finance_pressure"]
    + 0.14 * scenarios["maintenance_backlog_pressure"]
    + 0.12 * scenarios["governance_fragmentation"]
    + 0.09 * scenarios["geopolitical_chokepoint_pressure"]
    + 0.08 * scenarios["access_inequality_pressure"]
)

strategies["infrastructure_strategy_value_score"] = (
    0.16 * strategies["redundancy_gain"]
    + 0.16 * strategies["maintenance_gain"]
    + 0.14 * strategies["climate_adaptation_gain"]
    + 0.12 * strategies["digital_accountability_gain"]
    + 0.14 * strategies["governance_gain"]
    + 0.12 * strategies["finance_capacity_gain"]
    + 0.12 * strategies["equity_gain"]
    + 0.04 * strategies["implementation_capacity"]
)

risks["infrastructure_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["infrastructure_governance_capacity_score"] = (
    0.16 * governance["coordination"]
    + 0.16 * governance["public_finance"]
    + 0.16 * governance["maintenance_capacity"]
    + 0.14 * governance["digital_accountability"]
    + 0.14 * governance["climate_governance"]
    + 0.12 * governance["procurement_integrity"]
    + 0.12 * governance["equity_safeguards"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    load = (
        0.16 * row["centralization"]
        + 0.16 * row["climate_exposure"]
        + 0.12 * row["digital_dependence"]
        + 0.14 * (1 - row["redundancy"])
        + 0.14 * (1 - row["maintenance_integrity"])
        + 0.12 * (1 - row["coordination_quality"])
        + 0.10 * (1 - row["public_finance_capacity"])
        + 0.06 * (1 - row["equity_of_access"])
    )
    capacity = (
        0.22 * row["redundancy"]
        + 0.20 * row["coordination_quality"]
        + 0.18 * row["public_finance_capacity"]
        + 0.18 * row["maintenance_integrity"]
        + 0.14 * row["equity_of_access"]
        + 0.08 * (1 - row["climate_exposure"])
    )

    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.18 if t % 8 == 0 else 0.07
            cyber_or_control_shock = 0.10 * row["digital_dependence"] if t % 11 == 0 else 0.0

            response_gain = (
                0.22 * row["redundancy"]
                + 0.20 * row["coordination_quality"]
                + 0.16 * row["public_finance_capacity"]
                + 0.18 * row["maintenance_integrity"]
                + 0.14 * row["equity_of_access"]
                + 0.10 * (1 - row["climate_exposure"])
            )

            load = np.clip(
                load
                + 0.05 * shock
                + 0.04 * cyber_or_control_shock
                + 0.03 * row["climate_exposure"]
                + 0.02 * row["centralization"]
                + 0.02 * row["digital_dependence"]
                - 0.04 * row["redundancy"]
                - 0.03 * row["coordination_quality"]
                - 0.03 * row["maintenance_integrity"],
                0,
                1.5,
            )

            capacity = np.clip(
                capacity
                + 0.03 * row["coordination_quality"]
                + 0.03 * row["public_finance_capacity"]
                + 0.03 * row["maintenance_integrity"]
                + 0.02 * row["equity_of_access"]
                - 0.03 * shock
                - 0.02 * cyber_or_control_shock,
                0,
                1.6,
            )

            viability = np.clip(
                viability
                + 0.07 * response_gain
                + 0.04 * capacity
                - shock
                - cyber_or_control_shock
                - 0.06 * load,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "infrastructure_viability": viability,
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
        final_infrastructure_viability=("infrastructure_viability", "last"),
        mean_infrastructure_viability=("infrastructure_viability", "mean"),
        mean_system_load=("system_load", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_infrastructure_viability", ascending=False)
)

profiles.sort_values("infrastructure_viability_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_profile_scores.csv", index=False)
scenarios.sort_values("infrastructure_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_scenario_scores.csv", index=False)
strategies.sort_values("infrastructure_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_strategy_scores.csv", index=False)
risks.sort_values("infrastructure_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_risk_priority_scores.csv", index=False)
governance.sort_values("infrastructure_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_infrastructure_cascade_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_infrastructure_cascade_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("infrastructure_viability_score")
plt.barh(ranked["system_name"], ranked["infrastructure_viability_score"])
plt.xlabel("Infrastructure Viability Score")
plt.title(f"Infrastructure Viability — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "infrastructure_viability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["infrastructure_viability_score"], profiles["infrastructure_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["infrastructure_viability_score"], row["infrastructure_fragility_score"], row["system_name"], fontsize=7)
plt.xlabel("Infrastructure Viability")
plt.ylabel("Infrastructure Fragility")
plt.title("Infrastructure Viability vs Infrastructure Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "infrastructure_viability_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["infrastructure_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Infrastructure Viability")
plt.title("Infrastructure Viability Under Repeated Stress")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "infrastructure_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["system_load"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("System Load")
plt.title("Infrastructure System Load Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "infrastructure_system_load_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
