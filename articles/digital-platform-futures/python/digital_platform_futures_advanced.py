#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Digital Platform Futures.
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

platforms = pd.read_csv(DATA / "platform_profiles.csv")
risks = pd.read_csv(DATA / "platform_risk_register.csv")
accountability = pd.read_csv(DATA / "accountability_indicators.csv")
scenarios = pd.read_csv(DATA / "platform_scenarios.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

def public_capacity(df):
    return (
        0.18 * df["interoperability"]
        + 0.18 * df["public_accountability"]
        + 0.16 * df["user_rights"]
        + 0.14 * df["worker_protection"]
        + 0.14 * df["digital_public_value"]
        + 0.10 * df["ecological_responsibility"]
        + 0.05 * (1 - df["platform_power"])
        + 0.05 * (1 - df["data_advantage"])
    )

def dependency(df):
    return (
        0.24 * df["platform_power"]
        + 0.20 * df["data_advantage"]
        + 0.18 * (1 - df["interoperability"])
        + 0.14 * (1 - df["user_rights"])
        + 0.14 * (1 - df["public_accountability"])
        + 0.10 * (1 - df["worker_protection"])
    )

platforms["platform_power_score"] = (
    0.26 * platforms["network_effect_strength"]
    + 0.24 * platforms["data_advantage"]
    + 0.22 * platforms["gatekeeping_power"]
    + 0.16 * platforms["lock_in"]
    + 0.12 * (1 - platforms["interoperability"])
)

platforms["public_interest_platform_capacity_score"] = (
    0.18 * platforms["interoperability"]
    + 0.18 * platforms["public_accountability"]
    + 0.16 * platforms["user_rights"]
    + 0.14 * platforms["worker_protection"]
    + 0.14 * platforms["digital_public_value"]
    + 0.10 * platforms["ecological_responsibility"]
    + 0.05 * (1 - platforms["platform_power_score"])
    + 0.05 * (1 - platforms["data_advantage"])
)

platforms["platform_dependency_pressure_score"] = (
    0.24 * platforms["platform_power_score"]
    + 0.20 * platforms["data_advantage"]
    + 0.18 * (1 - platforms["interoperability"])
    + 0.14 * (1 - platforms["user_rights"])
    + 0.14 * (1 - platforms["public_accountability"])
    + 0.10 * (1 - platforms["worker_protection"])
)

risks["platform_risk_priority_score"] = (
    0.18 * risks["probability"]
    + 0.20 * risks["severity"]
    + 0.16 * risks["detection_difficulty"]
    + 0.16 * risks["accountability_gap"]
    + 0.14 * risks["dependency_exposure"]
    + 0.10 * risks["public_harm_relevance"]
    + 0.06 * (1 - risks["mitigation_capacity"])
)

accountability["accountability_capacity_score"] = (
    0.18 * accountability["transparency"]
    + 0.16 * accountability["auditability"]
    + 0.18 * accountability["contestability"]
    + 0.18 * accountability["enforceability"]
    + 0.10 * accountability["researcher_access"]
    + 0.12 * accountability["remedy_capacity"]
    + 0.08 * accountability["public_participation"]
)
accountability["accountability_gap_score"] = 1 - accountability["accountability_capacity_score"]

scenarios["public_interest_platform_capacity_score"] = public_capacity(scenarios)
scenarios["platform_dependency_pressure_score"] = dependency(scenarios)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    public_value = float(row["initial_public_value"])
    dependency_pressure = float(0.35 + 0.25 * row["platform_power"] + 0.20 * row["data_advantage"])
    accountability_capacity = float(row["public_accountability"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.08 if t % 10 == 0 else 0.03

            enclosure_force = (
                0.24 * row["platform_power"]
                + 0.20 * row["data_advantage"]
                + 0.18 * (1 - row["interoperability"])
                + 0.14 * (1 - row["user_rights"])
                + 0.12 * (1 - row["worker_protection"])
            )

            public_governance_force = (
                0.22 * row["public_accountability"]
                + 0.20 * row["user_rights"]
                + 0.18 * row["interoperability"]
                + 0.16 * row["worker_protection"]
                + 0.14 * row["digital_public_value"]
            )

            accountability_capacity = np.clip(
                accountability_capacity + 0.04 * row["public_accountability"] + 0.03 * row["user_rights"] + 0.03 * row["interoperability"] - 0.04 * row["platform_power"],
                0,
                1.4,
            )

            dependency_pressure = np.clip(
                dependency_pressure * 0.90 + enclosure_force + disruption - 0.10 * row["interoperability"] - 0.08 * row["public_accountability"],
                0,
                1.8,
            )

            public_value = np.clip(
                public_value + public_governance_force / 4 - enclosure_force / 4 + 0.04 * accountability_capacity - 0.03 * dependency_pressure,
                0,
                1.6,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "digital_public_value": public_value,
            "platform_dependency_pressure": dependency_pressure,
            "accountability_capacity": accountability_capacity,
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
        final_public_value=("digital_public_value", "last"),
        mean_dependency_pressure=("platform_dependency_pressure", "mean"),
        final_accountability_capacity=("accountability_capacity", "last")
    )
    .reset_index()
    .sort_values("final_public_value", ascending=False)
)

strategies["public_interest_platform_strategy_score"] = (
    0.16 * strategies["interoperability"]
    + 0.14 * strategies["user_rights"]
    + 0.14 * strategies["worker_protection"]
    + 0.16 * strategies["public_accountability"]
    + 0.10 * strategies["researcher_access"]
    + 0.10 * strategies["competition_enforcement"]
    + 0.10 * strategies["public_infrastructure"]
    + 0.08 * strategies["ecological_standards"]
    + 0.02 * strategies["remedy_capacity"]
)

strategies["accountability_strategy_score"] = (
    0.16 * strategies["public_accountability"]
    + 0.16 * strategies["remedy_capacity"]
    + 0.14 * strategies["user_rights"]
    + 0.12 * strategies["worker_protection"]
    + 0.12 * strategies["researcher_access"]
    + 0.12 * strategies["competition_enforcement"]
    + 0.10 * strategies["interoperability"]
    + 0.08 * strategies["public_infrastructure"]
)

platforms.sort_values("platform_dependency_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_platform_profile_scores.csv", index=False)
risks.sort_values("platform_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_platform_risk_scores.csv", index=False)
accountability.sort_values("accountability_gap_score", ascending=False).to_csv(OUTPUTS / "advanced_platform_accountability_scores.csv", index=False)
scenarios.sort_values("public_interest_platform_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_platform_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_digital_platform_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_digital_platform_pathway_summary.csv", index=False)
strategies.sort_values("public_interest_platform_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = platforms.sort_values("platform_dependency_pressure_score")
plt.barh(ranked["platform_name"], ranked["platform_dependency_pressure_score"])
plt.xlabel("Platform Dependency Pressure")
plt.title(f"Platform Dependency Pressure — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "platform_dependency_pressure_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_scenarios = scenarios.sort_values("public_interest_platform_capacity_score")
plt.barh(ranked_scenarios["scenario_name"], ranked_scenarios["public_interest_platform_capacity_score"])
plt.xlabel("Public-Interest Platform Capacity")
plt.title("Public-Interest Platform Capacity by Scenario")
plt.tight_layout()
plt.savefig(OUTPUTS / "public_interest_platform_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["digital_public_value"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Digital Public Value")
plt.title("Digital Public Value Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "digital_public_value_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["platform_dependency_pressure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Platform Dependency Pressure")
plt.title("Platform Dependency Pressure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "platform_dependency_pressure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
