#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Future Directions in Strategic Foresight.
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

profiles = pd.read_csv(DATA / "foresight_capability_profiles.csv")
scenarios = pd.read_csv(DATA / "foresight_system_scenarios.csv")
strategies = pd.read_csv(DATA / "foresight_strategy_options.csv")
risks = pd.read_csv(DATA / "foresight_risk_indicators.csv")
signals = pd.read_csv(DATA / "foresight_signal_records.csv")
pathways = pd.read_csv(DATA / "adaptive_strategy_pathways.csv")

profiles["foresight_capability_score"] = (
    0.16 * profiles["signal_detection"]
    + 0.16 * profiles["scenario_capability"]
    + 0.14 * profiles["learning_capacity"]
    + 0.14 * profiles["governance_integration"]
    + 0.12 * profiles["adaptive_flexibility"]
    + 0.10 * profiles["participatory_legitimacy"]
    + 0.10 * profiles["ethical_accountability"]
    + 0.08 * profiles["data_infrastructure"]
)

profiles["technical_capability_score"] = (
    0.35 * profiles["signal_detection"]
    + 0.35 * profiles["scenario_capability"]
    + 0.30 * profiles["data_infrastructure"]
)

profiles["governance_capability_score"] = (
    0.45 * profiles["governance_integration"]
    + 0.30 * profiles["adaptive_flexibility"]
    + 0.25 * profiles["learning_capacity"]
)

profiles["legitimacy_capability_score"] = (
    0.40 * profiles["participatory_legitimacy"]
    + 0.35 * profiles["ethical_accountability"]
    + 0.25 * profiles["public_legitimacy"]
)

profiles["capability_gap_score"] = (
    profiles["technical_capability_score"] -
    ((profiles["governance_capability_score"] + profiles["legitimacy_capability_score"]) / 2)
).clip(lower=0)

scenarios["foresight_system_risk_score"] = (
    0.12 * scenarios["signal_velocity"]
    + 0.16 * scenarios["uncertainty_load"]
    + 0.10 * (1 - scenarios["data_quality"])
    + 0.10 * scenarios["ai_dependence"]
    + 0.16 * (1 - scenarios["governance_authority"])
    + 0.10 * (1 - scenarios["participatory_depth"])
    + 0.12 * scenarios["ethical_risk"]
    + 0.08 * (1 - scenarios["institutional_learning"])
    + 0.06 * scenarios["coordination_complexity"]
)

strategies["foresight_capability_gain_score"] = (
    0.11 * strategies["signal_pipeline_gain"]
    + 0.12 * strategies["scenario_update_gain"]
    + 0.14 * strategies["governance_integration_gain"]
    + 0.10 * strategies["data_system_gain"]
    + 0.11 * strategies["participatory_legitimacy_gain"]
    + 0.11 * strategies["ethical_accountability_gain"]
    + 0.12 * strategies["adaptive_strategy_gain"]
    + 0.07 * strategies["ai_audit_gain"]
    + 0.08 * strategies["learning_capacity_gain"]
    + 0.02 * strategies["implementation_capacity"]
    + 0.02 * strategies["public_legitimacy_gain"]
)

risks["foresight_risk_priority_score"] = (
    0.14 * risks["probability_proxy"]
    + 0.17 * risks["severity"]
    + 0.12 * risks["irreversibility"]
    + 0.12 * risks["visibility_gap"]
    + 0.18 * risks["governance_gap"]
    + 0.17 * risks["legitimacy_gap"]
    + 0.10 * (1 - risks["preparedness"])
)

signals["strategic_attention_score"] = (
    0.16 * signals["signal_strength"]
    + 0.14 * signals["signal_velocity"]
    + 0.10 * signals["novelty"]
    + 0.20 * signals["relevance"]
    + 0.14 * signals["source_quality"]
    + 0.14 * signals["interpretive_confidence"]
    + 0.12 * signals["uncertainty"]
)

signals["ambiguity_score"] = signals["uncertainty"] * (1 - signals["interpretive_confidence"])

