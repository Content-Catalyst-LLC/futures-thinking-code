#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Economic Futures and Global Development.
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

futures = pd.read_csv(DATA / "development_futures.csv")
scenarios = pd.read_csv(DATA / "economic_scenarios.csv")
policies = pd.read_csv(DATA / "policy_portfolios.csv")
shocks = pd.read_csv(DATA / "shocks_and_stressors.csv")
institutions = pd.read_csv(DATA / "institutional_capacity.csv")
pathways = pd.read_csv(DATA / "development_pathways.csv")

futures["development_quality_score"] = (
    0.14 * futures["growth"]
    - 0.12 * futures["inequality"]
    - 0.14 * futures["ecological_stress"]
    + 0.13 * futures["institutional_capacity"]
    + 0.12 * futures["resilience"]
    + 0.08 * futures["fiscal_space"]
    + 0.08 * futures["labor_inclusion"]
    + 0.08 * futures["public_investment"]
    + 0.06 * futures["technology_diffusion"]
    + 0.03 * futures["trade_resilience"]
    + 0.02 * futures["democratic_legitimacy"]
)

futures["development_fragility_score"] = (
    0.16 * futures["inequality"]
    + 0.16 * futures["ecological_stress"]
    + 0.13 * (1 - futures["institutional_capacity"])
    + 0.13 * (1 - futures["resilience"])
    + 0.12 * (1 - futures["fiscal_space"])
    + 0.10 * (1 - futures["labor_inclusion"])
    + 0.08 * (1 - futures["public_investment"])
    + 0.06 * (1 - futures["trade_resilience"])
    + 0.06 * (1 - futures["democratic_legitimacy"])
)

scenarios["economic_future_stress_score"] = (
    0.16 * scenarios["financial_volatility"]
    + 0.16 * scenarios["climate_pressure"]
    + 0.14 * scenarios["trade_fragmentation"]
    + 0.14 * scenarios["debt_stress"]
    + 0.12 * (1 - scenarios["public_trust"])
    + 0.12 * (1 - scenarios["coordination_capacity"])
    + 0.08 * (1 - scenarios["global_growth"])
    + 0.08 * (1 - scenarios["energy_transition_speed"])
)

scenarios["development_opportunity_score"] = (
    0.18 * scenarios["global_growth"]
    + 0.16 * scenarios["technology_acceleration"]
    + 0.16 * scenarios["energy_transition_speed"]
    + 0.16 * scenarios["coordination_capacity"]
    + 0.14 * scenarios["public_trust"]
    + 0.10 * (1 - scenarios["debt_stress"])
    + 0.10 * (1 - scenarios["trade_fragmentation"])
)

policies["development_strategy_strength_score"] = (
    0.15 * policies["productive_capability"]
    + 0.14 * policies["distributional_inclusion"]
    + 0.14 * policies["ecological_viability"]
    + 0.14 * policies["resilience_capacity"]
    + 0.11 * policies["fiscal_sustainability"]
    + 0.10 * policies["labor_protection"]
    + 0.10 * policies["implementation_capacity"]
    + 0.06 * policies["democratic_legitimacy"]
    + 0.06 * (1 - policies["global_coordination_need"])
)

policies["implementation_risk_score"] = (
    0.24 * (1 - policies["implementation_capacity"])
    + 0.18 * policies["global_coordination_need"]
    + 0.16 * (1 - policies["fiscal_sustainability"])
    + 0.14 * (1 - policies["democratic_legitimacy"])
    + 0.12 * (1 - policies["resilience_capacity"])
    + 0.08 * (1 - policies["distributional_inclusion"])
    + 0.08 * (1 - policies["ecological_viability"])
)

shocks["development_shock_priority_score"] = (
    0.18 * shocks["probability_proxy"]
    + 0.20 * shocks["severity"]
    + 0.18 * shocks["systemic_reach"]
    + 0.17 * shocks["distributional_exposure"]
    + 0.15 * shocks["recovery_difficulty"]
    + 0.12 * (1 - shocks["policy_preparedness"])
)

institutions["institutional_capacity_score"] = (
    0.18 * institutions["administrative_capacity"]
    + 0.18 * institutions["coordination_capacity"]
    + 0.14 * institutions["public_trust"]
    + 0.14 * institutions["regulatory_quality"]
    + 0.14 * institutions["tax_capacity"]
    + 0.12 * institutions["learning_capacity"]
    + 0.10 * institutions["participation_quality"]
)

