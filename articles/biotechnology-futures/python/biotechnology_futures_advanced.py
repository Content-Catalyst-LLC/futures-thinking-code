#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Biotechnology Futures.
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

capabilities = pd.read_csv(DATA / "biotechnology_capabilities.csv")
risks = pd.read_csv(DATA / "biotechnology_risk_register.csv")
justice = pd.read_csv(DATA / "justice_indicators.csv")
scenarios = pd.read_csv(DATA / "biotechnology_scenarios.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

def capacity(df):
    return (
        0.16 * df["scientific_maturity"]
        + 0.18 * df["governance_readiness"]
        + 0.16 * df["public_legitimacy"]
        + 0.16 * df["equity_access"]
        + 0.12 * df["manufacturing_capacity"]
        + 0.12 * df["community_consent"]
        + 0.05 * (1 - df["ecological_uncertainty"])
        + 0.05 * (1 - df["dual_use_risk"])
    )

def risk_pressure(df):
    return (
        0.22 * df["dual_use_risk"]
        + 0.20 * df["ecological_uncertainty"]
        + 0.18 * (1 - df["governance_readiness"])
        + 0.16 * (1 - df["public_legitimacy"])
        + 0.14 * (1 - df["community_consent"])
        + 0.10 * (1 - df["equity_access"])
    )

capabilities["responsible_biotechnology_capacity_score"] = capacity(capabilities)
capabilities["biological_risk_pressure_score"] = risk_pressure(capabilities)

risks["risk_priority_score"] = (
    0.18 * risks["probability"]
    + 0.22 * risks["severity"]
    + 0.16 * risks["detection_difficulty"]
    + 0.16 * risks["governance_gap"]
    + 0.12 * risks["ecological_exposure"]
    + 0.10 * risks["dual_use_relevance"]
    + 0.06 * (1 - risks["mitigation_capacity"])
)

justice["biotechnology_justice_score"] = (
    0.20 * justice["equitable_access"]
    + 0.16 * justice["affected_voice"]
    + 0.16 * justice["consent_strength"]
    + 0.16 * justice["benefit_sharing"]
    + 0.14 * justice["repair_capacity"]
    + 0.10 * justice["community_governance"]
    + 0.08 * (1 - justice["harm_concentration"])
)

justice["harm_concentration_score"] = (
    0.32 * justice["harm_concentration"]
    + 0.18 * (1 - justice["equitable_access"])
    + 0.16 * (1 - justice["affected_voice"])
    + 0.14 * (1 - justice["consent_strength"])
    + 0.12 * (1 - justice["repair_capacity"])
    + 0.08 * (1 - justice["community_governance"])
)

scenarios["responsible_biotechnology_capacity_score"] = capacity(scenarios)
scenarios["biological_risk_pressure_score"] = risk_pressure(scenarios)
scenarios["justice_profile_score"] = (
    0.28 * scenarios["equity_access"]
    + 0.24 * scenarios["community_consent"]
    + 0.20 * scenarios["public_legitimacy"]
    + 0.16 * scenarios["governance_readiness"]
    + 0.12 * (1 - scenarios["biological_risk_pressure_score"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    biological_risk = float(0.30 + 0.20 * row["dual_use_risk"] + 0.15 * row["ecological_uncertainty"])
    access_capacity = float(row["equity"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.10 if t % 9 == 0 else 0.03

            innovation_force = (
                0.24 * row["science"]
                + 0.20 * row["manufacturing"]
                + 0.18 * row["governance"]
                + 0.16 * row["legitimacy"]
                + 0.16 * row["equity"]
            )

            pressure = (
                0.24 * row["dual_use_risk"]
                + 0.22 * row["ecological_uncertainty"]
                + 0.18 * (1 - row["governance"])
                + 0.16 * (1 - row["legitimacy"])
                + 0.12 * (1 - row["equity"])
                + disruption
            )

            access_capacity = np.clip(
                access_capacity + 0.04 * row["equity"] + 0.03 * row["governance"] + 0.02 * row["manufacturing"] - 0.03 * (1 - row["legitimacy"]),
                0,
                1.4,
            )

            biological_risk = np.clip(
                biological_risk * 0.88 + pressure - 0.08 * row["governance"] - 0.05 * row["legitimacy"],
                0,
                1.8,
            )

            viability = np.clip(
                viability + innovation_force / 4 - pressure / 4 + 0.04 * access_capacity - 0.03 * biological_risk,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "biotechnology_viability": viability,
            "biological_risk_pressure": biological_risk,
            "access_capacity": access_capacity,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "scenario_id", "pathway_name"])
    .agg(
        final_viability=("biotechnology_viability", "last"),
        mean_biological_risk=("biological_risk_pressure", "mean"),
        final_access_capacity=("access_capacity", "last")
    )
    .reset_index()
    .sort_values("final_viability", ascending=False)
)

strategies["public_interest_biotechnology_score"] = (
    0.16 * strategies["governance_strength"]
    + 0.14 * strategies["equity_access"]
    + 0.14 * strategies["community_consent"]
    + 0.12 * strategies["biosafety_capacity"]
    + 0.12 * strategies["biosecurity_capacity"]
    + 0.10 * strategies["open_science"]
    + 0.08 * strategies["public_manufacturing"]
    + 0.08 * strategies["ecological_monitoring"]
    + 0.06 * strategies["benefit_sharing"]
)

strategies["justice_governance_score"] = (
    0.18 * strategies["equity_access"]
    + 0.18 * strategies["community_consent"]
    + 0.16 * strategies["benefit_sharing"]
    + 0.14 * strategies["governance_strength"]
    + 0.12 * strategies["public_manufacturing"]
    + 0.10 * strategies["open_science"]
    + 0.08 * strategies["ecological_monitoring"]
    + 0.04 * strategies["biosafety_capacity"]
)

capabilities.sort_values("responsible_biotechnology_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_biotechnology_capability_scores.csv", index=False)
risks.sort_values("risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_biotechnology_risk_scores.csv", index=False)
justice.sort_values("biotechnology_justice_score", ascending=False).to_csv(OUTPUTS / "advanced_biotechnology_justice_scores.csv", index=False)
scenarios.sort_values("responsible_biotechnology_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_biotechnology_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_biotechnology_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_biotechnology_pathway_summary.csv", index=False)
strategies.sort_values("public_interest_biotechnology_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = scenarios.sort_values("responsible_biotechnology_capacity_score")
plt.barh(ranked["scenario_name"], ranked["responsible_biotechnology_capacity_score"])
plt.xlabel("Responsible Biotechnology Capacity")
plt.title(f"Responsible Biotechnology Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "responsible_biotechnology_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_risk = risks.sort_values("risk_priority_score")
plt.barh(ranked_risk["risk_name"], ranked_risk["risk_priority_score"])
plt.xlabel("Risk Priority")
plt.title("Biotechnology Risk Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "biotechnology_risk_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["biotechnology_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Biotechnology Viability")
plt.title("Biotechnology Viability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "biotechnology_viability_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
