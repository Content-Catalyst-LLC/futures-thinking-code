#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Global Governance Futures.
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
scenarios = pd.read_csv(DATA / "governance_scenarios.csv")
strategies = pd.read_csv(DATA / "governance_strategy_options.csv")
risks = pd.read_csv(DATA / "governance_risk_indicators.csv")
records = pd.read_csv(DATA / "institutional_records.csv")
pathways = pd.read_csv(DATA / "adaptive_governance_pathways.csv")

profiles["governance_capacity_score"] = (
    0.14 * profiles["institutional_capacity"]
    + 0.16 * profiles["legitimacy"]
    + 0.12 * profiles["legal_authority"]
    + 0.11 * profiles["finance_capacity"]
    + 0.13 * profiles["collective_action"]
    + 0.10 * profiles["technology_governance"]
    + 0.10 * profiles["planetary_risk_coordination"]
    + 0.08 * profiles["adaptive_learning"]
    + 0.08 * profiles["public_accountability"]
    + 0.08 * profiles["representation_equity"]
)

profiles["legitimacy_gap_score"] = (
    0.18 * (1 - profiles["legitimacy"])
    + 0.14 * (1 - profiles["representation_equity"])
    + 0.13 * (1 - profiles["public_accountability"])
    + 0.12 * (1 - profiles["legal_authority"])
    + 0.11 * (1 - profiles["collective_action"])
    + 0.10 * (1 - profiles["finance_capacity"])
    + 0.08 * (1 - profiles["institutional_capacity"])
    + 0.07 * (1 - profiles["technology_governance"])
    + 0.04 * (1 - profiles["planetary_risk_coordination"])
    + 0.03 * (1 - profiles["adaptive_learning"])
)

scenarios["global_governance_stress_score"] = (
    0.12 * scenarios["climate_stress"]
    + 0.10 * scenarios["health_stress"]
    + 0.10 * scenarios["finance_stress"]
    + 0.11 * scenarios["technology_stress"]
    + 0.08 * scenarios["migration_stress"]
    + 0.10 * scenarios["security_stress"]
    + 0.13 * scenarios["legitimacy_stress"]
    + 0.12 * scenarios["institutional_fragmentation"]
    + 0.09 * scenarios["private_power_pressure"]
    + 0.05 * scenarios["civil_society_constraint"]
)

strategies["governance_strategy_value_score"] = (
    0.13 * strategies["representation_gain"]
    + 0.12 * strategies["finance_gain"]
    + 0.12 * strategies["legal_accountability_gain"]
    + 0.11 * strategies["climate_governance_gain"]
    + 0.09 * strategies["health_governance_gain"]
    + 0.10 * strategies["technology_governance_gain"]
    + 0.08 * strategies["migration_protection_gain"]
    + 0.08 * strategies["security_coordination_gain"]
    + 0.08 * strategies["civil_society_gain"]
    + 0.04 * strategies["implementation_capacity"]
    + 0.05 * strategies["public_legitimacy_gain"]
)

