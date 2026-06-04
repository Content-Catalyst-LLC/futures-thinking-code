#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Financial Futures and Systemic Risk.
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

profiles = pd.read_csv(DATA / "financial_system_profiles.csv")
scenarios = pd.read_csv(DATA / "financial_scenarios.csv")
policies = pd.read_csv(DATA / "policy_options.csv")
risks = pd.read_csv(DATA / "risk_indicators.csv")
public_records = pd.read_csv(DATA / "public_finance_climate_records.csv")
pathways = pd.read_csv(DATA / "stress_pathways.csv")

profiles["financial_resilience_score"] = (
    0.14 * profiles["liquidity_resilience"]
    + 0.14 * profiles["household_security"]
    + 0.14 * profiles["regulatory_strength"]
    + 0.10 * profiles["public_finance_capacity"]
    + 0.10 * profiles["consumer_protection"]
    + 0.10 * profiles["productive_investment"]
    + 0.10 * (1 - profiles["leverage"])
    + 0.08 * (1 - profiles["climate_exposure"])
    + 0.06 * (1 - profiles["nonbank_exposure"])
    + 0.04 * (1 - profiles["digital_run_risk"])
)

profiles["systemic_risk_score"] = (
    0.16 * profiles["leverage"]
    + 0.14 * (1 - profiles["liquidity_resilience"])
    + 0.14 * profiles["climate_exposure"]
    + 0.13 * profiles["nonbank_exposure"]
    + 0.13 * profiles["digital_run_risk"]
    + 0.12 * (1 - profiles["household_security"])
    + 0.10 * (1 - profiles["public_finance_capacity"])
    + 0.08 * (1 - profiles["regulatory_strength"])
)

scenarios["financial_stress_pressure_score"] = (
    0.14 * scenarios["rate_shock"]
    + 0.16 * scenarios["liquidity_shock"]
    + 0.14 * scenarios["asset_price_shock"]
    + 0.14 * scenarios["climate_shock"]
    + 0.14 * scenarios["digital_run_pressure"]
    + 0.12 * scenarios["sovereign_refinancing_pressure"]
    + 0.10 * scenarios["nonbank_stress"]
    + 0.06 * scenarios["household_default_pressure"]
)

scenarios["social_financial_fragility_score"] = (
    0.18 * scenarios["household_default_pressure"]
    + 0.16 * scenarios["sovereign_refinancing_pressure"]
    + 0.14 * scenarios["climate_shock"]
    + 0.12 * scenarios["asset_price_shock"]
    + 0.12 * scenarios["rate_shock"]
    + 0.10 * scenarios["liquidity_shock"]
    + 0.10 * scenarios["nonbank_stress"]
    + 0.08 * scenarios["digital_run_pressure"]
)

policies["financial_stability_gain_score"] = (
    0.16 * policies["capital_buffer_strength"]
    + 0.16 * policies["liquidity_support"]
    + 0.14 * policies["consumer_protection_gain"]
    + 0.14 * policies["climate_risk_governance"]
    + 0.14 * policies["nonbank_oversight"]
    + 0.12 * policies["digital_resilience"]
    + 0.10 * policies["public_finance_support"]
    + 0.04 * policies["implementation_capacity"]
)

policies["implementation_risk_score"] = (
    0.28 * (1 - policies["implementation_capacity"])
    + 0.12 * (1 - policies["capital_buffer_strength"])
    + 0.12 * (1 - policies["liquidity_support"])
    + 0.12 * (1 - policies["consumer_protection_gain"])
    + 0.10 * (1 - policies["climate_risk_governance"])
    + 0.10 * (1 - policies["nonbank_oversight"])
    + 0.08 * (1 - policies["digital_resilience"])
    + 0.08 * (1 - policies["public_finance_support"])
)

risks["systemic_risk_priority_score"] = (
    0.15 * risks["probability_proxy"]
    + 0.18 * risks["severity"]
    + 0.17 * risks["contagion_potential"]
    + 0.14 * risks["opacity"]
    + 0.14 * risks["recovery_difficulty"]
    + 0.14 * risks["distributional_harm"]
    + 0.08 * (1 - risks["policy_preparedness"])
)

public_records["public_finance_resilience_score"] = (
    0.16 * public_records["tax_capacity"]
    + 0.16 * public_records["debt_sustainability"]
    + 0.16 * public_records["adaptation_finance"]
    + 0.12 * public_records["insurance_availability"]
    + 0.16 * public_records["public_investment_capacity"]
    + 0.14 * public_records["household_protection"]
    + 0.10 * public_records["climate_risk_disclosure"]
)

public_records["fiscal_climate_fragility_score"] = (
    0.18 * (1 - public_records["tax_capacity"])
    + 0.18 * (1 - public_records["debt_sustainability"])
    + 0.16 * (1 - public_records["public_investment_capacity"])
    + 0.14 * (1 - public_records["adaptation_finance"])
    + 0.12 * (1 - public_records["insurance_availability"])
    + 0.12 * (1 - public_records["household_protection"])
    + 0.10 * (1 - public_records["climate_risk_disclosure"])
)

