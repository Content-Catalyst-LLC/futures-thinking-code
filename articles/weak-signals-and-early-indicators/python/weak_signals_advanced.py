#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Weak Signals and Early Indicators.
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

signals = pd.read_csv(DATA / "weak_signals.csv")
indicators = pd.read_csv(DATA / "early_indicators.csv")
clusters = pd.read_csv(DATA / "signal_clusters.csv")
propagation = pd.read_csv(DATA / "propagation_pathways.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
watchlist = pd.read_csv(DATA / "watchlist.csv")

signals["weak_signal_profile"] = (
    0.10 * signals["visibility"]
    - 0.08 * signals["ambiguity"]
    + 0.24 * signals["systemic_connection"]
    + 0.22 * signals["propagation_potential"]
    + 0.12 * signals["institutional_recognition"]
    + 0.12 * signals["distributional_relevance"]
    + 0.20 * signals["monitoring_urgency"]
)

def classify(score):
    if score >= 0.72:
        return "High-priority watchlist"
    if score >= 0.62:
        return "Monitor and cluster"
    if score >= 0.54:
        return "Exploratory monitoring"
    return "Low-priority or background noise"

signals["priority_class"] = signals["weak_signal_profile"].apply(classify)

max_evidence = indicators["evidence_count"].max()
indicators["evidence_index"] = indicators["evidence_count"] / max_evidence
indicators["early_indicator_score"] = (
    0.25 * indicators["repetition_score"]
    + 0.25 * indicators["clarity_score"]
    + 0.20 * indicators["measurement_quality"]
    + 0.20 * indicators["policy_attention"]
    + 0.10 * indicators["evidence_index"]
)

clusters["cluster_priority"] = clusters["coherence"] * clusters["strategic_concern"]

propagation["propagation_strength"] = (
    0.25 * propagation["adoption"]
    + 0.25 * propagation["feedback"]
    + 0.20 * propagation["institutional_recognition"]
    + 0.15 * propagation["legitimacy"]
    - 0.20 * propagation["friction"]
)

assumptions["vulnerability_score"] = (
    assumptions["exposure"]
    * (1 - assumptions["confidence"])
    * (1 + (1 - assumptions["reversibility"]))
)

frequency_weight = {
    "monthly": 1.00,
    "quarterly": 0.88,
    "semiannual": 0.68,
    "annual": 0.48,
}
watchlist["frequency_weight"] = watchlist["review_frequency"].map(frequency_weight).fillna(0.50)
watchlist["watch_priority"] = 0.70 * watchlist["decision_linkage"] + 0.30 * watchlist["frequency_weight"]

signals = signals.sort_values("weak_signal_profile", ascending=False)
indicators = indicators.sort_values("early_indicator_score", ascending=False)
clusters = clusters.sort_values("cluster_priority", ascending=False)
propagation = propagation.sort_values("propagation_strength", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)
watchlist = watchlist.sort_values("watch_priority", ascending=False)

signals.to_csv(OUTPUTS / "advanced_weak_signal_profiles.csv", index=False)
indicators.to_csv(OUTPUTS / "advanced_early_indicator_scores.csv", index=False)
clusters.to_csv(OUTPUTS / "advanced_signal_cluster_priorities.csv", index=False)
propagation.to_csv(OUTPUTS / "advanced_propagation_pathway_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)
watchlist.to_csv(OUTPUTS / "advanced_watchlist_priorities.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(signals.head(10)["signal_title"], signals.head(10)["weak_signal_profile"])
plt.xlabel("Weak signal profile")
plt.title(f"Weak Signal Profiles — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "weak_signal_profiles.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(indicators["indicator_name"], indicators["early_indicator_score"])
plt.xlabel("Early indicator score")
plt.title("Early Indicator Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "early_indicator_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(clusters["cluster_name"], clusters["cluster_priority"])
plt.xlabel("Cluster priority")
plt.title("Signal Cluster Priorities")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_cluster_priorities.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(propagation["signal_id"], propagation["propagation_strength"])
plt.xlabel("Propagation strength")
plt.title("Propagation Pathway Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "propagation_pathway_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
