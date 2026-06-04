#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Future Generations and Long-Term Responsibility.
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

profiles = pd.read_csv(DATA / "intergenerational_responsibility_profiles.csv")
scenarios = pd.read_csv(DATA / "future_generation_scenarios.csv")
strategies = pd.read_csv(DATA / "intergenerational_strategy_options.csv")
risks = pd.read_csv(DATA / "long_term_risk_indicators.csv")
records = pd.read_csv(DATA / "inheritance_records.csv")
pathways = pd.read_csv(DATA / "adaptive_long_term_pathways.csv")

profiles["inherited_burden_score"] = (
    0.18 * profiles["climate_burden"]
    + 0.14 * profiles["debt_without_assets"]
    + 0.16 * profiles["infrastructure_decay"]
    + 0.18 * profiles["ecological_damage"]
    + 0.14 * profiles["technological_lock_in"]
    + 0.10 * (1 - profiles["institutional_capacity"])
    + 0.06 * (1 - profiles["adaptive_capacity"])
    + 0.04 * (1 - profiles["future_representation"])
)

profiles["future_freedom_score"] = (
    0.20 * profiles["institutional_capacity"]
    + 0.20 * profiles["adaptive_capacity"]
    + 0.16 * profiles["future_representation"]
    + 0.14 * (1 - profiles["technological_lock_in"])
    + 0.12 * (1 - profiles["infrastructure_decay"])
    + 0.10 * (1 - profiles["ecological_damage"])
    + 0.05 * (1 - profiles["climate_burden"])
    + 0.03 * (1 - profiles["debt_without_assets"])
)

profiles["stewardship_score"] = (
    0.18 * profiles["future_freedom_score"]
    + 0.18 * profiles["institutional_capacity"]
    + 0.18 * profiles["adaptive_capacity"]
    + 0.14 * profiles["future_representation"]
    + 0.12 * profiles["reparative_continuity"]
    + 0.10 * profiles["public_legitimacy"]
    - 0.06 * profiles["inherited_burden_score"]
    - 0.04 * profiles["ecological_damage"]
)

scenarios["long_term_risk_score"] = (
    0.13 * scenarios["short_term_pressure"]
    + 0.14 * scenarios["climate_delay"]
    + 0.14 * scenarios["ecological_threshold_risk"]
    + 0.11 * scenarios["debt_transfer"]
    + 0.12 * scenarios["maintenance_deferral"]
    + 0.11 * scenarios["technology_lock_in"]
    + 0.11 * scenarios["institutional_fragility"]
    + 0.07 * scenarios["future_representation_gap"]
    + 0.05 * scenarios["reparative_gap"]
    + 0.02 * (1 - scenarios["adaptive_learning_capacity"])
)

scenarios["stewardship_opportunity_score"] = (
    0.16 * (1 - scenarios["short_term_pressure"])
    + 0.14 * (1 - scenarios["climate_delay"])
    + 0.13 * (1 - scenarios["ecological_threshold_risk"])
    + 0.12 * (1 - scenarios["maintenance_deferral"])
    + 0.11 * (1 - scenarios["technology_lock_in"])
    + 0.10 * (1 - scenarios["institutional_fragility"])
    + 0.09 * (1 - scenarios["future_representation_gap"])
    + 0.08 * (1 - scenarios["reparative_gap"])
    + 0.05 * scenarios["adaptive_learning_capacity"]
    + 0.02 * (1 - scenarios["debt_transfer"])
)

strategies["intergenerational_strategy_value_score"] = (
    0.13 * strategies["future_generation_review_gain"]
    + 0.13 * strategies["climate_budgeting_gain"]
    + 0.12 * strategies["maintenance_accounting_gain"]
    + 0.12 * strategies["ecological_restoration_gain"]
    + 0.11 * strategies["public_investment_gain"]
    + 0.10 * strategies["youth_participation_gain"]
    + 0.10 * strategies["technology_accountability_gain"]
    + 0.09 * strategies["reparative_finance_gain"]
    + 0.07 * strategies["adaptive_governance_gain"]
    + 0.02 * strategies["implementation_capacity"]
    + 0.01 * strategies["public_legitimacy_gain"]
)

risks["long_term_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.16 * risks["severity"]
    + 0.15 * risks["irreversibility"]
    + 0.10 * risks["visibility_gap"]
    + 0.18 * risks["distributional_harm"]
    + 0.18 * risks["future_generation_harm"]
    + 0.09 * (1 - risks["preparedness"])
)

records["stewardship_capacity_score"] = (
    0.18 * records["future_freedom"]
    + 0.18 * records["institutional_capacity"]
    + 0.18 * records["adaptive_capacity"]
    + 0.14 * records["future_representation"]
    + 0.12 * records["reparative_continuity"]
    + 0.10 * records["public_legitimacy"]
    - 0.06 * records["inherited_burden"]
    - 0.04 * records["ecological_damage"]
)

