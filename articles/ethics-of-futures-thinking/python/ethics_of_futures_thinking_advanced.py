#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Ethics of Futures Thinking.
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

profiles = pd.read_csv(DATA / "ethical_futures_profiles.csv")
scenarios = pd.read_csv(DATA / "ethical_futures_scenarios.csv")
strategies = pd.read_csv(DATA / "ethical_strategy_options.csv")
risks = pd.read_csv(DATA / "ethical_risk_indicators.csv")
distribution = pd.read_csv(DATA / "stakeholder_distribution_paths.csv")
pathways = pd.read_csv(DATA / "intergenerational_ethics_pathways.csv")

profiles["ethical_futures_profile_score"] = (
    0.13 * profiles["intergenerational_responsibility"]
    + 0.12 * profiles["inclusion"]
    + 0.12 * profiles["accountability"]
    + 0.12 * profiles["risk_equity"]
    + 0.10 * profiles["transparency"]
    + 0.10 * profiles["contestability"]
    + 0.10 * profiles["precaution"]
    + 0.08 * profiles["adaptive_learning"]
    + 0.08 * profiles["epistemic_pluralism"]
    + 0.05 * profiles["public_legitimacy"]
)

profiles["ethical_capacity_gap"] = 1 - profiles["ethical_futures_profile_score"]

scenarios["ethical_failure_risk_score"] = (
    0.14 * scenarios["technocratic_opacity"]
    + 0.14 * scenarios["risk_inequality"]
    + 0.12 * scenarios["corporate_capture_pressure"]
    + 0.12 * scenarios["security_drift"]
    + 0.12 * scenarios["ai_opacity"]
    + 0.10 * (1 - scenarios["participation_depth"])
    + 0.10 * (1 - scenarios["intergenerational_weight"])
    + 0.08 * (1 - scenarios["accountability_strength"])
    + 0.04 * (1 - scenarios["climate_justice_alignment"])
    + 0.04 * (1 - scenarios["adaptive_learning_capacity"])
)

scenarios["ethical_opportunity_score"] = (
    0.15 * scenarios["participation_depth"]
    + 0.14 * scenarios["intergenerational_weight"]
    + 0.14 * scenarios["climate_justice_alignment"]
    + 0.14 * scenarios["accountability_strength"]
    + 0.11 * scenarios["adaptive_learning_capacity"]
    + 0.09 * (1 - scenarios["risk_inequality"])
    + 0.08 * (1 - scenarios["technocratic_opacity"])
    + 0.06 * (1 - scenarios["ai_opacity"])
    + 0.05 * (1 - scenarios["corporate_capture_pressure"])
    + 0.04 * (1 - scenarios["security_drift"])
)

strategies["ethical_strategy_value_score"] = (
    0.11 * strategies["value_transparency_gain"]
    + 0.13 * strategies["participation_gain"]
    + 0.13 * strategies["distributional_justice_gain"]
    + 0.12 * strategies["intergenerational_review_gain"]
    + 0.10 * strategies["epistemic_pluralism_gain"]
    + 0.09 * strategies["precaution_gain"]
    + 0.11 * strategies["accountability_gain"]
    + 0.10 * strategies["contestability_gain"]
    + 0.07 * strategies["adaptive_learning_gain"]
    + 0.02 * strategies["implementation_capacity"]
    + 0.02 * strategies["public_legitimacy_gain"]
)

risks["ethical_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.17 * risks["severity"]
    + 0.15 * risks["irreversibility"]
    + 0.10 * risks["visibility_gap"]
    + 0.20 * risks["distributional_harm"]
    + 0.14 * risks["rights_risk"]
    + 0.10 * (1 - risks["preparedness"])
)

distribution["net_welfare"] = distribution["benefit"] - distribution["risk"]
distribution["justice_adjusted_score"] = (
    distribution["benefit"]
    - distribution["risk"]
    - 0.35 * distribution["exposure"]
    + 0.25 * distribution["protection"]
    + 0.20 * distribution["moral_weight"]
    + 0.10 * distribution["voice_weight"]
)
distribution["vulnerability_gap"] = (distribution["exposure"] - distribution["protection"]).clip(lower=0)