def simulate_pathway(row):
    signal = float(row["signal_detection"])
    scenario = float(row["scenario_capability"])
    learning = float(row["learning_capacity"])
    governance = float(row["governance_integration"])
    adaptive = float(row["adaptive_flexibility"])
    participation = float(row["participatory_legitimacy"])
    ethics = float(row["ethical_accountability"])
    data = float(row["data_infrastructure"])
    horizon = int(row["time_horizon"])

    rows = []
    for t in range(1, horizon + 1):
        if t > 1:
            signal_shock = 0.012 if t % 6 == 0 else 0.0
            crisis_pressure = 0.014 if t % 10 == 0 else 0.0
            review_cycle = 0.014 if t % 12 == 0 else 0.0
            governance_drift = 0.010 if t % 17 == 0 else 0.0

            signal = np.clip(signal + signal_shock + 0.006 * data + 0.004 * learning - 0.004 * crisis_pressure, 0, 1.8)
            scenario = np.clip(scenario + 0.008 * signal + 0.006 * learning + review_cycle - 0.006 * governance_drift, 0, 1.8)
            learning = np.clip(learning + 0.008 * scenario + 0.006 * governance + review_cycle - 0.005 * crisis_pressure, 0, 1.8)
            governance = np.clip(governance + 0.007 * learning + 0.006 * participation + 0.005 * ethics - governance_drift - 0.004 * crisis_pressure, 0, 1.8)
            adaptive = np.clip(adaptive + 0.008 * learning + 0.007 * governance + 0.006 * scenario - 0.006 * crisis_pressure, 0, 1.8)
            participation = np.clip(participation + 0.006 * governance + 0.005 * ethics + review_cycle - 0.004 * governance_drift, 0, 1.8)
            ethics = np.clip(ethics + 0.006 * participation + 0.006 * governance + 0.004 * learning - 0.004 * crisis_pressure, 0, 1.8)
            data = np.clip(data + 0.006 * signal + 0.005 * scenario + 0.004 * learning - 0.003 * governance_drift, 0, 1.8)

        capability = (
            0.16 * signal
            + 0.16 * scenario
            + 0.14 * learning
            + 0.14 * governance
            + 0.12 * adaptive
            + 0.10 * participation
            + 0.10 * ethics
            + 0.08 * data
        )

        legitimacy = 0.40 * participation + 0.35 * ethics + 0.25 * governance

        rows.append({
            "pathway_id": row["pathway_id"],
            "institution_id": row["institution_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "signal_detection": signal,
            "scenario_capability": scenario,
            "learning_capacity": learning,
            "governance_integration": governance,
            "adaptive_flexibility": adaptive,
            "participatory_legitimacy": participation,
            "ethical_accountability": ethics,
            "data_infrastructure": data,
            "foresight_capability_score": capability,
            "legitimacy_score": legitimacy,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectory = pd.DataFrame(trajectory_rows)

summary = (
    trajectory.groupby(["pathway_id", "institution_id", "scenario_id", "pathway_name"])
    .agg(
        final_foresight_capability_score=("foresight_capability_score", "last"),
        mean_foresight_capability_score=("foresight_capability_score", "mean"),
        final_governance_integration=("governance_integration", "last"),
        final_learning_capacity=("learning_capacity", "last"),
        final_adaptive_flexibility=("adaptive_flexibility", "last"),
        final_legitimacy_score=("legitimacy_score", "last"),
    )
    .reset_index()
    .sort_values("final_foresight_capability_score", ascending=False)
)

np.random.seed(42)
time_steps = np.arange(1, 61)

signal_a = np.clip(np.linspace(0.30, 0.78, len(time_steps)) + np.random.normal(0, 0.035, len(time_steps)), 0, 1)
signal_b = np.clip(np.linspace(0.52, 0.38, len(time_steps)) + np.random.normal(0, 0.030, len(time_steps)), 0, 1)
signal_c = np.clip(np.linspace(0.22, 0.62, len(time_steps)) + np.random.normal(0, 0.045, len(time_steps)), 0, 1)

signals_df = pd.DataFrame({
    "time": time_steps,
    "signal_a": signal_a,
    "signal_b": signal_b,
    "signal_c": signal_c
})

weights = signals_df[["signal_a", "signal_b", "signal_c"]].div(
    signals_df[["signal_a", "signal_b", "signal_c"]].sum(axis=1),
    axis=0
)

weights.columns = ["scenario_a_weight", "scenario_b_weight", "scenario_c_weight"]
scenario_update = pd.concat([signals_df["time"], weights], axis=1)
scenario_update["uncertainty_load"] = 1 - scenario_update[["scenario_a_weight", "scenario_b_weight", "scenario_c_weight"]].max(axis=1)
scenario_update["learning_capacity"] = np.clip(0.42 + 0.006 * scenario_update["time"] + np.random.normal(0, 0.015, len(time_steps)), 0, 1)

strategy_performance = pd.DataFrame({
    "strategy": [
        "Optimize Current Model",
        "Robust Adaptive Portfolio",
        "Climate and Resilience Investment",
        "AI-Enabled Monitoring System",
        "Participatory Governance Pathway"
    ],
    "scenario_a_value": [0.82, 0.72, 0.68, 0.76, 0.64],
    "scenario_b_value": [0.44, 0.70, 0.76, 0.58, 0.72],
    "scenario_c_value": [0.36, 0.74, 0.82, 0.66, 0.78],
    "reversibility": [0.34, 0.78, 0.62, 0.54, 0.82],
    "governance_readiness": [0.48, 0.70, 0.72, 0.58, 0.84],
    "equity_score": [0.38, 0.66, 0.78, 0.46, 0.88]
})

records = []
for _, weight_row in scenario_update.iterrows():
    for _, strategy_row in strategy_performance.iterrows():
        expected_value = (
            weight_row["scenario_a_weight"] * strategy_row["scenario_a_value"]
            + weight_row["scenario_b_weight"] * strategy_row["scenario_b_value"]
            + weight_row["scenario_c_weight"] * strategy_row["scenario_c_value"]
        )
        adaptive_capacity = (
            0.35 * strategy_row["reversibility"]
            + 0.35 * strategy_row["governance_readiness"]
            + 0.30 * weight_row["learning_capacity"]
        )
        justice_adjusted_value = (
            0.70 * expected_value
            + 0.15 * adaptive_capacity
            + 0.15 * strategy_row["equity_score"]
            - 0.10 * weight_row["uncertainty_load"]
        )
        records.append({
            "time": weight_row["time"],
            "strategy": strategy_row["strategy"],
            "expected_value": expected_value,
            "adaptive_capacity": adaptive_capacity,
            "equity_score": strategy_row["equity_score"],
            "justice_adjusted_value": justice_adjusted_value
        })

strategy_paths = pd.DataFrame(records)

strategy_summary = (
    strategy_paths.groupby("strategy")
    .agg(
        mean_expected_value=("expected_value", "mean"),
        mean_adaptive_capacity=("adaptive_capacity", "mean"),
        mean_equity_score=("equity_score", "mean"),
        mean_justice_adjusted_value=("justice_adjusted_value", "mean"),
        minimum_justice_adjusted_value=("justice_adjusted_value", "min"),
        final_justice_adjusted_value=("justice_adjusted_value", "last"),
    )
    .reset_index()
    .sort_values("mean_justice_adjusted_value", ascending=False)
)

profiles.sort_values("foresight_capability_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_capability_scores.csv", index=False)
scenarios.sort_values("foresight_system_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_system_scenario_scores.csv", index=False)
strategies.sort_values("foresight_capability_gain_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_strategy_scores.csv", index=False)
risks.sort_values("foresight_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_risk_priority_scores.csv", index=False)
signals.sort_values("strategic_attention_score", ascending=False).to_csv(OUTPUTS / "advanced_foresight_signal_priority_scores.csv", index=False)
trajectory.to_csv(OUTPUTS / "advanced_adaptive_strategy_trajectories.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_strategy_summary.csv", index=False)
scenario_update.to_csv(OUTPUTS / "advanced_dynamic_scenario_updating.csv", index=False)
strategy_paths.to_csv(OUTPUTS / "advanced_dynamic_strategy_viability.csv", index=False)
strategy_summary.to_csv(OUTPUTS / "advanced_strategy_viability_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("foresight_capability_score")
plt.barh(ranked["institution_type"], ranked["foresight_capability_score"])
plt.xlabel("Foresight Capability Score")
plt.title(f"Integrated Foresight Capability — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "foresight_capability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["technical_capability_score"], profiles["legitimacy_capability_score"])
for _, row in profiles.iterrows():
    plt.text(row["technical_capability_score"], row["legitimacy_capability_score"], row["institution_type"], fontsize=7)
plt.xlabel("Technical Capability")
plt.ylabel("Legitimacy Capability")
plt.title("Technical Capability vs Participatory and Ethical Legitimacy")
plt.tight_layout()
plt.savefig(OUTPUTS / "technical_vs_legitimacy_capability.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(scenario_update["time"], scenario_update["scenario_a_weight"], label="Scenario A")
plt.plot(scenario_update["time"], scenario_update["scenario_b_weight"], label="Scenario B")
plt.plot(scenario_update["time"], scenario_update["scenario_c_weight"], label="Scenario C")
plt.xlabel("Time Step")
plt.ylabel("Scenario Weight")
plt.title("Dynamic Scenario Updating Under Changing Signals")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "dynamic_scenario_weights.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for strategy_name in strategy_paths["strategy"].unique():
    subset = strategy_paths[strategy_paths["strategy"] == strategy_name]
    plt.plot(subset["time"], subset["justice_adjusted_value"], label=strategy_name)
plt.xlabel("Time Step")
plt.ylabel("Justice-Adjusted Strategy Value")
plt.title("Strategy Viability Under Dynamic Scenario Weights")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_viability_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
