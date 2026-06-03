#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Strategic Foresight Methods.
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

methods = pd.read_csv(DATA / "foresight_methods.csv")
pipelines = pd.read_csv(DATA / "pipeline_profiles.csv")
signals = pd.read_csv(DATA / "signals.csv")
drivers = pd.read_csv(DATA / "drivers_uncertainties.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
translation = pd.read_csv(DATA / "strategy_translation.csv")

methods["method_profile_score"] = (
    0.16 * methods["detection_power"] +
    0.14 * methods["ambiguity_tolerance"] +
    0.16 * methods["structural_depth"] +
    0.18 * methods["actionability"] +
    0.14 * methods["participatory_depth"] +
    0.10 * methods["institutional_fit"] +
    0.12 * methods["learning_value"]
)

methods["method_risk_score"] = (
    methods["technocratic_risk"] *
    (1 - methods["participatory_depth"]) *
    (1 - methods["learning_value"])
)

pipelines["method_gain"] = (
    0.14 * pipelines["detection"] +
    0.15 * pipelines["interpretation"] +
    0.14 * pipelines["pattern_formation"] +
    0.16 * pipelines["uncertainty_structuring"] +
    0.16 * pipelines["strategic_design"] +
    0.12 * pipelines["legitimacy"] +
    0.13 * pipelines["uptake"]
)

pipelines["actionable_foresight_score"] = (
    pipelines["method_gain"] +
    0.15 * pipelines["legitimacy"] +
    0.15 * pipelines["uptake"] -
    0.20 * pipelines["resistance"]
)

signals["watch_score"] = (
    0.35 * signals["uncertainty"] +
    0.40 * signals["impact"] +
    0.25 * signals["novelty"]
)

drivers["criticality_score"] = (
    drivers["uncertainty"] *
    drivers["impact"] *
    drivers["velocity"]
)

assumptions["vulnerability_score"] = (
    assumptions["exposure"] *
    (1 - assumptions["confidence"]) *
    (1 + (1 - assumptions["reversibility"]))
)

frequency_weight = {
    "monthly": 1.00,
    "quarterly": 0.88,
    "semiannual": 0.68,
    "annual": 0.48,
}
translation["frequency_weight"] = translation["review_frequency"].map(frequency_weight).fillna(0.50)
translation["translation_priority"] = (
    0.70 * translation["decision_linkage"] +
    0.30 * translation["frequency_weight"]
)

methods = methods.sort_values("method_profile_score", ascending=False)
pipelines = pipelines.sort_values("actionable_foresight_score", ascending=False)
signals = signals.sort_values("watch_score", ascending=False)
drivers = drivers.sort_values("criticality_score", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)
translation = translation.sort_values("translation_priority", ascending=False)

methods.to_csv(OUTPUTS / "advanced_foresight_method_profiles.csv", index=False)
pipelines.to_csv(OUTPUTS / "advanced_pipeline_actionable_foresight_scores.csv", index=False)
signals.to_csv(OUTPUTS / "advanced_signal_watch_scores.csv", index=False)
drivers.to_csv(OUTPUTS / "advanced_driver_uncertainty_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)
translation.to_csv(OUTPUTS / "advanced_strategy_translation_index.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(methods["method"], methods["method_profile_score"])
plt.xlabel("Method profile score")
plt.title(f"Foresight Method Profiles — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "foresight_method_profiles.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(pipelines["pipeline_name"], pipelines["actionable_foresight_score"])
plt.xlabel("Actionable foresight score")
plt.title("Institutional Foresight Pipeline Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "pipeline_actionable_foresight_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(signals.head(8)["signal_id"], signals.head(8)["watch_score"])
plt.xlabel("Signal watch score")
plt.title("Signal Watch Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_watch_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(drivers.head(8)["driver_or_uncertainty"], drivers.head(8)["criticality_score"])
plt.xlabel("Criticality score")
plt.title("Driver and Critical Uncertainty Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "driver_uncertainty_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
