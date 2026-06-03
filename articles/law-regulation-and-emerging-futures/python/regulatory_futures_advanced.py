#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Law, Regulation, and Emerging Futures.
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

models = pd.read_csv(DATA / "regulatory_models.csv")
risks = pd.read_csv(DATA / "emerging_risk_register.csv")
rights = pd.read_csv(DATA / "rights_remedy_register.csv")
sandboxes = pd.read_csv(DATA / "sandbox_governance.csv")
scenarios = pd.read_csv(DATA / "regulatory_scenarios.csv")
pathways = pd.read_csv(DATA / "adaptive_regulatory_pathways.csv")
strategies = pd.read_csv(DATA / "strategy_options.csv")

models["future_ready_regulatory_capacity_score"] = (
    0.13 * models["foresight_capacity"]
    + 0.12 * models["monitoring_capacity"]
    + 0.12 * models["enforcement_capacity"]
    + 0.14 * models["rights_protection"]
    + 0.10 * models["public_participation"]
    + 0.12 * models["revision_authority"]
    + 0.10 * models["regulatory_learning"]
    + 0.08 * models["capture_resistance"]
    + 0.05 * models["legal_certainty"]
    + 0.04 * models["remedy_access"]
)

models["regulatory_lag_pressure_score"] = (
    0.16 * (1 - models["foresight_capacity"])
    + 0.14 * (1 - models["monitoring_capacity"])
    + 0.14 * (1 - models["revision_authority"])
    + 0.12 * (1 - models["regulatory_learning"])
    + 0.12 * (1 - models["enforcement_capacity"])
    + 0.10 * (1 - models["rights_protection"])
    + 0.08 * (1 - models["public_participation"])
    + 0.08 * (1 - models["capture_resistance"])
    + 0.06 * (1 - models["remedy_access"])
)

risks["emerging_regulatory_risk_score"] = (
    0.16 * risks["change_velocity"]
    + 0.18 * risks["harm_severity"]
    + 0.13 * risks["uncertainty"]
    + 0.15 * risks["irreversibility"]
    + 0.15 * risks["distributional_exposure"]
    + 0.15 * risks["regulatory_gap"]
    + 0.08 * (1 - risks["mitigation_capacity"])
)

rights["rights_remedy_strength_score"] = (
    0.14 * rights["notice"]
    + 0.14 * rights["explanation"]
    + 0.15 * rights["appeal"]
    + 0.15 * rights["audit_access"]
    + 0.14 * rights["public_enforcement"]
    + 0.12 * rights["collective_remedy"]
    + 0.08 * rights["compensation"]
    + 0.08 * rights["accessibility"]
)

sandboxes["sandbox_safeguard_score"] = (
    0.14 * sandboxes["public_interest_test"]
    + 0.12 * sandboxes["eligibility_transparency"]
    + 0.16 * sandboxes["rights_nonwaiver"]
    + 0.12 * sandboxes["participant_consent"]
    + 0.14 * sandboxes["independent_evaluation"]
    + 0.12 * sandboxes["exit_conditions"]
    + 0.10 * sandboxes["public_reporting"]
    + 0.10 * sandboxes["capture_control"]
)

sandboxes["sandbox_capture_risk_score"] = 1 - (
    0.25 * sandboxes["capture_control"]
    + 0.20 * sandboxes["public_reporting"]
    + 0.20 * sandboxes["independent_evaluation"]
    + 0.20 * sandboxes["eligibility_transparency"]
    + 0.15 * sandboxes["public_interest_test"]
)

scenarios["regulatory_future_stress_score"] = (
    0.16 * scenarios["technology_acceleration"]
    + 0.16 * scenarios["climate_stress"]
    + 0.14 * (1 - scenarios["public_trust"])
    + 0.12 * (1 - scenarios["institutional_capacity"])
    + 0.14 * scenarios["capture_pressure"]
    + 0.14 * scenarios["rights_risk"]
    + 0.08 * scenarios["international_fragmentation"]
    + 0.06 * (1 - scenarios["learning_capacity"])
)

