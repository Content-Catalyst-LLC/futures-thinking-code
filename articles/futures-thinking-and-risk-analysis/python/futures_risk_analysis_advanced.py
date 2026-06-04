#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Thinking and Risk Analysis.
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

profiles = pd.read_csv(DATA / "risk_profiles.csv")
scenarios = pd.read_csv(DATA / "risk_scenarios.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")
indicators = pd.read_csv(DATA / "risk_indicators.csv")
governance = pd.read_csv(DATA / "governance_records.csv")
pathways = pd.read_csv(DATA / "adaptive_pathways.csv")

profiles["futures_risk_profile_score"] = (
    0.12 * (1 - profiles["probability_confidence"])
    + 0.16 * profiles["structural_uncertainty"]
    + 0.14 * profiles["interdependence"]
    + 0.15 * profiles["vulnerability"]
    - 0.11 * profiles["resilience_capacity"]
    - 0.10 * profiles["governance_capacity"]
    - 0.08 * profiles["signal_visibility"]
    + 0.12 * profiles["tail_risk_severity"]
    + 0.10 * profiles["distributional_harm"]
    - 0.02 * profiles["adaptive_capacity"]
)

profiles["preparedness_gap_score"] = (
    0.18 * (1 - profiles["resilience_capacity"])
    + 0.18 * (1 - profiles["governance_capacity"])
    + 0.15 * (1 - profiles["signal_visibility"])
    + 0.15 * profiles["structural_uncertainty"]
    + 0.12 * profiles["vulnerability"]
    + 0.10 * profiles["tail_risk_severity"]
    + 0.08 * profiles["distributional_harm"]
    + 0.04 * (1 - profiles["adaptive_capacity"])
)

scenarios["systemic_risk_stress_score"] = (
    0.12 * scenarios["model_uncertainty"]
    + 0.09 * scenarios["data_uncertainty"]
    + 0.13 * scenarios["nonstationarity"]
    + 0.15 * scenarios["cascade_potential"]
    + 0.12 * scenarios["tail_risk_pressure"]
    + 0.10 * scenarios["exposure_pressure"]
    + 0.10 * scenarios["vulnerability_pressure"]
    + 0.08 * scenarios["governance_stress"]
    + 0.06 * scenarios["legitimacy_stress"]
    + 0.05 * scenarios["early_warning_gap"]
)

performance_fields = [
    "baseline_performance",
    "technology_disruption_performance",
    "climate_stress_performance",
    "geopolitical_fragmentation_performance",
    "financial_contagion_performance",
    "institutional_breakdown_performance",
    "systemic_cascade_performance",
]

performance_labels = [
    "Stable Baseline",
    "Technological Disruption",
    "Climate Stress",
    "Geopolitical Fragmentation",
    "Financial Contagion",
    "Institutional Breakdown",
    "Systemic Cascade",
]

performance_rows = []
for _, row in strategies.iterrows():
    for label, field in zip(performance_labels, performance_fields):
        performance_rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "scenario": label,
            "performance": row[field],
        })

strategy_perf = pd.DataFrame(performance_rows)
scenario_best = strategy_perf.groupby("scenario")["performance"].max().rename("scenario_best").reset_index()
strategy_perf = strategy_perf.merge(scenario_best, on="scenario")
strategy_perf["regret"] = strategy_perf["scenario_best"] - strategy_perf["performance"]

strategy_summary = (
    strategy_perf.groupby(["strategy_id", "strategy_name"])
    .agg(
        mean_performance=("performance", "mean"),
        worst_case=("performance", "min"),
        best_case=("performance", "max"),
        maximum_regret=("regret", "max"),
        mean_regret=("regret", "mean")
    )
    .reset_index()
)

strategy_meta = strategies[["strategy_id", "profile_id", "strategy_type", "monitoring_capacity", "adaptability", "implementation_capacity", "public_legitimacy", "description"]].copy()
strategy_summary = strategy_summary.merge(strategy_meta, on="strategy_id")

strategy_summary["governance_quality"] = (
    0.30 * strategy_summary["monitoring_capacity"]
    + 0.30 * strategy_summary["adaptability"]
    + 0.20 * strategy_summary["implementation_capacity"]
    + 0.20 * strategy_summary["public_legitimacy"]
)

strategy_summary["robustness_score"] = (
    0.42 * strategy_summary["worst_case"]
    + 0.28 * strategy_summary["mean_performance"]
    - 0.20 * strategy_summary["maximum_regret"]
    + 0.10 * strategy_summary["governance_quality"]
)

indicators["risk_indicator_priority_score"] = (
    0.13 * indicators["signal_strength"]
    + 0.11 * indicators["visibility_gap"]
    + 0.09 * (1 - indicators["lead_time"])
    + 0.15 * indicators["systemic_relevance"]
    + 0.16 * indicators["cascade_potential"]
    + 0.15 * indicators["tail_severity"]
    + 0.11 * indicators["preparedness_gap"]
    + 0.10 * indicators["distributional_harm"]
)

