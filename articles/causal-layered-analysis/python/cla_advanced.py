#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Causal Layered Analysis.
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

issues = pd.read_csv(DATA / "cla_issues.csv")
layers = pd.read_csv(DATA / "layer_codes.csv")
metaphors = pd.read_csv(DATA / "metaphor_map.csv")
reframes = pd.read_csv(DATA / "reframing_profiles.csv")
power = pd.read_csv(DATA / "power_audit.csv")
scenarios = pd.read_csv(DATA / "scenario_translation.csv")

issues["cla_depth_score"] = (
    0.10 * issues["litany_visibility"]
    + 0.18 * issues["systemic_explanation"]
    + 0.22 * issues["worldview_challenge"]
    + 0.20 * issues["myth_metaphor_depth"]
    + 0.16 * issues["reframing_potential"]
    + 0.08 * issues["power_sensitivity"]
    + 0.06 * issues["strategic_relevance"]
)

layers["layer_priority"] = layers["diagnostic_weight"] * layers["transformation_need"]
metaphors["metaphor_reframing_score"] = 0.60 * metaphors["metaphor_shift_score"] + 0.40 * metaphors["ethical_relevance"]

reframes["reframing_depth_score"] = (
    0.12 * reframes["litany_change"]
    + 0.20 * reframes["systemic_change"]
    + 0.22 * reframes["worldview_change"]
    + 0.22 * reframes["metaphor_change"]
    + 0.12 * reframes["power_awareness"]
    + 0.12 * reframes["strategic_coherence"]
)

power["power_legitimacy_score"] = (
    0.40 * power["power_risk"]
    + 0.30 * power["exclusion_risk"]
    + 0.30 * power["legitimacy_need"]
)

issues.sort_values("cla_depth_score", ascending=False).to_csv(OUTPUTS / "advanced_cla_issue_depth_scores.csv", index=False)
layers.sort_values("layer_priority", ascending=False).to_csv(OUTPUTS / "advanced_layer_transformation_priorities.csv", index=False)
metaphors.sort_values("metaphor_reframing_score", ascending=False).to_csv(OUTPUTS / "advanced_metaphor_reframing_scores.csv", index=False)
reframes.sort_values("reframing_depth_score", ascending=False).to_csv(OUTPUTS / "advanced_reframing_depth_scores.csv", index=False)
power.sort_values("power_legitimacy_score", ascending=False).to_csv(OUTPUTS / "advanced_power_legitimacy_audit_scores.csv", index=False)
scenarios.to_csv(OUTPUTS / "advanced_scenario_translation_register.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = issues.sort_values("cla_depth_score")
plt.barh(ranked["issue_title"], ranked["cla_depth_score"])
plt.xlabel("CLA depth score")
plt.title(f"CLA Issue Depth Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "cla_issue_depth_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
layer_summary = layers.groupby("layer_label")["layer_priority"].mean().sort_values()
plt.barh(layer_summary.index, layer_summary.values)
plt.xlabel("Average layer priority")
plt.title("Average Transformation Priority by CLA Layer")
plt.tight_layout()
plt.savefig(OUTPUTS / "layer_priority_summary.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_reframes = reframes.sort_values("reframing_depth_score")
plt.barh(ranked_reframes["new_metaphor"], ranked_reframes["reframing_depth_score"])
plt.xlabel("Reframing depth score")
plt.title("CLA Reframing Depth Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "reframing_depth_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_power = power.sort_values("power_legitimacy_score")
plt.barh(ranked_power["issue_id"], ranked_power["power_legitimacy_score"])
plt.xlabel("Power and legitimacy score")
plt.title("Power and Legitimacy Audit")
plt.tight_layout()
plt.savefig(OUTPUTS / "power_legitimacy_audit_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
