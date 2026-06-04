#!/usr/bin/env python3
"""
Standard-library workflow for Urban Futures.

Outputs:
- urban_profile_scores.csv
- urban_scenario_scores.csv
- urban_strategy_scores.csv
- urban_risk_priority_scores.csv
- urban_governance_capacity_scores.csv
- urban_stress_pathways.csv
- urban_stress_pathway_summary.csv
- urban_futures_report.md
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


def urban_viability(row: dict[str, str]) -> float:
    return (
        0.17 * float(row["infrastructure_strength"])
        + 0.16 * float(row["governance_capacity"])
        + 0.14 * float(row["housing_affordability"])
        - 0.14 * float(row["climate_exposure"])
        - 0.14 * float(row["inequality"])
        + 0.09 * float(row["digital_integration"])
        + 0.12 * float(row["public_finance_capacity"])
        + 0.14 * float(row["social_cohesion"])
        - 0.08 * float(row["maintenance_backlog"])
    )


def urban_fragility(row: dict[str, str]) -> float:
    return (
        0.15 * float(row["climate_exposure"])
        + 0.15 * float(row["inequality"])
        + 0.14 * float(row["maintenance_backlog"])
        + 0.13 * (1.0 - float(row["infrastructure_strength"]))
        + 0.13 * (1.0 - float(row["governance_capacity"]))
        + 0.12 * (1.0 - float(row["housing_affordability"]))
        + 0.10 * (1.0 - float(row["public_finance_capacity"]))
        + 0.10 * (1.0 - float(row["social_cohesion"]))
        + 0.08 * float(row["digital_integration"])
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
        ("profiles", profiles, ["infrastructure_strength", "governance_capacity", "housing_affordability", "climate_exposure", "inequality", "digital_integration", "public_finance_capacity", "social_cohesion", "maintenance_backlog"]),
        ("scenarios", scenarios, ["infrastructure_stress", "housing_pressure", "climate_pressure", "fiscal_pressure", "digital_dependency", "migration_pressure", "governance_fragmentation", "social_fragmentation"]),
        ("strategies", strategies, ["infrastructure_gain", "housing_stability_gain", "climate_resilience_gain", "governance_gain", "finance_gain", "digital_accountability_gain", "social_cohesion_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("governance", governance, ["coordination", "participation", "public_finance", "maintenance_capacity", "digital_accountability", "housing_governance", "climate_governance"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        viability = urban_viability(row)
        fragility = urban_fragility(row)

        if viability >= 0.20 and fragility < 0.48:
            profile_class = "Stronger adaptive urban profile"
        elif fragility >= 0.62:
            profile_class = "High urban fragility"
        else:
            profile_class = "Mixed or transitional urban future"

        rows.append({
            "profile_id": row["profile_id"],
            "city_future_name": row["city_future_name"],
            "city_type": row["city_type"],
            "urban_viability_score": round(viability, 4),
            "urban_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["urban_viability_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.15 * float(row["infrastructure_stress"])
            + 0.16 * float(row["housing_pressure"])
            + 0.15 * float(row["climate_pressure"])
            + 0.12 * float(row["fiscal_pressure"])
            + 0.10 * float(row["digital_dependency"])
            + 0.10 * float(row["migration_pressure"])
            + 0.12 * float(row["governance_fragmentation"])
            + 0.10 * float(row["social_fragmentation"])
        )

        opportunity = (
            0.18 * (1.0 - float(row["governance_fragmentation"]))
            + 0.16 * (1.0 - float(row["fiscal_pressure"]))
            + 0.14 * (1.0 - float(row["infrastructure_stress"]))
            + 0.14 * (1.0 - float(row["housing_pressure"]))
            + 0.12 * (1.0 - float(row["climate_pressure"]))
            + 0.10 * (1.0 - float(row["social_fragmentation"]))
            + 0.08 * (1.0 - float(row["migration_pressure"]))
            + 0.08 * (1.0 - float(row["digital_dependency"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "urban_stress_score": round(stress, 4),
            "urban_transformation_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["urban_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.16 * float(row["infrastructure_gain"])
            + 0.16 * float(row["housing_stability_gain"])
            + 0.14 * float(row["climate_resilience_gain"])
            + 0.14 * float(row["governance_gain"])
            + 0.12 * float(row["finance_gain"])
            + 0.10 * float(row["digital_accountability_gain"])
            + 0.14 * float(row["social_cohesion_gain"])
            + 0.04 * float(row["implementation_capacity"])
        )

        readiness = (
            0.24 * float(row["implementation_capacity"])
            + 0.16 * float(row["governance_gain"])
            + 0.14 * float(row["finance_gain"])
            + 0.14 * float(row["infrastructure_gain"])
            + 0.12 * float(row["housing_stability_gain"])
            + 0.10 * float(row["climate_resilience_gain"])
            + 0.06 * float(row["social_cohesion_gain"])
            + 0.04 * float(row["digital_accountability_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "urban_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["urban_strategy_value_score"]), reverse=True)
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
            "urban_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["urban_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.16 * float(row["coordination"])
            + 0.14 * float(row["participation"])
            + 0.14 * float(row["public_finance"])
            + 0.14 * float(row["maintenance_capacity"])
            + 0.12 * float(row["digital_accountability"])
            + 0.15 * float(row["housing_governance"])
            + 0.15 * float(row["climate_governance"])
        )

        legitimacy_gap = (
            0.16 * (1.0 - float(row["participation"]))
            + 0.16 * (1.0 - float(row["coordination"]))
            + 0.14 * (1.0 - float(row["housing_governance"]))
            + 0.14 * (1.0 - float(row["climate_governance"]))
            + 0.14 * (1.0 - float(row["public_finance"]))
            + 0.12 * (1.0 - float(row["maintenance_capacity"]))
            + 0.14 * (1.0 - float(row["digital_accountability"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "urban_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["urban_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        infrastructure = float(row["infrastructure"])
        governance = float(row["governance"])
        housing = float(row["housing_stability"])
        finance = float(row["public_finance"])
        cohesion = float(row["social_cohesion"])
        climate = float(row["climate_exposure"])
        digital = float(row["digital_dependency"])
        maintenance = float(row["maintenance_backlog"])
        viability = float(row["initial_viability"])
        horizon = int(row["time_horizon"])

        system_load = (
            0.18 * climate
            + 0.14 * maintenance
            + 0.14 * (1.0 - infrastructure)
            + 0.14 * (1.0 - housing)
            + 0.12 * (1.0 - finance)
            + 0.12 * (1.0 - governance)
            + 0.10 * (1.0 - cohesion)
            + 0.06 * digital
        )

        adaptive_capacity = (
            0.20 * infrastructure
            + 0.22 * governance
            + 0.18 * finance
            + 0.16 * housing
            + 0.16 * cohesion
            + 0.08 * (1.0 - climate)
        )

        viability_values: list[float] = []
        load_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.18 if t % 8 == 0 else 0.07

                response_gain = (
                    0.18 * infrastructure
                    + 0.22 * governance
                    + 0.18 * finance
                    + 0.16 * housing
                    + 0.16 * cohesion
                    + 0.10 * (1.0 - climate)
                )

                system_load = clamp(
                    system_load
                    + 0.05 * shock
                    + 0.03 * climate
                    + 0.03 * maintenance
                    + 0.02 * digital
                    - 0.03 * infrastructure
                    - 0.03 * governance
                    - 0.02 * housing,
                    0.0,
                    1.5,
                )

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.03 * governance
                    + 0.03 * finance
                    + 0.02 * cohesion
                    + 0.02 * infrastructure
                    - 0.03 * shock,
                    0.0,
                    1.6,
                )

                viability = clamp(
                    viability
                    + 0.07 * response_gain
                    + 0.04 * adaptive_capacity
                    - shock
                    - 0.06 * system_load
                    - 0.02 * maintenance,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            load_values.append(system_load)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "urban_viability": round(viability, 4),
                "system_load": round(system_load, 4),
                "adaptive_capacity": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_urban_viability": round(viability_values[-1], 4),
            "mean_urban_viability": round(mean(viability_values), 4),
            "mean_system_load": round(mean(load_values), 4),
            "final_adaptive_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_urban_viability"]), reverse=True)
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
        "## Urban Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['city_future_name']}**: viability {row['urban_viability_score']}; "
            f"fragility {row['urban_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Urban Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['urban_stress_score']}; "
            f"transformation opportunity {row['urban_transformation_opportunity_score']}."
        )

    lines.extend(["", "## Urban Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['urban_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Urban Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['urban_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Urban Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['urban_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Urban Stress Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_urban_viability']}; "
            f"mean load {row['mean_system_load']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_viability = mean(float(row["urban_viability_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["urban_fragility_score"]) for row in profile_scores)
    avg_pathway_viability = mean(float(row["final_urban_viability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Urban future profiles: {len(profile_scores)}.",
        f"- Urban scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average urban viability score: {round(avg_viability, 4)}.",
        f"- Average urban fragility score: {round(avg_fragility, 4)}.",
        f"- Average final pathway viability: {round(avg_pathway_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats urban futures as complex systems shaped by infrastructure, housing, climate exposure, inequality, digital integration, public finance, governance, social cohesion, maintenance, and adaptive capacity.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "urban_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "urban_system_profiles.csv")
    scenarios_raw = read_csv(DATA / "urban_scenarios.csv")
    strategies_raw = read_csv(DATA / "urban_strategy_options.csv")
    risks_raw = read_csv(DATA / "urban_risk_indicators.csv")
    governance_raw = read_csv(DATA / "urban_governance_records.csv")
    pathways_raw = read_csv(DATA / "urban_stress_pathways.csv")

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

    write_csv(OUTPUTS / "urban_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "urban_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "urban_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "urban_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "urban_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "urban_stress_pathways.csv", trajectories)
    write_csv(OUTPUTS / "urban_stress_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Urban futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