governance["risk_governance_capacity_score"] = (
    0.15 * governance["monitoring_capacity"]
    + 0.14 * governance["scenario_refresh_capacity"]
    + 0.14 * governance["cross_sector_coordination"]
    + 0.13 * governance["public_legitimacy"]
    + 0.14 * governance["learning_capacity"]
    + 0.10 * governance["flexible_finance"]
    + 0.10 * governance["accountability_capacity"]
    + 0.10 * governance["distributional_review_capacity"]
)

def simulate_pathway(row):
    preparedness = float(row["initial_preparedness"])
    monitoring = float(row["monitoring_capacity"])
    trigger = float(row["trigger_sensitivity"])
    learning = float(row["learning_capacity"])
    governance_capacity = float(row["governance_capacity"])
    resilience = float(row["resilience_capacity"])
    vulnerability = float(row["vulnerability_pressure"])
    cascade = float(row["cascade_pressure"])
    tail = float(row["tail_pressure"])
    legitimacy = float(row["public_legitimacy"])
    horizon = int(row["time_horizon"])

    stress = (
        0.22 * vulnerability
        + 0.26 * cascade
        + 0.22 * tail
        + 0.12 * (1 - governance_capacity)
        + 0.10 * (1 - monitoring)
        + 0.08 * (1 - legitimacy)
    )

    capacity = (
        0.20 * monitoring
        + 0.18 * trigger
        + 0.24 * learning
        + 0.18 * governance_capacity
        + 0.10 * resilience
        + 0.10 * legitimacy
    )

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.16 if t % 8 == 0 else 0.05
            tail_event = 0.12 * tail if t % 13 == 0 else 0.0
            cascade_event = 0.10 * cascade if t % 10 == 0 else 0.0

            warning_response = (
                0.05 * monitoring
                + 0.04 * trigger
                + 0.04 * learning
                + 0.03 * governance_capacity
                + 0.02 * legitimacy
            )

            stress = np.clip(
                stress + 0.06 * shock + tail_event + cascade_event + 0.03 * vulnerability - warning_response,
                0,
                1.6,
            )

            capacity = np.clip(
                capacity + 0.04 * learning + 0.03 * monitoring + 0.03 * trigger + 0.02 * governance_capacity + 0.02 * legitimacy - 0.03 * shock - 0.02 * stress,
                0,
                1.6,
            )

            preparedness = np.clip(
                preparedness + 0.04 * capacity + 0.03 * resilience + 0.02 * governance_capacity + 0.02 * legitimacy - 0.05 * stress - 0.03 * shock - 0.02 * tail_event - 0.02 * cascade_event,
                0,
                1.6,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "preparedness": preparedness,
            "system_stress": stress,
            "adaptive_capacity": capacity,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

path_summary = (
    paths
    .groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_preparedness=("preparedness", "last"),
        mean_preparedness=("preparedness", "mean"),
        mean_system_stress=("system_stress", "mean"),
        final_adaptive_capacity=("adaptive_capacity", "last")
    )
    .reset_index()
    .sort_values("final_preparedness", ascending=False)
)

profiles.sort_values("futures_risk_profile_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_profile_scores.csv", index=False)
scenarios.sort_values("systemic_risk_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_scenario_scores.csv", index=False)
strategy_perf.to_csv(OUTPUTS / "advanced_strategy_scenario_performance.csv", index=False)
strategy_summary.sort_values("robustness_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_robustness_scores.csv", index=False)
indicators.sort_values("risk_indicator_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_indicator_priority_scores.csv", index=False)
governance.sort_values("risk_governance_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_governance_capacity_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_pathway_trajectories.csv", index=False)
path_summary.to_csv(OUTPUTS / "advanced_adaptive_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("futures_risk_profile_score")
plt.barh(ranked["scenario_name"], ranked["futures_risk_profile_score"])
plt.xlabel("Futures Risk Profile Score")
plt.title(f"Futures Risk Profile — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "futures_risk_profile_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["futures_risk_profile_score"], profiles["preparedness_gap_score"])
for _, row in profiles.iterrows():
    plt.text(row["futures_risk_profile_score"], row["preparedness_gap_score"], row["scenario_name"], fontsize=7)
plt.xlabel("Futures Risk Profile")
plt.ylabel("Preparedness Gap")
plt.title("Futures Risk Profile vs Preparedness Gap")
plt.tight_layout()
plt.savefig(OUTPUTS / "futures_risk_vs_preparedness_gap.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_strategies = strategy_summary.sort_values("robustness_score")
plt.barh(ranked_strategies["strategy_name"], ranked_strategies["robustness_score"])
plt.xlabel("Robustness Score")
plt.title("Strategy Robustness Under Deep Uncertainty")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_robustness_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["preparedness"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Preparedness")
plt.title("Preparedness Across Adaptive Risk Pathways")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_pathway_preparedness_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
