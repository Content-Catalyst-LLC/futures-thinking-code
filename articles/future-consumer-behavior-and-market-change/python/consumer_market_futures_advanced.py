#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Future Consumer Behavior and Market Change.
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

profiles = pd.read_csv(DATA / "consumer_future_profiles.csv")
scenarios = pd.read_csv(DATA / "market_scenarios.csv")
options = pd.read_csv(DATA / "consumer_strategy_options.csv")
vulnerabilities = pd.read_csv(DATA / "vulnerability_indicators.csv")
regulations = pd.read_csv(DATA / "regulatory_market_records.csv")
pathways = pd.read_csv(DATA / "adoption_pathways.csv")

profiles["consumer_future_health_score"] = (
    0.14 * profiles["affordability"]
    + 0.16 * profiles["trust"]
    + 0.10 * profiles["sustainability_demand"]
    + 0.16 * profiles["access_inclusion"]
    + 0.10 * (1 - profiles["price_sensitivity"])
    + 0.12 * (1 - profiles["behavioral_friction"])
    + 0.06 * profiles["digital_dependence"]
    + 0.06 * profiles["regulatory_pressure"]
    + 0.06 * profiles["privacy_confidence"]
    + 0.04 * profiles["local_resilience"]
)

profiles["market_fragility_score"] = (
    0.16 * profiles["price_sensitivity"]
    + 0.16 * profiles["behavioral_friction"]
    + 0.14 * (1 - profiles["trust"])
    + 0.12 * (1 - profiles["access_inclusion"])
    + 0.10 * (1 - profiles["affordability"])
    + 0.10 * profiles["digital_dependence"]
    + 0.08 * (1 - profiles["privacy_confidence"])
    + 0.08 * (1 - profiles["local_resilience"])
    + 0.06 * profiles["regulatory_pressure"]
)

scenarios["market_transition_pressure_score"] = (
    0.16 * scenarios["cost_pressure"]
    + 0.16 * scenarios["trust_pressure"]
    + 0.14 * scenarios["technology_acceleration"]
    + 0.14 * scenarios["platform_concentration"]
    + 0.12 * scenarios["sustainability_pressure"]
    + 0.10 * scenarios["access_gap"]
    + 0.10 * scenarios["privacy_regulation"]
    + 0.08 * (1 - scenarios["consumer_protection_strength"])
)

scenarios["consumer_protection_opportunity_score"] = (
    0.22 * scenarios["consumer_protection_strength"]
    + 0.18 * scenarios["privacy_regulation"]
    + 0.14 * scenarios["sustainability_pressure"]
    + 0.12 * (1 - scenarios["access_gap"])
    + 0.10 * (1 - scenarios["trust_pressure"])
    + 0.10 * (1 - scenarios["cost_pressure"])
    + 0.08 * (1 - scenarios["platform_concentration"])
    + 0.06 * scenarios["technology_acceleration"]
)

options["consumer_support_strategy_score"] = (
    0.16 * options["affordability_support"]
    + 0.16 * options["trust_building"]
    + 0.14 * options["privacy_protection"]
    + 0.14 * options["access_inclusion"]
    + 0.14 * options["sustainability_credibility"]
    + 0.14 * options["behavioral_integrity"]
    + 0.06 * options["implementation_capacity"]
    + 0.06 * options["market_scalability"]
)

options["implementation_risk_score"] = (
    0.25 * (1 - options["implementation_capacity"])
    + 0.15 * (1 - options["market_scalability"])
    + 0.12 * (1 - options["trust_building"])
    + 0.12 * (1 - options["behavioral_integrity"])
    + 0.10 * (1 - options["privacy_protection"])
    + 0.10 * (1 - options["access_inclusion"])
    + 0.08 * (1 - options["affordability_support"])
    + 0.08 * (1 - options["sustainability_credibility"])
)

vulnerabilities["consumer_vulnerability_priority_score"] = (
    0.18 * vulnerabilities["budget_pressure"]
    + 0.16 * vulnerabilities["information_asymmetry"]
    + 0.14 * vulnerabilities["digital_exclusion"]
    + 0.18 * vulnerabilities["behavioral_manipulation"]
    + 0.14 * vulnerabilities["lack_of_alternatives"]
    + 0.10 * (1 - vulnerabilities["remedy_access"])
    + 0.10 * (1 - vulnerabilities["consumer_protection"])
)