institutions["institutional_fragility_score"] = (
    0.18 * (1 - institutions["administrative_capacity"])
    + 0.18 * (1 - institutions["coordination_capacity"])
    + 0.16 * (1 - institutions["public_trust"])
    + 0.14 * (1 - institutions["tax_capacity"])
    + 0.12 * (1 - institutions["regulatory_quality"])
    + 0.12 * (1 - institutions["learning_capacity"])
    + 0.10 * (1 - institutions["participation_quality"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    development = float(row["initial_development"])
    fragility = (
        0.22 * row["inequality"]
        + 0.20 * row["ecological_stress"]
        + 0.18 * (1 - row["resilience"])
        + 0.16 * (1 - row["institutional_capacity"])
        + 0.14 * (1 - row["fiscal_space"])
        + 0.10 * (1 - row["labor_inclusion"])
    )
    public_capacity = (
        0.34 * row["institutional_capacity"]
        + 0.20 * row["fiscal_space"]
        + 0.18 * row["adaptation"]
        + 0.14 * row["labor_inclusion"]
        + 0.14 * row["public_investment"]
    )
    fiscal_stress = 1 - row["fiscal_space"]
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.20 if t % 8 == 0 else 0.08
            ecological_pressure = 0.04 * row["ecological_stress"]
            inequality_drag = 0.04 * row["inequality"]
            institutional_response = (
                0.22 * row["institutional_capacity"]
                + 0.20 * row["adaptation"]
                + 0.18 * row["resilience"]
            )
            fiscal_response = (
                0.14 * row["fiscal_space"]
                + 0.12 * row["labor_inclusion"]
                + 0.10 * row["public_investment"]
            )

            fragility = np.clip(
                fragility
                + 0.05 * shock
                + ecological_pressure
                + inequality_drag
                - 0.04 * row["resilience"]
                - 0.04 * row["institutional_capacity"]
                - 0.03 * row["fiscal_space"]
                - 0.02 * row["public_investment"],
                0,
                1.4,
            )

            public_capacity = np.clip(
                public_capacity
                + 0.04 * row["institutional_capacity"]
                + 0.03 * row["fiscal_space"]
                + 0.03 * row["adaptation"]
                + 0.03 * row["public_investment"]
                + 0.02 * row["labor_inclusion"]
                - 0.04 * shock
                - 0.03 * fragility,
                0,
                1.5,
            )

            fiscal_stress = np.clip(
                fiscal_stress
                + 0.05 * shock
                + 0.04 * fragility
                + 0.03 * row["ecological_stress"]
                - 0.04 * row["fiscal_space"]
                - 0.03 * row["institutional_capacity"],
                0,
                1.4,
            )

            development = np.clip(
                development
                + row["growth"]
                + institutional_response / 8
                + fiscal_response / 8
                + 0.04 * public_capacity
                - shock
                - 0.05 * fragility
                - 0.03 * fiscal_stress,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "future_id": row["future_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "development_viability": development,
            "development_fragility": fragility,
            "public_capacity": public_capacity,
            "fiscal_stress": fiscal_stress,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths
    .groupby(["pathway_id", "future_id", "scenario_id", "pathway_name"])
    .agg(
        final_development_viability=("development_viability", "last"),
        mean_development_viability=("development_viability", "mean"),
        mean_development_fragility=("development_fragility", "mean"),
        final_public_capacity=("public_capacity", "last"),
        mean_fiscal_stress=("fiscal_stress", "mean")
    )
    .reset_index()
    .sort_values("final_development_viability", ascending=False)
)

futures.sort_values("development_quality_score", ascending=False).to_csv(OUTPUTS / "advanced_development_future_scores.csv", index=False)
scenarios.sort_values("development_opportunity_score", ascending=False).to_csv(OUTPUTS / "advanced_economic_scenario_scores.csv", index=False)
policies.sort_values("development_strategy_strength_score", ascending=False).to_csv(OUTPUTS / "advanced_policy_portfolio_scores.csv", index=False)
shocks.sort_values("development_shock_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_shock_priority_scores.csv", index=False)
institutions.sort_values("institutional_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_institutional_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_development_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_development_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = futures.sort_values("development_quality_score")
plt.barh(ranked["future_name"], ranked["development_quality_score"])
plt.xlabel("Development Quality Score")
plt.title(f"Development Quality — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "development_quality_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(futures["development_quality_score"], futures["development_fragility_score"])
for _, row in futures.iterrows():
    plt.text(row["development_quality_score"], row["development_fragility_score"], row["future_name"], fontsize=7)
plt.xlabel("Development Quality")
plt.ylabel("Development Fragility")
plt.title("Development Quality vs Fragility")
plt.tight_layout()
plt.savefig(OUTPUTS / "development_quality_vs_fragility.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["development_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Development Viability")
plt.title("Development Viability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "development_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["development_fragility"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Development Fragility")
plt.title("Development Fragility Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "development_fragility_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
