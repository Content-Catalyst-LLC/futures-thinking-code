#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Wheel and Impact Mapping.
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

consequences = pd.read_csv(DATA / "consequence_nodes.csv")
edges = pd.read_csv(DATA / "consequence_edges.csv")
actors = pd.read_csv(DATA / "actors.csv")
pathways = pd.read_csv(DATA / "impact_pathways.csv")
interventions = pd.read_csv(DATA / "interventions.csv")
monitoring = pd.read_csv(DATA / "monitoring_indicators.csv")
distribution = pd.read_csv(DATA / "distributional_audit.csv")

consequences["priority_score"] = (
    0.22 * consequences["likelihood"]
    + 0.26 * consequences["severity"]
    + 0.14 * consequences["uncertainty"]
    + 0.22 * consequences["distributional_burden"]
    + 0.16 * consequences["actionability"]
)

edges["edge_priority"] = edges["influence_strength"] * (1 + edges["feedback_potential"])

actors["actor_leverage_score"] = (
    0.30 * actors["decision_power"]
    + 0.25 * actors["implementation_role"]
    + 0.20 * actors["affectedness"]
    + 0.25 * actors["knowledge_value"]
)

pathways["impact_pathway_score"] = (
    0.40 * pathways["traceability_score"]
    + 0.30 * pathways["equity_relevance"]
    + 0.30 * pathways["implementation_feasibility"]
)

interventions["intervention_usefulness_score"] = (
    0.40 * interventions["risk_reduction"]
    + 0.25 * interventions["time_to_impact"]
    + 0.20 * (1 - interventions["cost_complexity"])
    + 0.15 * (1 - interventions["institutional_dependency"])
)

frequency_weight = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
monitoring["monitoring_gap"] = (monitoring["target"] - monitoring["baseline"]).abs()
monitoring["review_weight"] = monitoring["review_frequency"].map(frequency_weight).fillna(0.50)
monitoring["monitoring_priority"] = 0.70 * monitoring["monitoring_gap"] + 0.30 * monitoring["review_weight"]

distribution["distributional_risk_score"] = (
    0.35 * distribution["exposure"]
    + 0.30 * (1 - distribution["adaptive_capacity"])
    + 0.20 * (1 - distribution["decision_voice"])
    + 0.15 * distribution["burden_shift_risk"]
)

consequences.sort_values("priority_score", ascending=False).to_csv(OUTPUTS / "advanced_consequence_priority_scores.csv", index=False)
edges.sort_values("edge_priority", ascending=False).to_csv(OUTPUTS / "advanced_edge_influence_scores.csv", index=False)
actors.sort_values("actor_leverage_score", ascending=False).to_csv(OUTPUTS / "advanced_actor_leverage_scores.csv", index=False)
pathways.sort_values("impact_pathway_score", ascending=False).to_csv(OUTPUTS / "advanced_impact_pathway_scores.csv", index=False)
interventions.sort_values("intervention_usefulness_score", ascending=False).to_csv(OUTPUTS / "advanced_intervention_usefulness_scores.csv", index=False)
monitoring.sort_values("monitoring_priority", ascending=False).to_csv(OUTPUTS / "advanced_monitoring_gap_scores.csv", index=False)
distribution.sort_values("distributional_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_distributional_risk_scores.csv", index=False)

plot_consequences = consequences[consequences["consequence_order"] > 0].sort_values("priority_score").tail(12)
plt.figure(figsize=(10, 6))
plt.barh(plot_consequences["consequence"], plot_consequences["priority_score"])
plt.xlabel("Priority score")
plt.title(f"Futures Wheel Consequence Priorities — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "consequence_priority_scores.png", dpi=150)
plt.close()

domain_summary = consequences[consequences["consequence_order"] > 0].groupby("domain")["priority_score"].mean().sort_values()
plt.figure(figsize=(10, 6))
plt.barh(domain_summary.index, domain_summary.values)
plt.xlabel("Mean priority score")
plt.title("Consequence Priority by Domain")
plt.tight_layout()
plt.savefig(OUTPUTS / "consequence_domain_summary.png", dpi=150)
plt.close()

ranked_pathways = pathways.sort_values("impact_pathway_score")
plt.figure(figsize=(10, 6))
plt.barh(ranked_pathways["pathway_id"], ranked_pathways["impact_pathway_score"])
plt.xlabel("Impact pathway score")
plt.title("Impact Pathway Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "impact_pathway_scores.png", dpi=150)
plt.close()

ranked_distribution = distribution.sort_values("distributional_risk_score")
plt.figure(figsize=(10, 6))
plt.barh(ranked_distribution["affected_group"] + " / " + ranked_distribution["node_id"], ranked_distribution["distributional_risk_score"])
plt.xlabel("Distributional risk score")
plt.title("Distributional Risk Audit")
plt.tight_layout()
plt.savefig(OUTPUTS / "distributional_risk_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
