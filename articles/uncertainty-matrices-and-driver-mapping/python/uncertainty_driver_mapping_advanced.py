#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Uncertainty Matrices and Driver Mapping.
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

drivers = pd.read_csv(DATA / "driver_register.csv")
interactions = pd.read_csv(DATA / "driver_interactions.csv")
signals = pd.read_csv(DATA / "signals.csv")
monitoring = pd.read_csv(DATA / "monitoring_indicators.csv")
assumptions = pd.read_csv(DATA / "assumption_register.csv")

drivers["driver_priority_score"] = (
    0.22 * drivers["impact"]
    + 0.20 * drivers["uncertainty"]
    + 0.14 * drivers["urgency"]
    + 0.14 * drivers["interaction_strength"]
    + 0.12 * drivers["distributional_burden"]
    + 0.08 * drivers["monitoring_feasibility"]
    + 0.06 * drivers["evidence_strength"]
    + 0.04 * (1 - drivers["controllability"])
)

def classify(row):
    if row["impact"] >= 0.80 and row["uncertainty"] >= 0.72:
        return "Critical uncertainty"
    if row["impact"] >= 0.80 and row["uncertainty"] < 0.72:
        return "Baseline structural driver"
    if row["impact"] < 0.80 and row["uncertainty"] >= 0.72:
        return "Watchlist uncertainty"
    return "Lower-priority factor"

drivers["matrix_quadrant"] = drivers.apply(classify, axis=1)
drivers["axis_suitability_score"] = (
    drivers["impact"]
    * drivers["uncertainty"]
    * drivers["interaction_strength"]
    * drivers["monitoring_feasibility"]
    * drivers["evidence_strength"]
)

interactions["interaction_priority_score"] = interactions["influence_weight"] * (
    0.45 + 0.25 * interactions["delay_risk"] + 0.30 * interactions["cascade_potential"]
)

outgoing = interactions.groupby("source_driver_id")["influence_weight"].sum().rename("outgoing_influence")
incoming = interactions.groupby("target_driver_id")["influence_weight"].sum().rename("incoming_influence")
cross_impact = (
    pd.concat([outgoing, incoming], axis=1)
    .fillna(0)
    .reset_index()
    .rename(columns={"index": "driver_id"})
)
cross_impact["total_cross_impact"] = cross_impact["outgoing_influence"] + cross_impact["incoming_influence"]

axis_candidates = (
    drivers[drivers["matrix_quadrant"] == "Critical uncertainty"]
    .sort_values(["axis_suitability_score", "driver_priority_score"], ascending=False)
    .copy()
)
axis_candidates["axis_rank"] = range(1, len(axis_candidates) + 1)

signals["signal_priority_score"] = (
    0.15 * signals["novelty"]
    + 0.30 * signals["relevance"]
    + 0.25 * signals["urgency"]
    + 0.15 * signals["evidence_quality"]
    + 0.15 * signals["affected_voice"]
)

frequency = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
monitoring = monitoring.merge(
    drivers[["driver_id", "uncertainty", "urgency", "distributional_burden", "monitoring_feasibility"]],
    on="driver_id",
    how="left"
)
monitoring["monitoring_gap"] = (monitoring["threshold"] - monitoring["baseline"]).abs()
monitoring["review_weight"] = monitoring["review_frequency"].map(frequency).fillna(0.50)
monitoring["monitoring_priority_score"] = (
    0.30 * monitoring["uncertainty"]
    + 0.20 * monitoring["urgency"]
    + 0.18 * monitoring["distributional_burden"]
    + 0.17 * monitoring["monitoring_gap"]
    + 0.15 * monitoring["review_weight"]
)

assumptions["assumption_failure_risk"] = (
    (1 - assumptions["confidence"]) * 0.45 + assumptions["fragility"] * 0.55
)

drivers.sort_values("driver_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_driver_priority_scores.csv", index=False)
interactions.sort_values("interaction_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_driver_interaction_scores.csv", index=False)
cross_impact.sort_values("total_cross_impact", ascending=False).to_csv(OUTPUTS / "advanced_driver_cross_impact_scores.csv", index=False)
axis_candidates.to_csv(OUTPUTS / "advanced_scenario_axis_candidates.csv", index=False)
signals.sort_values("signal_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_signal_priority_scores.csv", index=False)
monitoring.sort_values("monitoring_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_monitoring_priority_scores.csv", index=False)
assumptions.sort_values("assumption_failure_risk", ascending=False).to_csv(OUTPUTS / "advanced_assumption_fragility_scores.csv", index=False)

plt.figure(figsize=(9, 6))
plt.scatter(drivers["uncertainty"], drivers["impact"])
for _, row in drivers.iterrows():
    plt.annotate(row["driver_id"], (row["uncertainty"], row["impact"]))
plt.axvline(0.72, linestyle="--")
plt.axhline(0.80, linestyle="--")
plt.xlabel("Uncertainty")
plt.ylabel("Impact")
plt.title(f"Impact-Uncertainty Matrix — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "impact_uncertainty_matrix.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked = drivers.sort_values("driver_priority_score")
plt.barh(ranked["driver_name"], ranked["driver_priority_score"])
plt.xlabel("Driver Priority")
plt.title("Driver Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_priority_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_cross = cross_impact.sort_values("total_cross_impact")
plt.barh(ranked_cross["driver_id"], ranked_cross["total_cross_impact"])
plt.xlabel("Total Cross-Impact")
plt.title("Driver Cross-Impact Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_cross_impact_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