def simulate_pathway(row):
    present_benefit = float(row["present_benefit"])
    future_benefit = float(row["future_benefit"])
    present_risk = float(row["present_risk"])
    future_risk = float(row["future_risk"])
    discount = float(row["discount_weight"])
    inequality = float(row["inequality_penalty"])
    participation = float(row["participation_quality"])
    accountability = float(row["accountability_strength"])
    precaution = float(row["precaution_strength"])
    learning = float(row["adaptive_learning_capacity"])
    horizon = int(row["time_horizon"])

    legitimacy = 0.30 * participation + 0.28 * accountability + 0.18 * precaution + 0.14 * learning + 0.10 * discount
    justice = 0.25 * present_benefit + 0.25 * future_benefit * discount - 0.20 * present_risk - 0.20 * future_risk - 0.10 * inequality + 0.10 * legitimacy

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            short_term_pressure = 0.008 if t % 6 == 0 else 0.0
            model_error = 0.006 if t % 9 == 0 else 0.0
            crisis_pressure = 0.010 if t % 13 == 0 else 0.0

            present_benefit = np.clip(present_benefit + 0.012 + short_term_pressure - 0.006 * participation - 0.004 * precaution, 0, 1.8)
            future_benefit = np.clip(future_benefit + 0.012 * discount + 0.010 * learning + 0.006 * accountability - 0.008 * short_term_pressure - 0.006 * model_error, 0, 1.8)
            present_risk = np.clip(present_risk + 0.006 * inequality + 0.006 * model_error - 0.006 * accountability - 0.005 * precaution, 0, 1.8)
            future_risk = np.clip(future_risk + 0.010 * inequality + 0.008 * crisis_pressure + 0.006 * model_error - 0.010 * precaution - 0.008 * learning - 0.006 * accountability, 0, 1.8)
            legitimacy = np.clip(legitimacy + 0.008 * participation + 0.008 * accountability + 0.006 * learning - 0.008 * inequality - 0.005 * present_risk, 0, 1.8)
            justice = np.clip(0.25 * present_benefit + 0.25 * future_benefit * discount - 0.20 * present_risk - 0.20 * future_risk - 0.10 * inequality + 0.10 * legitimacy, -1, 1.8)

        rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "present_benefit": present_benefit,
            "future_benefit": future_benefit,
            "present_risk": present_risk,
            "future_risk": future_risk,
            "legitimacy": legitimacy,
            "justice_adjusted_score": justice,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "scenario_id", "pathway_name"])
    .agg(
        final_present_benefit=("present_benefit", "last"),
        final_future_benefit=("future_benefit", "last"),
        mean_risk=("future_risk", "mean"),
        final_legitimacy=("legitimacy", "last"),
        final_justice_adjusted_score=("justice_adjusted_score", "last"),
        mean_justice_adjusted_score=("justice_adjusted_score", "mean"),
    )
    .reset_index()
    .sort_values("final_justice_adjusted_score", ascending=False)
)

profiles.sort_values("ethical_futures_profile_score", ascending=False).to_csv(OUTPUTS / "advanced_ethical_futures_profile_scores.csv", index=False)
scenarios.sort_values("ethical_failure_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_ethical_scenario_scores.csv", index=False)
strategies.sort_values("ethical_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_ethical_strategy_scores.csv", index=False)
risks.sort_values("ethical_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_ethical_risk_priority_scores.csv", index=False)
distribution.sort_values("justice_adjusted_score").to_csv(OUTPUTS / "advanced_stakeholder_distribution_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_intergenerational_ethics_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_intergenerational_ethics_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("ethical_futures_profile_score")
plt.barh(ranked["institution_type"], ranked["ethical_futures_profile_score"])
plt.xlabel("Ethical Futures Profile Score")
plt.title(f"Ethical Futures Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "ethical_futures_profile_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["risk_equity"], profiles["accountability"])
for _, row in profiles.iterrows():
    plt.text(row["risk_equity"], row["accountability"], row["institution_type"], fontsize=7)
plt.xlabel("Risk Equity")
plt.ylabel("Accountability")
plt.title("Risk Equity vs Accountability")
plt.tight_layout()
plt.savefig(OUTPUTS / "risk_equity_vs_accountability.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["justice_adjusted_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Justice-Adjusted Score")
plt.title("Intergenerational Justice-Adjusted Pathways")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "intergenerational_justice_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
grouped = distribution.groupby("group_name")["justice_adjusted_score"].mean().sort_values()
plt.barh(grouped.index, grouped.values)
plt.xlabel("Mean Justice-Adjusted Score")
plt.title("Stakeholder Distribution Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "stakeholder_distribution_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