regulations["public_interest_market_governance_score"] = (
    0.16 * regulations["privacy_rules"]
    + 0.14 * regulations["pricing_transparency"]
    + 0.14 * regulations["subscription_fairness"]
    + 0.14 * regulations["accessibility_enforcement"]
    + 0.14 * regulations["green_claims_enforcement"]
    + 0.14 * regulations["platform_accountability"]
    + 0.14 * regulations["consumer_remedy_strength"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    adoption = float(row["initial_adoption"])
    trust = float(row["trust"])
    vulnerability = (
        0.24 * (1 - row["affordability"])
        + 0.20 * row["behavioral_friction"]
        + 0.18 * row["price_sensitivity"]
        + 0.16 * (1 - row["access_index"])
        + 0.12 * (1 - trust)
        + 0.10 * row["platform_visibility"]
    )
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            pressure_event = 0.16 if t % 8 == 0 else 0.05

            enabling_force = (
                0.20 * row["affordability"]
                + 0.20 * trust
                + 0.18 * row["access_index"]
                + 0.16 * row["platform_visibility"]
                + 0.14 * row["sustainability_demand"]
                + 0.12 * row["social_influence"]
            )

            barrier_force = (
                0.22 * row["behavioral_friction"]
                + 0.20 * row["price_sensitivity"]
                + 0.18 * (1 - row["affordability"])
                + 0.14 * (1 - row["access_index"])
                + 0.14 * (1 - trust)
                + 0.12 * pressure_event
            )

            trust = np.clip(
                trust
                + 0.03 * row["access_index"]
                + 0.03 * row["affordability"]
                + 0.02 * row["sustainability_demand"]
                - 0.04 * row["behavioral_friction"]
                - 0.03 * pressure_event,
                0,
                1.2,
            )

            vulnerability = np.clip(
                vulnerability
                + 0.05 * pressure_event
                + 0.03 * row["price_sensitivity"]
                + 0.03 * row["behavioral_friction"]
                - 0.03 * row["access_index"]
                - 0.03 * trust,
                0,
                1.4,
            )

            diffusion = 0.18 * adoption * (1 - adoption)
            adoption = np.clip(
                adoption
                + diffusion
                + 0.06 * enabling_force
                - 0.05 * barrier_force
                - 0.03 * vulnerability,
                0,
                1.0,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "adoption": adoption,
            "trust": trust,
            "consumer_vulnerability": vulnerability,
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
        final_adoption=("adoption", "last"),
        mean_adoption=("adoption", "mean"),
        final_trust=("trust", "last"),
        mean_vulnerability=("consumer_vulnerability", "mean")
    )
    .reset_index()
    .sort_values("final_adoption", ascending=False)
)

profiles.sort_values("consumer_future_health_score", ascending=False).to_csv(OUTPUTS / "advanced_consumer_future_profile_scores.csv", index=False)
scenarios.sort_values("consumer_protection_opportunity_score", ascending=False).to_csv(OUTPUTS / "advanced_market_scenario_scores.csv", index=False)
options.sort_values("consumer_support_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_consumer_strategy_option_scores.csv", index=False)
vulnerabilities.sort_values("consumer_vulnerability_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_vulnerability_priority_scores.csv", index=False)
regulations.sort_values("public_interest_market_governance_score", ascending=False).to_csv(OUTPUTS / "advanced_regulatory_market_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adoption_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adoption_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("consumer_future_health_score")
plt.barh(ranked["consumer_future_name"], ranked["consumer_future_health_score"])
plt.xlabel("Consumer Future Health Score")
plt.title(f"Consumer Future Health — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "consumer_future_health_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["consumer_future_health_score"], profiles["market_fragility_score"])
for _, row in profiles.iterrows():
    plt.text(row["consumer_future_health_score"], row["market_fragility_score"], row["consumer_future_name"], fontsize=7)
plt.xlabel("Consumer Future Health")
plt.ylabel("Market Fragility")
plt.title("Consumer Future Health vs Market Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "consumer_health_vs_market_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["adoption"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Adoption")
plt.title("Consumer Market Adoption Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "consumer_adoption_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["consumer_vulnerability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Consumer Vulnerability")
plt.title("Consumer Vulnerability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "consumer_vulnerability_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
