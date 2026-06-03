#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Thinking in Business Strategy.
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

strategies = pd.read_csv(DATA / "strategy_profiles.csv")
scenarios = pd.read_csv(DATA / "future_scenarios.csv")
options = pd.read_csv(DATA / "strategic_options.csv")
capabilities = pd.read_csv(DATA / "capability_register.csv")
indicators = pd.read_csv(DATA / "early_warning_indicators.csv")
pathways = pd.read_csv(DATA / "dynamic_capability_pathways.csv")

strategies["business_futures_readiness_score"] = (
    0.14 * strategies["innovation_capacity"]
    - 0.10 * strategies["uncertainty_exposure"]
    + 0.15 * strategies["resilience"]
    + 0.14 * strategies["strategic_flexibility"]
    + 0.10 * strategies["organizational_alignment"]
    + 0.12 * strategies["sensing_capability"]
    + 0.08 * strategies["capital_flexibility"]
    + 0.09 * strategies["legitimacy_trust"]
    + 0.08 * strategies["transition_readiness"]
)

strategies["strategic_fragility_score"] = (
    0.18 * strategies["uncertainty_exposure"]
    + 0.14 * (1 - strategies["resilience"])
    + 0.14 * (1 - strategies["strategic_flexibility"])
    + 0.13 * (1 - strategies["sensing_capability"])
    + 0.11 * (1 - strategies["capital_flexibility"])
    + 0.10 * (1 - strategies["organizational_alignment"])
    + 0.10 * (1 - strategies["legitimacy_trust"])
    + 0.10 * (1 - strategies["transition_readiness"])
)

options["net_strategic_option_value"] = (
    0.22 * options["learning_value"]
    + 0.20 * options["upside_potential"]
    + 0.15 * options["reversibility"]
    + 0.15 * options["scalability"]
    + 0.14 * options["strategic_fit"]
    + 0.14 * options["signal_sensitivity"]
    - 0.20 * options["cost_to_maintain"]
)

options["option_quality_score"] = (
    0.18 * options["learning_value"]
    + 0.18 * options["strategic_fit"]
    + 0.16 * options["signal_sensitivity"]
    + 0.14 * options["reversibility"]
    + 0.14 * options["scalability"]
    + 0.12 * options["upside_potential"]
    + 0.08 * (1 - options["cost_to_maintain"])
)

capabilities["future_capability_gap"] = (capabilities["future_importance"] - capabilities["current_strength"]).clip(lower=0)
capabilities["capability_investment_priority"] = (
    0.34 * capabilities["future_importance"]
    + 0.20 * capabilities["development_difficulty"]
    + 0.18 * capabilities["coordination_requirement"]
    + 0.14 * capabilities["investment_need"]
    + 0.14 * (1 - capabilities["current_strength"])
)

indicators["trigger_proximity"] = 1 - (indicators["trigger_threshold"] - indicators["current_signal_strength"]).clip(lower=0)
indicators["strategic_signal_urgency"] = (
    0.25 * indicators["current_signal_strength"]
    + 0.22 * indicators["strategic_relevance"]
    + 0.16 * indicators["lead_time"]
    + 0.12 * (1 - indicators["monitoring_difficulty"])
    + 0.25 * indicators["trigger_proximity"]
)

stress_rows = []
for _, strategy in strategies.iterrows():
    for _, scenario in scenarios.iterrows():
        opportunity = (
            0.18 * scenario["market_growth"]
            + 0.16 * scenario["technology_acceleration"] * strategy["innovation_capacity"]
            + 0.14 * scenario["capital_availability"] * strategy["capital_flexibility"]
            + 0.14 * scenario["consumer_trust_pressure"] * strategy["legitimacy_trust"]
            + 0.12 * strategy["sensing_capability"]
            + 0.12 * strategy["strategic_flexibility"]
            + 0.14 * strategy["transition_readiness"]
        )

        pressure = (
            0.16 * scenario["regulatory_pressure"] * (1 - strategy["transition_readiness"])
            + 0.16 * scenario["climate_stress"] * (1 - strategy["resilience"])
            + 0.14 * (1 - scenario["supply_chain_stability"]) * (1 - strategy["resilience"])
            + 0.14 * (1 - scenario["capital_availability"]) * (1 - strategy["capital_flexibility"])
            + 0.14 * scenario["geopolitical_fragmentation"] * (1 - strategy["strategic_flexibility"])
            + 0.12 * scenario["consumer_trust_pressure"] * (1 - strategy["legitimacy_trust"])
            + 0.14 * strategy["uncertainty_exposure"]
        )

        stress_rows.append({
            "strategy_id": strategy["strategy_id"],
            "strategy_name": strategy["strategy_name"],
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "scenario_opportunity_score": opportunity,
            "scenario_pressure_score": pressure,
            "cross_scenario_viability": np.clip(0.65 + opportunity - pressure, 0, 1.5),
        })

