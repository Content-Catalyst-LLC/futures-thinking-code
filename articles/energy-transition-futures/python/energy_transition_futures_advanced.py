#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Energy Transition Futures.
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

capabilities = pd.read_csv(DATA / "energy_transition_capabilities.csv")
risks = pd.read_csv(DATA / "transition_risk_register.csv")
justice = pd.read_csv(DATA / "justice_indicators.csv")
scenarios = pd.read_csv(DATA / "energy_transition_scenarios.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

def readiness(df):
    return (
        0.14 * df["clean_power_expansion"]
        + 0.14 * df["grid_readiness"]
        + 0.12 * df["storage_flexibility"]
        + 0.12 * df["electrification_capacity"]
        + 0.12 * df["fossil_phase_down"]
        + 0.12 * df["energy_justice"]
        + 0.10 * df["labor_transition"]
        + 0.08 * df["material_responsibility"]
        + 0.06 * df["climate_resilience"]
    )

def risk_pressure(df):
    return (
        0.18 * (1 - df["grid_readiness"])
        + 0.16 * (1 - df["storage_flexibility"])
        + 0.16 * (1 - df["fossil_phase_down"])
        + 0.14 * (1 - df["energy_justice"])
        + 0.12 * (1 - df["labor_transition"])
        + 0.12 * (1 - df["material_responsibility"])
        + 0.12 * (1 - df["climate_resilience"])
    )

capabilities["transition_readiness_score"] = readiness(capabilities)
capabilities["transition_risk_pressure_score"] = risk_pressure(capabilities)
capabilities["justice_resilience_capacity_score"] = (
    0.24 * capabilities["energy_justice"]
    + 0.20 * capabilities["labor_transition"]
    + 0.18 * capabilities["climate_resilience"]
    + 0.16 * capabilities["material_responsibility"]
    + 0.12 * capabilities["fossil_phase_down"]
    + 0.10 * capabilities["grid_readiness"]
)

risks["transition_risk_priority_score"] = (
    0.18 * risks["probability"]
    + 0.20 * risks["severity"]
    + 0.14 * risks["detection_difficulty"]
    + 0.16 * risks["governance_gap"]
    + 0.14 * risks["infrastructure_exposure"]
    + 0.12 * risks["justice_relevance"]
    + 0.06 * (1 - risks["mitigation_capacity"])
)

justice["energy_justice_score"] = (
    0.18 * justice["affordability"]
    + 0.16 * justice["community_voice"]
    + 0.16 * justice["worker_security"]
    + 0.16 * justice["health_benefit"]
    + 0.12 * justice["ownership_access"]
    + 0.12 * justice["repair_capacity"]
    + 0.10 * justice["harm_reduction"]
)
justice["energy_justice_gap_score"] = 1 - justice["energy_justice_score"]

scenarios["transition_readiness_score"] = readiness(scenarios)
scenarios["transition_risk_pressure_score"] = risk_pressure(scenarios)
scenarios["justice_resilience_capacity_score"] = (
    0.24 * scenarios["energy_justice"]
    + 0.20 * scenarios["labor_transition"]
    + 0.18 * scenarios["climate_resilience"]
    + 0.16 * scenarios["material_responsibility"]
    + 0.12 * scenarios["fossil_phase_down"]
    + 0.10 * scenarios["grid_readiness"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    transition_capacity = float(row["initial_transition_capacity"])
    emissions_pressure = float(0.90 - 0.22 * row["clean_power"] - 0.18 * row["fossil_phase_down"])
    justice_resilience = float(0.50 * row["justice"] + 0.25 * row["labor"] + 0.25 * row["resilience"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.09 if t % 10 == 0 else 0.03

            infrastructure_force = (
                0.22 * row["clean_power"]
                + 0.20 * row["grid"]
                + 0.16 * row["storage"]
                + 0.16 * row["electrification"]
                + 0.12 * row["resilience"]
            )

            social_force = (
                0.18 * row["justice"]
                + 0.16 * row["labor"]
                + 0.12 * row["materials"]
                + 0.10 * row["fossil_phase_down"]
            )

            pressure = (
                0.18 * (1 - row["grid"])
                + 0.16 * (1 - row["storage"])
                + 0.16 * (1 - row["fossil_phase_down"])
                + 0.14 * (1 - row["justice"])
                + 0.12 * (1 - row["labor"])
                + 0.12 * (1 - row["materials"])
                + 0.12 * (1 - row["resilience"])
                + disruption
            )

            justice_resilience = np.clip(
                justice_resilience + 0.04 * row["justice"] + 0.03 * row["labor"] + 0.03 * row["resilience"] + 0.02 * row["materials"] - 0.04 * pressure,
                0,
                1.5,
            )

            emissions_pressure = np.clip(
                emissions_pressure * 0.92 + 0.08 * (1 - row["fossil_phase_down"]) + 0.05 * (1 - row["electrification"]) - 0.08 * row["clean_power"] - 0.06 * row["grid"],
                0,
                1.5,
            )

            transition_capacity = np.clip(
                transition_capacity + infrastructure_force / 5 + social_force / 6 + 0.04 * justice_resilience - 0.08 * pressure - 0.03 * emissions_pressure,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "transition_capacity": transition_capacity,
            "emissions_pressure": emissions_pressure,
            "justice_resilience_score": justice_resilience,
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
        final_transition_capacity=("transition_capacity", "last"),
        mean_emissions_pressure=("emissions_pressure", "mean"),
        final_justice_resilience_score=("justice_resilience_score", "last")
    )
    .reset_index()
    .sort_values("final_transition_capacity", ascending=False)
)

strategies["public_interest_transition_strategy_score"] = (
    0.14 * strategies["grid_investment"]
    + 0.12 * strategies["clean_power_deployment"]
    + 0.12 * strategies["electrification_support"]
    + 0.12 * strategies["fossil_phase_down_planning"]
    + 0.14 * strategies["justice_investment"]
    + 0.12 * strategies["labor_protection"]
    + 0.10 * strategies["material_governance"]
    + 0.08 * strategies["resilience_investment"]
    + 0.06 * strategies["public_finance"]
)

strategies["justice_resilience_strategy_score"] = (
    0.18 * strategies["justice_investment"]
    + 0.16 * strategies["labor_protection"]
    + 0.14 * strategies["resilience_investment"]
    + 0.14 * strategies["material_governance"]
    + 0.12 * strategies["fossil_phase_down_planning"]
    + 0.10 * strategies["grid_investment"]
    + 0.08 * strategies["public_finance"]
    + 0.08 * strategies["electrification_support"]
)

capabilities.sort_values("transition_readiness_score", ascending=False).to_csv(OUTPUTS / "advanced_energy_transition_capability_scores.csv", index=False)
risks.sort_values("transition_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_transition_risk_scores.csv", index=False)
justice.sort_values("energy_justice_score", ascending=False).to_csv(OUTPUTS / "advanced_energy_justice_scores.csv", index=False)
scenarios.sort_values("transition_readiness_score", ascending=False).to_csv(OUTPUTS / "advanced_energy_transition_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_energy_transition_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_energy_transition_pathway_summary.csv", index=False)
strategies.sort_values("public_interest_transition_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = scenarios.sort_values("transition_readiness_score")
plt.barh(ranked["scenario_name"], ranked["transition_readiness_score"])
plt.xlabel("Transition Readiness")
plt.title(f"Transition Readiness — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "transition_readiness_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_risk = risks.sort_values("transition_risk_priority_score")
plt.barh(ranked_risk["risk_name"], ranked_risk["transition_risk_priority_score"])
plt.xlabel("Risk Priority")
plt.title("Energy Transition Risk Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "transition_risk_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["transition_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Transition Capacity")
plt.title("Energy Transition Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "energy_transition_capacity_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["emissions_pressure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Emissions Pressure")
plt.title("Emissions Pressure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "energy_emissions_pressure_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