risks["governance_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

records["institutional_capacity_score"] = (
    0.14 * records["diplomatic_capacity"]
    + 0.13 * records["monitoring_capacity"]
    + 0.13 * records["finance_capacity"]
    + 0.13 * records["legal_accountability"]
    + 0.13 * records["scientific_capacity"]
    + 0.12 * records["implementation_capacity"]
    + 0.12 * records["public_accountability"]
    + 0.10 * records["civil_society_space"]
)

def simulate_pathway(row):
    governance_state = float(row["initial_governance_capacity"])
    institutional = float(row["institutional_capacity"])
    legitimacy = float(row["legitimacy"])
    law = float(row["legal_authority"])
    finance = float(row["finance_capacity"])
    collective = float(row["collective_action"])
    tech = float(row["technology_governance"])
    planetary = float(row["planetary_coordination"])
    learning = float(row["adaptive_learning"])
    accountability = float(row["public_accountability"])
    stress = float(row["system_stress"])
    horizon = int(row["time_horizon"])

    legitimacy_state = (
        0.28 * legitimacy
        + 0.18 * collective
        + 0.16 * law
        + 0.14 * finance
        + 0.14 * accountability
        + 0.10 * learning
    )

    adaptive_state = (
        0.26 * learning
        + 0.16 * institutional
        + 0.14 * legitimacy
        + 0.12 * finance
        + 0.12 * collective
        + 0.12 * planetary
        + 0.08 * accountability
    )

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            shock_total = 0.05
            shock_total += 0.12 if t % 8 == 0 else 0.0
            shock_total += 0.10 if t % 11 == 0 else 0.0
            shock_total += 0.09 if t % 13 == 0 else 0.0
            shock_total += 0.08 if t % 9 == 0 else 0.0
            shock_total += 0.07 if t % 10 == 0 else 0.0

            coordination_response = (
                0.05 * institutional
                + 0.05 * collective
                + 0.04 * finance
                + 0.04 * planetary
                + 0.03 * tech
                + 0.03 * law
                + 0.02 * accountability
            )

            legitimacy_response = (
                0.04 * legitimacy
                + 0.04 * collective
                + 0.03 * finance
                + 0.03 * learning
                + 0.03 * accountability
            )

            stress = np.clip(
                stress
                + shock_total
                + 0.04 * (1 - collective)
                + 0.04 * (1 - finance)
                + 0.03 * (1 - legitimacy)
                + 0.03 * (1 - accountability)
                - coordination_response,
                0,
                1.8,
            )

            adaptive_state = np.clip(
                adaptive_state
                + 0.04 * learning
                + 0.03 * institutional
                + 0.03 * legitimacy
                + 0.02 * tech
                + 0.02 * accountability
                - 0.03 * stress,
                0,
                1.8,
            )

            legitimacy_state = np.clip(
                legitimacy_state
                + legitimacy_response
                - 0.04 * stress
                - 0.03 * (1 - law)
                - 0.02 * (1 - accountability),
                0,
                1.8,
            )

            governance_state = np.clip(
                governance_state
                + 0.05 * adaptive_state
                + 0.04 * legitimacy_state
                + 0.03 * institutional
                + 0.02 * finance
                - 0.06 * stress
                - 0.02 * shock_total,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "governance_capacity": governance_state,
            "system_stress": stress,
            "legitimacy": legitimacy_state,
            "adaptive_learning": adaptive_state,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_governance_capacity=("governance_capacity", "last"),
        mean_governance_capacity=("governance_capacity", "mean"),
        mean_system_stress=("system_stress", "mean"),
        final_legitimacy=("legitimacy", "last"),
        final_adaptive_learning=("adaptive_learning", "last"),
    )
    .reset_index()
    .sort_values("final_governance_capacity", ascending=False)
)

profiles.sort_values("governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_profile_scores.csv", index=False)
scenarios.sort_values("global_governance_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_scenario_scores.csv", index=False)
strategies.sort_values("governance_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_strategy_scores.csv", index=False)
risks.sort_values("governance_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_risk_priority_scores.csv", index=False)
records.sort_values("institutional_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_institutional_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_governance_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_governance_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("governance_capacity_score")
plt.barh(ranked["future_name"], ranked["governance_capacity_score"])
plt.xlabel("Governance Capacity Score")
plt.title(f"Global Governance Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "global_governance_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["governance_capacity_score"], profiles["legitimacy_gap_score"])
for _, row in profiles.iterrows():
    plt.text(row["governance_capacity_score"], row["legitimacy_gap_score"], row["future_name"], fontsize=7)
plt.xlabel("Governance Capacity")
plt.ylabel("Legitimacy Gap")
plt.title("Governance Capacity vs Legitimacy Gap")
plt.tight_layout()
plt.savefig(OUTPUTS / "governance_capacity_vs_legitimacy_gap.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["governance_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Governance Capacity")
plt.title("Adaptive Governance Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_governance_capacity_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
