#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Hope, Dread, and the Politics of the Future.
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

profiles = pd.read_csv(DATA / "future_emotion_profiles.csv")
scenarios = pd.read_csv(DATA / "future_politics_scenarios.csv")
strategies = pd.read_csv(DATA / "future_emotion_strategy_options.csv")
risks = pd.read_csv(DATA / "future_emotion_risk_indicators.csv")
records = pd.read_csv(DATA / "future_emotion_records.csv")
pathways = pd.read_csv(DATA / "adaptive_future_emotion_pathways.csv")

profiles["mobilization_score"] = profiles["agency"] * (profiles["hope"] + 0.55 * profiles["dread"]) * profiles["trust"]
profiles["paralysis_risk_score"] = profiles["dread"] * (1 - profiles["agency"]) * (1 - profiles["trust"])
profiles["disciplined_hope_score"] = (
    0.18 * profiles["hope"]
    + 0.18 * profiles["agency"]
    + 0.16 * profiles["trust"]
    + 0.16 * profiles["institutional_capacity"]
    + 0.14 * profiles["narrative_accountability"]
    + 0.12 * profiles["repair_capacity"]
    - 0.04 * profiles["future_fatigue"]
    - 0.02 * profiles["polarization"]
)
profiles["fear_politics_risk_score"] = (
    0.24 * profiles["dread"]
    + 0.22 * profiles["polarization"]
    + 0.18 * (1 - profiles["trust"])
    + 0.16 * (1 - profiles["agency"])
    + 0.12 * profiles["future_fatigue"]
    + 0.08 * (1 - profiles["narrative_accountability"])
)

scenarios["future_politics_risk_score"] = (
    0.14 * scenarios["threat_intensity"]
    + 0.12 * (1 - scenarios["agency_pathways"])
    + 0.12 * (1 - scenarios["institutional_trust"])
    + 0.14 * scenarios["scapegoating_intensity"]
    + 0.12 * scenarios["false_reassurance"]
    + 0.12 * scenarios["crisis_fatigue"]
    + 0.09 * (1 - scenarios["narrative_accountability"])
    + 0.07 * (1 - scenarios["democratic_participation"])
    + 0.05 * (1 - scenarios["repair_orientation"])
    + 0.03 * (1 - scenarios["learning_capacity"])
)

strategies["future_emotion_strategy_value_score"] = (
    0.13 * strategies["agency_pathway_gain"]
    + 0.12 * strategies["trust_repair_gain"]
    + 0.13 * strategies["narrative_accountability_gain"]
    + 0.11 * strategies["participatory_foresight_gain"]
    + 0.11 * strategies["climate_truth_action_gain"]
    + 0.10 * strategies["youth_representation_gain"]
    + 0.08 * strategies["media_literacy_gain"]
    + 0.10 * strategies["repair_capacity_gain"]
    + 0.08 * strategies["fear_politics_resistance_gain"]
    + 0.02 * strategies["implementation_capacity"]
    + 0.02 * strategies["public_legitimacy_gain"]
)

risks["future_emotion_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.16 * risks["severity"]
    + 0.12 * risks["irreversibility"]
    + 0.12 * risks["visibility_gap"]
    + 0.16 * risks["distributional_harm"]
    + 0.20 * risks["democratic_harm"]
    + 0.10 * (1 - risks["preparedness"])
)

records["mobilization_score"] = records["agency"] * (records["hope"] + 0.55 * records["dread"]) * records["trust"]
records["paralysis_risk_score"] = records["dread"] * (1 - records["agency"]) * (1 - records["trust"])
records["disciplined_hope_score"] = (
    0.22 * records["hope"]
    + 0.22 * records["agency"]
    + 0.18 * records["trust"]
    + 0.18 * records["repair_capacity"]
    + 0.12 * records["narrative_accountability"]
    - 0.05 * records["future_fatigue"]
    - 0.03 * records["polarization"]
)
records["false_hope_risk_score"] = (records["hope"] - records["narrative_accountability"] - records["repair_capacity"]).clip(lower=0)

