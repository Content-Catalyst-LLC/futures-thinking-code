#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Societal Transformation and Long-Term Change.
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

drivers = pd.read_csv(DATA / "transformation_drivers.csv")
signals = pd.read_csv(DATA / "weak_signals.csv")
scenarios = pd.read_csv(DATA / "transformation_scenarios.csv")
pressures = pd.read_csv(DATA / "system_pressure_indicators.csv")
equity = pd.read_csv(DATA / "equity_indicators.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

drivers["driver_transformation_priority"] = (
    0.18 * drivers["transformative_intensity"]
    + 0.14 * drivers["uncertainty"]
    + 0.16 * drivers["system_reach"]
    + 0.14 * drivers["feedback_strength"]
    + 0.14 * drivers["threshold_proximity"]
    + 0.12 * drivers["governance_relevance"]
    + 0.12 * drivers["equity_relevance"]
)

signals["signal_priority_score"] = (
    0.14 * signals["novelty"]
    + 0.24 * signals["relevance"]
    + 0.20 * signals["urgency"]
    + 0.14 * signals["evidence_quality"]
    + 0.16 * signals["affected_voice"]
    + 0.12 * signals["source_traceability"]
)

scenarios["transformation_depth_score"] = (
    0.18 * scenarios["technology_intensity"]
    + 0.18 * scenarios["economic_restructuring"]
    + 0.18 * scenarios["ecological_stress"]
    + 0.16 * scenarios["institutional_adaptability"]
    + 0.14 * scenarios["social_cohesion"]
    + 0.08 * scenarios["equity_protection"]
    + 0.08 * scenarios["public_legitimacy"]
)

scenarios["just_transformation_capacity_score"] = (
    0.22 * scenarios["institutional_adaptability"]
    + 0.22 * scenarios["equity_protection"]
    + 0.20 * scenarios["public_legitimacy"]
    + 0.18 * scenarios["social_cohesion"]
    + 0.10 * (1 - scenarios["ecological_stress"])
    + 0.08 * scenarios["economic_restructuring"]
)

scenarios["fragility_score"] = (
    0.26 * scenarios["ecological_stress"]
    + 0.22 * (1 - scenarios["institutional_adaptability"])
    + 0.20 * (1 - scenarios["social_cohesion"])
    + 0.18 * (1 - scenarios["public_legitimacy"])
    + 0.14 * (1 - scenarios["equity_protection"])
)

pressures["threshold_gap"] = pressures["current_value"] - pressures["threshold_value"]
pressures["threshold_breached"] = pressures["current_value"] >= pressures["threshold_value"]
review_weight = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
pressures["review_weight"] = pressures["review_frequency"].map(review_weight).fillna(0.50)
pressures["pressure_score"] = (
    0.35 * pressures["current_value"]
    + 0.30 * pressures["threshold_breached"].astype(float)
    + 0.20 * pressures["threshold_gap"].clip(lower=0)
    + 0.15 * pressures["review_weight"]
)

equity["justice_capacity_score"] = (
    0.20 * equity["voice"]
    + 0.22 * equity["protection"]
    + 0.22 * equity["repair"]
    + 0.18 * equity["agency"]
    + 0.18 * (1 - equity["burden_concentration"])
)

equity["harm_concentration_score"] = (
    0.30 * equity["exposure"]
    + 0.30 * equity["burden_concentration"]
    + 0.16 * (1 - equity["voice"])
    + 0.12 * (1 - equity["protection"])
    + 0.12 * (1 - equity["agency"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    pressure_index = float(row["ecology"] + row["economic_restructuring"])
    transformation_depth = 0.30
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            periodic_shock = 0.10 * row["ecology"] if t % 9 == 0 else 0.035 * row["ecology"]
            structural_pressure = (
                0.26 * row["ecology"]
                + 0.18 * row["economic_restructuring"]
                + 0.16 * (1 - row["public_legitimacy"])
                + 0.16 * (1 - row["equity_protection"])
                + periodic_shock
            )
            adaptive_capacity = (
                0.24 * row["institution"]
                + 0.18 * row["technology"]
                + 0.18 * row["public_legitimacy"]
                + 0.18 * row["equity_protection"]
            )
            threshold_effect = 0.08 if structural_pressure > adaptive_capacity else 0.00
            viability = np.clip(viability - structural_pressure / 5 + adaptive_capacity / 4 - threshold_effect, 0, 2.0)
            pressure_index = np.clip(structural_pressure + pressure_index * 0.92, 0, 2.5)
            transformation_depth = np.clip(
                transformation_depth
                + 0.04 * row["technology"]
                + 0.04 * row["economic_restructuring"]
                + 0.03 * row["ecology"]
                + 0.02 * row["institution"],
                0,
                2.5,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "transformation_viability": viability,
            "pressure_index": pressure_index,
            "transformation_depth": transformation_depth,
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
        final_viability=("transformation_viability", "last"),
        mean_viability=("transformation_viability", "mean"),
        max_pressure=("pressure_index", "max"),
        final_transformation_depth=("transformation_depth", "last")
    )
    .reset_index()
    .sort_values("final_viability", ascending=False)
)

strategies["public_interest_transformation_score"] = (
    0.14 * strategies["adaptation_depth"]
    + 0.16 * strategies["transformation_depth"]
    + 0.18 * strategies["equity_commitment"]
    + 0.16 * strategies["public_investment"]
    + 0.14 * strategies["institutional_learning"]
    + 0.12 * strategies["participation_strength"]
    + 0.10 * strategies["ecological_responsibility"]
)

drivers.sort_values("driver_transformation_priority", ascending=False).to_csv(OUTPUTS / "advanced_transformation_driver_scores.csv", index=False)
signals.sort_values("signal_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_weak_signal_priority_scores.csv", index=False)
scenarios.sort_values("just_transformation_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_transformation_scenario_scores.csv", index=False)
pressures.sort_values("pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_system_pressure_scores.csv", index=False)
equity.sort_values("justice_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_equity_justice_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_societal_transformation_paths.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_societal_transformation_summary.csv", index=False)
strategies.sort_values("public_interest_transformation_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = scenarios.sort_values("just_transformation_capacity_score")
plt.barh(ranked["scenario_name"], ranked["just_transformation_capacity_score"])
plt.xlabel("Just Transformation Capacity")
plt.title(f"Just Transformation Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "just_transformation_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_pressure = pressures.sort_values("pressure_score")
plt.barh(ranked_pressure["indicator_name"], ranked_pressure["pressure_score"])
plt.xlabel("System Pressure Score")
plt.title("System Pressure Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "system_pressure_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_equity = equity.sort_values("justice_capacity_score")
plt.barh(ranked_equity["equity_dimension"], ranked_equity["justice_capacity_score"])
plt.xlabel("Justice Capacity Score")
plt.title("Equity and Justice Capacity Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "equity_justice_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["transformation_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Transformation Viability")
plt.title("Societal Transformation Viability Pathways")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "societal_transformation_viability_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
