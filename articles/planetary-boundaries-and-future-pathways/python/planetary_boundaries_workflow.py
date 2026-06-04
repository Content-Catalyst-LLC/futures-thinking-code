#!/usr/bin/env python3
"""
Standard-library workflow for Planetary Boundaries and Future Pathways.

Outputs:
- planetary_pathway_scores.csv
- boundary_scenario_scores.csv
- pathway_strategy_scores.csv
- planetary_risk_priority_scores.csv
- planetary_governance_capacity_scores.csv
- planetary_pathway_simulation_paths.csv
- planetary_pathway_simulation_summary.csv
- planetary_boundaries_report.md
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


def boundary_pressure(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["climate_pressure"])
        + 0.16 * float(row["biosphere_pressure"])
        + 0.12 * float(row["land_pressure"])
        + 0.12 * float(row["freshwater_pressure"])
        + 0.10 * float(row["nutrient_pressure"])
        + 0.10 * float(row["ocean_pressure"])
        + 0.08 * float(row["aerosol_pressure"])
        + 0.10 * float(row["novel_entity_pressure"])
        + 0.06 * float(row["technology_dependence"])
    )


def safe_and_just_score(row: dict[str, str]) -> float:
    pressure = boundary_pressure(row)
    return (
        0.22 * float(row["social_foundation_security"])
        + 0.20 * float(row["governance_capacity"])
        + 0.20 * float(row["justice_capacity"])
        + 0.14 * float(row["regeneration_capacity"])
        - 0.20 * pressure
        + 0.04 * (1.0 - float(row["technology_dependence"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    governance: list[dict[str, str]],
    simulations: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    pathway_ids = {row["pathway_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["pathway_id"] not in pathway_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing pathway {row['pathway_id']}.")

    for row in risks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Risk indicator {row['risk_id']} references missing scenario {row['scenario_id']}.")

    for row in governance:
        if row["pathway_id"] not in pathway_ids:
            errors.append(f"Governance record {row['record_id']} references missing pathway {row['pathway_id']}.")

    for row in simulations:
        if row["pathway_id"] not in pathway_ids:
            errors.append(f"Simulation {row['simulation_id']} references missing pathway {row['pathway_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Simulation {row['simulation_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["climate_pressure", "biosphere_pressure", "land_pressure", "freshwater_pressure", "nutrient_pressure", "ocean_pressure", "aerosol_pressure", "novel_entity_pressure", "social_foundation_security", "governance_capacity", "justice_capacity", "technology_dependence", "regeneration_capacity"]),
        ("scenarios", scenarios, ["climate_stress", "biosphere_stress", "land_stress", "freshwater_stress", "nutrient_stress", "ocean_stress", "aerosol_stress", "novel_entity_stress", "social_stress", "governance_fragmentation"]),
        ("strategies", strategies, ["climate_reduction", "biosphere_recovery", "land_restoration", "water_security", "nutrient_circularity", "novel_entity_control", "social_foundation_gain", "governance_gain", "justice_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("governance", governance, ["monitoring_capacity", "policy_coordination", "public_finance", "participation", "justice_safeguards", "international_cooperation", "implementation_capacity"]),
        ("simulations", simulations, ["boundary_pressure", "social_foundations", "governance", "justice", "technology_dependence", "regeneration", "initial_viability"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("pathway_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or row.get("simulation_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_pathways(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        pressure = boundary_pressure(row)
        score = safe_and_just_score(row)

        if score >= 0.30 and pressure < 0.48:
            profile_class = "Stronger safe-and-just pathway"
        elif pressure >= 0.70:
            profile_class = "High planetary overshoot risk"
        else:
            profile_class = "Mixed or transitional planetary pathway"

        rows.append({
            "pathway_id": row["pathway_id"],
            "pathway_name": row["pathway_name"],
            "pathway_type": row["pathway_type"],
            "total_boundary_pressure_score": round(pressure, 4),
            "safe_and_just_pathway_score": round(score, 4),
            "pathway_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["safe_and_just_pathway_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.16 * float(row["climate_stress"])
            + 0.16 * float(row["biosphere_stress"])
            + 0.12 * float(row["land_stress"])
            + 0.12 * float(row["freshwater_stress"])
            + 0.10 * float(row["nutrient_stress"])
            + 0.10 * float(row["ocean_stress"])
            + 0.08 * float(row["aerosol_stress"])
            + 0.10 * float(row["novel_entity_stress"])
            + 0.08 * float(row["social_stress"])
            + 0.08 * float(row["governance_fragmentation"])
        )

        opportunity = (
            0.16 * (1.0 - float(row["climate_stress"]))
            + 0.16 * (1.0 - float(row["biosphere_stress"]))
            + 0.12 * (1.0 - float(row["freshwater_stress"]))
            + 0.12 * (1.0 - float(row["land_stress"]))
            + 0.10 * (1.0 - float(row["nutrient_stress"]))
            + 0.10 * (1.0 - float(row["novel_entity_stress"]))
            + 0.10 * (1.0 - float(row["social_stress"]))
            + 0.10 * (1.0 - float(row["governance_fragmentation"]))
            + 0.04 * (1.0 - float(row["ocean_stress"]))
            + 0.02 * (1.0 - float(row["aerosol_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "planetary_stress_score": round(stress, 4),
            "transformation_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["planetary_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.14 * float(row["climate_reduction"])
            + 0.14 * float(row["biosphere_recovery"])
            + 0.11 * float(row["land_restoration"])
            + 0.11 * float(row["water_security"])
            + 0.09 * float(row["nutrient_circularity"])
            + 0.09 * float(row["novel_entity_control"])
            + 0.12 * float(row["social_foundation_gain"])
            + 0.10 * float(row["governance_gain"])
            + 0.08 * float(row["justice_gain"])
            + 0.02 * float(row["implementation_capacity"])
        )

        readiness = (
            0.24 * float(row["implementation_capacity"])
            + 0.17 * float(row["governance_gain"])
            + 0.15 * float(row["justice_gain"])
            + 0.13 * float(row["social_foundation_gain"])
            + 0.10 * float(row["climate_reduction"])
            + 0.08 * float(row["biosphere_recovery"])
            + 0.06 * float(row["water_security"])
            + 0.04 * float(row["land_restoration"])
            + 0.03 * float(row["novel_entity_control"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "pathway_id": row["pathway_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "pathway_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["pathway_strategy_value_score"]), reverse=True)
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
            "planetary_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["planetary_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.16 * float(row["monitoring_capacity"])
            + 0.17 * float(row["policy_coordination"])
            + 0.15 * float(row["public_finance"])
            + 0.14 * float(row["participation"])
            + 0.15 * float(row["justice_safeguards"])
            + 0.12 * float(row["international_cooperation"])
            + 0.11 * float(row["implementation_capacity"])
        )

        legitimacy_gap = (
            0.18 * (1.0 - float(row["participation"]))
            + 0.17 * (1.0 - float(row["justice_safeguards"]))
            + 0.15 * (1.0 - float(row["policy_coordination"]))
            + 0.14 * (1.0 - float(row["public_finance"]))
            + 0.13 * (1.0 - float(row["monitoring_capacity"]))
            + 0.12 * (1.0 - float(row["implementation_capacity"]))
            + 0.11 * (1.0 - float(row["international_cooperation"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "pathway_id": row["pathway_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "planetary_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["planetary_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(simulations: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in simulations:
        pressure = float(row["boundary_pressure"])
        social = float(row["social_foundations"])
        governance = float(row["governance"])
        justice = float(row["justice"])
        technology = float(row["technology_dependence"])
        regeneration = float(row["regeneration"])
        viability = float(row["initial_viability"])
        horizon = int(row["time_horizon"])

        adaptive_capacity = (
            0.26 * governance
            + 0.24 * justice
            + 0.22 * social
            + 0.18 * regeneration
            + 0.10 * (1.0 - technology)
        )

        viability_values: list[float] = []
        pressure_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.16 if t % 8 == 0 else 0.06
                technology_risk = 0.06 * technology if t % 11 == 0 else 0.0

                pressure = clamp(
                    pressure
                    + 0.04 * shock
                    + 0.03 * technology
                    + 0.02 * technology_risk
                    - 0.04 * regeneration
                    - 0.03 * governance
                    - 0.02 * justice,
                    0.0,
                    1.5,
                )

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.03 * governance
                    + 0.03 * justice
                    + 0.02 * social
                    + 0.02 * regeneration
                    - 0.03 * shock
                    - 0.02 * pressure,
                    0.0,
                    1.6,
                )

                viability = clamp(
                    viability
                    + 0.05 * adaptive_capacity
                    + 0.04 * social
                    + 0.03 * regeneration
                    - shock
                    - technology_risk
                    - 0.07 * pressure,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            pressure_values.append(pressure)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "simulation_id": row["simulation_id"],
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "simulation_name": row["simulation_name"],
                "time_step": t,
                "pathway_viability": round(viability, 4),
                "boundary_pressure": round(pressure, 4),
                "adaptive_capacity": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "simulation_id": row["simulation_id"],
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "simulation_name": row["simulation_name"],
            "final_pathway_viability": round(viability_values[-1], 4),
            "mean_pathway_viability": round(mean(viability_values), 4),
            "mean_boundary_pressure": round(mean(pressure_values), 4),
            "final_adaptive_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_pathway_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    pathway_scores: list[dict[str, Any]],
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
        "## Planetary Pathway Scores",
        "",
    ]

    for row in pathway_scores:
        lines.append(
            f"- **{row['pathway_name']}**: boundary pressure {row['total_boundary_pressure_score']}; "
            f"safe-and-just score {row['safe_and_just_pathway_score']}; class: {row['pathway_class']}."
        )

    lines.extend(["", "## Boundary Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['planetary_stress_score']}; "
            f"transformation opportunity {row['transformation_opportunity_score']}."
        )

    lines.extend(["", "## Pathway Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['pathway_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Planetary Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['planetary_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Planetary Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['planetary_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['simulation_name']}**: final viability {row['final_pathway_viability']}; "
            f"mean boundary pressure {row['mean_boundary_pressure']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_pressure = mean(float(row["total_boundary_pressure_score"]) for row in pathway_scores)
    avg_safe_score = mean(float(row["safe_and_just_pathway_score"]) for row in pathway_scores)
    avg_pathway_viability = mean(float(row["final_pathway_viability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Planetary pathway profiles: {len(pathway_scores)}.",
        f"- Boundary scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average boundary pressure score: {round(avg_pressure, 4)}.",
        f"- Average safe-and-just pathway score: {round(avg_safe_score, 4)}.",
        f"- Average final pathway viability: {round(avg_pathway_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats planetary boundaries and future pathways as coupled Earth-system and social-system trajectories shaped by ecological pressure, social foundations, governance, justice, technology dependence, regeneration, and adaptive capacity.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "planetary_boundaries_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "planetary_pathway_profiles.csv")
    scenarios_raw = read_csv(DATA / "boundary_scenarios.csv")
    strategies_raw = read_csv(DATA / "pathway_strategy_options.csv")
    risks_raw = read_csv(DATA / "planetary_risk_indicators.csv")
    governance_raw = read_csv(DATA / "planetary_governance_records.csv")
    simulations_raw = read_csv(DATA / "planetary_pathway_simulations.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, governance_raw, simulations_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    pathway_scores = score_pathways(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    governance_scores = score_governance(governance_raw)
    trajectories, pathway_summary = simulate_pathways(simulations_raw)

    write_csv(OUTPUTS / "planetary_pathway_scores.csv", pathway_scores)
    write_csv(OUTPUTS / "boundary_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "pathway_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "planetary_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "planetary_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "planetary_pathway_simulation_paths.csv", trajectories)
    write_csv(OUTPUTS / "planetary_pathway_simulation_summary.csv", pathway_summary)

    write_report(config, pathway_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Planetary boundaries workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
