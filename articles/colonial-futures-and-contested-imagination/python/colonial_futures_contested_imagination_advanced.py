#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Colonial Futures and Contested Imagination.
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

profiles = pd.read_csv(DATA / "colonial_future_profiles.csv")
scenarios = pd.read_csv(DATA / "colonial_future_scenarios.csv")
strategies = pd.read_csv(DATA / "reparative_strategy_options.csv")
risks = pd.read_csv(DATA / "coloniality_risk_indicators.csv")
records = pd.read_csv(DATA / "extraction_voice_records.csv")
pathways = pd.read_csv(DATA / "adaptive_colonial_future_pathways.csv")

profiles["coloniality_risk_score"] = (
    0.12 * profiles["agenda_setting_power"]
    + 0.12 * (1 - profiles["consent_quality"])
    + 0.12 * profiles["land_exposure"]
    + 0.12 * profiles["external_control"]
    + 0.11 * (1 - profiles["epistemic_justice"])
    + 0.10 * (1 - profiles["local_benefit"])
    + 0.10 * profiles["ecological_harm"]
    + 0.09 * (1 - profiles["reparative_capacity"])
    + 0.07 * (1 - profiles["sovereignty_recognition"])
    + 0.03 * (1 - profiles["data_sovereignty"])
    + 0.02 * (1 - profiles["labor_protection"])
)

profiles["reparative_future_score"] = (
    0.16 * profiles["consent_quality"]
    + 0.15 * profiles["epistemic_justice"]
    + 0.14 * profiles["local_benefit"]
    + 0.16 * profiles["reparative_capacity"]
    + 0.14 * profiles["sovereignty_recognition"]
    + 0.08 * profiles["data_sovereignty"]
    + 0.07 * profiles["labor_protection"]
    + 0.05 * (1 - profiles["external_control"])
    + 0.03 * (1 - profiles["land_exposure"])
    + 0.02 * (1 - profiles["ecological_harm"])
)

profiles["reparative_gap_score"] = (profiles["coloniality_risk_score"] - profiles["reparative_future_score"]).clip(lower=0)

scenarios["colonial_pressure_score"] = (
    0.14 * scenarios["extraction_pressure"]
    + 0.14 * scenarios["external_control_pressure"]
    + 0.13 * scenarios["consent_gap"]
    + 0.12 * scenarios["land_risk"]
    + 0.12 * scenarios["knowledge_erasure"]
    + 0.10 * scenarios["data_extraction"]
    + 0.09 * scenarios["security_drift"]
    + 0.08 * scenarios["ecological_harm"]
    + 0.05 * (1 - scenarios["reparative_opening"])
    + 0.03 * (1 - scenarios["community_voice"])
)

strategies["reparative_strategy_value_score"] = (
    0.13 * strategies["land_return_gain"]
    + 0.13 * strategies["consent_quality_gain"]
    + 0.12 * strategies["community_ownership_gain"]
    + 0.12 * strategies["epistemic_justice_gain"]
    + 0.10 * strategies["data_sovereignty_gain"]
    + 0.10 * strategies["labor_rights_gain"]
    + 0.10 * strategies["ecological_restoration_gain"]
    + 0.09 * strategies["reparative_finance_gain"]
    + 0.07 * strategies["accountability_gain"]
    + 0.02 * strategies["implementation_capacity"]
    + 0.02 * strategies["legitimacy_gain"]
)

risks["coloniality_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.17 * risks["severity"]
    + 0.15 * risks["irreversibility"]
    + 0.10 * risks["visibility_gap"]
    + 0.20 * risks["distributional_harm"]
    + 0.14 * risks["rights_risk"]
    + 0.10 * (1 - risks["preparedness"])
)

records["future_making_legitimacy_score"] = (
    0.18 * records["community_voice"]
    + 0.16 * records["local_benefit"]
    + 0.16 * records["reparative_capacity"]
    + 0.16 * records["consent_quality"]
    + 0.14 * records["sovereignty_recognition"]
    - 0.08 * records["extraction_burden"]
    - 0.07 * records["external_control"]
    - 0.05 * records["ecological_harm"]
)

records["reparative_gap_score"] = (
    records["extraction_burden"]
    + records["external_control"]
    + records["ecological_harm"]
    - records["local_benefit"]
    - records["reparative_capacity"]
    - records["consent_quality"]
).clip(lower=0)

