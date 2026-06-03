#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Early Warning Systems and Futures Intelligence.
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
indicators = pd.read_csv(DATA / "indicators.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
scenario_monitors = pd.read_csv(DATA / "scenario_monitors.csv")
interactions = pd.read_csv(DATA / "cross_system_interactions.csv")
protocols = pd.read_csv(DATA / "response_protocols.csv")

signals["warning_score"] = (
    0.12 * signals["novelty"]
    + 0.22 * signals["relevance"]
    + 0.20 * signals["urgency"]
    + 0.13 * signals["evidence_quality"]
    + 0.11 * signals["affected_voice"]
    + 0.13 * signals["vulnerability"]
    + 0.09 * signals["lead_time_value"]
)

def warning_level(score):
    if score >= 0.82:
        return "Escalate"
    if score >= 0.76:
        return "Watch closely"
    return "Monitor"

signals["warning_level"] = signals["warning_score"].apply(warning_level)

frequency = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
indicators["threshold_gap"] = indicators["current_value"] - indicators["threshold_value"]
indicators["threshold_breached"] = indicators["current_value"] >= indicators["threshold_value"]
indicators["positive_gap"] = indicators["threshold_gap"].clip(lower=0)
indicators["review_weight"] = indicators["review_frequency"].map(frequency).fillna(0.50)
indicators["trigger_priority_score"] = (
    0.45 * indicators["threshold_breached"].astype(float)
    + 0.25 * indicators["current_value"]
    + 0.20 * indicators["positive_gap"]
    + 0.10 * indicators["review_weight"]
)

assumptions["assumption_failure_risk"] = (
    0.45 * (1 - assumptions["confidence"])
    + 0.55 * assumptions["fragility"]
)

scenario_monitors["scenario_monitor_score"] = (
    scenario_monitors["scenario_relevance"] * scenario_monitors["monitoring_weight"]
)

interactions["cascade_warning_score"] = interactions["influence_weight"] * (
    0.40 + 0.25 * interactions["delay_risk"] + 0.35 * interactions["cascade_potential"]
)

protocols = protocols.merge(
    indicators[["response_protocol_id", "trigger_priority_score"]],
    on="response_protocol_id",
    how="left"
)
protocols["trigger_priority_score"] = protocols["trigger_priority_score"].fillna(0)
action_weight = {"escalate": 1.00, "pause": 0.96, "prepare": 0.72, "watch": 0.54}
protocols["action_weight"] = protocols["action_level"].map(action_weight).fillna(0.50)
protocols["public_required"] = (protocols["public_communication_required"].str.lower() == "yes").astype(float)
protocols["accountability_required"] = (protocols["accountability_review_required"].str.lower() == "yes").astype(float)
protocols["response_priority_score"] = (
    0.55 * protocols["trigger_priority_score"]
    + 0.20 * protocols["action_weight"]
    + 0.15 * protocols["public_required"]
    + 0.10 * protocols["accountability_required"]
)

signals.sort_values("warning_score", ascending=False).to_csv(OUTPUTS / "advanced_signal_warning_scores.csv", index=False)
indicators.sort_values("trigger_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_threshold_trigger_scores.csv", index=False)
assumptions.sort_values("assumption_failure_risk", ascending=False).to_csv(OUTPUTS / "advanced_assumption_failure_scores.csv", index=False)
scenario_monitors.sort_values("scenario_monitor_score", ascending=False).to_csv(OUTPUTS / "advanced_scenario_monitor_scores.csv", index=False)
interactions.sort_values("cascade_warning_score", ascending=False).to_csv(OUTPUTS / "advanced_cross_system_cascade_scores.csv", index=False)
protocols.sort_values("response_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_response_protocol_priorities.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = signals.sort_values("warning_score")
plt.barh(ranked["signal_name"], ranked["warning_score"])
plt.xlabel("Warning Score")
plt.title(f"Signal Warning Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_warning_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_indicators = indicators.sort_values("trigger_priority_score")
plt.barh(ranked_indicators["indicator_name"], ranked_indicators["trigger_priority_score"])
plt.xlabel("Trigger Priority")
plt.title("Threshold Trigger Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "threshold_trigger_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_assumptions = assumptions.sort_values("assumption_failure_risk")
plt.barh(ranked_assumptions["assumption_name"], ranked_assumptions["assumption_failure_risk"])
plt.xlabel("Assumption Failure Risk")
plt.title("Assumption Failure Risk Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "assumption_failure_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_cascades = interactions.sort_values("cascade_warning_score")
labels = ranked_cascades["source_domain"] + " → " + ranked_cascades["target_domain"]
plt.barh(labels, ranked_cascades["cascade_warning_score"])
plt.xlabel("Cascade Warning Score")
plt.title("Cross-System Cascade Warning Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "cross_system_cascade_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
