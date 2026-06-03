#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Horizon Scanning.
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

signals = pd.read_csv(DATA / "signals.csv")
sources = pd.read_csv(DATA / "sources.csv")
clusters = pd.read_csv(DATA / "signal_clusters.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
watchlist = pd.read_csv(DATA / "watchlist.csv")
institutions = pd.read_csv(DATA / "institutional_profiles.csv")

signals["horizon_scanning_profile"] = (
    0.10 * signals["visibility"]
    - 0.08 * signals["ambiguity"]
    + 0.22 * signals["structural_connection"]
    + 0.18 * signals["domain_diversity"]
    + 0.14 * signals["source_diversity"]
    + 0.14 * signals["assumption_challenge"]
    + 0.30 * signals["strategic_relevance"]
)

def classify(score):
    if score >= 0.72:
        return "High-priority watchlist"
    if score >= 0.62:
        return "Monitor and cluster"
    if score >= 0.54:
        return "Exploratory monitoring"
    return "Low-priority or background noise"

signals["priority_class"] = signals["horizon_scanning_profile"].apply(classify)

for col in ["elite_source", "community_source", "scientific_source", "policy_source", "cultural_source"]:
    sources[col] = sources[col].astype(str).str.lower().eq("true").astype(float)

sources["source_value_score"] = (
    sources["reliability"] * (1 - sources["blind_spot_risk"])
    + 0.20 * sources["community_source"]
    + 0.10 * sources["scientific_source"]
    + 0.10 * sources["policy_source"]
    + 0.08 * sources["cultural_source"]
    - 0.08 * sources["elite_source"] * sources["blind_spot_risk"]
)

clusters["cluster_priority"] = clusters["coherence"] * clusters["strategic_concern"]

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
watchlist["frequency_weight"] = watchlist["review_frequency"].map(frequency_weight).fillna(0.50)
watchlist["watch_priority"] = 0.70 * watchlist["decision_linkage"] + 0.30 * watchlist["frequency_weight"]

institutions["scanning_effectiveness_score"] = (
    0.20 * institutions["signal_strength"]
    - 0.16 * institutions["ambiguity"]
    + 0.24 * institutions["filtering_quality"]
    + 0.22 * institutions["source_diversity"]
    + 0.22 * institutions["institutional_uptake"]
    - 0.16 * institutions["resistance"]
)

signals = signals.sort_values("horizon_scanning_profile", ascending=False)
sources = sources.sort_values("source_value_score", ascending=False)
clusters = clusters.sort_values("cluster_priority", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)
watchlist = watchlist.sort_values("watch_priority", ascending=False)
institutions = institutions.sort_values("scanning_effectiveness_score", ascending=False)

signals.to_csv(OUTPUTS / "advanced_horizon_signal_profiles.csv", index=False)
sources.to_csv(OUTPUTS / "advanced_source_diversity_audit.csv", index=False)
clusters.to_csv(OUTPUTS / "advanced_signal_cluster_priorities.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)
watchlist.to_csv(OUTPUTS / "advanced_watchlist_priorities.csv", index=False)
institutions.to_csv(OUTPUTS / "advanced_institutional_scanning_effectiveness.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(signals.head(10)["signal_title"], signals.head(10)["horizon_scanning_profile"])
plt.xlabel("Horizon scanning profile")
plt.title(f"Signal Profiles — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "horizon_signal_profiles.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(sources["source_name"], sources["source_value_score"])
plt.xlabel("Source value score")
plt.title("Source Diversity Audit")
plt.tight_layout()
plt.savefig(OUTPUTS / "source_diversity_audit.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(clusters["cluster_name"], clusters["cluster_priority"])
plt.xlabel("Cluster priority")
plt.title("Signal Cluster Priorities")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_cluster_priorities.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(institutions["profile_name"], institutions["scanning_effectiveness_score"])
plt.xlabel("Scanning effectiveness score")
plt.title("Institutional Scanning Effectiveness")
plt.tight_layout()
plt.savefig(OUTPUTS / "institutional_scanning_effectiveness.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
