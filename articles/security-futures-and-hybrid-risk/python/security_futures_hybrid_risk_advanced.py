#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Security Futures and Hybrid Risk.
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

profiles = pd.read_csv(DATA / "security_profiles.csv")
scenarios = pd.read_csv(DATA / "security_scenarios.csv")
strategies = pd.read_csv(DATA / "security_strategy_options.csv")
risks = pd.read_csv(DATA / "security_risk_indicators.csv")
dependencies = pd.read_csv(DATA / "infrastructure_dependencies.csv")
pathways = pd.read_csv(DATA / "adaptive_security_pathways.csv")

profiles["hybrid_risk_score"] = (
    0.13 * profiles["cyber_exposure"]
    + 0.13 * profiles["infrastructure_dependence"]
    + 0.13 * profiles["information_vulnerability"]
    + 0.12 * profiles["climate_security_stress"]
    + 0.10 * profiles["resource_dependence"]
    + 0.11 * (1 - profiles["institutional_coordination"])
    + 0.10 * (1 - profiles["civilian_protection"])
    + 0.10 * (1 - profiles["adaptive_resilience"])
    + 0.05 * (1 - profiles["public_trust"])
    + 0.03 * (1 - profiles["attribution_clarity"])
)

profiles["security_resilience_score"] = (
    0.20 * profiles["institutional_coordination"]
    + 0.22 * profiles["civilian_protection"]
    + 0.22 * profiles["adaptive_resilience"]
    + 0.16 * profiles["public_trust"]
    + 0.08 * profiles["attribution_clarity"]
    + 0.04 * (1 - profiles["cyber_exposure"])
    + 0.04 * (1 - profiles["information_vulnerability"])
    + 0.04 * (1 - profiles["infrastructure_dependence"])
)

profiles["resilience_gap_score"] = (profiles["hybrid_risk_score"] - profiles["security_resilience_score"]).clip(lower=0)

scenarios["hybrid_security_stress_score"] = (
    0.13 * scenarios["cyber_shock"]
    + 0.13 * scenarios["infrastructure_shock"]
    + 0.12 * scenarios["information_shock"]
    + 0.12 * scenarios["climate_shock"]
    + 0.10 * scenarios["resource_shock"]
    + 0.08 * scenarios["migration_pressure"]
    + 0.10 * scenarios["security_escalation"]
    + 0.09 * scenarios["institutional_fragmentation"]
    + 0.06 * scenarios["private_infrastructure_dependency"]
    + 0.07 * scenarios["civilian_harm_pressure"]
)

strategies["security_strategy_value_score"] = (
    0.12 * strategies["cyber_resilience_gain"]
    + 0.12 * strategies["infrastructure_redundancy_gain"]
    + 0.12 * strategies["information_integrity_gain"]
    + 0.10 * strategies["climate_security_adaptation_gain"]
    + 0.09 * strategies["resource_security_gain"]
    + 0.12 * strategies["institutional_coordination_gain"]
    + 0.12 * strategies["civilian_protection_gain"]
    + 0.07 * strategies["deterrence_gain"]
    + 0.08 * strategies["adaptive_learning_gain"]
    + 0.03 * strategies["implementation_capacity"]
    + 0.03 * strategies["public_legitimacy_gain"]
)

risks["hybrid_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.18 * risks["cascade_potential"]
    + 0.10 * risks["visibility_gap"]
    + 0.13 * risks["recovery_difficulty"]
    + 0.17 * risks["distributional_harm"]
    + 0.10 * (1 - risks["preparedness"])
)

dependencies["cascade_exposure_score"] = (
    dependencies["dependency_weight"]
    * dependencies["disruption_sensitivity"]
    * dependencies["public_harm_potential"]
    * (1 - dependencies["recovery_capacity"])
)

dependencies["public_private_risk_score"] = (
    0.40 * dependencies["private_operator_dependency"]
    + 0.30 * dependencies["public_harm_potential"]
    + 0.20 * dependencies["disruption_sensitivity"]
    + 0.10 * (1 - dependencies["recovery_capacity"])
)

