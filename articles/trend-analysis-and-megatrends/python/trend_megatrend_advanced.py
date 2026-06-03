#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Trend Analysis and Megatrends.
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

trends = pd.read_csv(DATA / "trend_profiles.csv")
interactions = pd.read_csv(DATA / "megatrend_interactions.csv")
signals = pd.read_csv(DATA / "signals.csv")
indicators = pd.read_csv(DATA / "indicators.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
strategy = pd.read_csv(DATA / "strategy_implications.csv")

trends["long_term_change_profile"] = (
    0.20 * trends["momentum"] +
    0.22 * trends["structural_depth"] +
    0.22 * trends["cross_system_influence"] -
    0.12 * trends["reversibility"] -
    0.14 * trends["uncertainty"] +
    0.10 * trends["distributional_sensitivity"]
)

def classify(score):
    if score >= 0.55:
        return "Megatrend-level structural force"
    if score >= 0.48:
        return "Megatrend candidate"
    if score >= 0.42:
        return "Established strategic trend"
    return "Emerging or domain-specific trend"

trends["classification"] = trends["long_term_change_profile"].apply(classify)
interactions["interaction_priority"] = interactions["interaction_strength"] * interactions["systemic_risk"]
signals["watch_score"] = 0.35 * signals["uncertainty"] + 0.40 * signals["impact"] + 0.25 * signals["novelty"]
indicators["movement_score"] = (indicators["current_value"] - indicators["baseline_value"]) * indicators["confidence"]
assumptions["vulnerability_score"] = assumptions["exposure"] * (1 - assumptions["confidence"]) * (1 + (1 - assumptions["reversibility"]))

frequency_weight = {
    "monthly": 1.00,
    "quarterly": 0.88,
    "semiannual": 0.68,
    "annual": 0.48,
}
strategy["frequency_weight"] = strategy["review_frequency"].map(frequency_weight).fillna(0.50)
strategy["translation_priority"] = 0.70 * strategy["decision_linkage"] + 0.30 * strategy["frequency_weight"]

trends = trends.sort_values("long_term_change_profile", ascending=False)
interactions = interactions.sort_values("interaction_priority", ascending=False)
signals = signals.sort_values("watch_score", ascending=False)
indicators = indicators.sort_values("movement_score", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)
strategy = strategy.sort_values("translation_priority", ascending=False)

trends.to_csv(OUTPUTS / "advanced_trend_megatrend_profiles.csv", index=False)
interactions.to_csv(OUTPUTS / "advanced_megatrend_interaction_priorities.csv", index=False)
signals.to_csv(OUTPUTS / "advanced_signal_watch_scores.csv", index=False)
indicators.to_csv(OUTPUTS / "advanced_indicator_movement_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)
strategy.to_csv(OUTPUTS / "advanced_strategy_translation_priorities.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(trends["pattern_type"], trends["long_term_change_profile"])
plt.xlabel("Long-term change profile")
plt.title(f"Trend and Megatrend Profiles — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "trend_megatrend_profiles.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(interactions.head(8)["interaction_id"], interactions.head(8)["interaction_priority"])
plt.xlabel("Interaction priority")
plt.title("Megatrend Interaction Priorities")
plt.tight_layout()
plt.savefig(OUTPUTS / "megatrend_interaction_priorities.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(signals.head(8)["signal_id"], signals.head(8)["watch_score"])
plt.xlabel("Watch score")
plt.title("Trend Signal Watch Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_watch_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(assumptions.head(7)["assumption_id"], assumptions.head(7)["vulnerability_score"])
plt.xlabel("Vulnerability score")
plt.title("Trend Interpretation Assumption Vulnerability")
plt.tight_layout()
plt.savefig(OUTPUTS / "assumption_vulnerability_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
