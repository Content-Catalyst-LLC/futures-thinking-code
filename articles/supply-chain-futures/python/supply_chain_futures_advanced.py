#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Supply Chain Futures.
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

profiles = pd.read_csv(DATA / "supply_chain_profiles.csv")
scenarios = pd.read_csv(DATA / "supply_chain_scenarios.csv")
strategies = pd.read_csv(DATA / "resilience_strategies.csv")
chokepoints = pd.read_csv(DATA / "chokepoint_risk_register.csv")
procurement = pd.read_csv(DATA / "procurement_circularity_records.csv")
pathways = pd.read_csv(DATA / "disruption_pathways.csv")

profiles["supply_chain_resilience_score"] = (
    0.10 * profiles["cost_efficiency"]
    + 0.16 * profiles["supplier_diversification"]
    + 0.14 * profiles["inventory_buffer"]
    + 0.14 * profiles["supply_visibility"]
    + 0.12 * profiles["labor_accountability"]
    + 0.13 * profiles["climate_adaptation"]
    + 0.09 * profiles["digital_traceability"]
    + 0.06 * profiles["circularity"]
    + 0.04 * profiles["regulatory_readiness"]
    + 0.02 * profiles["recovery_capacity"]
)

profiles["supply_chain_fragility_score"] = (
    0.16 * (1 - profiles["supplier_diversification"])
    + 0.16 * (1 - profiles["inventory_buffer"])
    + 0.14 * (1 - profiles["supply_visibility"])
    + 0.14 * (1 - profiles["climate_adaptation"])
    + 0.12 * (1 - profiles["labor_accountability"])
    + 0.10 * (1 - profiles["recovery_capacity"])
    + 0.08 * (1 - profiles["regulatory_readiness"])
    + 0.06 * (1 - profiles["digital_traceability"])
    + 0.04 * (1 - profiles["circularity"])
)

scenarios["disruption_pressure_score"] = (
    0.16 * scenarios["trade_fragmentation"]
    + 0.18 * scenarios["climate_disruption"]
    + 0.14 * scenarios["critical_minerals_pressure"]
    + 0.12 * scenarios["labor_stress"]
    + 0.14 * scenarios["transport_chokepoint_pressure"]
    + 0.10 * scenarios["regulatory_pressure"]
    + 0.10 * scenarios["demand_volatility"]
    + 0.06 * scenarios["technology_acceleration"]
)

scenarios["adaptation_opportunity_score"] = (
    0.16 * scenarios["technology_acceleration"]
    + 0.16 * scenarios["regulatory_pressure"]
    + 0.14 * scenarios["climate_disruption"]
    + 0.14 * scenarios["critical_minerals_pressure"]
    + 0.12 * scenarios["demand_volatility"]
    + 0.10 * scenarios["trade_fragmentation"]
    + 0.10 * scenarios["labor_stress"]
    + 0.08 * scenarios["transport_chokepoint_pressure"]
)

strategies["resilience_gain_score"] = (
    0.18 * strategies["supplier_diversification_gain"]
    + 0.16 * strategies["buffer_gain"]
    + 0.16 * strategies["visibility_gain"]
    + 0.14 * strategies["labor_accountability_gain"]
    + 0.16 * strategies["climate_adaptation_gain"]
    + 0.10 * strategies["circularity_gain"]
    + 0.10 * strategies["implementation_capacity"]
    - 0.10 * strategies["cost_burden"]
)

strategies["implementation_risk_score"] = (
    0.28 * (1 - strategies["implementation_capacity"])
    + 0.18 * strategies["cost_burden"]
    + 0.10 * (1 - strategies["supplier_diversification_gain"])
    + 0.10 * (1 - strategies["buffer_gain"])
    + 0.10 * (1 - strategies["visibility_gain"])
    + 0.10 * (1 - strategies["labor_accountability_gain"])
    + 0.08 * (1 - strategies["climate_adaptation_gain"])
    + 0.06 * (1 - strategies["circularity_gain"])
)

chokepoints["chokepoint_priority_score"] = (
    0.18 * chokepoints["dependency_concentration"]
    + 0.17 * chokepoints["substitution_difficulty"]
    + 0.16 * chokepoints["disruption_probability"]
    + 0.18 * chokepoints["systemic_reach"]
    + 0.17 * chokepoints["recovery_difficulty"]
    + 0.14 * chokepoints["visibility_gap"]
)

