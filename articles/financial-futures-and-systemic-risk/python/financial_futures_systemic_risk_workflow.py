#!/usr/bin/env python3
"""
Standard-library workflow for Financial Futures and Systemic Risk.

Outputs:
- financial_profile_scores.csv
- financial_scenario_scores.csv
- policy_option_scores.csv
- risk_indicator_priority_scores.csv
- public_finance_climate_scores.csv
- stress_pathways.csv
- stress_pathway_summary.csv
- financial_futures_systemic_risk_report.md
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
CONFIG = ROOT / "article_config.json"
OUTPUTS.mkdir(exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def clamp(value: float, low: float = 0.0, high: float = 1.8) -> float:
    return max(low, min(high, value))


def financial_resilience(row: dict[str, str]) -> float:
    return (
        0.14 * float(row["liquidity_resilience"])
        + 0.14 * float(row["household_security"])
        + 0.14 * float(row["regulatory_strength"])
        + 0.10 * float(row["public_finance_capacity"])
        + 0.10 * float(row["consumer_protection"])
        + 0.10 * float(row["productive_investment"])
        + 0.10 * (1.0 - float(row["leverage"]))
        + 0.08 * (1.0 - float(row["climate_exposure"]))
        + 0.06 * (1.0 - float(row["nonbank_exposure"]))
        + 0.04 * (1.0 - float(row["digital_run_risk"]))
    )


def systemic_risk(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["leverage"])
        + 0.14 * (1.0 - float(row["liquidity_resilience"]))
        + 0.14 * float(row["climate_exposure"])
        + 0.13 * float(row["nonbank_exposure"])
        + 0.13 * float(row["digital_run_risk"])
        + 0.12 * (1.0 - float(row["household_security"]))
        + 0.10 * (1.0 - float(row["public_finance_capacity"]))
        + 0.08 * (1.0 - float(row["regulatory_strength"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    policies: list[dict[str, str]],
    risks: list[dict[str, str]],
    public_records: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in policies:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Policy {row['policy_id']} references missing profile {row['profile_id']}.")

    for row in risks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Risk indicator {row['risk_id']} references missing scenario {row['scenario_id']}.")

    for row in public_records:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Public finance record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["leverage", "liquidity_resilience", "household_security", "climate_exposure", "nonbank_exposure", "digital_run_risk", "regulatory_strength", "public_finance_capacity", "consumer_protection", "productive_investment"]),
        ("scenarios", scenarios, ["rate_shock", "liquidity_shock", "asset_price_shock", "climate_shock", "digital_run_pressure", "sovereign_refinancing_pressure", "nonbank_stress", "household_default_pressure"]),
        ("policies", policies, ["capital_buffer_strength", "liquidity_support", "consumer_protection_gain", "climate_risk_governance", "nonbank_oversight", "digital_resilience", "public_finance_support", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "contagion_potential", "opacity", "recovery_difficulty", "distributional_harm", "policy_preparedness"]),
        ("public_records", public_records, ["tax_capacity", "debt_sustainability", "adaptation_finance", "insurance_availability", "public_investment_capacity", "household_protection", "climate_risk_disclosure"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("policy_id") or row.get("risk_id") or row.get("record_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        resilience = financial_resilience(row)
        risk = systemic_risk(row)

        if resilience >= 0.66 and risk < 0.46:
            profile_class = "Stronger financial resilience profile"
        elif risk >= 0.66:
            profile_class = "High systemic risk profile"
        else:
            profile_class = "Mixed or transitional financial future"

        rows.append({
            "profile_id": row["profile_id"],
            "financial_future_name": row["financial_future_name"],
            "financial_future_type": row["financial_future_type"],
            "financial_resilience_score": round(resilience, 4),
            "systemic_risk_score": round(risk, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["financial_resilience_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress_pressure = (
            0.14 * float(row["rate_shock"])
            + 0.16 * float(row["liquidity_shock"])
            + 0.14 * float(row["asset_price_shock"])
            + 0.14 * float(row["climate_shock"])
            + 0.14 * float(row["digital_run_pressure"])
            + 0.12 * float(row["sovereign_refinancing_pressure"])
            + 0.10 * float(row["nonbank_stress"])
            + 0.06 * float(row["household_default_pressure"])
        )

        social_fragility = (
            0.18 * float(row["household_default_pressure"])
            + 0.16 * float(row["sovereign_refinancing_pressure"])
            + 0.14 * float(row["climate_shock"])
            + 0.12 * float(row["asset_price_shock"])
            + 0.12 * float(row["rate_shock"])
            + 0.10 * float(row["liquidity_shock"])
            + 0.10 * float(row["nonbank_stress"])
            + 0.08 * float(row["digital_run_pressure"])
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "financial_stress_pressure_score": round(stress_pressure, 4),
            "social_financial_fragility_score": round(social_fragility, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["financial_stress_pressure_score"]), reverse=True)
    return rows


def score_policies(policies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in policies:
        stability_gain = (
            0.16 * float(row["capital_buffer_strength"])
            + 0.16 * float(row["liquidity_support"])
            + 0.14 * float(row["consumer_protection_gain"])
            + 0.14 * float(row["climate_risk_governance"])
            + 0.14 * float(row["nonbank_oversight"])
            + 0.12 * float(row["digital_resilience"])
            + 0.10 * float(row["public_finance_support"])
            + 0.04 * float(row["implementation_capacity"])
        )

        implementation_risk = (
            0.28 * (1.0 - float(row["implementation_capacity"]))
            + 0.12 * (1.0 - float(row["capital_buffer_strength"]))
            + 0.12 * (1.0 - float(row["liquidity_support"]))
            + 0.12 * (1.0 - float(row["consumer_protection_gain"]))
            + 0.10 * (1.0 - float(row["climate_risk_governance"]))
            + 0.10 * (1.0 - float(row["nonbank_oversight"]))
            + 0.08 * (1.0 - float(row["digital_resilience"]))
            + 0.08 * (1.0 - float(row["public_finance_support"]))
        )

        rows.append({
            "policy_id": row["policy_id"],
            "profile_id": row["profile_id"],
            "policy_name": row["policy_name"],
            "policy_type": row["policy_type"],
            "financial_stability_gain_score": round(stability_gain, 4),
            "implementation_risk_score": round(implementation_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["financial_stability_gain_score"]), reverse=True)
    return rows


def score_risk_indicators(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.15 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.17 * float(row["contagion_potential"])
            + 0.14 * float(row["opacity"])
            + 0.14 * float(row["recovery_difficulty"])
            + 0.14 * float(row["distributional_harm"])
            + 0.08 * (1.0 - float(row["policy_preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "systemic_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "policy_preparedness": float(row["policy_preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["systemic_risk_priority_score"]), reverse=True)
    return rows


def score_public_records(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        public_resilience = (
            0.16 * float(row["tax_capacity"])
            + 0.16 * float(row["debt_sustainability"])
            + 0.16 * float(row["adaptation_finance"])
            + 0.12 * float(row["insurance_availability"])
            + 0.16 * float(row["public_investment_capacity"])
            + 0.14 * float(row["household_protection"])
            + 0.10 * float(row["climate_risk_disclosure"])
        )

        fiscal_fragility = (
            0.18 * (1.0 - float(row["tax_capacity"]))
            + 0.18 * (1.0 - float(row["debt_sustainability"]))
            + 0.16 * (1.0 - float(row["public_investment_capacity"]))
            + 0.14 * (1.0 - float(row["adaptation_finance"]))
            + 0.12 * (1.0 - float(row["insurance_availability"]))
            + 0.12 * (1.0 - float(row["household_protection"]))
            + 0.10 * (1.0 - float(row["climate_risk_disclosure"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "public_finance_resilience_score": round(public_resilience, 4),
            "fiscal_climate_fragility_score": round(fiscal_fragility, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_finance_resilience_score"]), reverse=True)
    return rows


def simulate_stress(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        leverage = float(row["leverage"])
        liquidity = float(row["liquidity_resilience"])
        household = float(row["household_security"])
        climate = float(row["climate_exposure"])
        nonbank = float(row["nonbank_exposure"])
        digital = float(row["digital_run_risk"])
        regulation = float(row["regulatory_strength"])
        public_finance = float(row["public_finance_capacity"])
        stability = float(row["initial_stability"])
        horizon = int(row["time_horizon"])

        risk = (
            0.18 * leverage
            + 0.16 * (1.0 - liquidity)
            + 0.14 * climate
            + 0.14 * nonbank
            + 0.14 * digital
            + 0.12 * (1.0 - household)
            + 0.12 * (1.0 - regulation)
        )
        public_capacity = (
            0.34 * public_finance
            + 0.26 * regulation
            + 0.22 * household
            + 0.18 * liquidity
        )

        stability_values: list[float] = []
        risk_values: list[float] = []
        public_capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.18 if t % 8 == 0 else 0.06

                fragility_force = (
                    0.20 * leverage
                    + 0.16 * nonbank
                    + 0.16 * digital
                    + 0.14 * climate
                    + 0.12 * (1.0 - household)
                    + 0.12 * (1.0 - liquidity)
                    + 0.10 * shock
                )

                resilience_force = (
                    0.22 * liquidity
                    + 0.20 * regulation
                    + 0.18 * public_finance
                    + 0.16 * household
                    + 0.12 * (1.0 - leverage)
                    + 0.12 * (1.0 - digital)
                )

                risk = clamp(
                    risk
                    + 0.05 * shock
                    + 0.04 * fragility_force
                    - 0.04 * resilience_force,
                    0.0,
                    1.4,
                )

                public_capacity = clamp(
                    public_capacity
                    + 0.04 * public_finance
                    + 0.03 * regulation
                    + 0.02 * household
                    - 0.04 * shock
                    - 0.03 * risk,
                    0.0,
                    1.5,
                )

                stability = clamp(
                    stability
                    + 0.07 * resilience_force
                    + 0.04 * public_capacity
                    - shock
                    - 0.06 * risk
                    - 0.03 * fragility_force,
                    0.0,
                    1.8,
                )

            stability_values.append(stability)
            risk_values.append(risk)
            public_capacity_values.append(public_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "financial_stability": round(stability, 4),
                "systemic_risk": round(risk, 4),
                "public_capacity": round(public_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_financial_stability": round(stability_values[-1], 4),
            "mean_financial_stability": round(mean(stability_values), 4),
            "mean_systemic_risk": round(mean(risk_values), 4),
            "final_public_capacity": round(public_capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_financial_stability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    policy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    public_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Financial Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['financial_future_name']}**: resilience {row['financial_resilience_score']}; "
            f"systemic risk {row['systemic_risk_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Financial Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress pressure {row['financial_stress_pressure_score']}; "
            f"social fragility {row['social_financial_fragility_score']}."
        )

    lines.extend(["", "## Policy Option Scores", ""])
    for row in policy_scores:
        lines.append(
            f"- **{row['policy_name']}**: stability gain {row['financial_stability_gain_score']}; "
            f"implementation risk {row['implementation_risk_score']}."
        )

    lines.extend(["", "## Systemic Risk Indicator Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['systemic_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['policy_preparedness']}."
        )

    lines.extend(["", "## Public Finance and Climate Scores", ""])
    for row in public_scores:
        lines.append(
            f"- **{row['record_name']}**: public finance resilience {row['public_finance_resilience_score']}; "
            f"fiscal-climate fragility {row['fiscal_climate_fragility_score']}."
        )

    lines.extend(["", "## Stress Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final stability {row['final_financial_stability']}; "
            f"mean systemic risk {row['mean_systemic_risk']}; final public capacity {row['final_public_capacity']}."
        )

    avg_resilience = mean(float(row["financial_resilience_score"]) for row in profile_scores)
    avg_risk = mean(float(row["systemic_risk_score"]) for row in profile_scores)
    avg_stability = mean(float(row["final_financial_stability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Financial future profiles: {len(profile_scores)}.",
        f"- Financial scenarios: {len(scenario_scores)}.",
        f"- Policy options: {len(policy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Public finance and climate records: {len(public_scores)}.",
        f"- Average financial resilience score: {round(avg_resilience, 4)}.",
        f"- Average systemic risk score: {round(avg_risk, 4)}.",
        f"- Average final financial stability: {round(avg_stability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats financial futures as complex systems shaped by leverage, liquidity, household security, climate exposure, nonbank finance, digital run risk, regulation, public finance, consumer protection, and productive investment.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "financial_futures_systemic_risk_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "financial_system_profiles.csv")
    scenarios_raw = read_csv(DATA / "financial_scenarios.csv")
    policies_raw = read_csv(DATA / "policy_options.csv")
    risks_raw = read_csv(DATA / "risk_indicators.csv")
    public_raw = read_csv(DATA / "public_finance_climate_records.csv")
    pathways_raw = read_csv(DATA / "stress_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, policies_raw, risks_raw, public_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    policy_scores = score_policies(policies_raw)
    risk_scores = score_risk_indicators(risks_raw)
    public_scores = score_public_records(public_raw)
    trajectories, pathway_summary = simulate_stress(pathways_raw)

    write_csv(OUTPUTS / "financial_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "financial_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "policy_option_scores.csv", policy_scores)
    write_csv(OUTPUTS / "risk_indicator_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "public_finance_climate_scores.csv", public_scores)
    write_csv(OUTPUTS / "stress_pathways.csv", trajectories)
    write_csv(OUTPUTS / "stress_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, policy_scores, risk_scores, public_scores, pathway_summary)

    print(f"Financial futures systemic risk workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
