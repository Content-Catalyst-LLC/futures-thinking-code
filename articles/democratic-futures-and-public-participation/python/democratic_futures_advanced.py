#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Democratic Futures and Public Participation.
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

models = pd.read_csv(DATA / "participation_models.csv")
representation = pd.read_csv(DATA / "representation_profiles.csv")
uptake = pd.read_csv(DATA / "decision_uptake_register.csv")
scenarios = pd.read_csv(DATA / "future_scenarios.csv")
pathways = pd.read_csv(DATA / "democratic_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

models["democratic_futures_capacity_score"] = (
    0.11 * models["inclusion"]
    + 0.12 * models["deliberative_quality"]
    + 0.11 * models["representation"]
    + 0.14 * models["institutional_uptake"]
    + 0.12 * models["accountability"]
    + 0.12 * models["justice_safeguards"]
    + 0.08 * models["public_learning"]
    + 0.10 * models["decision_influence"]
    + 0.05 * models["accessibility"]
    + 0.05 * models["community_authority"]
)

models["tokenism_risk_score"] = (
    0.18 * (1 - models["institutional_uptake"])
    + 0.16 * (1 - models["decision_influence"])
    + 0.14 * (1 - models["accountability"])
    + 0.14 * (1 - models["community_authority"])
    + 0.12 * (1 - models["justice_safeguards"])
    + 0.10 * (1 - models["representation"])
    + 0.08 * (1 - models["deliberative_quality"])
    + 0.08 * (1 - models["inclusion"])
)

representation["representation_quality_score"] = (
    0.20 * representation["affectedness"]
    + 0.20 * representation["representation_quality"]
    + 0.16 * representation["barrier_reduction"]
    + 0.12 * representation["compensation"]
    + 0.14 * representation["decision_access"]
    + 0.08 * representation["trust_condition"]
    + 0.10 * representation["knowledge_recognition"]
)

uptake["decision_uptake_score"] = (
    0.18 * uptake["response_duty"]
    + 0.16 * uptake["budget_connection"]
    + 0.16 * uptake["policy_influence"]
    + 0.14 * uptake["regulatory_influence"]
    + 0.14 * uptake["implementation_tracking"]
    + 0.12 * uptake["public_reporting"]
    + 0.10 * uptake["remedy_access"]
)

scenarios["democratic_stress_pressure_score"] = (
    0.16 * (1 - scenarios["public_trust"])
    + 0.14 * (1 - scenarios["participation_quality"])
    + 0.14 * (1 - scenarios["institutional_responsiveness"])
    + 0.14 * scenarios["inequality_pressure"]
    + 0.12 * scenarios["platform_power"]
    + 0.12 * scenarios["climate_stress"]
    + 0.12 * scenarios["democratic_polarization"]
    + 0.06 * (1 - scenarios["civic_capacity"])
)

scenarios["democratic_futures_opportunity_score"] = (
    0.20 * scenarios["public_trust"]
    + 0.20 * scenarios["participation_quality"]
    + 0.18 * scenarios["institutional_responsiveness"]
    + 0.16 * scenarios["civic_capacity"]
    + 0.10 * (1 - scenarios["democratic_polarization"])
    + 0.08 * (1 - scenarios["inequality_pressure"])
    + 0.08 * (1 - scenarios["platform_power"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    trust = float(row["initial_trust"])
    uptake_state = float(row["uptake"])
    learning_state = float(row["learning"])
    capacity_state = (
        0.14 * row["inclusion"]
        + 0.14 * row["deliberation"]
        + 0.14 * row["representation"]
        + 0.18 * uptake_state
        + 0.14 * row["accountability"]
        + 0.14 * row["justice"]
        + 0.12 * learning_state
    )
    tokenism = 1 - (0.50 * uptake_state + 0.50 * row["accountability"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            pressure = 0.14 if t % 8 == 0 else 0.05

            participation_quality = (
                0.22 * row["inclusion"]
                + 0.22 * row["deliberation"]
                + 0.18 * row["representation"]
                + 0.18 * row["justice"]
                + 0.10 * learning_state
                + 0.10 * row["accountability"]
            )

            institutional_response = (
                0.36 * uptake_state
                + 0.28 * row["accountability"]
                + 0.20 * row["authority"]
                + 0.16 * learning_state
            )

            uptake_state = np.clip(
                uptake_state
                + 0.04 * row["uptake"]
                + 0.03 * row["accountability"]
                + 0.03 * row["authority"]
                + 0.02 * learning_state
                - 0.03 * pressure,
                0,
                1.4,
            )

            tokenism = np.clip(
                tokenism
                + 0.05 * pressure
                - 0.04 * uptake_state
                - 0.04 * row["accountability"]
                - 0.03 * row["justice"]
                - 0.02 * row["authority"],
                0,
                1.2,
            )

            learning_state = np.clip(
                learning_state
                + 0.03 * row["learning"]
                + 0.03 * row["deliberation"]
                + 0.02 * uptake_state
                - 0.02 * pressure,
                0,
                1.4,
            )

            trust = np.clip(
                trust
                + 0.05 * uptake_state
                + 0.04 * row["accountability"]
                + 0.03 * row["justice"]
                + 0.02 * row["authority"]
                - 0.06 * tokenism
                - 0.02 * pressure,
                0,
                1.4,
            )

            capacity_state = np.clip(
                capacity_state
                + participation_quality / 7
                + institutional_response / 7
                + 0.04 * trust
                - 0.08 * tokenism
                - 0.04 * pressure,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "model_id": row["model_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "democratic_futures_capacity": capacity_state,
            "public_trust": trust,
            "institutional_uptake": uptake_state,
            "tokenism_risk": tokenism,
            "learning_score": learning_state,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "model_id", "scenario_id", "pathway_name"])
    .agg(
        final_democratic_futures_capacity=("democratic_futures_capacity", "last"),
        mean_democratic_futures_capacity=("democratic_futures_capacity", "mean"),
        final_public_trust=("public_trust", "last"),
        final_institutional_uptake=("institutional_uptake", "last"),
        mean_tokenism_risk=("tokenism_risk", "mean"),
        final_learning_score=("learning_score", "last")
    )
    .reset_index()
    .sort_values("final_democratic_futures_capacity", ascending=False)
)

strategies["democratic_futures_strategy_score"] = (
    0.12 * strategies["inclusion_design"]
    + 0.12 * strategies["deliberative_design"]
    + 0.12 * strategies["representation_quality"]
    + 0.14 * strategies["response_duty"]
    + 0.12 * strategies["budget_link"]
    + 0.12 * strategies["accountability_tracking"]
    + 0.12 * strategies["justice_safeguards"]
    + 0.08 * strategies["remedy_access"]
    + 0.06 * strategies["public_learning"]
)

strategies["decision_influence_strategy_score"] = (
    0.18 * strategies["response_duty"]
    + 0.18 * strategies["budget_link"]
    + 0.16 * strategies["accountability_tracking"]
    + 0.14 * strategies["remedy_access"]
    + 0.12 * strategies["justice_safeguards"]
    + 0.10 * strategies["representation_quality"]
    + 0.08 * strategies["deliberative_design"]
    + 0.04 * strategies["public_learning"]
)

models.sort_values("democratic_futures_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_participation_model_scores.csv", index=False)
representation.sort_values("representation_quality_score", ascending=False).to_csv(OUTPUTS / "advanced_representation_quality_scores.csv", index=False)
uptake.sort_values("decision_uptake_score", ascending=False).to_csv(OUTPUTS / "advanced_decision_uptake_scores.csv", index=False)
scenarios.sort_values("democratic_futures_opportunity_score", ascending=False).to_csv(OUTPUTS / "advanced_future_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_democratic_futures_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_democratic_futures_pathway_summary.csv", index=False)
strategies.sort_values("democratic_futures_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = models.sort_values("democratic_futures_capacity_score")
plt.barh(ranked["participation_model"], ranked["democratic_futures_capacity_score"])
plt.xlabel("Democratic Futures Capacity")
plt.title(f"Participation Model Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "democratic_futures_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_risk = models.sort_values("tokenism_risk_score")
plt.barh(ranked_risk["participation_model"], ranked_risk["tokenism_risk_score"])
plt.xlabel("Tokenism Risk")
plt.title("Tokenism Risk by Participation Model")
plt.tight_layout()
plt.savefig(OUTPUTS / "tokenism_risk_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["democratic_futures_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Democratic Futures Capacity")
plt.title("Democratic Futures Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "democratic_futures_capacity_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["tokenism_risk"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Tokenism Risk")
plt.title("Tokenism Risk Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "tokenism_risk_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