procurement["public_interest_supply_governance_score"] = (
    0.18 * procurement["public_value"]
    + 0.18 * procurement["resilience_support"]
    + 0.14 * procurement["labor_standard_strength"]
    + 0.14 * procurement["environmental_performance"]
    + 0.14 * procurement["traceability_quality"]
    + 0.12 * procurement["circular_material_capacity"]
    + 0.10 * procurement["implementation_readiness"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    exposure = (
        0.22 * (1 - row["diversification"])
        + 0.20 * (1 - row["buffer"])
        + 0.18 * (1 - row["visibility"])
        + 0.16 * (1 - row["climate_adaptation"])
        + 0.12 * (1 - row["labor_accountability"])
        + 0.12 * (1 - row["recovery_capacity"])
    )
    recovery = (
        0.24 * row["recovery_capacity"]
        + 0.20 * row["visibility"]
        + 0.18 * row["buffer"]
        + 0.16 * row["diversification"]
        + 0.12 * row["traceability"]
        + 0.10 * row["labor_accountability"]
    )
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.20 if t % 8 == 0 else 0.06

            adaptive_capacity = (
                0.20 * row["diversification"]
                + 0.18 * row["buffer"]
                + 0.18 * row["visibility"]
                + 0.16 * row["recovery_capacity"]
                + 0.12 * row["climate_adaptation"]
                + 0.10 * row["traceability"]
                + 0.06 * row["labor_accountability"]
            )

            exposure = np.clip(
                exposure
                + 0.06 * disruption
                - 0.03 * row["diversification"]
                - 0.03 * row["buffer"]
                - 0.03 * row["visibility"]
                - 0.03 * row["climate_adaptation"]
                - 0.02 * row["labor_accountability"],
                0,
                1.4,
            )

            recovery = np.clip(
                recovery
                + 0.03 * row["recovery_capacity"]
                + 0.03 * row["visibility"]
                + 0.02 * row["buffer"]
                + 0.02 * row["traceability"]
                - 0.04 * disruption,
                0,
                1.5,
            )

            viability = np.clip(
                viability
                + 0.04 * row["cost_efficiency"]
                + 0.08 * adaptive_capacity
                + 0.05 * recovery
                - disruption
                - 0.05 * exposure,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "supply_chain_viability": viability,
            "disruption_exposure": exposure,
            "recovery_score": recovery,
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
        final_viability=("supply_chain_viability", "last"),
        mean_viability=("supply_chain_viability", "mean"),
        mean_disruption_exposure=("disruption_exposure", "mean"),
        final_recovery_score=("recovery_score", "last")
    )
    .reset_index()
    .sort_values("final_viability", ascending=False)
)

profiles.sort_values("supply_chain_resilience_score", ascending=False).to_csv(OUTPUTS / "advanced_supply_chain_profile_scores.csv", index=False)
scenarios.sort_values("disruption_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_supply_chain_scenario_scores.csv", index=False)
strategies.sort_values("resilience_gain_score", ascending=False).to_csv(OUTPUTS / "advanced_resilience_strategy_scores.csv", index=False)
chokepoints.sort_values("chokepoint_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_chokepoint_priority_scores.csv", index=False)
procurement.sort_values("public_interest_supply_governance_score", ascending=False).to_csv(OUTPUTS / "advanced_procurement_circularity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_disruption_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_disruption_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("supply_chain_resilience_score")
plt.barh(ranked["supply_chain_name"], ranked["supply_chain_resilience_score"])
plt.xlabel("Supply Chain Resilience Score")
plt.title(f"Supply Chain Resilience — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "supply_chain_resilience_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["supply_chain_resilience_score"], profiles["supply_chain_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["supply_chain_resilience_score"], row["supply_chain_fragility_score"], row["supply_chain_name"], fontsize=7)
plt.xlabel("Supply Chain Resilience")
plt.ylabel("Supply Chain Fragility")
plt.title("Supply Chain Resilience vs Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "supply_chain_resilience_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["supply_chain_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Supply Chain Viability")
plt.title("Supply Chain Viability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "supply_chain_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["disruption_exposure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Disruption Exposure")
plt.title("Supply Chain Disruption Exposure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "supply_chain_disruption_exposure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
