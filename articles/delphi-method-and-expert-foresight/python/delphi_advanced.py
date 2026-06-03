#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Delphi Method and Expert Foresight.
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

panel = pd.read_csv(DATA / "expert_panel.csv")
responses = pd.read_csv(DATA / "delphi_responses.csv")
issues = pd.read_csv(DATA / "issue_priorities.csv")
rationales = pd.read_csv(DATA / "qualitative_rationales.csv")
translations = pd.read_csv(DATA / "foresight_outputs.csv")

for col in ["formal_expert", "practice_expert", "community_expert", "ethics_expert"]:
    panel[col] = panel[col].astype(str).str.lower().eq("true").astype(float)

panel["panel_diversity_score"] = (
    panel[["formal_expert", "practice_expert", "community_expert", "ethics_expert"]].mean(axis=1)
    * panel["panel_weight"]
    * (1 - panel["blind_spot_risk"])
)

responses["uncertainty_range"] = responses["high_estimate"] - responses["low_estimate"]
responses["judgment_profile"] = (
    0.25 * responses["likelihood"]
    + 0.35 * responses["impact"]
    + 0.25 * responses["urgency"]
    + 0.15 * responses["feasibility"]
)

round_summary = (
    responses.groupby(["issue_id", "round"])
    .agg(
        respondent_count=("expert_id", "count"),
        median_judgment_profile=("judgment_profile", "median"),
        mean_judgment_profile=("judgment_profile", "mean"),
        std_judgment_profile=("judgment_profile", "std"),
        lower_quartile=("judgment_profile", lambda x: x.quantile(0.25)),
        upper_quartile=("judgment_profile", lambda x: x.quantile(0.75)),
        median_likelihood=("likelihood", "median"),
        median_impact=("impact", "median"),
        median_urgency=("urgency", "median"),
        mean_uncertainty_range=("uncertainty_range", "mean"),
    )
    .reset_index()
)

round_summary["interquartile_range"] = round_summary["upper_quartile"] - round_summary["lower_quartile"]
round_summary["stability_shift"] = (
    round_summary.sort_values(["issue_id", "round"])
    .groupby("issue_id")["median_judgment_profile"]
    .diff()
    .abs()
)

issues["priority_score"] = (
    0.25 * issues["likelihood"]
    + 0.30 * issues["impact"]
    + 0.20 * issues["urgency"]
    + 0.15 * issues["governance_relevance"]
    + 0.10 * issues["monitoring_need"]
)
issues["uncertainty_adjusted_priority"] = issues["priority_score"] * (1 + 0.20 * issues["uncertainty"])

rationale_counts = (
    responses["rationale_code"]
    .value_counts()
    .rename_axis("rationale_code")
    .reset_index(name="response_count")
    .merge(rationales, on="rationale_code", how="left")
)

panel.sort_values("panel_diversity_score", ascending=False).to_csv(OUTPUTS / "advanced_panel_diversity_audit.csv", index=False)
responses.to_csv(OUTPUTS / "advanced_expert_judgment_profiles.csv", index=False)
round_summary.to_csv(OUTPUTS / "advanced_delphi_round_metrics.csv", index=False)
issues.sort_values("uncertainty_adjusted_priority", ascending=False).to_csv(OUTPUTS / "advanced_issue_priority_scores.csv", index=False)
rationale_counts.to_csv(OUTPUTS / "advanced_rationale_theme_summary.csv", index=False)
translations.to_csv(OUTPUTS / "advanced_foresight_translation_register.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(panel.sort_values("panel_diversity_score")["expert_id"], panel.sort_values("panel_diversity_score")["panel_diversity_score"])
plt.xlabel("Panel diversity score")
plt.title(f"Panel Diversity Audit — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "panel_diversity_audit.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for expert_id in responses["expert_id"].unique():
    subset = responses[responses["expert_id"] == expert_id].sort_values("round")
    plt.plot(subset["round"], subset["judgment_profile"], marker="o", linewidth=1, alpha=0.6)
plt.xlabel("Round")
plt.ylabel("Judgment profile")
plt.title("Expert Judgment Profiles Across Delphi Rounds")
plt.tight_layout()
plt.savefig(OUTPUTS / "expert_judgment_profiles_by_round.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(round_summary["round"], round_summary["interquartile_range"], marker="o", linewidth=1.8)
plt.xlabel("Round")
plt.ylabel("Interquartile range")
plt.title("Delphi Dispersion Across Rounds")
plt.tight_layout()
plt.savefig(OUTPUTS / "delphi_dispersion_by_round.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_issues = issues.sort_values("uncertainty_adjusted_priority")
plt.barh(ranked_issues["issue_title"], ranked_issues["uncertainty_adjusted_priority"])
plt.xlabel("Uncertainty-adjusted priority")
plt.title("Delphi Issue Priority Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "issue_priority_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
