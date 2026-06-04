#!/usr/bin/env python3
"""
Standard-library workflow for Migration, Demography, and Future Societies.

Outputs:
- demographic_profile_scores.csv
- migration_demography_scenario_scores.csv
- demographic_strategy_scores.csv
- demographic_risk_priority_scores.csv
- care_urban_capacity_scores.csv
- adaptive_demographic_trajectories.csv
- adaptive_demographic_summary.csv
- migration_demography_future_societies_report.md
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


def demographic_stress_score(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["aging_pressure"])
        + 0.13 * float(row["youth_opportunity_gap"])
        + 0.12 * float(row["migration_pressure"])
        + 0.13 * (1.0 - float(row["care_capacity"]))
        + 0.12 * float(row["housing_pressure"])
        + 0.10 * (1.0 - float(row["labor_adaptation"]))
        + 0.11 * float(row["climate_mobility_exposure"])
        + 0.08 * (1.0 - float(row["social_cohesion"]))
        + 0.05 * (1.0 - float(row["gender_equity"]))
        + 0.03 * (1.0 - float(row["public_health_capacity"]))
    )


def demographic_adaptive_capacity(row: dict[str, str]) -> float:
    return (
        0.18 * float(row["care_capacity"])
        + 0.16 * float(row["labor_adaptation"])
        + 0.16 * float(row["social_cohesion"])
        + 0.13 * float(row["gender_equity"])
        + 0.13 * float(row["public_health_capacity"])
        + 0.10 * (1.0 - float(row["housing_pressure"]))
        + 0.08 * (1.0 - float(row["youth_opportunity_gap"]))
        + 0.06 * (1.0 - float(row["climate_mobility_exposure"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    care_records: list[dict[str, str]],
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

    for row in care_records:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Care/urban record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["birth_rate", "death_rate", "net_migration_rate", "aging_pressure", "youth_opportunity_gap", "migration_pressure", "care_capacity", "housing_pressure", "labor_adaptation", "climate_mobility_exposure", "social_cohesion", "gender_equity", "public_health_capacity"]),
        ("scenarios", scenarios, ["aging_shock", "youth_employment_shock", "housing_shock", "care_shock", "climate_mobility_shock", "border_restriction_pressure", "labor_shortage_pressure", "public_health_shock", "social_cohesion_stress", "rights_protection_gap"]),
        ("strategies", strategies, ["care_investment_gain", "housing_affordability_gain", "youth_opportunity_gain", "legal_mobility_gain", "labor_protection_gain", "climate_adaptation_gain", "reproductive_health_gain", "gender_equity_gain", "public_health_gain", "social_cohesion_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("care_records", care_records, ["care_workforce_capacity", "unpaid_care_burden", "eldercare_demand", "childcare_demand", "affordable_housing_supply", "urban_service_capacity", "integration_capacity", "public_health_capacity"]),
        ("pathways", pathways, ["birth_rate", "death_rate", "net_migration_rate", "aging_pressure", "youth_opportunity_gap", "care_capacity", "housing_pressure", "labor_adaptation", "climate_mobility_exposure", "social_cohesion", "initial_adaptive_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if "rate" in field:
                    if not -0.05 <= value <= 0.05:
                        errors.append(f"{dataset_name} record {row_id} field {field} outside expected rate range.")
                else:
                    if not 0.0 <= value <= 1.0:
                        errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in profiles:
        stress = demographic_stress_score(row)
        capacity = demographic_adaptive_capacity(row)
        gap = max(0.0, stress - capacity)

        if stress >= 0.70:
            profile_class = "High demographic stress"
        elif capacity >= 0.65:
            profile_class = "Stronger demographic adaptation"
        else:
            profile_class = "Mixed or transitional demographic future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "demographic_stress_score": round(stress, 4),
            "adaptive_capacity_score": round(capacity, 4),
            "adaptation_gap_score": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["demographic_stress_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        pressure = (
            0.12 * float(row["aging_shock"])
            + 0.12 * float(row["youth_employment_shock"])
            + 0.12 * float(row["housing_shock"])
            + 0.12 * float(row["care_shock"])
            + 0.13 * float(row["climate_mobility_shock"])
            + 0.10 * float(row["border_restriction_pressure"])
            + 0.09 * float(row["labor_shortage_pressure"])
            + 0.08 * float(row["public_health_shock"])
            + 0.07 * float(row["social_cohesion_stress"])
            + 0.05 * float(row["rights_protection_gap"])
        )

        humane_governance_opportunity = (
            0.14 * (1.0 - float(row["rights_protection_gap"]))
            + 0.13 * (1.0 - float(row["border_restriction_pressure"]))
            + 0.13 * (1.0 - float(row["social_cohesion_stress"]))
            + 0.12 * (1.0 - float(row["care_shock"]))
            + 0.12 * (1.0 - float(row["housing_shock"]))
            + 0.10 * (1.0 - float(row["youth_employment_shock"]))
            + 0.09 * (1.0 - float(row["public_health_shock"]))
            + 0.07 * (1.0 - float(row["climate_mobility_shock"]))
            + 0.05 * (1.0 - float(row["aging_shock"]))
            + 0.05 * (1.0 - float(row["labor_shortage_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "demographic_pressure_score": round(pressure, 4),
            "humane_governance_opportunity_score": round(humane_governance_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["demographic_pressure_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        value = (
            0.13 * float(row["care_investment_gain"])
            + 0.12 * float(row["housing_affordability_gain"])
            + 0.12 * float(row["youth_opportunity_gain"])
            + 0.12 * float(row["legal_mobility_gain"])
            + 0.11 * float(row["labor_protection_gain"])
            + 0.10 * float(row["climate_adaptation_gain"])
            + 0.09 * float(row["reproductive_health_gain"])
            + 0.08 * float(row["gender_equity_gain"])
            + 0.07 * float(row["public_health_gain"])
            + 0.04 * float(row["social_cohesion_gain"])
            + 0.02 * float(row["implementation_capacity"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.14 * float(row["social_cohesion_gain"])
            + 0.12 * float(row["care_investment_gain"])
            + 0.12 * float(row["housing_affordability_gain"])
            + 0.10 * float(row["labor_protection_gain"])
            + 0.10 * float(row["legal_mobility_gain"])
            + 0.08 * float(row["public_health_gain"])
            + 0.06 * float(row["youth_opportunity_gain"])
            + 0.05 * float(row["gender_equity_gain"])
            + 0.03 * float(row["climate_adaptation_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "demographic_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["demographic_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.15 * float(row["cascade_potential"])
            + 0.10 * float(row["visibility_gap"])
            + 0.13 * float(row["recovery_difficulty"])
            + 0.20 * float(row["distributional_harm"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "demographic_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["demographic_risk_priority_score"]), reverse=True)
    return rows


def score_care_urban_records(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        care_stress = (
            0.28 * float(row["eldercare_demand"])
            + 0.20 * float(row["childcare_demand"])
            + 0.20 * float(row["unpaid_care_burden"])
            + 0.14 * (1.0 - float(row["care_workforce_capacity"]))
            + 0.10 * (1.0 - float(row["public_health_capacity"]))
            + 0.08 * (1.0 - float(row["integration_capacity"]))
        )

        urban_absorption = (
            0.24 * float(row["affordable_housing_supply"])
            + 0.20 * float(row["urban_service_capacity"])
            + 0.18 * float(row["integration_capacity"])
            + 0.16 * float(row["public_health_capacity"])
            + 0.14 * float(row["care_workforce_capacity"])
            + 0.08 * (1.0 - float(row["unpaid_care_burden"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "care_stress_score": round(care_stress, 4),
            "urban_absorption_capacity_score": round(urban_absorption, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["care_stress_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        population = float(row["population_base"])
        birth_rate = float(row["birth_rate"])
        death_rate = float(row["death_rate"])
        net_migration_rate = float(row["net_migration_rate"])
        aging = float(row["aging_pressure"])
        youth_gap = float(row["youth_opportunity_gap"])
        care_capacity = float(row["care_capacity"])
        housing = float(row["housing_pressure"])
        labor = float(row["labor_adaptation"])
        climate = float(row["climate_mobility_exposure"])
        cohesion = float(row["social_cohesion"])
        adaptive = float(row["initial_adaptive_capacity"])
        horizon = int(row["time_horizon"])

        demographic_stress = (
            0.16 * aging
            + 0.14 * youth_gap
            + 0.14 * housing
            + 0.14 * climate
            + 0.12 * (1.0 - care_capacity)
            + 0.12 * (1.0 - labor)
            + 0.10 * (1.0 - cohesion)
            + 0.08 * min(1.0, abs(net_migration_rate) * 100.0)
        )

        care_stress = (
            0.36 * aging
            + 0.18 * youth_gap
            + 0.16 * (1.0 - care_capacity)
            + 0.12 * (1.0 - labor)
            + 0.10 * housing
            + 0.08 * (1.0 - cohesion)
        )

        mobility_pressure = (
            0.34 * climate
            + 0.18 * housing
            + 0.16 * youth_gap
            + 0.14 * (1.0 - labor)
            + 0.10 * (1.0 - cohesion)
            + 0.08 * aging
        )

        population_values: list[float] = []
        stress_values: list[float] = []
        care_values: list[float] = []
        mobility_values: list[float] = []
        adaptive_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                climate_shock = 0.004 if t % 10 == 0 else 0.0
                housing_shock = 0.003 if t % 8 == 0 else 0.0
                care_shock = 0.003 if t % 12 == 0 else 0.0

                births = population * birth_rate
                deaths = population * death_rate
                net_migration = population * (
                    net_migration_rate
                    + climate_shock * climate
                    - housing_shock * housing
                )

                population = max(0.0, population + births - deaths + net_migration)

                care_stress = clamp(
                    care_stress
                    + 0.04 * aging
                    + care_shock
                    + 0.03 * housing
                    - 0.05 * care_capacity
                    - 0.03 * labor,
                    0.0,
                    1.8,
                )

                mobility_pressure = clamp(
                    mobility_pressure
                    + 0.04 * climate
                    + 0.03 * housing
                    + climate_shock
                    - 0.03 * labor
                    - 0.03 * cohesion,
                    0.0,
                    1.8,
                )

                demographic_stress = clamp(
                    demographic_stress
                    + 0.03 * care_stress
                    + 0.03 * mobility_pressure
                    + 0.02 * youth_gap
                    + 0.02 * aging
                    - 0.04 * adaptive,
                    0.0,
                    1.8,
                )

                adaptive = clamp(
                    adaptive
                    + 0.03 * care_capacity
                    + 0.03 * labor
                    + 0.02 * cohesion
                    - 0.03 * demographic_stress
                    - 0.02 * care_stress,
                    0.0,
                    1.8,
                )

            population_values.append(population)
            stress_values.append(demographic_stress)
            care_values.append(care_stress)
            mobility_values.append(mobility_pressure)
            adaptive_values.append(adaptive)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "population": round(population, 2),
                "demographic_stress": round(demographic_stress, 4),
                "care_stress": round(care_stress, 4),
                "mobility_pressure": round(mobility_pressure, 4),
                "adaptive_capacity": round(adaptive, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_population": round(population_values[-1], 2),
            "population_change_percent": round(((population_values[-1] / population_values[0]) - 1.0) * 100.0, 2),
            "final_demographic_stress": round(stress_values[-1], 4),
            "mean_care_stress": round(mean(care_values), 4),
            "mean_mobility_pressure": round(mean(mobility_values), 4),
            "final_adaptive_capacity": round(adaptive_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_adaptive_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    care_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Demographic Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: stress {row['demographic_stress_score']}; "
            f"adaptive capacity {row['adaptive_capacity_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: demographic pressure {row['demographic_pressure_score']}; "
            f"humane governance opportunity {row['humane_governance_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['demographic_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Demographic Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['demographic_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Care and Urban Capacity Scores", ""])
    for row in care_scores:
        lines.append(
            f"- **{row['record_name']}**: care stress {row['care_stress_score']}; "
            f"urban absorption capacity {row['urban_absorption_capacity_score']}."
        )

    lines.extend(["", "## Adaptive Demographic Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final population {row['final_population']}; "
            f"population change {row['population_change_percent']}%; final stress {row['final_demographic_stress']}; "
            f"final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_stress = mean(float(row["demographic_stress_score"]) for row in profile_scores)
    avg_capacity = mean(float(row["adaptive_capacity_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["demographic_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Demographic profiles: {len(profile_scores)}.",
        f"- Scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Care/urban records: {len(care_scores)}.",
        f"- Average demographic stress score: {round(avg_stress, 4)}.",
        f"- Average adaptive capacity score: {round(avg_capacity, 4)}.",
        f"- Average strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats migration, demography, and future societies as systems shaped by aging, youth opportunity, mobility, care, housing, labor adaptation, climate exposure, gender equity, public health, social cohesion, and rights-based governance.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "migration_demography_future_societies_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "demographic_profiles.csv")
    scenarios_raw = read_csv(DATA / "migration_demography_scenarios.csv")
    strategies_raw = read_csv(DATA / "demographic_strategy_options.csv")
    risks_raw = read_csv(DATA / "demographic_risk_indicators.csv")
    care_raw = read_csv(DATA / "care_urban_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_demographic_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, care_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    care_scores = score_care_urban_records(care_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "demographic_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "migration_demography_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "demographic_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "demographic_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "care_urban_capacity_scores.csv", care_scores)
    write_csv(OUTPUTS / "adaptive_demographic_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_demographic_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, care_scores, pathway_summary)

    print(f"Migration and demographic futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