scenario_stress = pd.DataFrame(stress_rows)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    option_value = 0.28 * row["flexibility"] + 0.22 * row["sensing"] + 0.18 * row["capital_flexibility"] + 0.18 * row["innovation"] + 0.14 * row["transition_readiness"]
    fragility = 1 - (0.28 * row["resilience"] + 0.20 * row["flexibility"] + 0.18 * row["trust"] + 0.18 * row["capital_flexibility"] + 0.16 * row["alignment"])
    learning = 0.35 * row["sensing"] + 0.25 * row["innovation"] + 0.22 * row["alignment"] + 0.18 * row["transition_readiness"]
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.18 if t % 8 == 0 else 0.06

            response_gain = (
                0.18 * row["innovation"]
                + 0.20 * row["resilience"]
                + 0.20 * row["flexibility"]
                + 0.16 * row["sensing"]
                + 0.10 * row["capital_flexibility"]
                + 0.08 * row["trust"]
                + 0.08 * row["transition_readiness"]
            )

            option_value = np.clip(
                option_value
                + 0.03 * row["flexibility"]
                + 0.03 * row["sensing"]
                + 0.02 * row["capital_flexibility"]
                + 0.02 * row["innovation"]
                - 0.04 * disruption,
                0,
                1.5,
            )

            fragility = np.clip(
                fragility
                + 0.06 * disruption
                - 0.03 * row["resilience"]
                - 0.03 * row["flexibility"]
                - 0.02 * row["trust"]
                - 0.02 * row["alignment"]
                - 0.02 * row["transition_readiness"],
                0,
                1.4,
            )

            learning = np.clip(
                learning
                + 0.03 * row["sensing"]
                + 0.03 * row["alignment"]
                + 0.02 * row["innovation"]
                + 0.02 * row["transition_readiness"]
                - 0.02 * disruption,
                0,
                1.4,
            )

            viability = np.clip(
                viability
                - disruption
                - 0.04 * fragility
                + response_gain / 4
                + 0.05 * option_value
                + 0.03 * learning,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "strategy_id": row["strategy_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "strategic_viability": viability,
            "strategic_option_value": option_value,
            "fragility_score": fragility,
            "learning_score": learning,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths
    .groupby(["pathway_id", "strategy_id", "scenario_id", "pathway_name"])
    .agg(
        final_strategic_viability=("strategic_viability", "last"),
        mean_strategic_viability=("strategic_viability", "mean"),
        final_option_value=("strategic_option_value", "last"),
        mean_fragility_score=("fragility_score", "mean"),
        final_learning_score=("learning_score", "last")
    )
    .reset_index()
    .sort_values("final_strategic_viability", ascending=False)
)

strategies.sort_values("business_futures_readiness_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_profile_scores.csv", index=False)
options.sort_values("net_strategic_option_value", ascending=False).to_csv(OUTPUTS / "advanced_strategic_option_scores.csv", index=False)
capabilities.sort_values("capability_investment_priority", ascending=False).to_csv(OUTPUTS / "advanced_capability_priority_scores.csv", index=False)
indicators.sort_values("strategic_signal_urgency", ascending=False).to_csv(OUTPUTS / "advanced_early_warning_indicator_scores.csv", index=False)
scenario_stress.sort_values(["strategy_id", "cross_scenario_viability"], ascending=[True, False]).to_csv(OUTPUTS / "advanced_scenario_stress_test_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_dynamic_capability_paths.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_dynamic_capability_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = strategies.sort_values("business_futures_readiness_score")
plt.barh(ranked["strategy_name"], ranked["business_futures_readiness_score"])
plt.xlabel("Business Futures Readiness")
plt.title(f"Strategy Futures Readiness — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "business_futures_readiness_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(strategies["business_futures_readiness_score"], strategies["strategic_fragility_score"])
for _, row in strategies.iterrows():
    plt.text(row["business_futures_readiness_score"], row["strategic_fragility_score"], row["strategy_name"], fontsize=7)
plt.xlabel("Business Futures Readiness")
plt.ylabel("Strategic Fragility")
plt.title("Futures Readiness vs Strategic Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "readiness_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["strategic_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Strategic Viability")
plt.title("Strategic Viability Paths Under Uncertainty")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "strategic_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["fragility_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Fragility Score")
plt.title("Strategic Fragility Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "strategic_fragility_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
