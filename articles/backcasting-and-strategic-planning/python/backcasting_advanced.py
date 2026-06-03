#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Backcasting and Strategic Planning.
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

futures = pd.read_csv(DATA / "desired_futures.csv")
baselines = pd.read_csv(DATA / "current_baselines.csv")
pathways = pd.read_csv(DATA / "pathways.csv")
milestones = pd.read_csv(DATA / "milestones.csv")
constraints = pd.read_csv(DATA / "constraints.csv")
stress = pd.read_csv(DATA / "scenario_stress_tests.csv")
triggers = pd.read_csv(DATA / "monitoring_triggers.csv")

dimensions = [
    "decarbonization",
    "equity",
    "resilience",
    "institutional_capacity",
    "public_legitimacy",
    "ecological_integrity",
]

merged = futures.merge(baselines, on="future_id")
for dimension in dimensions:
    merged[f"{dimension}_gap"] = merged[dimension] - merged[f"current_{dimension}"]

merged["strategic_gap_score"] = merged[[f"{d}_gap" for d in dimensions]].mean(axis=1)

pathways["pathway_viability_score"] = (
    0.18 * pathways["feasibility"]
    - 0.16 * pathways["institutional_difficulty"]
    + 0.14 * pathways["transition_speed"]
    + 0.18 * pathways["stakeholder_alignment"]
    + 0.16 * pathways["resilience"]
    + 0.12 * pathways["justice"]
    + 0.14 * pathways["adaptability"]
    - 0.12 * pathways["political_friction"]
)

def classify(score):
    if score >= 0.55:
        return "Strong adaptive pathway"
    if score >= 0.45:
        return "Potential pathway with constraints"
    return "Fragile or high-risk pathway"

pathways["pathway_class"] = pathways["pathway_viability_score"].apply(classify)
milestones["milestone_risk_priority"] = milestones["risk_score"] * (1 - milestones["completion_score"])
constraints["constraint_priority"] = constraints["impact"] * constraints["severity"] * (1 + (1 - constraints["reversibility"]))

stress["stress_burden_score"] = (
    0.22 * stress["climate_stress"]
    + 0.20 * stress["political_resistance"]
    + 0.20 * stress["funding_constraint"]
    + 0.18 * stress["technology_uncertainty"]
    + 0.20 * (1 - stress["public_trust"])
)

frequency_weight = {
    "monthly": 1.00,
    "quarterly": 0.88,
    "semiannual": 0.68,
    "annual": 0.48,
}
triggers["frequency_weight"] = triggers["review_frequency"].map(frequency_weight).fillna(0.50)
triggers["trigger_priority"] = 0.60 * triggers["threshold"] + 0.40 * triggers["frequency_weight"]

merged = merged.sort_values("strategic_gap_score", ascending=False)
pathways = pathways.sort_values("pathway_viability_score", ascending=False)
milestones = milestones.sort_values("milestone_risk_priority", ascending=False)
constraints = constraints.sort_values("constraint_priority", ascending=False)
stress = stress.sort_values("stress_burden_score", ascending=False)
triggers = triggers.sort_values("trigger_priority", ascending=False)

merged.to_csv(OUTPUTS / "advanced_strategic_gap_scores.csv", index=False)
pathways.to_csv(OUTPUTS / "advanced_pathway_viability_scores.csv", index=False)
milestones.to_csv(OUTPUTS / "advanced_milestone_risk_priorities.csv", index=False)
constraints.to_csv(OUTPUTS / "advanced_constraint_priorities.csv", index=False)
stress.to_csv(OUTPUTS / "advanced_scenario_stress_burdens.csv", index=False)
triggers.to_csv(OUTPUTS / "advanced_monitoring_trigger_register.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(merged["future_name"], merged["strategic_gap_score"])
plt.xlabel("Strategic gap score")
plt.title(f"Strategic Gap Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategic_gap_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(pathways["pathway_name"], pathways["pathway_viability_score"])
plt.xlabel("Pathway viability score")
plt.title("Backcasting Pathway Viability")
plt.tight_layout()
plt.savefig(OUTPUTS / "pathway_viability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(milestones.head(10)["milestone_id"], milestones.head(10)["milestone_risk_priority"])
plt.xlabel("Milestone risk priority")
plt.title("Highest-Priority Milestone Risks")
plt.tight_layout()
plt.savefig(OUTPUTS / "milestone_risk_priorities.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(stress["stress_id"], stress["stress_burden_score"])
plt.xlabel("Stress burden score")
plt.title("Scenario Stress Burdens")
plt.tight_layout()
plt.savefig(OUTPUTS / "scenario_stress_burdens.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