scenarios["future_ready_regulatory_opportunity_score"] = (
    0.22 * scenarios["institutional_capacity"]
    + 0.20 * scenarios["learning_capacity"]
    + 0.18 * scenarios["public_trust"]
    + 0.12 * (1 - scenarios["capture_pressure"])
    + 0.12 * (1 - scenarios["rights_risk"])
    + 0.08 * (1 - scenarios["international_fragmentation"])
    + 0.08 * (1 - scenarios["climate_stress"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    trust = float(row["initial_trust"])
    capacity = (
        0.14 * row["foresight"]
        + 0.13 * row["monitoring"]
        + 0.13 * row["enforcement"]
        + 0.15 * row["rights"]
        + 0.12 * row["participation"]
        + 0.13 * row["revision"]
        + 0.12 * row["learning"]
        + 0.08 * row["capture_resistance"]
    )
    lag = 1 - (0.45 * row["foresight"] + 0.35 * row["monitoring"] + 0.20 * row["revision"])
    rights_state = float(row["rights"])
    learning_state = float(row["learning"])
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            pressure = 0.16 if t % 8 == 0 else 0.06

            anticipatory_gain = 0.24 * row["foresight"] + 0.20 * row["monitoring"]
            legal_gain = 0.22 * row["revision"] + 0.18 * row["enforcement"]
            legitimacy_gain = 0.16 * row["participation"] + 0.14 * row["capture_resistance"]
            learning_gain = 0.18 * learning_state

            lag = np.clip(
                lag + 0.08 * pressure - 0.04 * anticipatory_gain - 0.03 * legal_gain - 0.02 * learning_gain,
                0,
                1.4,
            )

            rights_state = np.clip(
                rights_state + 0.04 * row["rights"] + 0.03 * row["enforcement"] + 0.02 * row["participation"] - 0.04 * lag,
                0,
                1.4,
            )

            learning_state = np.clip(
                learning_state + 0.04 * row["learning"] + 0.03 * row["monitoring"] + 0.02 * row["revision"] - 0.02 * pressure,
                0,
                1.4,
            )

            trust = np.clip(
                trust + 0.04 * rights_state + 0.03 * row["participation"] + 0.03 * row["capture_resistance"] - 0.05 * lag,
                0,
                1.4,
            )

            capacity = np.clip(
                capacity + anticipatory_gain / 7 + legal_gain / 7 + legitimacy_gain / 8 + learning_gain / 8 - 0.08 * lag - 0.03 * pressure,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "model_id": row["model_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "future_ready_regulatory_capacity": capacity,
            "regulatory_lag_pressure": lag,
            "rights_protection": rights_state,
            "public_trust": trust,
            "learning_score": learning_state,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

trajectories = pd.DataFrame(trajectory_rows)

summary = (
    trajectories
    .groupby(["pathway_id", "model_id", "scenario_id", "pathway_name"])
    .agg(
        final_regulatory_capacity=("future_ready_regulatory_capacity", "last"),
        mean_regulatory_capacity=("future_ready_regulatory_capacity", "mean"),
        mean_regulatory_lag_pressure=("regulatory_lag_pressure", "mean"),
        final_rights_protection=("rights_protection", "last"),
        final_public_trust=("public_trust", "last"),
        final_learning_score=("learning_score", "last")
    )
    .reset_index()
    .sort_values("final_regulatory_capacity", ascending=False)
)

strategies["future_ready_regulatory_strategy_score"] = (
    0.13 * strategies["foresight_capacity"]
    + 0.12 * strategies["monitoring_design"]
    + 0.14 * strategies["rights_safeguards"]
    + 0.11 * strategies["public_participation"]
    + 0.13 * strategies["revision_triggers"]
    + 0.12 * strategies["enforcement_capacity"]
    + 0.10 * strategies["remedy_access"]
    + 0.10 * strategies["capture_resistance"]
    + 0.05 * strategies["legal_certainty"]
)

strategies["rights_accountability_strategy_score"] = (
    0.18 * strategies["rights_safeguards"]
    + 0.16 * strategies["remedy_access"]
    + 0.16 * strategies["enforcement_capacity"]
    + 0.14 * strategies["capture_resistance"]
    + 0.12 * strategies["public_participation"]
    + 0.10 * strategies["monitoring_design"]
    + 0.08 * strategies["revision_triggers"]
    + 0.06 * strategies["legal_certainty"]
)

models.sort_values("future_ready_regulatory_capacity_score", ascending=False).to_csv(OUTPUTS / "advanced_regulatory_model_scores.csv", index=False)
risks.sort_values("emerging_regulatory_risk_score", ascending=False).to_csv(OUTPUTS / "advanced_emerging_risk_scores.csv", index=False)
rights.sort_values("rights_remedy_strength_score", ascending=False).to_csv(OUTPUTS / "advanced_rights_remedy_scores.csv", index=False)
sandboxes.sort_values("sandbox_safeguard_score", ascending=False).to_csv(OUTPUTS / "advanced_sandbox_safeguard_scores.csv", index=False)
scenarios.sort_values("future_ready_regulatory_opportunity_score", ascending=False).to_csv(OUTPUTS / "advanced_regulatory_scenario_scores.csv", index=False)
trajectories.to_csv(OUTPUTS / "advanced_adaptive_regulatory_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_adaptive_regulatory_pathway_summary.csv", index=False)
strategies.sort_values("future_ready_regulatory_strategy_score", ascending=False).to_csv(OUTPUTS / "advanced_strategy_option_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = models.sort_values("future_ready_regulatory_capacity_score")
plt.barh(ranked["regulatory_model"], ranked["future_ready_regulatory_capacity_score"])
plt.xlabel("Future-Ready Regulatory Capacity")
plt.title(f"Regulatory Futures Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "regulatory_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_lag = models.sort_values("regulatory_lag_pressure_score")
plt.barh(ranked_lag["regulatory_model"], ranked_lag["regulatory_lag_pressure_score"])
plt.xlabel("Regulatory Lag Pressure")
plt.title("Regulatory Lag Pressure by Model")
plt.tight_layout()
plt.savefig(OUTPUTS / "regulatory_lag_pressure_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["future_ready_regulatory_capacity"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Regulatory Capacity")
plt.title("Future-Ready Regulatory Capacity Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "regulatory_capacity_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in trajectories["pathway_name"].unique():
    subset = trajectories[trajectories["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["regulatory_lag_pressure"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Regulatory Lag Pressure")
plt.title("Regulatory Lag Pressure Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "regulatory_lag_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
