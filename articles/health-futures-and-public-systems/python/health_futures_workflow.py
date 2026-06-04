#!/usr/bin/env python3
"""
Standard-library workflow for Health Futures and Public Systems.

Outputs:
- health_system_profile_scores.csv
- health_scenario_scores.csv
- health_strategy_scores.csv
- health_risk_priority_scores.csv
- health_governance_capacity_scores.csv
- health_stress_pathways.csv
- health_stress_pathway_summary.csv
- health_futures_report.md
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


def health_resilience(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["prevention_capacity"])
        + 0.12 * float(row["healthcare_access"])
        + 0.15 * float(row["public_health_infrastructure"])
        + 0.10 * float(row["climate_readiness"])
        + 0.11 * float(row["workforce_resilience"])
        + 0.08 * float(row["technology_governance"])
        + 0.11 * float(row["social_protection"])
        + 0.08 * float(row["public_trust"])
        + 0.07 * float(row["equity_capacity"])
        + 0.05 * float(row["care_capacity"])
    )


def health_fragility(row: dict[str, str]) -> float:
    return (
        0.13 * (1.0 - float(row["prevention_capacity"]))
        + 0.12 * (1.0 - float(row["healthcare_access"]))
        + 0.15 * (1.0 - float(row["public_health_infrastructure"]))
        + 0.11 * (1.0 - float(row["climate_readiness"]))
        + 0.13 * (1.0 - float(row["workforce_resilience"]))
        + 0.08 * (1.0 - float(row["technology_governance"]))
        + 0.10 * (1.0 - float(row["social_protection"]))
        + 0.08 * (1.0 - float(row["public_trust"]))
        + 0.06 * (1.0 - float(row["equity_capacity"]))
        + 0.04 * (1.0 - float(row["care_capacity"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    governance: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing profile {row['profile_id']}.")

    for row in risks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Risk indicator {row['risk_id']} references missing scenario {row['scenario_id']}.")

    for row in governance:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Governance record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["prevention_capacity", "healthcare_access", "public_health_infrastructure", "climate_readiness", "workforce_resilience", "technology_governance", "social_protection", "public_trust", "equity_capacity", "care_capacity"]),
        ("scenarios", scenarios, ["disease_burden_pressure", "climate_health_pressure", "biological_risk_pressure", "workforce_pressure", "care_pressure", "chronic_disease_pressure", "mental_health_pressure", "technology_governance_pressure", "trust_pressure", "equity_pressure"]),
        ("strategies", strategies, ["prevention_gain", "access_gain", "public_health_gain", "climate_health_gain", "workforce_gain", "technology_governance_gain", "social_protection_gain", "trust_gain", "equity_gain", "care_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("governance", governance, ["monitoring_capacity", "public_health_finance", "workforce_capacity", "community_participation", "technology_accountability", "equity_safeguards", "emergency_coordination", "care_system_capacity"]),
        ("pathways", pathways, ["prevention", "healthcare_access", "public_health", "climate_readiness", "workforce", "social_protection", "public_trust", "equity", "care_capacity", "initial_resilience"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        resilience = health_resilience(row)
        fragility = health_fragility(row)

        if resilience >= 0.70 and fragility < 0.35:
            profile_class = "Stronger public health resilience"
        elif fragility >= 0.55:
            profile_class = "High health system fragility"
        else:
            profile_class = "Mixed or transitional health future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "public_health_resilience_score": round(resilience, 4),
            "health_system_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_health_resilience_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.12 * float(row["disease_burden_pressure"])
            + 0.13 * float(row["climate_health_pressure"])
            + 0.13 * float(row["biological_risk_pressure"])
            + 0.13 * float(row["workforce_pressure"])
            + 0.11 * float(row["care_pressure"])
            + 0.11 * float(row["chronic_disease_pressure"])
            + 0.10 * float(row["mental_health_pressure"])
            + 0.07 * float(row["technology_governance_pressure"])
            + 0.05 * float(row["trust_pressure"])
            + 0.05 * float(row["equity_pressure"])
        )

        opportunity = (
            0.14 * (1.0 - float(row["disease_burden_pressure"]))
            + 0.13 * (1.0 - float(row["workforce_pressure"]))
            + 0.13 * (1.0 - float(row["climate_health_pressure"]))
            + 0.12 * (1.0 - float(row["biological_risk_pressure"]))
            + 0.12 * (1.0 - float(row["care_pressure"]))
            + 0.10 * (1.0 - float(row["trust_pressure"]))
            + 0.10 * (1.0 - float(row["equity_pressure"]))
            + 0.08 * (1.0 - float(row["chronic_disease_pressure"]))
            + 0.05 * (1.0 - float(row["mental_health_pressure"]))
            + 0.03 * (1.0 - float(row["technology_governance_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "health_system_stress_score": round(stress, 4),
            "health_transformation_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["health_system_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.13 * float(row["prevention_gain"])
            + 0.12 * float(row["access_gain"])
            + 0.14 * float(row["public_health_gain"])
            + 0.11 * float(row["climate_health_gain"])
            + 0.11 * float(row["workforce_gain"])
            + 0.08 * float(row["technology_governance_gain"])
            + 0.10 * float(row["social_protection_gain"])
            + 0.08 * float(row["trust_gain"])
            + 0.08 * float(row["equity_gain"])
            + 0.04 * float(row["care_gain"])
            + 0.01 * float(row["implementation_capacity"])
        )

        readiness = (
            0.22 * float(row["implementation_capacity"])
            + 0.14 * float(row["workforce_gain"])
            + 0.13 * float(row["public_health_gain"])
            + 0.12 * float(row["trust_gain"])
            + 0.11 * float(row["equity_gain"])
            + 0.10 * float(row["access_gain"])
            + 0.08 * float(row["social_protection_gain"])
            + 0.06 * float(row["prevention_gain"])
            + 0.04 * float(row["technology_governance_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "health_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["health_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.17 * float(row["cascade_potential"])
            + 0.12 * float(row["visibility_gap"])
            + 0.14 * float(row["recovery_difficulty"])
            + 0.17 * float(row["distributional_harm"])
            + 0.08 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "health_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["health_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.15 * float(row["monitoring_capacity"])
            + 0.15 * float(row["public_health_finance"])
            + 0.14 * float(row["workforce_capacity"])
            + 0.13 * float(row["community_participation"])
            + 0.11 * float(row["technology_accountability"])
            + 0.13 * float(row["equity_safeguards"])
            + 0.11 * float(row["emergency_coordination"])
            + 0.08 * float(row["care_system_capacity"])
        )

        legitimacy_gap = (
            0.17 * (1.0 - float(row["community_participation"]))
            + 0.16 * (1.0 - float(row["equity_safeguards"]))
            + 0.14 * (1.0 - float(row["public_health_finance"]))
            + 0.13 * (1.0 - float(row["monitoring_capacity"]))
            + 0.12 * (1.0 - float(row["workforce_capacity"]))
            + 0.10 * (1.0 - float(row["technology_accountability"]))
            + 0.10 * (1.0 - float(row["emergency_coordination"]))
            + 0.08 * (1.0 - float(row["care_system_capacity"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "health_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["health_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        prevention = float(row["prevention"])
        access = float(row["healthcare_access"])
        public_health = float(row["public_health"])
        climate = float(row["climate_readiness"])
        workforce = float(row["workforce"])
        social = float(row["social_protection"])
        trust = float(row["public_trust"])
        equity = float(row["equity"])
        care = float(row["care_capacity"])
        resilience = float(row["initial_resilience"])
        horizon = int(row["time_horizon"])

        system_stress = (
            0.15 * (1.0 - prevention)
            + 0.13 * (1.0 - access)
            + 0.15 * (1.0 - public_health)
            + 0.13 * (1.0 - climate)
            + 0.13 * (1.0 - workforce)
            + 0.10 * (1.0 - social)
            + 0.08 * (1.0 - trust)
            + 0.08 * (1.0 - equity)
            + 0.05 * (1.0 - care)
        )

        adaptive_capacity = (
            0.15 * prevention
            + 0.13 * access
            + 0.18 * public_health
            + 0.11 * climate
            + 0.13 * workforce
            + 0.10 * social
            + 0.08 * trust
            + 0.08 * equity
            + 0.04 * care
        )

        resilience_values: list[float] = []
        stress_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.18 if t % 8 == 0 else 0.06
                biological_shock = 0.11 if t % 13 == 0 else 0.0
                care_shock = 0.06 * (1.0 - care) if t % 10 == 0 else 0.0

                learning_gain = (
                    0.17 * public_health
                    + 0.15 * prevention
                    + 0.13 * workforce
                    + 0.13 * trust
                    + 0.13 * equity
                    + 0.11 * access
                    + 0.10 * social
                    + 0.08 * care
                )

                compound_penalty = (
                    0.04 * (1.0 - climate)
                    + 0.04 * (1.0 - workforce)
                    + 0.03 * (1.0 - public_health)
                    + 0.03 * (1.0 - social)
                    + 0.02 * (1.0 - care)
                )

                system_stress = clamp(
                    system_stress
                    + 0.05 * shock
                    + 0.06 * biological_shock
                    + care_shock
                    + compound_penalty
                    - 0.04 * prevention
                    - 0.03 * public_health
                    - 0.03 * social
                    - 0.02 * trust,
                    0.0,
                    1.6,
                )

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.03 * public_health
                    + 0.03 * workforce
                    + 0.02 * trust
                    + 0.02 * equity
                    + 0.02 * prevention
                    + 0.01 * care
                    - 0.03 * shock
                    - 0.02 * biological_shock
                    - 0.02 * system_stress,
                    0.0,
                    1.6,
                )

                resilience = clamp(
                    resilience
                    + 0.05 * learning_gain
                    + 0.04 * adaptive_capacity
                    - shock
                    - biological_shock
                    - care_shock
                    - 0.06 * system_stress,
                    0.0,
                    1.8,
                )

            resilience_values.append(resilience)
            stress_values.append(system_stress)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "public_health_resilience": round(resilience, 4),
                "system_stress": round(system_stress, 4),
                "adaptive_capacity": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_resilience": round(resilience_values[-1], 4),
            "mean_resilience": round(mean(resilience_values), 4),
            "mean_system_stress": round(mean(stress_values), 4),
            "final_adaptive_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_resilience"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    governance_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Health System Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: resilience {row['public_health_resilience_score']}; "
            f"fragility {row['health_system_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Health Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['health_system_stress_score']}; "
            f"transformation opportunity {row['health_transformation_opportunity_score']}."
        )

    lines.extend(["", "## Health Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['health_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Health Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['health_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Health Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['health_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Health Stress Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final resilience {row['final_resilience']}; "
            f"mean stress {row['mean_system_stress']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_resilience = mean(float(row["public_health_resilience_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["health_system_fragility_score"]) for row in profile_scores)
    avg_pathway_resilience = mean(float(row["final_resilience"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Health system profiles: {len(profile_scores)}.",
        f"- Health scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average public health resilience score: {round(avg_resilience, 4)}.",
        f"- Average health system fragility score: {round(avg_fragility, 4)}.",
        f"- Average final pathway resilience: {round(avg_pathway_resilience, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats health futures as public systems shaped by prevention, healthcare access, public health infrastructure, climate readiness, workforce resilience, technology governance, social protection, public trust, equity, care capacity, and adaptive capacity.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "health_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "health_system_profiles.csv")
    scenarios_raw = read_csv(DATA / "health_futures_scenarios.csv")
    strategies_raw = read_csv(DATA / "health_strategy_options.csv")
    risks_raw = read_csv(DATA / "health_risk_indicators.csv")
    governance_raw = read_csv(DATA / "health_governance_records.csv")
    pathways_raw = read_csv(DATA / "health_stress_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, governance_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    governance_scores = score_governance(governance_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "health_system_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "health_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "health_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "health_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "health_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "health_stress_pathways.csv", trajectories)
    write_csv(OUTPUTS / "health_stress_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Health futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
