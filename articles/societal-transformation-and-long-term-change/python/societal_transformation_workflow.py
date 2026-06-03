#!/usr/bin/env python3
"""
Standard-library workflow for Societal Transformation and Long-Term Change.

Outputs:
- transformation_driver_scores.csv
- weak_signal_priority_scores.csv
- transformation_scenario_scores.csv
- system_pressure_scores.csv
- equity_justice_scores.csv
- societal_transformation_paths.csv
- societal_transformation_summary.csv
- strategy_option_scores.csv
- societal_transformation_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 2.5) -> float:
    return max(low, min(high, value))


def validate_records(
    drivers: list[dict[str, str]],
    signals: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    equity: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    driver_ids = {row["driver_id"] for row in drivers}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in signals:
        if row["driver_id"] not in driver_ids:
            errors.append(f"Signal {row['signal_id']} references missing driver {row['driver_id']}.")

    for row in equity:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Equity indicator {row['equity_id']} references missing scenario {row['scenario_id']}.")

    for row in pathways:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_files = [
        ("drivers", drivers, ["transformative_intensity", "uncertainty", "system_reach", "feedback_strength", "threshold_proximity", "governance_relevance", "equity_relevance"]),
        ("signals", signals, ["novelty", "relevance", "urgency", "evidence_quality", "affected_voice", "source_traceability"]),
        ("scenarios", scenarios, ["technology_intensity", "institutional_adaptability", "ecological_stress", "social_cohesion", "economic_restructuring", "equity_protection", "public_legitimacy"]),
    ]

    for file_name, rows, fields in numeric_files:
        for row in rows:
            row_id = row.get("driver_id") or row.get("signal_id") or row.get("scenario_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{file_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_drivers(drivers: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in drivers:
        intensity = float(row["transformative_intensity"])
        uncertainty = float(row["uncertainty"])
        reach = float(row["system_reach"])
        feedback = float(row["feedback_strength"])
        threshold = float(row["threshold_proximity"])
        governance = float(row["governance_relevance"])
        equity = float(row["equity_relevance"])

        priority = (
            0.18 * intensity
            + 0.14 * uncertainty
            + 0.16 * reach
            + 0.14 * feedback
            + 0.14 * threshold
            + 0.12 * governance
            + 0.12 * equity
        )

        rows.append({
            "driver_id": row["driver_id"],
            "driver_name": row["driver_name"],
            "driver_domain": row["driver_domain"],
            "transformative_intensity": intensity,
            "uncertainty": uncertainty,
            "system_reach": reach,
            "feedback_strength": feedback,
            "threshold_proximity": threshold,
            "governance_relevance": governance,
            "equity_relevance": equity,
            "driver_transformation_priority": round(priority, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["driver_transformation_priority"]), reverse=True)
    return rows


def score_signals(signals: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in signals:
        novelty = float(row["novelty"])
        relevance = float(row["relevance"])
        urgency = float(row["urgency"])
        evidence = float(row["evidence_quality"])
        affected = float(row["affected_voice"])
        traceability = float(row["source_traceability"])

        score = (
            0.14 * novelty
            + 0.24 * relevance
            + 0.20 * urgency
            + 0.14 * evidence
            + 0.16 * affected
            + 0.12 * traceability
        )

        rows.append({
            "signal_id": row["signal_id"],
            "driver_id": row["driver_id"],
            "signal_name": row["signal_name"],
            "signal_type": row["signal_type"],
            "signal_priority_score": round(score, 4),
            "interpretation": row["interpretation"],
        })

    rows.sort(key=lambda item: float(item["signal_priority_score"]), reverse=True)
    return rows


def classify_scenario(capacity: float, fragility: float) -> str:
    if capacity >= 0.72:
        return "Strong just-transformation capacity"
    if fragility >= 0.62:
        return "Fragile or high-risk transformation"
    return "Contested transition pathway"


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        technology = float(row["technology_intensity"])
        institution = float(row["institutional_adaptability"])
        ecology = float(row["ecological_stress"])
        cohesion = float(row["social_cohesion"])
        economy = float(row["economic_restructuring"])
        equity = float(row["equity_protection"])
        legitimacy = float(row["public_legitimacy"])

        depth = (
            0.18 * technology
            + 0.18 * economy
            + 0.18 * ecology
            + 0.16 * institution
            + 0.14 * cohesion
            + 0.08 * equity
            + 0.08 * legitimacy
        )

        capacity = (
            0.22 * institution
            + 0.22 * equity
            + 0.20 * legitimacy
            + 0.18 * cohesion
            + 0.10 * (1.0 - ecology)
            + 0.08 * economy
        )

        fragility = (
            0.26 * ecology
            + 0.22 * (1.0 - institution)
            + 0.20 * (1.0 - cohesion)
            + 0.18 * (1.0 - legitimacy)
            + 0.14 * (1.0 - equity)
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "time_horizon": row["time_horizon"],
            "transformation_depth_score": round(depth, 4),
            "just_transformation_capacity_score": round(capacity, 4),
            "fragility_score": round(fragility, 4),
            "transformation_class": classify_scenario(capacity, fragility),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["just_transformation_capacity_score"]), reverse=True)
    return rows


def score_pressure_indicators(indicators: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }

    for row in indicators:
        baseline = float(row["baseline"])
        current = float(row["current_value"])
        threshold = float(row["threshold_value"])
        gap = current - threshold
        breach = current >= threshold
        review_weight = frequency_weight.get(row["review_frequency"], 0.50)

        pressure_score = (
            0.35 * current
            + 0.30 * (1.0 if breach else 0.0)
            + 0.20 * max(0.0, gap)
            + 0.15 * review_weight
        )

        rows.append({
            "indicator_id": row["indicator_id"],
            "indicator_name": row["indicator_name"],
            "domain": row["domain"],
            "baseline": baseline,
            "current_value": current,
            "threshold_value": threshold,
            "threshold_gap": round(gap, 4),
            "threshold_breached": breach,
            "pressure_score": round(pressure_score, 4),
            "review_frequency": row["review_frequency"],
            "owner": row["owner"],
            "interpretation": row["interpretation"],
        })

    rows.sort(key=lambda item: float(item["pressure_score"]), reverse=True)
    return rows


def score_equity(equity_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in equity_rows:
        exposure = float(row["exposure"])
        voice = float(row["voice"])
        protection = float(row["protection"])
        repair = float(row["repair"])
        burden = float(row["burden_concentration"])
        agency = float(row["agency"])

        justice = (
            0.20 * voice
            + 0.22 * protection
            + 0.22 * repair
            + 0.18 * agency
            + 0.18 * (1.0 - burden)
        )

        harm = (
            0.30 * exposure
            + 0.30 * burden
            + 0.16 * (1.0 - voice)
            + 0.12 * (1.0 - protection)
            + 0.12 * (1.0 - agency)
        )

        rows.append({
            "equity_id": row["equity_id"],
            "scenario_id": row["scenario_id"],
            "equity_dimension": row["equity_dimension"],
            "justice_capacity_score": round(justice, 4),
            "harm_concentration_score": round(harm, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["justice_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        technology = float(row["technology"])
        institution = float(row["institution"])
        ecology = float(row["ecology"])
        economy = float(row["economic_restructuring"])
        legitimacy = float(row["public_legitimacy"])
        equity = float(row["equity_protection"])
        viability = float(row["initial_viability"])
        pressure_index = ecology + economy
        transformation_depth = 0.30
        horizon = int(row["time_horizon"])

        viability_values: list[float] = []
        pressure_values: list[float] = []
        depth_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                periodic_shock = 0.10 * ecology if t % 9 == 0 else 0.035 * ecology

                structural_pressure = (
                    0.26 * ecology
                    + 0.18 * economy
                    + 0.16 * (1.0 - legitimacy)
                    + 0.16 * (1.0 - equity)
                    + periodic_shock
                )

                adaptive_capacity = (
                    0.24 * institution
                    + 0.18 * technology
                    + 0.18 * legitimacy
                    + 0.18 * equity
                )

                threshold_effect = 0.08 if structural_pressure > adaptive_capacity else 0.00
                viability = clamp(viability - structural_pressure / 5 + adaptive_capacity / 4 - threshold_effect, 0.0, 2.0)
                pressure_index = clamp(structural_pressure + pressure_index * 0.92, 0.0, 2.5)
                transformation_depth = clamp(
                    transformation_depth + 0.04 * technology + 0.04 * economy + 0.03 * ecology + 0.02 * institution,
                    0.0,
                    2.5,
                )

            viability_values.append(viability)
            pressure_values.append(pressure_index)
            depth_values.append(transformation_depth)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "transformation_viability": round(viability, 4),
                "pressure_index": round(pressure_index, 4),
                "transformation_depth": round(transformation_depth, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_viability": round(viability_values[-1], 4),
            "mean_viability": round(mean(viability_values), 4),
            "max_pressure": round(max(pressure_values), 4),
            "final_transformation_depth": round(depth_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        adaptation = float(row["adaptation_depth"])
        transformation = float(row["transformation_depth"])
        equity = float(row["equity_commitment"])
        investment = float(row["public_investment"])
        learning = float(row["institutional_learning"])
        participation = float(row["participation_strength"])
        ecology = float(row["ecological_responsibility"])

        public_interest = (
            0.14 * adaptation
            + 0.16 * transformation
            + 0.18 * equity
            + 0.16 * investment
            + 0.14 * learning
            + 0.12 * participation
            + 0.10 * ecology
        )

        institutional_viability = (
            0.18 * adaptation
            + 0.14 * transformation
            + 0.14 * equity
            + 0.16 * investment
            + 0.18 * learning
            + 0.10 * participation
            + 0.10 * ecology
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "public_interest_transformation_score": round(public_interest, 4),
            "institutional_viability_score": round(institutional_viability, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_transformation_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    drivers: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pressures: list[dict[str, Any]],
    equity: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Transformation Driver Priorities",
        "",
    ]

    for row in drivers:
        lines.append(
            f"- **{row['driver_name']}**: priority {row['driver_transformation_priority']}; "
            f"domain: {row['driver_domain']}."
        )

    lines.extend(["", "## Weak Signal Priorities", ""])
    for row in signals:
        lines.append(
            f"- **{row['signal_name']}**: signal priority {row['signal_priority_score']}; "
            f"interpretation: {row['interpretation']}"
        )

    lines.extend(["", "## Transformation Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: just-transformation capacity {row['just_transformation_capacity_score']}; "
            f"fragility {row['fragility_score']}; class: {row['transformation_class']}."
        )

    lines.extend(["", "## System Pressure Indicators", ""])
    for row in pressures:
        breach = "breached" if row["threshold_breached"] else "not breached"
        lines.append(
            f"- **{row['indicator_name']}**: pressure score {row['pressure_score']}; threshold {breach}."
        )

    lines.extend(["", "## Equity and Justice Scores", ""])
    for row in equity:
        lines.append(
            f"- **{row['equity_dimension']}**: justice capacity {row['justice_capacity_score']}; "
            f"harm concentration {row['harm_concentration_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_viability']}; "
            f"max pressure {row['max_pressure']}; final transformation depth {row['final_transformation_depth']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: public-interest transformation {row['public_interest_transformation_score']}; "
            f"institutional viability {row['institutional_viability_score']}."
        )

    avg_capacity = mean(float(row["just_transformation_capacity_score"]) for row in scenarios)
    avg_pressure = mean(float(row["pressure_score"]) for row in pressures)
    avg_justice = mean(float(row["justice_capacity_score"]) for row in equity)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Transformation drivers: {len(drivers)}.",
        f"- Weak signals: {len(signals)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- System pressure indicators: {len(pressures)}.",
        f"- Equity indicators: {len(equity)}.",
        f"- Average just-transformation capacity: {round(avg_capacity, 4)}.",
        f"- Average system pressure score: {round(avg_pressure, 4)}.",
        f"- Average justice capacity score: {round(avg_justice, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats societal transformation as a long-term interaction among structural drivers, weak signals, system pressure, institutional capacity, equity protection, public legitimacy, and pathway dynamics. It is designed to support transparent futures analysis rather than prediction.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "societal_transformation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    drivers_raw = read_csv(DATA / "transformation_drivers.csv")
    signals_raw = read_csv(DATA / "weak_signals.csv")
    scenarios_raw = read_csv(DATA / "transformation_scenarios.csv")
    pressures_raw = read_csv(DATA / "system_pressure_indicators.csv")
    equity_raw = read_csv(DATA / "equity_indicators.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(drivers_raw, signals_raw, scenarios_raw, equity_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    drivers = score_drivers(drivers_raw)
    signals = score_signals(signals_raw)
    scenarios = score_scenarios(scenarios_raw)
    pressures = score_pressure_indicators(pressures_raw)
    equity = score_equity(equity_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "transformation_driver_scores.csv", drivers)
    write_csv(OUTPUTS / "weak_signal_priority_scores.csv", signals)
    write_csv(OUTPUTS / "transformation_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "system_pressure_scores.csv", pressures)
    write_csv(OUTPUTS / "equity_justice_scores.csv", equity)
    write_csv(OUTPUTS / "societal_transformation_paths.csv", trajectories)
    write_csv(OUTPUTS / "societal_transformation_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, drivers, signals, scenarios, pressures, equity, pathway_summary, strategies)

    print(f"Societal transformation workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
