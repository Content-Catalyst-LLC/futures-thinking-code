#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Institutional Adaptation.
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

profiles = pd.read_csv(DATA / "institutional_profiles.csv")
risks = pd.read_csv(DATA / "adaptation_risk_register.csv")
feedback = pd.read_csv(DATA / "feedback_indicators.csv")
scenarios = pd.read_csv(DATA / "adaptation_scenarios.csv")
pathways = pd.read_csv(DATA / "adaptive_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

profiles["adaptive_profile_score"] = (
    0.18 * profiles["learning_capacity"]
    + 0.16 * profiles["structural_flexibility"]
    + 0.16 * profiles["coordination_capacity"]
    + 0.14 * profiles["legitimacy"]
    + 0.14 * profiles["feedback_sensitivity"]
    + 0.10 * profiles["resource_mobility"]
    + 0.08 * profiles["shock_responsiveness"]
    - 0.10 * profiles["rigidity"]
    + 0.04 * profiles["intergenerational_responsibility"]
)

profiles["fragility_pressure_score"] = (
    0.20 * profiles["rigidity"]
    + 0.16 * (1 - profiles["learning_capacity"])
    + 0.16 * (1 - profiles["structural_flexibility"])
    + 0.14 * (1 - profiles["coordination_capacity"])
    + 0.12 * (1 - profiles["legitimacy"])
    + 0.12 * (1 - profiles["feedback_sensitivity"])
    + 0.10 * (1 - profiles["resource_mobility"])
)

risks["adaptation_risk_priority_score"] = (
    0.18 * risks["probability"]
    + 0.20 * risks["severity"]
    + 0.14 * risks["detection_difficulty"]
    + 0.16 * risks["governance_gap"]
    + 0.12 * risks["legitimacy_exposure"]
    + 0.12 * risks["implementation_exposure"]
    + 0.08 * (1 - risks["mitigation_capacity"])
)

feedback["feedback_capacity_score"] = (
    0.18 * feedback["signal_detection"]
    + 0.16 * feedback["interpretation_capacity"]
    + 0.16 * feedback["evaluation_quality"]
    + 0.14 * feedback["memory_retention"]
    + 0.14 * feedback["revision_authority"]
    + 0.12 * feedback["community_feedback"]
    + 0.10 * feedback["public_reporting"]
)

feedback["feedback_gap_score"] = 1 - feedback["feedback_capacity_score"]

scenarios["institutional_stress_pressure_score"] = (
    0.18 * scenarios["environmental_pressure"]
    + 0.18 * scenarios["technological_change"]
    + 0.14 * scenarios["demographic_pressure"]
    + 0.14 * scenarios["fiscal_constraint"]
    + 0.12 * (1 - scenarios["public_trust"])
    + 0.12 * scenarios["coordination_demand"]
    + 0.12 * scenarios["crisis_frequency"]
)

scenarios["adaptation_opportunity_score"] = (
    0.24 * scenarios["public_trust"]
    + 0.22 * (1 - scenarios["fiscal_constraint"])
    + 0.18 * (1 - scenarios["crisis_frequency"])
    + 0.14 * (1 - scenarios["environmental_pressure"])
    + 0.12 * (1 - scenarios["technological_change"])
    + 0.10 * scenarios["coordination_demand"]
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    legitimacy_state = float(row["legitimacy"])
    learning_state = float(row["learning"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.18 if t % 7 == 0 else 0.08

            adaptation_gain = (
                0.20 * learning_state
                + 0.18 * row["flexibility"]
                + 0.18 * row["coordination"]
                + 0.16 * row["feedback"]
                + 0.14 * row["resources"]
                + 0.10 * legitimacy_state
                - 0.18 * row["rigidity"]
            )

            legitimacy_state = np.clip(
                legitimacy_state + 0.04 * row["legitimacy"] + 0.03 * row["feedback"] + 0.02 * row["coordination"] - 0.04 * disruption - 0.03 * row["rigidity"],
                0,
                1.4,
            )

            learning_state = np.clip(
                learning_state + 0.04 * row["feedback"] + 0.03 * row["learning"] + 0.02 * row["coordination"] - 0.03 * row["rigidity"] - 0.02 * disruption,
                0,
                1.4,
            )

            viability = np.clip(
                viability - disruption + adaptation_gain + 0.04 * learning_state - 0.04 * (1 - legitimacy_state),
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "institution_id": row["institution_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "institutional_viability": viability,
            "legitimacy_score": legitimacy_state,
            "learning_score": learning_state,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "institution_id", "scenario_id", "pathway_name"])
    .agg(
        final_institutional_viability=("institutional_viability", "last"),
        mean_institutional_viability=("institutional_viability", "mean"),
        final_legitimacy_score=("legitimacy_score", "last"),
        final_learning_score=("learning_score", "last")
    )
    .reset_index()
    .sort_values("final_institutional_viability", ascending=False)
)

strategies["institutional_adaptation_strategy_score"] = (
    0.16 * strategies["learning_systems"]
    + 0.14 * strategies["adaptive_legal_design"]
    + 0.14 * strategies["cross_agency_coordination"]
    + 0.14 * strategies["participatory_governance"]
    + 0.12 * strategies["long_term_budgeting"]
    + 0.12 * strategies["feedback_infrastructure"]
    + 0.10 * strategies["accountability_safeguards"]
    + 0.05 * strategies["resource_mobility"]
    + 0.03 * strategies["power_analysis"]
)

strategies["legitimacy_and_accountability_strategy_score"] = (
    0.18 * strategies["participatory_governance"]
    + 0.16 * strategies["accountability_safeguards"]
    + 0.14 * strategies["power_analysis"]
    + 0.12 * strategies["feedback_infrastructure"]
    + 0.12 * strategies["learning_systems"]
    + 0.10 * strategies["cross_agency_coordination"]
    + 0.10 * strategies["long_term_budgeting"]
    + 0.08 * strategies["adaptive_legal_design"]
)

profiles.sort_values("adaptive_profile_score", ascending=False).to_csv(OUTPUTS / "advanced_institutional_profile_scores.csv", index=False)
risks.sort_values("adaptation_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_adaptation_risk_scores.csv", index=False)
feedback.sort_values("feedback_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_feedback_capacity_scores.csv", index=False)
scenarios.sort_values("institutional_stress_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_adaptation_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_institutional_adaptation_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_institutional_adaptation_pathway_summary.csv", index=False)
strategies.sort_values("institutional_adaptation_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("adaptive_profile_score")
plt.barh(ranked["institution_name"], ranked["adaptive_profile_score"])
plt.xlabel("Adaptive Profile")
plt.title(f"Adaptive Profile Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "institutional_adaptive_profile_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_risk = risks.sort_values("adaptation_risk_priority_score")
plt.barh(ranked_risk["risk_name"], ranked_risk["adaptation_risk_priority_score"])
plt.xlabel("Risk Priority")
plt.title("Institutional Adaptation Risk Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptation_risk_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["institutional_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Institutional Viability")
plt.title("Institutional Viability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "institutional_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["legitimacy_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Legitimacy Score")
plt.title("Institutional Legitimacy Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "institutional_legitimacy_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
