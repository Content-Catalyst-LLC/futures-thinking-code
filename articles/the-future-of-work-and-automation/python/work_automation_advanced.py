#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for The Future of Work and Automation.
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

occupations = pd.read_csv(DATA / "occupation_profiles.csv")
tasks = pd.read_csv(DATA / "task_exposure_matrix.csv")
scenarios = pd.read_csv(DATA / "work_scenarios.csv")
risks = pd.read_csv(DATA / "algorithmic_management_risks.csv")
protections = pd.read_csv(DATA / "social_protection_indicators.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

occupations["exposure_pressure_score"] = (
    0.34 * occupations["task_exposure"]
    + 0.22 * occupations["surveillance_intensity"]
    + 0.18 * (1 - occupations["worker_voice"])
    + 0.14 * (1 - occupations["training_access"])
    + 0.12 * (1 - occupations["social_protection"])
)

occupations["worker_centered_capacity_score"] = (
    0.20 * occupations["augmentation_capacity"]
    + 0.20 * occupations["worker_voice"]
    + 0.16 * occupations["training_access"]
    + 0.16 * occupations["social_protection"]
    + 0.14 * occupations["wage_security"]
    + 0.14 * (1 - occupations["surveillance_intensity"])
)

occupations["transition_risk_score"] = (
    occupations["task_exposure"]
    * (1 - occupations["training_access"])
    * (1 - occupations["social_protection"] + occupations["surveillance_intensity"] / 2)
)

occupations["adjusted_job_quality_score"] = (
    0.28 * occupations["initial_job_quality"]
    + 0.18 * occupations["wage_security"]
    + 0.18 * occupations["worker_voice"]
    + 0.16 * occupations["social_protection"]
    + 0.12 * occupations["training_access"]
    + 0.08 * (1 - occupations["surveillance_intensity"])
)

tasks["weighted_automation_exposure"] = tasks["task_weight"] * (
    0.42 * tasks["ai_exposure"]
    + 0.28 * tasks["robotics_exposure"]
    + 0.18 * tasks["monitoring_exposure"]
    + 0.12 * (1 - tasks["human_context_requirement"])
)

tasks["weighted_augmentation_score"] = tasks["task_weight"] * (
    0.60 * tasks["augmentation_potential"]
    + 0.25 * tasks["human_context_requirement"]
    + 0.15 * tasks["ai_exposure"]
)

tasks["task_substitution_pressure"] = tasks["weighted_automation_exposure"] - tasks["weighted_augmentation_score"] / 2

scenarios["worker_centered_capacity_score"] = (
    0.18 * scenarios["augmentation_capacity"]
    + 0.18 * scenarios["worker_voice"]
    + 0.18 * scenarios["job_quality"]
    + 0.14 * scenarios["transition_support"]
    + 0.14 * scenarios["skill_mobility"]
    + 0.12 * scenarios["social_protection"]
    + 0.06 * (1 - scenarios["surveillance_intensity"])
)

scenarios["displacement_control_pressure_score"] = (
    0.30 * scenarios["automation_intensity"]
    + 0.22 * scenarios["surveillance_intensity"]
    + 0.18 * (1 - scenarios["transition_support"])
    + 0.16 * (1 - scenarios["skill_mobility"])
    + 0.14 * (1 - scenarios["social_protection"])
)

risks["algorithmic_management_risk_score"] = (
    0.18 * risks["probability"]
    + 0.20 * risks["severity"]
    + 0.14 * risks["detection_difficulty"]
    + 0.16 * risks["worker_voice_gap"]
    + 0.16 * risks["due_process_gap"]
    + 0.10 * risks["privacy_exposure"]
    + 0.06 * (1 - risks["mitigation_capacity"])
)

protections["social_protection_readiness_score"] = (
    0.16 * protections["training_access"]
    + 0.16 * protections["income_support"]
    + 0.14 * protections["portable_benefits"]
    + 0.14 * protections["wage_floor"]
    + 0.14 * protections["appeal_rights"]
    + 0.14 * protections["collective_bargaining_access"]
    + 0.12 * protections["public_investment"]
)
protections["social_protection_gap_score"] = 1 - protections["social_protection_readiness_score"]

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    job_quality = float(row["initial_job_quality"])
    transition_risk = float(row["task_exposure"] * (1 - row["training_access"]))
    skill_mobility = float(row["training_access"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            automation_pressure = 0.05 + 0.10 * row["task_exposure"]
            augmentation_gain = 0.08 * row["augmentation_capacity"]
            voice_buffer = 0.06 * row["worker_voice"]
            protection_buffer = 0.05 * row["social_protection"]
            surveillance_penalty = 0.07 * row["surveillance_intensity"]
            shock = 0.08 if t % 10 == 0 else 0.02

            transition_risk = np.clip(
                transition_risk * 0.90 + automation_pressure + shock - 0.06 * row["training_access"] - 0.05 * row["social_protection"],
                0,
                1.5,
            )

            skill_mobility = np.clip(
                skill_mobility + 0.04 * row["training_access"] + 0.03 * row["augmentation_capacity"] - 0.02 * row["surveillance_intensity"],
                0,
                1.2,
            )

            job_quality = np.clip(
                job_quality + augmentation_gain + voice_buffer + protection_buffer - automation_pressure / 2 - surveillance_penalty - shock / 2,
                0,
                1.5,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "occupation_id": row["occupation_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "job_quality": job_quality,
            "transition_risk": transition_risk,
            "skill_mobility": skill_mobility,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "occupation_id", "pathway_name"])
    .agg(
        final_job_quality=("job_quality", "last"),
        mean_transition_risk=("transition_risk", "mean"),
        final_skill_mobility=("skill_mobility", "last")
    )
    .reset_index()
    .sort_values("final_job_quality", ascending=False)
)

strategies["worker_centered_strategy_score"] = (
    0.16 * strategies["automation_governance"]
    + 0.18 * strategies["worker_voice"]
    + 0.14 * strategies["training_commitment"]
    + 0.14 * strategies["social_protection"]
    + 0.14 * strategies["job_quality_commitment"]
    + 0.10 * strategies["privacy_protection"]
    + 0.08 * strategies["productivity_sharing"]
    + 0.06 * strategies["care_investment"]
)

strategies["shared_prosperity_score"] = (
    0.14 * strategies["worker_voice"]
    + 0.14 * strategies["social_protection"]
    + 0.14 * strategies["job_quality_commitment"]
    + 0.16 * strategies["productivity_sharing"]
    + 0.14 * strategies["care_investment"]
    + 0.14 * strategies["training_commitment"]
    + 0.14 * strategies["automation_governance"]
)

occupations.sort_values("transition_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_occupation_future_scores.csv", index=False)
tasks.sort_values("task_substitution_pressure", ascending=False).to_csv(OUTPUTS / "advanced_task_exposure_scores.csv", index=False)
scenarios.sort_values("worker_centered_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_work_scenario_scores.csv", index=False)
risks.sort_values("algorithmic_management_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_algorithmic_management_risk_scores.csv", index=False)
protections.sort_values("social_protection_gap_score", ascending=False).to_csv(OUTPUTS / "advanced_social_protection_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_work_automation_paths.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_work_automation_summary.csv", index=False)
strategies.sort_values("worker_centered_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = occupations.sort_values("transition_risk_score")
plt.barh(ranked["occupation_name"], ranked["transition_risk_score"])
plt.xlabel("Transition Risk Score")
plt.title(f"Occupation Transition Risk — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "occupation_transition_risk_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_quality = occupations.sort_values("adjusted_job_quality_score")
plt.barh(ranked_quality["occupation_name"], ranked_quality["adjusted_job_quality_score"])
plt.xlabel("Adjusted Job Quality Score")
plt.title("Adjusted Job Quality by Occupation")
plt.tight_layout()
plt.savefig(OUTPUTS / "occupation_job_quality_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_scenarios = scenarios.sort_values("worker_centered_capacity_score")
plt.barh(ranked_scenarios["scenario_name"], ranked_scenarios["worker_centered_capacity_score"])
plt.xlabel("Worker-Centered Capacity")
plt.title("Worker-Centered Capacity by Scenario")
plt.tight_layout()
plt.savefig(OUTPUTS / "worker_centered_scenario_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["job_quality"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Job Quality")
plt.title("Job Quality Paths Under Automation")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "job_quality_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["transition_risk"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Transition Risk")
plt.title("Transition Risk Paths Under Automation")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "transition_risk_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
