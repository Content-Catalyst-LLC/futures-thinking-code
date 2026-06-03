#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Thinking in Public Policy.
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

policies = pd.read_csv(DATA / "policy_options.csv")
scenarios = pd.read_csv(DATA / "scenario_profiles.csv")
capacity = pd.read_csv(DATA / "institutional_capacity.csv")
risks = pd.read_csv(DATA / "policy_risk_register.csv")
pathways = pd.read_csv(DATA / "adaptive_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

policies["policy_futures_profile_score"] = (
    0.20 * policies["robustness"]
    + 0.16 * policies["equity"]
    + 0.18 * policies["adaptability"]
    + 0.14 * policies["coordination"]
    + 0.14 * policies["legitimacy"]
    + 0.08 * policies["implementation_capacity"]
    + 0.06 * policies["learning_capacity"]
    + 0.04 * policies["intergenerational_responsibility"]
)

policies["policy_fragility_pressure_score"] = (
    0.20 * (1 - policies["robustness"])
    + 0.18 * (1 - policies["adaptability"])
    + 0.16 * (1 - policies["coordination"])
    + 0.14 * (1 - policies["legitimacy"])
    + 0.12 * (1 - policies["equity"])
    + 0.10 * (1 - policies["learning_capacity"])
    + 0.10 * (1 - policies["implementation_capacity"])
)

scenarios["policy_stress_pressure_score"] = (
    0.18 * scenarios["economic_volatility"]
    + 0.16 * scenarios["technological_disruption"]
    + 0.18 * scenarios["climate_stress"]
    + 0.12 * scenarios["demographic_pressure"]
    + 0.16 * scenarios["geopolitical_instability"]
    + 0.10 * (1 - scenarios["public_trust"])
    + 0.06 * (1 - scenarios["institutional_capacity"])
    + 0.04 * (1 - scenarios["fiscal_space"])
)

capacity["anticipatory_governance_capacity_score"] = (
    0.18 * capacity["detection_capacity"]
    + 0.18 * capacity["learning_capacity"]
    + 0.16 * capacity["coordination_quality"]
    + 0.12 * capacity["budget_alignment"]
    + 0.12 * capacity["implementation_capacity"]
    + 0.10 * capacity["public_participation"]
    + 0.08 * capacity["data_infrastructure"]
    + 0.06 * capacity["accountability_capacity"]
)

capacity["capacity_gap_score"] = 1 - capacity["anticipatory_governance_capacity_score"]

risks["policy_risk_priority_score"] = (
    0.18 * risks["probability"]
    + 0.20 * risks["severity"]
    + 0.14 * risks["detection_difficulty"]
    + 0.16 * risks["governance_gap"]
    + 0.12 * risks["equity_exposure"]
    + 0.12 * risks["implementation_exposure"]
    + 0.08 * (1 - risks["mitigation_capacity"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    viability = float(row["initial_viability"])
    legitimacy_state = float(row["legitimacy"])
    equity_state = float(row["equity"])
    adaptive_learning = float(row["learning_capacity"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            disruption = 0.17 if t % 8 == 0 else 0.06

            response_gain = (
                0.22 * row["robustness"]
                + 0.24 * row["adaptability"]
                + 0.20 * row["coordination"]
                + 0.16 * row["legitimacy"]
                + 0.12 * row["equity"]
                + 0.06 * row["learning_capacity"]
            )

            implementation_drag = 0.10 * (1 - row["implementation_capacity"])
            trust_drag = 0.06 * (1 - legitimacy_state)
            inequity_drag = 0.06 * (1 - equity_state)

            adaptive_learning = np.clip(
                adaptive_learning + 0.04 * row["learning_capacity"] + 0.03 * row["adaptability"] + 0.02 * row["coordination"] - 0.04 * disruption,
                0,
                1.4,
            )

            legitimacy_state = np.clip(
                legitimacy_state + 0.04 * row["legitimacy"] + 0.03 * row["equity"] + 0.02 * row["coordination"] - 0.04 * disruption - 0.02 * (1 - row["implementation_capacity"]),
                0,
                1.4,
            )

            equity_state = np.clip(
                equity_state + 0.04 * row["equity"] + 0.02 * row["coordination"] + 0.02 * row["learning_capacity"] - 0.03 * disruption,
                0,
                1.4,
            )

            viability = np.clip(
                viability - disruption + response_gain / 4 + 0.04 * adaptive_learning - implementation_drag - trust_drag - inequity_drag,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "policy_id": row["policy_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "policy_viability": viability,
            "legitimacy_score": legitimacy_state,
            "equity_score": equity_state,
            "adaptive_learning_score": adaptive_learning,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "policy_id", "scenario_id", "pathway_name"])
    .agg(
        final_policy_viability=("policy_viability", "last"),
        mean_policy_viability=("policy_viability", "mean"),
        final_legitimacy_score=("legitimacy_score", "last"),
        final_equity_score=("equity_score", "last"),
        final_adaptive_learning_score=("adaptive_learning_score", "last")
    )
    .reset_index()
    .sort_values("final_policy_viability", ascending=False)
)

strategies["foresight_capacity_strategy_score"] = (
    0.12 * strategies["horizon_scanning"]
    + 0.14 * strategies["scenario_planning"]
    + 0.16 * strategies["adaptive_policy_design"]
    + 0.14 * strategies["public_participation"]
    + 0.12 * strategies["budget_alignment"]
    + 0.12 * strategies["evaluation_capacity"]
    + 0.10 * strategies["interagency_coordination"]
    + 0.06 * strategies["equity_analysis"]
    + 0.04 * strategies["implementation_support"]
)

strategies["operational_governance_strategy_score"] = (
    0.18 * strategies["budget_alignment"]
    + 0.18 * strategies["implementation_support"]
    + 0.16 * strategies["evaluation_capacity"]
    + 0.14 * strategies["interagency_coordination"]
    + 0.12 * strategies["adaptive_policy_design"]
    + 0.10 * strategies["horizon_scanning"]
    + 0.06 * strategies["scenario_planning"]
    + 0.06 * strategies["equity_analysis"]
)

policies.sort_values("policy_futures_profile_score", ascending=False).to_csv(OUTPUTS / "advanced_policy_option_scores.csv", index=False)
scenarios.sort_values("policy_stress_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_scenario_profile_scores.csv", index=False)
capacity.sort_values("anticipatory_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_institutional_capacity_scores.csv", index=False)
risks.sort_values("policy_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_policy_risk_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_adaptive_policy_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_policy_pathway_summary.csv", index=False)
strategies.sort_values("foresight_capacity_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = policies.sort_values("policy_futures_profile_score")
plt.barh(ranked["policy_name"], ranked["policy_futures_profile_score"])
plt.xlabel("Policy Futures Profile")
plt.title(f"Policy Futures Profile — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "policy_futures_profile_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_risk = risks.sort_values("policy_risk_priority_score")
plt.barh(ranked_risk["risk_name"], ranked_risk["policy_risk_priority_score"])
plt.xlabel("Risk Priority")
plt.title("Public Policy Risk Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "policy_risk_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["policy_viability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Policy Viability")
plt.title("Adaptive Policy Viability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_policy_viability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["legitimacy_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Legitimacy Score")
plt.title("Policy Legitimacy Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "policy_legitimacy_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
