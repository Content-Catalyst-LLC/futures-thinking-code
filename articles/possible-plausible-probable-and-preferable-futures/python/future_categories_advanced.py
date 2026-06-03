#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for future-category classification.
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

futures = pd.read_csv(DATA / "candidate_futures.csv")
strategies = pd.read_csv(DATA / "strategies.csv")
shifts = pd.read_csv(DATA / "category_shifts.csv")

futures["plausibility_score"] = (
    0.40 * futures["driver_support"] +
    0.35 * futures["pathway_coherence"] +
    0.25 * futures["constraint_fit"]
)

futures["probability_score"] = (
    0.70 * futures["current_trend_strength"] +
    0.30 * futures["driver_support"]
)

futures["preference_score"] = (
    0.30 * futures["justice_value"] +
    0.25 * futures["sustainability_value"] +
    0.25 * futures["resilience_value"] +
    0.20 * futures["legitimacy_value"]
)

def classify(row):
    plausible = row["plausibility_score"] >= 0.65
    probable = row["probability_score"] >= 0.65
    preferable = row["preference_score"] >= 0.65
    if plausible and probable and preferable:
        return "Probable and Preferable"
    if plausible and probable and not preferable:
        return "Probable but Not Preferable"
    if plausible and not probable and preferable:
        return "Preferable but Not Yet Probable"
    if preferable and not plausible:
        return "Preferable but Needs Pathway"
    if plausible and not probable:
        return "Plausible Strategic Scenario"
    return "Possible or Emerging"

futures["classification"] = futures.apply(classify, axis=1)
futures["strategic_priority"] = (
    0.35 * futures["plausibility_score"] +
    0.25 * futures["probability_score"] +
    0.40 * futures["preference_score"]
)

strategies["category_fit_score"] = (
    0.20 * strategies["probable_fit"] +
    0.30 * strategies["plausible_fit"] +
    0.30 * strategies["preferable_fit"] +
    0.20 * strategies["adaptive_capacity"] -
    0.05 * strategies["implementation_difficulty"] +
    0.05 * strategies["equity_sensitivity"]
)

shifts["review_priority_score"] = shifts["shift_strength"] * shifts["monitoring_priority"].map({"high": 1.2, "medium": 1.0, "low": 0.8}).fillna(1.0)

futures = futures.sort_values("strategic_priority", ascending=False)
strategies = strategies.sort_values("category_fit_score", ascending=False)
shifts = shifts.sort_values("review_priority_score", ascending=False)

futures.to_csv(OUTPUTS / "advanced_future_category_classification.csv", index=False)
strategies.to_csv(OUTPUTS / "advanced_strategy_category_fit.csv", index=False)
shifts.to_csv(OUTPUTS / "advanced_category_shift_monitor.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(futures["future"], futures["strategic_priority"])
plt.xlabel("Strategic priority")
plt.title(f"Strategic Priority — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "future_strategic_priority.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(strategies["strategy"], strategies["category_fit_score"])
plt.xlabel("Category fit score")
plt.title("Strategy Fit Across Future Categories")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_category_fit.png", dpi=150)
plt.close()

score_long = futures.melt(
    id_vars=["future"],
    value_vars=["plausibility_score", "probability_score", "preference_score"],
    var_name="dimension",
    value_name="score"
)
score_long.to_csv(OUTPUTS / "future_category_scores_long.csv", index=False)

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
