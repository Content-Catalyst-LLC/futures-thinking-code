#!/usr/bin/env python3
"""
Standard-library workflow for Food, Water, and Land-Use Futures.

Outputs:
- food_water_land_profile_scores.csv
- resource_scenario_scores.csv
- adaptation_strategy_scores.csv
- resource_risk_priority_scores.csv
- resource_governance_capacity_scores.csv
- resource_stress_pathways.csv
- resource_stress_pathway_summary.csv
- food_water_land_futures_report.md
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


def fwl_resilience(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["production_capacity"])
        + 0.16 * float(row["water_security"])
        + 0.15 * float(row["soil_health"])
        + 0.14 * float(row["biodiversity_integrity"])
        + 0.14 * float(row["governance_capacity"])
        - 0.12 * float(row["climate_exposure"])
        - 0.08 * float(row["market_vulnerability"])
        + 0.14 * float(row["justice_capacity"])
        + 0.12 * float(row["livelihood_resilience"])
    )


def fwl_fragility(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["climate_exposure"])
        + 0.14 * float(row["market_vulnerability"])
        + 0.14 * (1.0 - float(row["water_security"]))
        + 0.13 * (1.0 - float(row["soil_health"]))
        + 0.12 * (1.0 - float(row["biodiversity_integrity"]))
        + 0.12 * (1.0 - float(row["governance_capacity"]))
        + 0.10 * (1.0 - float(row["justice_capacity"]))
        + 0.06 * (1.0 - float(row["livelihood_resilience"]))
        + 0.03 * (1.0 - float(row["production_capacity"]))
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
        ("profiles", profiles, ["production_capacity", "water_security", "soil_health", "biodiversity_integrity", "governance_capacity", "climate_exposure", "market_vulnerability", "justice_capacity", "livelihood_resilience"]),
        ("scenarios", scenarios, ["food_pressure", "water_pressure", "land_pressure", "soil_degradation_pressure", "biodiversity_pressure", "climate_pressure", "market_pressure", "governance_fragmentation", "rights_conflict_pressure"]),
        ("strategies", strategies, ["production_gain", "water_gain", "soil_gain", "biodiversity_gain", "governance_gain", "justice_gain", "livelihood_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("governance", governance, ["land_rights", "water_governance", "food_security_institutions", "soil_monitoring", "biodiversity_governance", "participation", "public_finance"]),
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
        resilience = fwl_resilience(row)
        fragility = fwl_fragility(row)

        if resilience >= 0.42 and fragility < 0.48:
            profile_class = "Stronger regenerative resilience"
        elif fragility >= 0.62:
            profile_class = "High systemic fragility"
        else:
            profile_class = "Mixed or transitional pathway"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "food_water_land_resilience_score": round(resilience, 4),
            "food_water_land_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["food_water_land_resilience_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.13 * float(row["food_pressure"])
            + 0.15 * float(row["water_pressure"])
            + 0.13 * float(row["land_pressure"])
            + 0.13 * float(row["soil_degradation_pressure"])
            + 0.12 * float(row["biodiversity_pressure"])
            + 0.14 * float(row["climate_pressure"])
            + 0.09 * float(row["market_pressure"])
            + 0.06 * float(row["governance_fragmentation"])
            + 0.05 * float(row["rights_conflict_pressure"])
        )

        opportunity = (
            0.15 * (1.0 - float(row["water_pressure"]))
            + 0.15 * (1.0 - float(row["soil_degradation_pressure"]))
            + 0.14 * (1.0 - float(row["biodiversity_pressure"]))
            + 0.14 * (1.0 - float(row["governance_fragmentation"]))
            + 0.12 * (1.0 - float(row["rights_conflict_pressure"]))
            + 0.11 * (1.0 - float(row["food_pressure"]))
            + 0.09 * (1.0 - float(row["climate_pressure"]))
            + 0.06 * (1.0 - float(row["market_pressure"]))
            + 0.04 * (1.0 - float(row["land_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "resource_stress_score": round(stress, 4),
            "resource_transformation_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["resource_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.12 * float(row["production_gain"])
            + 0.16 * float(row["water_gain"])
            + 0.16 * float(row["soil_gain"])
            + 0.15 * float(row["biodiversity_gain"])
            + 0.14 * float(row["governance_gain"])
            + 0.15 * float(row["justice_gain"])
            + 0.08 * float(row["livelihood_gain"])
            + 0.04 * float(row["implementation_capacity"])
        )

        readiness = (
            0.24 * float(row["implementation_capacity"])
            + 0.16 * float(row["governance_gain"])
            + 0.14 * float(row["justice_gain"])
            + 0.12 * float(row["water_gain"])
            + 0.12 * float(row["soil_gain"])
            + 0.10 * float(row["livelihood_gain"])
            + 0.08 * float(row["production_gain"])
            + 0.04 * float(row["biodiversity_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "resource_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["resource_strategy_value_score"]), reverse=True)
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
            "resource_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["resource_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.15 * float(row["land_rights"])
            + 0.17 * float(row["water_governance"])
            + 0.15 * float(row["food_security_institutions"])
            + 0.13 * float(row["soil_monitoring"])
            + 0.14 * float(row["biodiversity_governance"])
            + 0.14 * float(row["participation"])
            + 0.12 * float(row["public_finance"])
        )

        legitimacy_gap = (
            0.18 * (1.0 - float(row["participation"]))
            + 0.17 * (1.0 - float(row["land_rights"]))
            + 0.15 * (1.0 - float(row["water_governance"]))
            + 0.14 * (1.0 - float(row["food_security_institutions"]))
            + 0.13 * (1.0 - float(row["biodiversity_governance"]))
            + 0.12 * (1.0 - float(row["public_finance"]))
            + 0.11 * (1.0 - float(row["soil_monitoring"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "resource_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["resource_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        production = float(row["production"])
        water = float(row["water_security"])
        soil = float(row["soil_health"])
        biodiversity = float(row["biodiversity"])
        governance = float(row["governance"])
        justice = float(row["justice"])
        livelihoods = float(row["livelihood_resilience"])
        climate = float(row["climate_exposure"])
        market = float(row["market_vulnerability"])
        resilience = float(row["initial_resilience"])
        horizon = int(row["time_horizon"])

        resource_stress = (
            0.18 * climate
            + 0.15 * market
            + 0.15 * (1.0 - water)
            + 0.13 * (1.0 - soil)
            + 0.12 * (1.0 - biodiversity)
            + 0.12 * (1.0 - governance)
            + 0.10 * (1.0 - justice)
            + 0.05 * (1.0 - livelihoods)
        )

        adaptive_capacity = (
            0.18 * governance
            + 0.18 * justice
            + 0.16 * water
            + 0.16 * soil
            + 0.14 * biodiversity
            + 0.10 * production
            + 0.08 * livelihoods
        )

        resilience_values: list[float] = []
        stress_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.18 if t % 8 == 0 else 0.06

                regeneration = (
                    0.18 * soil
                    + 0.18 * water
                    + 0.16 * biodiversity
                    + 0.16 * governance
                    + 0.14 * justice
                    + 0.10 * production
                    + 0.08 * livelihoods
                )

                resource_stress = clamp(
                    resource_stress
                    + 0.05 * shock
                    + 0.04 * climate
                    + 0.03 * market
                    - 0.04 * water
                    - 0.03 * soil
                    - 0.03 * governance
                    - 0.02 * justice,
                    0.0,
                    1.6,
                )

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.03 * governance
                    + 0.03 * justice
                    + 0.02 * soil
                    + 0.02 * biodiversity
                    + 0.02 * livelihoods
                    - 0.03 * shock,
                    0.0,
                    1.6,
                )

                resilience = clamp(
                    resilience
                    + 0.06 * regeneration
                    + 0.04 * adaptive_capacity
                    - shock
                    - 0.06 * resource_stress,
                    0.0,
                    1.8,
                )

            resilience_values.append(resilience)
            stress_values.append(resource_stress)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "food_water_land_resilience": round(resilience, 4),
                "resource_stress": round(resource_stress, 4),
                "adaptive_capacity": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_resilience": round(resilience_values[-1], 4),
            "mean_resilience": round(mean(resilience_values), 4),
            "mean_resource_stress": round(mean(stress_values), 4),
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
        "## Food-Water-Land Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: resilience {row['food_water_land_resilience_score']}; "
            f"fragility {row['food_water_land_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Resource Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['resource_stress_score']}; "
            f"transformation opportunity {row['resource_transformation_opportunity_score']}."
        )

    lines.extend(["", "## Adaptation Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['resource_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Resource Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['resource_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Resource Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['resource_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Resource Stress Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final resilience {row['final_resilience']}; "
            f"mean stress {row['mean_resource_stress']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_resilience = mean(float(row["food_water_land_resilience_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["food_water_land_fragility_score"]) for row in profile_scores)
    avg_pathway_resilience = mean(float(row["final_resilience"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Food-water-land profiles: {len(profile_scores)}.",
        f"- Resource scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average resilience score: {round(avg_resilience, 4)}.",
        f"- Average fragility score: {round(avg_fragility, 4)}.",
        f"- Average final pathway resilience: {round(avg_pathway_resilience, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats food, water, and land-use futures as coupled social-ecological systems shaped by production, water, soil, biodiversity, governance, climate exposure, markets, justice, livelihoods, and adaptive capacity.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "food_water_land_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "food_water_land_profiles.csv")
    scenarios_raw = read_csv(DATA / "resource_scenarios.csv")
    strategies_raw = read_csv(DATA / "adaptation_strategy_options.csv")
    risks_raw = read_csv(DATA / "resource_risk_indicators.csv")
    governance_raw = read_csv(DATA / "resource_governance_records.csv")
    pathways_raw = read_csv(DATA / "resource_stress_pathways.csv")

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

    write_csv(OUTPUTS / "food_water_land_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "resource_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "adaptation_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "resource_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "resource_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "resource_stress_pathways.csv", trajectories)
    write_csv(OUTPUTS / "resource_stress_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Food-water-land futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
