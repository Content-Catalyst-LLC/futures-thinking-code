#!/usr/bin/env python3
"""
Standard-library workflow for Global Governance Futures.

Outputs:
- governance_profile_scores.csv
- governance_scenario_scores.csv
- governance_strategy_scores.csv
- governance_risk_priority_scores.csv
- institutional_capacity_scores.csv
- adaptive_governance_trajectories.csv
- adaptive_governance_summary.csv
- global_governance_futures_report.md
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


def governance_capacity(row: dict[str, str]) -> float:
    return (
        0.14 * float(row["institutional_capacity"])
        + 0.16 * float(row["legitimacy"])
        + 0.12 * float(row["legal_authority"])
        + 0.11 * float(row["finance_capacity"])
        + 0.13 * float(row["collective_action"])
        + 0.10 * float(row["technology_governance"])
        + 0.10 * float(row["planetary_risk_coordination"])
        + 0.08 * float(row["adaptive_learning"])
        + 0.08 * float(row["public_accountability"])
        + 0.08 * float(row["representation_equity"])
    )


def legitimacy_gap(row: dict[str, str]) -> float:
    return (
        0.18 * (1.0 - float(row["legitimacy"]))
        + 0.14 * (1.0 - float(row["representation_equity"]))
        + 0.13 * (1.0 - float(row["public_accountability"]))
        + 0.12 * (1.0 - float(row["legal_authority"]))
        + 0.11 * (1.0 - float(row["collective_action"]))
        + 0.10 * (1.0 - float(row["finance_capacity"]))
        + 0.08 * (1.0 - float(row["institutional_capacity"]))
        + 0.07 * (1.0 - float(row["technology_governance"]))
        + 0.04 * (1.0 - float(row["planetary_risk_coordination"]))
        + 0.03 * (1.0 - float(row["adaptive_learning"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    records: list[dict[str, str]],
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

    for row in records:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Institutional record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["institutional_capacity", "legitimacy", "legal_authority", "finance_capacity", "collective_action", "technology_governance", "planetary_risk_coordination", "adaptive_learning", "public_accountability", "representation_equity"]),
        ("scenarios", scenarios, ["climate_stress", "health_stress", "finance_stress", "technology_stress", "migration_stress", "security_stress", "legitimacy_stress", "institutional_fragmentation", "private_power_pressure", "civil_society_constraint"]),
        ("strategies", strategies, ["representation_gain", "finance_gain", "legal_accountability_gain", "climate_governance_gain", "health_governance_gain", "technology_governance_gain", "migration_protection_gain", "security_coordination_gain", "civil_society_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("records", records, ["diplomatic_capacity", "monitoring_capacity", "finance_capacity", "legal_accountability", "scientific_capacity", "implementation_capacity", "public_accountability", "civil_society_space"]),
        ("pathways", pathways, ["initial_governance_capacity", "institutional_capacity", "legitimacy", "legal_authority", "finance_capacity", "collective_action", "technology_governance", "planetary_coordination", "adaptive_learning", "public_accountability", "system_stress"]),
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
        capacity = governance_capacity(row)
        gap = legitimacy_gap(row)

        if capacity >= 0.70 and gap < 0.35:
            profile_class = "Stronger governance capacity"
        elif gap >= 0.60:
            profile_class = "High legitimacy and capacity gap"
        else:
            profile_class = "Mixed or transitional governance future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["governance_capacity_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.12 * float(row["climate_stress"])
            + 0.10 * float(row["health_stress"])
            + 0.10 * float(row["finance_stress"])
            + 0.11 * float(row["technology_stress"])
            + 0.08 * float(row["migration_stress"])
            + 0.10 * float(row["security_stress"])
            + 0.13 * float(row["legitimacy_stress"])
            + 0.12 * float(row["institutional_fragmentation"])
            + 0.09 * float(row["private_power_pressure"])
            + 0.05 * float(row["civil_society_constraint"])
        )

        cooperation_opportunity = (
            0.15 * (1.0 - float(row["legitimacy_stress"]))
            + 0.14 * (1.0 - float(row["institutional_fragmentation"]))
            + 0.12 * (1.0 - float(row["civil_society_constraint"]))
            + 0.11 * (1.0 - float(row["private_power_pressure"]))
            + 0.10 * (1.0 - float(row["security_stress"]))
            + 0.10 * (1.0 - float(row["technology_stress"]))
            + 0.09 * (1.0 - float(row["finance_stress"]))
            + 0.08 * (1.0 - float(row["climate_stress"]))
            + 0.06 * (1.0 - float(row["health_stress"]))
            + 0.05 * (1.0 - float(row["migration_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "global_governance_stress_score": round(stress, 4),
            "cooperation_opportunity_score": round(cooperation_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["global_governance_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.13 * float(row["representation_gain"])
            + 0.12 * float(row["finance_gain"])
            + 0.12 * float(row["legal_accountability_gain"])
            + 0.11 * float(row["climate_governance_gain"])
            + 0.09 * float(row["health_governance_gain"])
            + 0.10 * float(row["technology_governance_gain"])
            + 0.08 * float(row["migration_protection_gain"])
            + 0.08 * float(row["security_coordination_gain"])
            + 0.08 * float(row["civil_society_gain"])
            + 0.04 * float(row["implementation_capacity"])
            + 0.05 * float(row["public_legitimacy_gain"])
        )

        readiness = (
            0.22 * float(row["implementation_capacity"])
            + 0.16 * float(row["public_legitimacy_gain"])
            + 0.12 * float(row["finance_gain"])
            + 0.11 * float(row["representation_gain"])
            + 0.10 * float(row["legal_accountability_gain"])
            + 0.08 * float(row["civil_society_gain"])
            + 0.07 * float(row["climate_governance_gain"])
            + 0.06 * float(row["technology_governance_gain"])
            + 0.04 * float(row["health_governance_gain"])
            + 0.04 * float(row["security_coordination_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "governance_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["governance_strategy_value_score"]), reverse=True)
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
            "governance_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["governance_risk_priority_score"]), reverse=True)
    return rows


def score_institutional_records(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.14 * float(row["diplomatic_capacity"])
            + 0.13 * float(row["monitoring_capacity"])
            + 0.13 * float(row["finance_capacity"])
            + 0.13 * float(row["legal_accountability"])
            + 0.13 * float(row["scientific_capacity"])
            + 0.12 * float(row["implementation_capacity"])
            + 0.12 * float(row["public_accountability"])
            + 0.10 * float(row["civil_society_space"])
        )

        accountability_gap = (
            0.18 * (1.0 - float(row["public_accountability"]))
            + 0.16 * (1.0 - float(row["civil_society_space"]))
            + 0.14 * (1.0 - float(row["legal_accountability"]))
            + 0.13 * (1.0 - float(row["implementation_capacity"]))
            + 0.11 * (1.0 - float(row["finance_capacity"]))
            + 0.10 * (1.0 - float(row["monitoring_capacity"]))
            + 0.10 * (1.0 - float(row["diplomatic_capacity"]))
            + 0.08 * (1.0 - float(row["scientific_capacity"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "institutional_capacity_score": round(capacity, 4),
            "accountability_gap_score": round(accountability_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["institutional_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        governance_state = float(row["initial_governance_capacity"])
        institutional = float(row["institutional_capacity"])
        legitimacy = float(row["legitimacy"])
        law = float(row["legal_authority"])
        finance = float(row["finance_capacity"])
        collective = float(row["collective_action"])
        tech = float(row["technology_governance"])
        planetary = float(row["planetary_coordination"])
        learning = float(row["adaptive_learning"])
        accountability = float(row["public_accountability"])
        stress = float(row["system_stress"])
        horizon = int(row["time_horizon"])

        legitimacy_state = (
            0.28 * legitimacy
            + 0.18 * collective
            + 0.16 * law
            + 0.14 * finance
            + 0.14 * accountability
            + 0.10 * learning
        )

        adaptive_state = (
            0.26 * learning
            + 0.16 * institutional
            + 0.14 * legitimacy
            + 0.12 * finance
            + 0.12 * collective
            + 0.12 * planetary
            + 0.08 * accountability
        )

        capacity_values: list[float] = []
        stress_values: list[float] = []
        legitimacy_values: list[float] = []
        adaptive_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                ordinary_stress = 0.05
                climate_shock = 0.12 if t % 8 == 0 else 0.0
                health_shock = 0.10 if t % 11 == 0 else 0.0
                finance_shock = 0.09 if t % 13 == 0 else 0.0
                technology_shock = 0.08 if t % 9 == 0 else 0.0
                migration_security_shock = 0.07 if t % 10 == 0 else 0.0

                shock_total = ordinary_stress + climate_shock + health_shock + finance_shock + technology_shock + migration_security_shock

                coordination_response = (
                    0.05 * institutional
                    + 0.05 * collective
                    + 0.04 * finance
                    + 0.04 * planetary
                    + 0.03 * tech
                    + 0.03 * law
                    + 0.02 * accountability
                )

                legitimacy_response = (
                    0.04 * legitimacy
                    + 0.04 * collective
                    + 0.03 * finance
                    + 0.03 * learning
                    + 0.03 * accountability
                )

                stress = clamp(
                    stress
                    + shock_total
                    + 0.04 * (1.0 - collective)
                    + 0.04 * (1.0 - finance)
                    + 0.03 * (1.0 - legitimacy)
                    + 0.03 * (1.0 - accountability)
                    - coordination_response,
                    0.0,
                    1.8,
                )

                adaptive_state = clamp(
                    adaptive_state
                    + 0.04 * learning
                    + 0.03 * institutional
                    + 0.03 * legitimacy
                    + 0.02 * tech
                    + 0.02 * accountability
                    - 0.03 * stress,
                    0.0,
                    1.8,
                )

                legitimacy_state = clamp(
                    legitimacy_state
                    + legitimacy_response
                    - 0.04 * stress
                    - 0.03 * (1.0 - law)
                    - 0.02 * (1.0 - accountability),
                    0.0,
                    1.8,
                )

                governance_state = clamp(
                    governance_state
                    + 0.05 * adaptive_state
                    + 0.04 * legitimacy_state
                    + 0.03 * institutional
                    + 0.02 * finance
                    - 0.06 * stress
                    - 0.02 * shock_total,
                    0.0,
                    1.8,
                )

            capacity_values.append(governance_state)
            stress_values.append(stress)
            legitimacy_values.append(legitimacy_state)
            adaptive_values.append(adaptive_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "governance_capacity": round(governance_state, 4),
                "system_stress": round(stress, 4),
                "legitimacy": round(legitimacy_state, 4),
                "adaptive_learning": round(adaptive_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_governance_capacity": round(capacity_values[-1], 4),
            "mean_governance_capacity": round(mean(capacity_values), 4),
            "mean_system_stress": round(mean(stress_values), 4),
            "final_legitimacy": round(legitimacy_values[-1], 4),
            "final_adaptive_learning": round(adaptive_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_governance_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    institutional_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Governance Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: capacity {row['governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['global_governance_stress_score']}; "
            f"cooperation opportunity {row['cooperation_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['governance_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['governance_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Institutional Capacity Scores", ""])
    for row in institutional_scores:
        lines.append(
            f"- **{row['record_name']}**: institutional capacity {row['institutional_capacity_score']}; "
            f"accountability gap {row['accountability_gap_score']}."
        )

    lines.extend(["", "## Adaptive Governance Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final capacity {row['final_governance_capacity']}; "
            f"mean stress {row['mean_system_stress']}; final legitimacy {row['final_legitimacy']}."
        )

    avg_capacity = mean(float(row["governance_capacity_score"]) for row in profile_scores)
    avg_gap = mean(float(row["legitimacy_gap_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["governance_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Governance profiles: {len(profile_scores)}.",
        f"- Scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Institutional records: {len(institutional_scores)}.",
        f"- Average governance capacity score: {round(avg_capacity, 4)}.",
        f"- Average legitimacy gap score: {round(avg_gap, 4)}.",
        f"- Average strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats global governance futures as institutional systems shaped by capacity, legitimacy, law, finance, collective action, technology governance, planetary risk coordination, adaptive learning, accountability, and representation.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "global_governance_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "governance_profiles.csv")
    scenarios_raw = read_csv(DATA / "governance_scenarios.csv")
    strategies_raw = read_csv(DATA / "governance_strategy_options.csv")
    risks_raw = read_csv(DATA / "governance_risk_indicators.csv")
    records_raw = read_csv(DATA / "institutional_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_governance_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, records_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    institutional_scores = score_institutional_records(records_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "governance_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "governance_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "governance_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "governance_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "institutional_capacity_scores.csv", institutional_scores)
    write_csv(OUTPUTS / "adaptive_governance_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_governance_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, institutional_scores, pathway_summary)

    print(f"Global governance futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
