#!/usr/bin/env python3
"""
Standard-library workflow for Energy Transition Futures.

Outputs:
- energy_transition_capability_scores.csv
- transition_risk_scores.csv
- energy_justice_scores.csv
- energy_transition_scenario_scores.csv
- energy_transition_pathways.csv
- energy_transition_pathway_summary.csv
- strategy_option_scores.csv
- energy_transition_futures_report.md
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


def transition_readiness(clean_power: float, grid: float, storage: float, electrification: float, fossil_phase_down: float, justice: float, labor: float, materials: float, resilience: float) -> float:
    return (
        0.14 * clean_power
        + 0.14 * grid
        + 0.12 * storage
        + 0.12 * electrification
        + 0.12 * fossil_phase_down
        + 0.12 * justice
        + 0.10 * labor
        + 0.08 * materials
        + 0.06 * resilience
    )


def transition_risk_pressure(grid: float, storage: float, fossil_phase_down: float, justice: float, labor: float, materials: float, resilience: float) -> float:
    return (
        0.18 * (1.0 - grid)
        + 0.16 * (1.0 - storage)
        + 0.16 * (1.0 - fossil_phase_down)
        + 0.14 * (1.0 - justice)
        + 0.12 * (1.0 - labor)
        + 0.12 * (1.0 - materials)
        + 0.12 * (1.0 - resilience)
    )


def justice_resilience_capacity(justice: float, labor: float, resilience: float, materials: float, fossil_phase_down: float, grid: float) -> float:
    return (
        0.24 * justice
        + 0.20 * labor
        + 0.18 * resilience
        + 0.16 * materials
        + 0.12 * fossil_phase_down
        + 0.10 * grid
    )


def validate_records(
    capabilities: list[dict[str, str]],
    risks: list[dict[str, str]],
    justice: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    capability_ids = {row["capability_id"] for row in capabilities}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["capability_id"] not in capability_ids:
            errors.append(f"Risk {row['risk_id']} references missing capability {row['capability_id']}.")

    for row in justice:
        if row["capability_id"] not in capability_ids:
            errors.append(f"Justice indicator {row['justice_id']} references missing capability {row['capability_id']}.")

    for row in pathways:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("capabilities", capabilities, ["clean_power_expansion", "grid_readiness", "storage_flexibility", "electrification_capacity", "fossil_phase_down", "energy_justice", "labor_transition", "material_responsibility", "climate_resilience"]),
        ("risks", risks, ["probability", "severity", "detection_difficulty", "governance_gap", "infrastructure_exposure", "justice_relevance", "mitigation_capacity"]),
        ("justice", justice, ["affordability", "community_voice", "worker_security", "health_benefit", "ownership_access", "repair_capacity", "harm_reduction"]),
        ("scenarios", scenarios, ["clean_power_expansion", "grid_readiness", "storage_flexibility", "electrification_capacity", "fossil_phase_down", "energy_justice", "labor_transition", "material_responsibility", "climate_resilience"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("capability_id") or row.get("scenario_id") or row.get("risk_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_capabilities(capabilities: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in capabilities:
        clean = float(row["clean_power_expansion"])
        grid = float(row["grid_readiness"])
        storage = float(row["storage_flexibility"])
        electrification = float(row["electrification_capacity"])
        phase_down = float(row["fossil_phase_down"])
        justice = float(row["energy_justice"])
        labor = float(row["labor_transition"])
        materials = float(row["material_responsibility"])
        resilience = float(row["climate_resilience"])

        readiness = transition_readiness(clean, grid, storage, electrification, phase_down, justice, labor, materials, resilience)
        risk = transition_risk_pressure(grid, storage, phase_down, justice, labor, materials, resilience)
        jr = justice_resilience_capacity(justice, labor, resilience, materials, phase_down, grid)

        rows.append({
            "capability_id": row["capability_id"],
            "capability_name": row["capability_name"],
            "domain": row["domain"],
            "transition_readiness_score": round(readiness, 4),
            "transition_risk_pressure_score": round(risk, 4),
            "justice_resilience_capacity_score": round(jr, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["transition_readiness_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        probability = float(row["probability"])
        severity = float(row["severity"])
        detection = float(row["detection_difficulty"])
        governance_gap = float(row["governance_gap"])
        infrastructure = float(row["infrastructure_exposure"])
        justice = float(row["justice_relevance"])
        mitigation = float(row["mitigation_capacity"])

        priority = (
            0.18 * probability
            + 0.20 * severity
            + 0.14 * detection
            + 0.16 * governance_gap
            + 0.14 * infrastructure
            + 0.12 * justice
            + 0.06 * (1.0 - mitigation)
        )

        rows.append({
            "risk_id": row["risk_id"],
            "capability_id": row["capability_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "transition_risk_priority_score": round(priority, 4),
            "mitigation_capacity": mitigation,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["transition_risk_priority_score"]), reverse=True)
    return rows


def score_justice(justice_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in justice_rows:
        affordability = float(row["affordability"])
        voice = float(row["community_voice"])
        worker = float(row["worker_security"])
        health = float(row["health_benefit"])
        ownership = float(row["ownership_access"])
        repair = float(row["repair_capacity"])
        harm = float(row["harm_reduction"])

        score = (
            0.18 * affordability
            + 0.16 * voice
            + 0.16 * worker
            + 0.16 * health
            + 0.12 * ownership
            + 0.12 * repair
            + 0.10 * harm
        )

        rows.append({
            "justice_id": row["justice_id"],
            "capability_id": row["capability_id"],
            "justice_dimension": row["justice_dimension"],
            "energy_justice_score": round(score, 4),
            "energy_justice_gap_score": round(1.0 - score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["energy_justice_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        clean = float(row["clean_power_expansion"])
        grid = float(row["grid_readiness"])
        storage = float(row["storage_flexibility"])
        electrification = float(row["electrification_capacity"])
        phase_down = float(row["fossil_phase_down"])
        justice = float(row["energy_justice"])
        labor = float(row["labor_transition"])
        materials = float(row["material_responsibility"])
        resilience = float(row["climate_resilience"])

        readiness = transition_readiness(clean, grid, storage, electrification, phase_down, justice, labor, materials, resilience)
        risk = transition_risk_pressure(grid, storage, phase_down, justice, labor, materials, resilience)
        jr = justice_resilience_capacity(justice, labor, resilience, materials, phase_down, grid)

        if readiness >= 0.75 and jr >= 0.75:
            scenario_class = "High readiness and justice capacity"
        elif risk >= 0.55:
            scenario_class = "High transition risk pressure"
        else:
            scenario_class = "Contested transition pathway"

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "transition_readiness_score": round(readiness, 4),
            "transition_risk_pressure_score": round(risk, 4),
            "justice_resilience_capacity_score": round(jr, 4),
            "scenario_class": scenario_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["transition_readiness_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        clean = float(row["clean_power"])
        grid = float(row["grid"])
        storage = float(row["storage"])
        electrification = float(row["electrification"])
        phase_down = float(row["fossil_phase_down"])
        justice = float(row["justice"])
        labor = float(row["labor"])
        materials = float(row["materials"])
        resilience = float(row["resilience"])
        transition_capacity = float(row["initial_transition_capacity"])
        emissions_pressure = 0.90 - 0.22 * clean - 0.18 * phase_down
        justice_resilience = 0.50 * justice + 0.25 * labor + 0.25 * resilience
        horizon = int(row["time_horizon"])

        capacity_values: list[float] = []
        emissions_values: list[float] = []
        jr_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.09 if t % 10 == 0 else 0.03

                infrastructure_force = (
                    0.22 * clean
                    + 0.20 * grid
                    + 0.16 * storage
                    + 0.16 * electrification
                    + 0.12 * resilience
                )

                social_force = (
                    0.18 * justice
                    + 0.16 * labor
                    + 0.12 * materials
                    + 0.10 * phase_down
                )

                risk_pressure = (
                    0.18 * (1.0 - grid)
                    + 0.16 * (1.0 - storage)
                    + 0.16 * (1.0 - phase_down)
                    + 0.14 * (1.0 - justice)
                    + 0.12 * (1.0 - labor)
                    + 0.12 * (1.0 - materials)
                    + 0.12 * (1.0 - resilience)
                    + disruption
                )

                justice_resilience = clamp(
                    justice_resilience
                    + 0.04 * justice
                    + 0.03 * labor
                    + 0.03 * resilience
                    + 0.02 * materials
                    - 0.04 * risk_pressure,
                    0.0,
                    1.5,
                )

                emissions_pressure = clamp(
                    emissions_pressure * 0.92
                    + 0.08 * (1.0 - phase_down)
                    + 0.05 * (1.0 - electrification)
                    - 0.08 * clean
                    - 0.06 * grid,
                    0.0,
                    1.5,
                )

                transition_capacity = clamp(
                    transition_capacity
                    + infrastructure_force / 5.0
                    + social_force / 6.0
                    + 0.04 * justice_resilience
                    - 0.08 * risk_pressure
                    - 0.03 * emissions_pressure,
                    0.0,
                    1.8,
                )

            capacity_values.append(transition_capacity)
            emissions_values.append(emissions_pressure)
            jr_values.append(justice_resilience)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "transition_capacity": round(transition_capacity, 4),
                "emissions_pressure": round(emissions_pressure, 4),
                "justice_resilience_score": round(justice_resilience, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_transition_capacity": round(capacity_values[-1], 4),
            "mean_emissions_pressure": round(mean(emissions_values), 4),
            "final_justice_resilience_score": round(jr_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_transition_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        grid = float(row["grid_investment"])
        clean = float(row["clean_power_deployment"])
        electrification = float(row["electrification_support"])
        phase_down = float(row["fossil_phase_down_planning"])
        justice = float(row["justice_investment"])
        labor = float(row["labor_protection"])
        materials = float(row["material_governance"])
        resilience = float(row["resilience_investment"])
        finance = float(row["public_finance"])

        public_interest = (
            0.14 * grid
            + 0.12 * clean
            + 0.12 * electrification
            + 0.12 * phase_down
            + 0.14 * justice
            + 0.12 * labor
            + 0.10 * materials
            + 0.08 * resilience
            + 0.06 * finance
        )

        justice_resilience = (
            0.18 * justice
            + 0.16 * labor
            + 0.14 * resilience
            + 0.14 * materials
            + 0.12 * phase_down
            + 0.10 * grid
            + 0.08 * finance
            + 0.08 * electrification
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "public_interest_transition_strategy_score": round(public_interest, 4),
            "justice_resilience_strategy_score": round(justice_resilience, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_transition_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    capabilities: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    justice: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Energy Transition Capability Scores",
        "",
    ]

    for row in capabilities:
        lines.append(
            f"- **{row['capability_name']}**: readiness {row['transition_readiness_score']}; "
            f"risk pressure {row['transition_risk_pressure_score']}; justice-resilience capacity {row['justice_resilience_capacity_score']}."
        )

    lines.extend(["", "## Transition Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['transition_risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Energy Justice Scores", ""])
    for row in justice:
        lines.append(
            f"- **{row['justice_dimension']}**: energy justice score {row['energy_justice_score']}; "
            f"gap {row['energy_justice_gap_score']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: transition readiness {row['transition_readiness_score']}; "
            f"risk pressure {row['transition_risk_pressure_score']}; class: {row['scenario_class']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final transition capacity {row['final_transition_capacity']}; "
            f"mean emissions pressure {row['mean_emissions_pressure']}; final justice-resilience score {row['final_justice_resilience_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: public-interest transition strategy {row['public_interest_transition_strategy_score']}; "
            f"justice-resilience strategy {row['justice_resilience_strategy_score']}."
        )

    avg_readiness = mean(float(row["transition_readiness_score"]) for row in capabilities)
    avg_risk = mean(float(row["transition_risk_priority_score"]) for row in risks)
    avg_justice = mean(float(row["energy_justice_score"]) for row in justice)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Capabilities: {len(capabilities)}.",
        f"- Risk records: {len(risks)}.",
        f"- Justice indicators: {len(justice)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- Average transition readiness score: {round(avg_readiness, 4)}.",
        f"- Average transition risk priority: {round(avg_risk, 4)}.",
        f"- Average energy justice score: {round(avg_justice, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats energy transition futures as a systems-governance challenge. It compares clean power, grid readiness, storage and flexibility, electrification, fossil phase-down, energy justice, labor transition, material responsibility, climate resilience, emissions pressure, and public-interest strategy options.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "energy_transition_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    capabilities_raw = read_csv(DATA / "energy_transition_capabilities.csv")
    risks_raw = read_csv(DATA / "transition_risk_register.csv")
    justice_raw = read_csv(DATA / "justice_indicators.csv")
    scenarios_raw = read_csv(DATA / "energy_transition_scenarios.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(capabilities_raw, risks_raw, justice_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    capabilities = score_capabilities(capabilities_raw)
    risks = score_risks(risks_raw)
    justice = score_justice(justice_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "energy_transition_capability_scores.csv", capabilities)
    write_csv(OUTPUTS / "transition_risk_scores.csv", risks)
    write_csv(OUTPUTS / "energy_justice_scores.csv", justice)
    write_csv(OUTPUTS / "energy_transition_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "energy_transition_pathways.csv", trajectories)
    write_csv(OUTPUTS / "energy_transition_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, capabilities, risks, justice, scenarios, pathway_summary, strategies)

    print(f"Energy transition futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
