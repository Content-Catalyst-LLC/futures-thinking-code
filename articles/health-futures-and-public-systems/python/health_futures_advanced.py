#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Health Futures and Public Systems.
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

profiles = pd.read_csv(DATA / "health_system_profiles.csv")
scenarios = pd.read_csv(DATA / "health_futures_scenarios.csv")
strategies = pd.read_csv(DATA / "health_strategy_options.csv")
risks = pd.read_csv(DATA / "health_risk_indicators.csv")
governance = pd.read_csv(DATA / "health_governance_records.csv")
pathways = pd.read_csv(DATA / "health_stress_pathways.csv")

profiles["public_health_resilience_score"] = (
    0.13 * profiles["prevention_capacity"]
    + 0.12 * profiles["healthcare_access"]
    + 0.15 * profiles["public_health_infrastructure"]
    + 0.10 * profiles["climate_readiness"]
    + 0.11 * profiles["workforce_resilience"]
    + 0.08 * profiles["technology_governance"]
    + 0.11 * profiles["social_protection"]
    + 0.08 * profiles["public_trust"]
    + 0.07 * profiles["equity_capacity"]
    + 0.05 * profiles["care_capacity"]
)

profiles["health_system_fragility_score"] = (
    0.13 * (1 - profiles["prevention_capacity"])
    + 0.12 * (1 - profiles["healthcare_access"])
    + 0.15 * (1 - profiles["public_health_infrastructure"])
    + 0.11 * (1 - profiles["climate_readiness"])
    + 0.13 * (1 - profiles["workforce_resilience"])
    + 0.08 * (1 - profiles["technology_governance"])
    + 0.10 * (1 - profiles["social_protection"])
    + 0.08 * (1 - profiles["public_trust"])
    + 0.06 * (1 - profiles["equity_capacity"])
    + 0.04 * (1 - profiles["care_capacity"])
)

scenarios["health_system_stress_score"] = (
    0.12 * scenarios["disease_burden_pressure"]
    + 0.13 * scenarios["climate_health_pressure"]
    + 0.13 * scenarios["biological_risk_pressure"]
    + 0.13 * scenarios["workforce_pressure"]
    + 0.11 * scenarios["care_pressure"]
    + 0.11 * scenarios["chronic_disease_pressure"]
    + 0.10 * scenarios["mental_health_pressure"]
    + 0.07 * scenarios["technology_governance_pressure"]
    + 0.05 * scenarios["trust_pressure"]
    + 0.05 * scenarios["equity_pressure"]
)

strategies["health_strategy_value_score"] = (
    0.13 * strategies["prevention_gain"]
    + 0.12 * strategies["access_gain"]
    + 0.14 * strategies["public_health_gain"]
    + 0.11 * strategies["climate_health_gain"]
    + 0.11 * strategies["workforce_gain"]
    + 0.08 * strategies["technology_governance_gain"]
    + 0.10 * strategies["social_protection_gain"]
    + 0.08 * strategies["trust_gain"]
    + 0.08 * strategies["equity_gain"]
    + 0.04 * strategies["care_gain"]
    + 0.01 * strategies["implementation_capacity"]
)

risks["health_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["cascade_potential"]
    + 0.12 * risks["visibility_gap"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.08 * (1 - risks["preparedness"])
)

governance["health_governance_capacity_score"] = (
    0.15 * governance["monitoring_capacity"]
    + 0.15 * governance["public_health_finance"]
    + 0.14 * governance["workforce_capacity"]
    + 0.13 * governance["community_participation"]
    + 0.11 * governance["technology_accountability"]
    + 0.13 * governance["equity_safeguards"]
    + 0.11 * governance["emergency_coordination"]
    + 0.08 * governance["care_system_capacity"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    resilience = float(row["initial_resilience"])
    prevention = float(row["prevention"])
    access = float(row["healthcare_access"])
    public_health = float(row["public_health"])
    climate = float(row["climate_readiness"])
    workforce = float(row["workforce"])
    social = float(row["social_protection"])
    trust = float(row["public_trust"])
    equity = float(row["equity"])
    care = float(row["care_capacity"])

    stress = (
        0.15 * (1 - prevention)
        + 0.13 * (1 - access)
        + 0.15 * (1 - public_health)
        + 0.13 * (1 - climate)
        + 0.13 * (1 - workforce)
        + 0.10 * (1 - social)
        + 0.08 * (1 - trust)
        + 0.08 * (1 - equity)
        + 0.05 * (1 - care)
    )

    capacity = (
        0.15 * prevention
        + 0.13 * access
        + 0.18 * public_health
        + 0.11 * climate
        + 0.13 * workforce
        + 0.10 * social
        + 0.08 * trust
        + 0.08 * equity
        + 0.04 * care
    )

    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.18 if t % 8 == 0 else 0.06
            biological_shock = 0.11 if t % 13 == 0 else 0.0
            care_shock = 0.06 * (1 - care) if t % 10 == 0 else 0.0

            learning_gain = (
                0.17 * public_health
                + 0.15 * prevention
                + 0.13 * workforce
                + 0.13 * trust
                + 0.13 * equity
                + 0.11 * access
                + 0.10 * social
                + 0.08 * care
            )

            compound_penalty = (
                0.04 * (1 - climate)
                + 0.04 * (1 - workforce)
                + 0.03 * (1 - public_health)
                + 0.03 * (1 - social)
                + 0.02 * (1 - care)
            )

            stress = np.clip(
                stress
                + 0.05 * shock
                + 0.06 * biological_shock
                + care_shock
                + compound_penalty
                - 0.04 * prevention
                - 0.03 * public_health
                - 0.03 * social
                - 0.02 * trust,
                0,
                1.6,
            )

            capacity = np.clip(
                capacity
                + 0.03 * public_health
                + 0.03 * workforce
                + 0.02 * trust
                + 0.02 * equity
                + 0.02 * prevention
                + 0.01 * care
                - 0.03 * shock
                - 0.02 * biological_shock
                - 0.02 * stress,
                0,
                1.6,
            )

            resilience = np.clip(
                resilience
                + 0.05 * learning_gain
                + 0.04 * capacity
                - shock
                - biological_shock
                - care_shock
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
            "public_health_resilience": resilience,
            "system_stress": stress,
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
        final_resilience=("public_health_resilience", "last"),
        mean_resilience=("public_health_resilience", "mean"),
        mean_system_stress=("system_stress", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_resilience", ascending=False)
)

profiles.sort_values("public_health_resilience_score", ascending=False).to_csv(OUTPUTS / "advanced_health_system_profile_scores.csv", index=False)
scenarios.sort_values("health_system_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_health_scenario_scores.csv", index=False)
strategies.sort_values("health_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_health_strategy_scores.csv", index=False)
risks.sort_values("health_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_health_risk_priority_scores.csv", index=False)
governance.sort_values("health_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_health_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_health_stress_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_health_stress_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("public_health_resilience_score")
plt.barh(ranked["future_name"], ranked["public_health_resilience_score"])
plt.xlabel("Public Health Resilience Score")
plt.title(f"Public Health Resilience — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "health_futures_resilience_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["public_health_resilience_score"], profiles["health_system_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["public_health_resilience_score"], row["health_system_fragility_score"], row["future_name"], fontsize=7)
plt.xlabel("Public Health Resilience")
plt.ylabel("Health System Fragility")
plt.title("Health System Resilience vs Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "health_resilience_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["public_health_resilience"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Public Health Resilience")
plt.title("Public Health Resilience Under Repeated Stress")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "health_futures_resilience_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["system_stress"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("System Stress")
plt.title("Health System Stress Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "health_futures_system_stress_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