def simulate_pathway(row):
    resilience = float(row["initial_resilience"])
    cyber = float(row["cyber_exposure"])
    infra = float(row["infrastructure_dependence"])
    info = float(row["information_vulnerability"])
    climate = float(row["climate_security_stress"])
    resource = float(row["resource_dependence"])
    coordination = float(row["institutional_coordination"])
    protection = float(row["civilian_protection"])
    adaptive = float(row["adaptive_resilience"])
    trust = float(row["public_trust"])
    system_stress = float(row["system_stress"])
    horizon = int(row["time_horizon"])

    hybrid_risk = (
        0.16 * cyber
        + 0.15 * infra
        + 0.14 * info
        + 0.13 * climate
        + 0.10 * resource
        + 0.12 * (1 - coordination)
        + 0.10 * (1 - protection)
        + 0.10 * (1 - adaptive)
    )

    cascade_pressure = (
        0.26 * infra
        + 0.18 * cyber
        + 0.14 * resource
        + 0.12 * climate
        + 0.12 * (1 - coordination)
        + 0.10 * info
        + 0.08 * (1 - adaptive)
    )

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            shock_total = 0.04
            shock_total += 0.12 * cyber if t % 8 == 0 else 0.0
            shock_total += 0.10 * infra if t % 10 == 0 else 0.0
            shock_total += 0.09 * info if t % 9 == 0 else 0.0
            shock_total += 0.11 * climate if t % 13 == 0 else 0.0
            shock_total += 0.08 * resource if t % 11 == 0 else 0.0

            response_capacity = (
                0.06 * coordination
                + 0.06 * adaptive
                + 0.04 * protection
                + 0.03 * trust
            )

            cascade_pressure = np.clip(
                cascade_pressure + shock_total + 0.04 * infra + 0.03 * cyber + 0.03 * resource - response_capacity,
                0,
                1.8,
            )

            hybrid_risk = np.clip(
                hybrid_risk + 0.05 * cascade_pressure + 0.04 * info + 0.03 * climate + shock_total + 0.02 * system_stress - response_capacity,
                0,
                1.8,
            )

            resilience = np.clip(
                resilience + 0.04 * adaptive + 0.03 * coordination + 0.03 * protection + 0.02 * trust - 0.04 * hybrid_risk - 0.02 * shock_total,
                0,
                1.8,
            )

            trust = np.clip(
                trust + 0.04 * protection + 0.03 * coordination + 0.02 * adaptive - 0.04 * (0.09 * info if t % 9 == 0 else 0.0) - 0.03 * hybrid_risk,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "hybrid_risk": hybrid_risk,
            "cascade_pressure": cascade_pressure,
            "security_resilience": resilience,
            "public_trust": trust,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths.groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_hybrid_risk=("hybrid_risk", "last"),
        mean_hybrid_risk=("hybrid_risk", "mean"),
        final_cascade_pressure=("cascade_pressure", "last"),
        final_security_resilience=("security_resilience", "last"),
        final_public_trust=("public_trust", "last"),
    )
    .reset_index()
    .sort_values("final_security_resilience", ascending=False)
)

profiles.sort_values("hybrid_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_security_profile_scores.csv", index=False)
scenarios.sort_values("hybrid_security_stress_score", ascending=False).to_csv(OUTPUTS / "advanced_security_scenario_scores.csv", index=False)
strategies.sort_values("security_strategy_value_score", ascending=False).to_csv(OUTPUTS / "advanced_security_strategy_scores.csv", index=False)
risks.sort_values("hybrid_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_hybrid_risk_priority_scores.csv", index=False)
dependencies.sort_values("cascade_exposure_score", ascending=False).to_csv(OUTPUTS / "advanced_infrastructure_cascade_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_adaptive_security_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_security_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("hybrid_risk_score")
plt.barh(ranked["future_name"], ranked["hybrid_risk_score"])
plt.xlabel("Hybrid Risk Score")
plt.title(f"Hybrid Risk — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "hybrid_risk_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["hybrid_risk_score"], profiles["security_resilience_score"])
for _, row in profiles.iterrows():
    plt.text(row["hybrid_risk_score"], row["security_resilience_score"], row["future_name"], fontsize=7)
plt.xlabel("Hybrid Risk")
plt.ylabel("Security Resilience")
plt.title("Hybrid Risk vs Security Resilience")
plt.tight_layout()
plt.savefig(OUTPUTS / "hybrid_risk_vs_security_resilience.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["hybrid_risk"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Hybrid Risk")
plt.title("Adaptive Security Hybrid Risk Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_security_hybrid_risk_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["security_resilience"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Security Resilience")
plt.title("Adaptive Security Resilience Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "adaptive_security_resilience_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