def simulate_pathway(row):
    hope = float(row["hope"])
    dread = float(row["dread"])
    agency = float(row["agency"])
    trust = float(row["trust"])
    fatigue = float(row["future_fatigue"])
    repair = float(row["repair_capacity"])
    polarization = float(row["polarization"])
    accountability = float(row["narrative_accountability"])
    horizon = int(row["time_horizon"])

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            crisis_spike = 0.018 if t % 8 == 0 else 0.0
            progress_signal = 0.015 if t % 10 == 0 else 0.0
            institutional_failure = 0.014 if t % 13 == 0 else 0.0
            backlash = 0.012 if t % 17 == 0 else 0.0

            dread = np.clip(dread + crisis_spike + 0.010 * fatigue + 0.006 * polarization - 0.010 * agency - 0.008 * trust, 0, 1.8)
            trust = np.clip(trust + progress_signal + 0.010 * repair + 0.006 * accountability - institutional_failure - 0.006 * fatigue, 0, 1.8)
            agency = np.clip(agency + 0.010 * trust + 0.012 * repair + progress_signal - 0.010 * fatigue - 0.006 * dread, 0, 1.8)
            fatigue = np.clip(fatigue + 0.010 * dread + institutional_failure - 0.012 * agency - 0.010 * trust, 0, 1.8)
            repair = np.clip(repair + 0.010 * agency + 0.008 * trust + progress_signal - 0.006 * fatigue, 0, 1.8)
            accountability = np.clip(accountability + 0.008 * trust + 0.008 * agency + progress_signal - 0.006 * institutional_failure, 0, 1.8)
            polarization = np.clip(polarization + backlash + 0.006 * dread - 0.010 * trust - 0.008 * accountability, 0, 1.8)
            hope = np.clip(hope + 0.012 * agency + 0.010 * trust + 0.010 * repair + 0.006 * accountability - 0.008 * fatigue - 0.004 * dread, 0, 1.8)

        mobilization = np.clip(agency * (hope + 0.55 * dread) * trust, 0, 2.5)
        paralysis = np.clip(dread * (1 - min(agency, 1)) * (1 - min(trust, 1)), 0, 1.8)
        disciplined = np.clip(0.22 * hope + 0.22 * agency + 0.18 * trust + 0.18 * repair + 0.12 * accountability - 0.05 * fatigue - 0.03 * polarization, -1, 1.8)
        fear = np.clip(0.24 * dread + 0.22 * polarization + 0.18 * (1 - min(trust, 1)) + 0.16 * (1 - min(agency, 1)) + 0.12 * fatigue + 0.08 * (1 - min(accountability, 1)), 0, 1.8)

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "hope": hope,
            "dread": dread,
            "agency": agency,
            "trust": trust,
            "future_fatigue": fatigue,
            "repair_capacity": repair,
            "polarization": polarization,
            "narrative_accountability": accountability,
            "mobilization_score": mobilization,
            "paralysis_risk_score": paralysis,
            "disciplined_hope_score": disciplined,
            "fear_politics_risk_score": fear,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_hope=("hope", "last"),
        final_dread=("dread", "last"),
        final_agency=("agency", "last"),
        final_trust=("trust", "last"),
        final_future_fatigue=("future_fatigue", "last"),
        final_mobilization_score=("mobilization_score", "last"),
        final_paralysis_risk_score=("paralysis_risk_score", "last"),
        final_disciplined_hope_score=("disciplined_hope_score", "last"),
        mean_disciplined_hope_score=("disciplined_hope_score", "mean"),
    )
    .reset_index()
    .sort_values("final_disciplined_hope_score", ascending=False)
)

profiles.sort_values("disciplined_hope_score", ascending=False).to_csv(OUTPUTS / "advanced_future_emotion_profile_scores.csv", index=False)
scenarios.sort_values("future_politics_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_future_politics_scenario_scores.csv", index=False)
strategies.sort_values("future_emotion_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_future_emotion_strategy_scores.csv", index=False)
risks.sort_values("future_emotion_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_future_emotion_risk_priority_scores.csv", index=False)
records.sort_values("disciplined_hope_score", ascending=False).to_csv(OUTPUTS / "advanced_future_emotion_record_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_future_emotion_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_future_emotion_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("disciplined_hope_score")
plt.barh(ranked["scenario_name"], ranked["disciplined_hope_score"])
plt.xlabel("Disciplined Hope Score")
plt.title(f"Disciplined Hope — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "disciplined_hope_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["fear_politics_risk_score"], profiles["disciplined_hope_score"])
for _, row in profiles.iterrows():
    plt.text(row["fear_politics_risk_score"], row["disciplined_hope_score"], row["scenario_name"], fontsize=7)
plt.xlabel("Fear-Politics Risk")
plt.ylabel("Disciplined Hope")
plt.title("Fear-Politics Risk vs Disciplined Hope")
plt.tight_layout()
plt.savefig(OUTPUTS / "fear_politics_vs_disciplined_hope.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["disciplined_hope_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Disciplined Hope Score")
plt.title("Disciplined Hope Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "disciplined_hope_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["paralysis_risk_score"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Paralysis Risk")
plt.title("Paralysis Risk Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "paralysis_risk_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