def simulate_pathway(row):
    horizon = int(row["time_horizon"])
    stability = float(row["initial_stability"])
    risk = (
        0.18 * row["leverage"]
        + 0.16 * (1 - row["liquidity_resilience"])
        + 0.14 * row["climate_exposure"]
        + 0.14 * row["nonbank_exposure"]
        + 0.14 * row["digital_run_risk"]
        + 0.12 * (1 - row["household_security"])
        + 0.12 * (1 - row["regulatory_strength"])
    )
    public_capacity = (
        0.34 * row["public_finance_capacity"]
        + 0.26 * row["regulatory_strength"]
        + 0.22 * row["household_security"]
        + 0.18 * row["liquidity_resilience"]
    )
    rows = []

    for t in range(1, horizon + 1):
        if t > 1:
            shock = 0.18 if t % 8 == 0 else 0.06

            fragility_force = (
                0.20 * row["leverage"]
                + 0.16 * row["nonbank_exposure"]
                + 0.16 * row["digital_run_risk"]
                + 0.14 * row["climate_exposure"]
                + 0.12 * (1 - row["household_security"])
                + 0.12 * (1 - row["liquidity_resilience"])
                + 0.10 * shock
            )

            resilience_force = (
                0.22 * row["liquidity_resilience"]
                + 0.20 * row["regulatory_strength"]
                + 0.18 * row["public_finance_capacity"]
                + 0.16 * row["household_security"]
                + 0.12 * (1 - row["leverage"])
                + 0.12 * (1 - row["digital_run_risk"])
            )

            risk = np.clip(
                risk + 0.05 * shock + 0.04 * fragility_force - 0.04 * resilience_force,
                0,
                1.4,
            )

            public_capacity = np.clip(
                public_capacity
                + 0.04 * row["public_finance_capacity"]
                + 0.03 * row["regulatory_strength"]
                + 0.02 * row["household_security"]
                - 0.04 * shock
                - 0.03 * risk,
                0,
                1.5,
            )

            stability = np.clip(
                stability
                + 0.07 * resilience_force
                + 0.04 * public_capacity
                - shock
                - 0.06 * risk
                - 0.03 * fragility_force,
                0,
                1.8,
            )

        rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "time_step": t,
            "financial_stability": stability,
            "systemic_risk": risk,
            "public_capacity": public_capacity,
        })

    return rows

trajectory_rows = []
for _, row in pathways.iterrows():
    trajectory_rows.extend(simulate_pathway(row))

paths = pd.DataFrame(trajectory_rows)

summary = (
    paths
    .groupby(["pathway_id", "profile_id", "scenario_id", "pathway_name"])
    .agg(
        final_financial_stability=("financial_stability", "last"),
        mean_financial_stability=("financial_stability", "mean"),
        mean_systemic_risk=("systemic_risk", "mean"),
        final_public_capacity=("public_capacity", "last")
    )
    .reset_index()
    .sort_values("final_financial_stability", ascending=False)
)

profiles.sort_values("financial_resilience_score", ascending=False).to_csv(OUTPUTS / "advanced_financial_profile_scores.csv", index=False)
scenarios.sort_values("financial_stress_pressure_score", ascending=False).to_csv(OUTPUTS / "advanced_financial_scenario_scores.csv", index=False)
policies.sort_values("financial_stability_gain_score", ascending=False).to_csv(OUTPUTS / "advanced_policy_option_scores.csv", index=False)
risks.sort_values("systemic_risk_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_risk_indicator_priority_scores.csv", index=False)
public_records.sort_values("public_finance_resilience_score", ascending=False).to_csv(OUTPUTS / "advanced_public_finance_climate_scores.csv", index=False)
paths.to_csv(OUTPUTS / "advanced_stress_pathways.csv", index=False)
summary.to_csv(OUTPUTS / "advanced_stress_pathway_summary.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = profiles.sort_values("financial_resilience_score")
plt.barh(ranked["financial_future_name"], ranked["financial_resilience_score"])
plt.xlabel("Financial Resilience Score")
plt.title(f"Financial Resilience — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "financial_resilience_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["financial_resilience_score"], profiles["systemic_risk_score"])
for _, row in profiles.iterrows():
    plt.text(row["financial_resilience_score"], row["systemic_risk_score"], row["financial_future_name"], fontsize=7)
plt.xlabel("Financial Resilience")
plt.ylabel("Systemic Risk")
plt.title("Financial Resilience vs Systemic Risk")
plt.tight_layout()
plt.savefig(OUTPUTS / "financial_resilience_vs_systemic_risk.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["financial_stability"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Financial Stability")
plt.title("Financial Stability Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "financial_stability_paths.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
for pathway_name in paths["pathway_name"].unique():
    subset = paths[paths["pathway_name"] == pathway_name]
    plt.plot(subset["time_step"], subset["systemic_risk"], label=pathway_name)

plt.xlabel("Time Step")
plt.ylabel("Systemic Risk")
plt.title("Systemic Risk Paths")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUTPUTS / "systemic_risk_paths.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