def simulate_pathway(row):
    extraction = float(row["extraction_burden"])
    voice = float(row["community_voice"])
    external = float(row["external_control"])
    harm = float(row["ecological_harm"])
    benefit = float(row["local_benefit"])
    repair = float(row["reparative_capacity"])
    consent = float(row["consent_quality"])
    sovereignty = float(row["sovereignty_recognition"])
    horizon = int(row["time_horizon"])

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            extraction_push = 0.018 if t % 7 == 0 else 0.0
            resistance_cycle = 0.020 if t % 9 == 0 else 0.0
            repair_window = 0.018 if t % 11 == 0 else 0.0
            backlash = 0.010 if t % 13 == 0 else 0.0

            extraction = np.clip(extraction + extraction_push + 0.012 * external - 0.014 * voice - 0.012 * repair - 0.008 * consent, 0, 1.8)
            voice = np.clip(voice + resistance_cycle + 0.014 * repair + 0.010 * sovereignty - 0.010 * external - 0.006 * extraction - backlash, 0, 1.8)
            external = np.clip(external + 0.010 * extraction + backlash - 0.014 * voice - 0.010 * repair - 0.008 * sovereignty, 0, 1.8)
            harm = np.clip(harm + 0.012 * extraction + 0.006 * external - 0.014 * repair - 0.008 * consent, 0, 1.8)
            benefit = np.clip(benefit + 0.012 * voice + 0.010 * repair + repair_window - 0.006 * external, 0, 1.8)
            repair = np.clip(repair + 0.014 * voice + 0.010 * consent + 0.010 * sovereignty + repair_window - 0.008 * external - 0.006 * extraction, 0, 1.8)
            consent = np.clip(consent + 0.012 * voice + 0.008 * sovereignty + 0.006 * repair - 0.008 * external, 0, 1.8)
            sovereignty = np.clip(sovereignty + 0.010 * voice + 0.008 * consent + 0.008 * repair - 0.008 * external, 0, 1.8)

        legitimacy = np.clip(
            0.18 * voice + 0.16 * benefit + 0.16 * repair + 0.16 * consent + 0.14 * sovereignty
            - 0.08 * extraction - 0.07 * external - 0.05 * harm,
            -1,
            1.8,
        )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "extraction_burden": extraction,
            "community_voice": voice,
            "external_control": external,
            "ecological_harm": harm,
            "local_benefit": benefit,
            "reparative_capacity": repair,
            "consent_quality": consent,
            "sovereignty_recognition": sovereignty,
            "legitimacy": legitimacy,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_extraction_burden=("extraction_burden", "last"),
        final_community_voice=("community_voice", "last"),
        final_external_control=("external_control", "last"),
        final_ecological_harm=("ecological_harm", "last"),
        final_reparative_capacity=("reparative_capacity", "last"),
        final_legitimacy=("legitimacy", "last"),
        mean_legitimacy=("legitimacy", "mean"),
    )
    .reset_index()
    .sort_values("final_legitimacy", ascending=False)
)

profiles.sort_values("coloniality_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_colonial_future_profile_scores.csv", index=False)
scenarios.sort_values("colonial_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_colonial_future_scenario_scores.csv", index=False)
strategies.sort_values("reparative_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_reparative_strategy_scores.csv", index=False)
risks.sort_values("coloniality_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_coloniality_risk_priority_scores.csv", index=False)
records.sort_values("reparative_gap_score", ascending=False).to_csv(OUTPUTS / "advanced_extraction_voice_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_colonial_future_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_colonial_future_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("coloniality_risk_score")
plt.barh(ranked["future_name"], ranked["coloniality_risk_score"])
plt.xlabel("Coloniality Risk Score")
plt.title(f"Coloniality Risk — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "coloniality_risk_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["coloniality_risk_score"], profiles["reparative_future_score"])
for _, row in profiles.iterrows():
    plt.text(row["coloniality_risk_score"], row["reparative_future_score"], row["future_name"], fontsize=7)
plt.xlabel("Coloniality Risk")
plt.ylabel("Reparative Future Capacity")
plt.title("Coloniality Risk vs Reparative Future Capacity")
plt.tight_layout()
plt.savefig(OUTPUTS / "coloniality_risk_vs_reparative_capacity.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["legitimacy"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Legitimacy")
plt.title("Legitimacy Paths Across Colonial and Contested Futures")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "legitimacy_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["reparative_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Reparative Capacity")
plt.title("Reparative Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "reparative_capacity_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
