#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for AI and the Future of Decision-Making.
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
    import numpy as np
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

systems = pd.read_csv(DATA / "decision_system_profiles.csv")
governance = pd.read_csv(DATA / "governance_controls.csv")
risks = pd.read_csv(DATA / "risk_indicators.csv")
equity = pd.read_csv(DATA / "equity_harm_indicators.csv")
pathways = pd.read_csv(DATA / "pathway_parameters.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

systems["decision_system_profile_score"] = (
    0.16 * systems["human_judgment"]
    + 0.16 * systems["machine_inference"]
    + 0.16 * systems["coordination_quality"]
    + 0.12 * systems["transparency"]
    + 0.12 * systems["uncertainty_management"]
    + 0.12 * systems["accountability"]
    + 0.08 * systems["contestability"]
    + 0.08 * systems["equity_protection"]
)

systems["governance_profile_score"] = (
    0.22 * systems["transparency"]
    + 0.24 * systems["accountability"]
    + 0.24 * systems["contestability"]
    + 0.18 * systems["uncertainty_management"]
    + 0.12 * systems["equity_protection"]
)

systems["risk_profile_score"] = (
    0.26 * systems["automation_intensity"]
    + 0.20 * (1 - systems["accountability"])
    + 0.20 * (1 - systems["contestability"])
    + 0.18 * (1 - systems["transparency"])
    + 0.16 * (1 - systems["equity_protection"])
)

governance["governance_readiness_score"] = (
    0.16 * governance["documentation"]
    + 0.16 * governance["auditability"]
    + 0.14 * governance["explainability"]
    + 0.16 * governance["human_oversight"]
    + 0.14 * governance["appeal_rights"]
    + 0.12 * governance["monitoring_strength"]
    + 0.12 * governance["enforcement_capacity"]
)
governance["governance_gap_score"] = 1 - governance["governance_readiness_score"]

risks["risk_priority_score"] = (
    0.22 * risks["probability"]
    + 0.24 * risks["severity"]
    + 0.18 * risks["detection_difficulty"]
    + 0.18 * risks["governance_gap"]
    + 0.12 * risks["affected_population_exposure"]
    + 0.06 * (1 - risks["mitigation_capacity"])
)

equity["justice_capacity_score"] = (
    0.18 * equity["contestability"]
    + 0.18 * equity["voice"]
    + 0.20 * equity["protection"]
    + 0.18 * equity["repair_capacity"]
    + 0.14 * (1 - equity["error_burden"])
    + 0.12 * (1 - equity["vulnerability"])
)

equity["harm_risk_score"] = (
    0.25 * equity["error_burden"]
    + 0.22 * equity["exposure"]
    + 0.22 * equity["vulnerability"]
    + 0.16 * (1 - equity["contestability"])
    + 0.15 * (1 - equity["repair_capacity"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    decision_quality = float(row["initial_decision_quality"])
    uncertainty_pressure = 0.20
    harm_risk = 0.20
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            regime_shift = 0.16 if t % 9 == 0 else 0.06
            governance_buffer = 0.10 * row["governance"] + 0.08 * row["contestability"]
            performance_gain = (
                0.22 * row["human"]
                + 0.24 * row["machine"]
                + 0.26 * row["coordination"]
                + 0.16 * row["governance"]
                + 0.12 * row["contestability"]
            )
            automation_fragility = 0.10 * row["machine"] * (1 - row["governance"]) * (1 - row["contestability"])
            uncertainty_pressure = np.clip(uncertainty_pressure * 0.88 + regime_shift + automation_fragility, 0, 1.5)
            harm_risk = np.clip(
                0.35 * (1 - row["governance"])
                + 0.35 * (1 - row["contestability"])
                + 0.20 * automation_fragility
                + 0.10 * regime_shift,
                0,
                1.0,
            )
            decision_quality = np.clip(
                decision_quality - regime_shift - automation_fragility + performance_gain / 4 + governance_buffer / 3,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "system_id": row["system_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "decision_quality": decision_quality,
            "uncertainty_pressure": uncertainty_pressure,
            "harm_risk": harm_risk,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "system_id", "pathway_name"])
    .agg(
        final_decision_quality=("decision_quality", "last"),
        mean_decision_quality=("decision_quality", "mean"),
        max_uncertainty_pressure=("uncertainty_pressure", "max"),
        mean_harm_risk=("harm_risk", "mean")
    )
    .reset_index()
    .sort_values("final_decision_quality", ascending=False)
)

strategies["public_interest_decision_score"] = (
    0.12 * strategies["human_authority"]
    + 0.12 * strategies["machine_capability"]
    + 0.16 * strategies["coordination_design"]
    + 0.12 * strategies["transparency"]
    + 0.16 * strategies["accountability"]
    + 0.14 * strategies["contestability"]
    + 0.10 * strategies["equity_protection"]
    + 0.08 * strategies["uncertainty_stress_testing"]
)

strategies["governance_strength_score"] = (
    0.16 * strategies["transparency"]
    + 0.20 * strategies["accountability"]
    + 0.18 * strategies["contestability"]
    + 0.16 * strategies["equity_protection"]
    + 0.16 * strategies["uncertainty_stress_testing"]
    + 0.14 * strategies["coordination_design"]
)

systems.sort_values("decision_system_profile_score", ascending=False).to_csv(OUTPUTS / "advanced_decision_system_profile_scores.csv", index=False)
governance.sort_values("governance_gap_score", ascending=False).to_csv(OUTPUTS / "advanced_governance_readiness_scores.csv", index=False)
risks.sort_values("risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_priority_scores.csv", index=False)
equity.sort_values("harm_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_equity_harm_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_hybrid_decision_performance.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_hybrid_decision_summary.csv", index=False)
strategies.sort_values("public_interest_decision_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = systems.sort_values("decision_system_profile_score")
plt.barh(ranked["system_type"], ranked["decision_system_profile_score"])
plt.xlabel("Decision-System Profile Score")
plt.title(f"Decision-System Profile Scores — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "decision_system_profile_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_gaps = governance.sort_values("governance_gap_score")
plt.barh(ranked_gaps["control_name"], ranked_gaps["governance_gap_score"])
plt.xlabel("Governance Gap Score")
plt.title("AI Decision-System Governance Gaps")
plt.tight_layout()
plt.savefig(OUTPUTS / "governance_gap_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["decision_quality"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Decision Quality")
plt.title("Hybrid Decision Performance Under Uncertainty")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "hybrid_decision_quality_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["harm_risk"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Harm Risk")
plt.title("Decision-System Harm Risk Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "hybrid_decision_harm_risk_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