records["burden_gap_score"] = (
    records["inherited_burden"] + records["ecological_damage"] - records["future_freedom"] - records["adaptive_capacity"]
).clip(lower=0)

def simulate_pathway(row):
    burden = float(row["inherited_burden"])
    freedom = float(row["future_freedom"])
    institution = float(row["institutional_capacity"])
    ecology = float(row["ecological_damage"])
    adaptive = float(row["adaptive_capacity"])
    representation = float(row["future_representation"])
    repair = float(row["reparative_continuity"])
    legitimacy = float(row["public_legitimacy"])
    horizon = int(row["time_horizon"])

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            short_term_pressure = 0.010 if t % 6 == 0 else 0.0
            climate_shock = 0.014 if t % 10 == 0 else 0.0
            repair_window = 0.012 if t % 12 == 0 else 0.0
            institutional_shock = 0.010 if t % 17 == 0 else 0.0

            burden = np.clip(burden + short_term_pressure + 0.010 * ecology + 0.006 * institutional_shock - 0.012 * adaptive - 0.010 * representation - 0.008 * repair, 0, 1.8)
            ecology = np.clip(ecology + climate_shock + 0.008 * burden - 0.014 * adaptive - 0.010 * institution - 0.008 * repair, 0, 1.8)
            institution = np.clip(institution + 0.010 * representation + 0.008 * adaptive + 0.006 * legitimacy - 0.008 * burden - 0.006 * short_term_pressure - 0.006 * institutional_shock, 0, 1.8)
            adaptive = np.clip(adaptive + 0.010 * institution + 0.008 * representation + repair_window - 0.010 * ecology - 0.006 * burden, 0, 1.8)
            representation = np.clip(representation + 0.008 * institution + 0.008 * legitimacy + repair_window - 0.006 * short_term_pressure, 0, 1.8)
            repair = np.clip(repair + 0.010 * representation + 0.008 * institution + repair_window - 0.006 * burden - 0.004 * ecology, 0, 1.8)
            legitimacy = np.clip(legitimacy + 0.008 * representation + 0.007 * institution + 0.006 * repair - 0.006 * burden - 0.005 * ecology, 0, 1.8)
            freedom = np.clip(freedom + 0.010 * adaptive + 0.008 * institution + 0.006 * representation + 0.006 * repair - 0.012 * burden - 0.010 * ecology, 0, 1.8)

        stewardship = np.clip(
            0.18 * freedom
            + 0.18 * institution
            + 0.18 * adaptive
            + 0.14 * representation
            + 0.12 * repair
            + 0.10 * legitimacy
            - 0.06 * burden
            - 0.04 * ecology,
            -1,
            1.8,
        )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "inherited_burden": burden,
            "future_freedom": freedom,
            "institutional_capacity": institution,
            "ecological_damage": ecology,
            "adaptive_capacity": adaptive,
            "future_representation": representation,
            "reparative_continuity": repair,
            "public_legitimacy": legitimacy,
            "stewardship_score": stewardship,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_inherited_burden=("inherited_burden", "last"),
        final_future_freedom=("future_freedom", "last"),
        final_institutional_capacity=("institutional_capacity", "last"),
        final_ecological_damage=("ecological_damage", "last"),
        final_adaptive_capacity=("adaptive_capacity", "last"),
        final_future_representation=("future_representation", "last"),
        final_stewardship_score=("stewardship_score", "last"),
        mean_stewardship_score=("stewardship_score", "mean"),
    )
    .reset_index()
    .sort_values("final_stewardship_score", ascending=False)
)

profiles.sort_values("stewardship_score", ascending=False).to_csv(OUTPUTS / "advanced_intergenerational_profile_scores.csv", index=False)
scenarios.sort_values("long_term_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_future_generation_scenario_scores.csv", index=False)
strategies.sort_values("intergenerational_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_intergenerational_strategy_scores.csv", index=False)
risks.sort_values("long_term_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_long_term_risk_priority_scores.csv", index=False)
records.sort_values("stewardship_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_inheritance_record_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_long_term_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_long_term_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("stewardship_score")
plt.barh(ranked["scenario_name"], ranked["stewardship_score"])
plt.xlabel("Stewardship Score")
plt.title(f"Stewardship Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "stewardship_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["inherited_burden_score"], profiles["future_freedom_score"])
for _, row in profiles.iterrows():
    plt.text(row["inherited_burden_score"], row["future_freedom_score"], row["scenario_name"], fontsize=7)
plt.xlabel("Inherited Burden")
plt.ylabel("Future Freedom")
plt.title("Inherited Burden vs Future Freedom")
plt.tight_layout()
plt.savefig(OUTPUTS / "inherited_burden_vs_future_freedom.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["stewardship_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Stewardship Score")
plt.title("Long-Term Stewardship Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "long_term_stewardship_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["inherited_burden"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Inherited Burden")
plt.title("Inherited Burden Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "inherited_burden_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
