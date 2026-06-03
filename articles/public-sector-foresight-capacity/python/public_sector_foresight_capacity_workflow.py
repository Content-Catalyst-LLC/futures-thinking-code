#!/usr/bin/env python3
"""
Standard-library workflow for Public-Sector Foresight Capacity.

Outputs:
- foresight_capacity_scores.csv
- scanning_signal_scores.csv
- decision_uptake_scores.csv
- scenario_cycle_scores.csv
- foresight_capacity_pathways.csv
- foresight_capacity_pathway_summary.csv
- strategy_option_scores.csv
- public_sector_foresight_capacity_report.md
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


def capacity_score(row: dict[str, str]) -> float:
    return (
        0.12 * float(row["scanning_capacity"])
        + 0.12 * float(row["scenario_capacity"])
        + 0.14 * float(row["decision_uptake"])
        + 0.12 * float(row["participation_capacity"])
        + 0.12 * float(row["budget_connection"])
        + 0.10 * float(row["evaluation_capacity"])
        + 0.10 * float(row["institutional_learning"])
        + 0.10 * float(row["implementation_authority"])
        + 0.05 * float(row["knowledge_infrastructure"])
        + 0.03 * float(row["legitimacy"])
    )


def capacity_gap(row: dict[str, str]) -> float:
    return (
        0.16 * (1.0 - float(row["decision_uptake"]))
        + 0.14 * (1.0 - float(row["budget_connection"]))
        + 0.14 * (1.0 - float(row["implementation_authority"]))
        + 0.12 * (1.0 - float(row["scanning_capacity"]))
        + 0.12 * (1.0 - float(row["scenario_capacity"]))
        + 0.10 * (1.0 - float(row["participation_capacity"]))
        + 0.10 * (1.0 - float(row["evaluation_capacity"]))
        + 0.08 * (1.0 - float(row["institutional_learning"]))
        + 0.04 * (1.0 - float(row["knowledge_infrastructure"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    signals: list[dict[str, str]],
    uptake: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    capacity_ids = {row["capacity_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in uptake:
        if row["capacity_id"] not in capacity_ids:
            errors.append(f"Uptake record {row['uptake_id']} references missing capacity profile {row['capacity_id']}.")

    for row in pathways:
        if row["capacity_id"] not in capacity_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing capacity profile {row['capacity_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["scanning_capacity", "scenario_capacity", "decision_uptake", "participation_capacity", "budget_connection", "evaluation_capacity", "institutional_learning", "implementation_authority", "knowledge_infrastructure", "legitimacy"]),
        ("signals", signals, ["signal_strength", "novelty", "uncertainty", "policy_relevance", "equity_relevance", "detection_difficulty", "response_readiness"]),
        ("uptake", uptake, ["uptake_strength", "budget_influence", "regulatory_influence", "procurement_influence", "implementation_influence", "evaluation_influence", "participation_influence"]),
        ("scenarios", scenarios, ["technology_disruption", "climate_stress", "fiscal_pressure", "public_trust", "institutional_capacity", "participation_quality", "review_frequency", "implementation_pressure"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("capacity_id") or row.get("scenario_id") or row.get("signal_id") or row.get("uptake_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in profiles:
        score = capacity_score(row)
        gap = capacity_gap(row)

        if score >= 0.72:
            maturity = "Integrated foresight capacity"
        elif gap >= 0.55:
            maturity = "Low or symbolic foresight capacity"
        else:
            maturity = "Developing foresight capacity"

        rows.append({
            "capacity_id": row["capacity_id"],
            "foresight_model": row["foresight_model"],
            "institution_type": row["institution_type"],
            "foresight_capacity_score": round(score, 4),
            "capacity_gap_score": round(gap, 4),
            "maturity_class": maturity,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_capacity_score"]), reverse=True)
    return rows


def score_signals(signals: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in signals:
        priority = (
            0.16 * float(row["signal_strength"])
            + 0.12 * float(row["novelty"])
            + 0.12 * float(row["uncertainty"])
            + 0.18 * float(row["policy_relevance"])
            + 0.16 * float(row["equity_relevance"])
            + 0.12 * float(row["detection_difficulty"])
            + 0.14 * (1.0 - float(row["response_readiness"]))
        )

        rows.append({
            "signal_id": row["signal_id"],
            "signal_name": row["signal_name"],
            "domain": row["domain"],
            "scanning_signal_priority_score": round(priority, 4),
            "response_gap_score": round(1.0 - float(row["response_readiness"]), 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["scanning_signal_priority_score"]), reverse=True)
    return rows


def score_uptake(uptake: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in uptake:
        score = (
            0.20 * float(row["uptake_strength"])
            + 0.18 * float(row["budget_influence"])
            + 0.14 * float(row["regulatory_influence"])
            + 0.12 * float(row["procurement_influence"])
            + 0.14 * float(row["implementation_influence"])
            + 0.12 * float(row["evaluation_influence"])
            + 0.10 * float(row["participation_influence"])
        )

        rows.append({
            "uptake_id": row["uptake_id"],
            "capacity_id": row["capacity_id"],
            "decision_area": row["decision_area"],
            "decision_uptake_score": round(score, 4),
            "budget_influence": float(row["budget_influence"]),
            "implementation_influence": float(row["implementation_influence"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["decision_uptake_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        stress = (
            0.16 * float(row["technology_disruption"])
            + 0.18 * float(row["climate_stress"])
            + 0.14 * float(row["fiscal_pressure"])
            + 0.12 * (1.0 - float(row["public_trust"]))
            + 0.12 * (1.0 - float(row["institutional_capacity"]))
            + 0.10 * (1.0 - float(row["participation_quality"]))
            + 0.08 * (1.0 - float(row["review_frequency"]))
            + 0.10 * float(row["implementation_pressure"])
        )

        opportunity = (
            0.22 * float(row["institutional_capacity"])
            + 0.20 * float(row["participation_quality"])
            + 0.18 * float(row["public_trust"])
            + 0.14 * float(row["review_frequency"])
            + 0.10 * (1.0 - float(row["fiscal_pressure"]))
            + 0.08 * (1.0 - float(row["technology_disruption"]))
            + 0.08 * (1.0 - float(row["climate_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "foresight_stress_pressure_score": round(stress, 4),
            "foresight_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_stress_pressure_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        scanning = float(row["scanning"])
        scenarios = float(row["scenarios"])
        participation = float(row["participation"])
        budget = float(row["budget"])
        evaluation = float(row["evaluation"])
        learning = float(row["learning"])
        authority = float(row["authority"])
        legitimacy_base = float(row["legitimacy"])
        capacity = float(row["initial_capacity"])
        uptake = 0.5 * budget + 0.5 * authority
        legitimacy = legitimacy_base
        learning_state = learning
        horizon = int(row["time_horizon"])

        capacity_values: list[float] = []
        uptake_values: list[float] = []
        legitimacy_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                pressure = 0.16 if t % 8 == 0 else 0.06

                analytic_gain = 0.22 * scanning + 0.22 * scenarios
                institutional_gain = 0.20 * budget + 0.18 * authority + 0.16 * evaluation
                democratic_gain = 0.16 * participation + 0.10 * legitimacy
                learning_gain = 0.14 * learning_state

                uptake = clamp(
                    uptake
                    + 0.05 * budget
                    + 0.05 * authority
                    + 0.03 * evaluation
                    - 0.04 * pressure,
                    0.0,
                    1.4,
                )

                legitimacy = clamp(
                    legitimacy
                    + 0.05 * participation
                    + 0.03 * evaluation
                    + 0.02 * legitimacy_base
                    - 0.03 * pressure,
                    0.0,
                    1.4,
                )

                learning_state = clamp(
                    learning_state
                    + 0.04 * learning
                    + 0.03 * evaluation
                    + 0.02 * uptake
                    - 0.02 * pressure,
                    0.0,
                    1.4,
                )

                capacity = clamp(
                    capacity
                    + analytic_gain / 6.0
                    + institutional_gain / 6.0
                    + democratic_gain / 7.0
                    + learning_gain / 7.0
                    - 0.08 * pressure
                    + 0.04 * uptake,
                    0.0,
                    1.8,
                )

            capacity_values.append(capacity)
            uptake_values.append(uptake)
            legitimacy_values.append(legitimacy)
            learning_values.append(learning_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "capacity_id": row["capacity_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "foresight_capacity": round(capacity, 4),
                "decision_uptake": round(uptake, 4),
                "legitimacy_score": round(legitimacy, 4),
                "learning_score": round(learning_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "capacity_id": row["capacity_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_foresight_capacity": round(capacity_values[-1], 4),
            "mean_foresight_capacity": round(mean(capacity_values), 4),
            "final_decision_uptake": round(uptake_values[-1], 4),
            "final_legitimacy_score": round(legitimacy_values[-1], 4),
            "final_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_foresight_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        score = (
            0.12 * float(row["foresight_mandate"])
            + 0.12 * float(row["horizon_scanning"])
            + 0.13 * float(row["scenario_cycles"])
            + 0.13 * float(row["decision_pathways"])
            + 0.12 * float(row["participatory_foresight"])
            + 0.12 * float(row["budget_alignment"])
            + 0.10 * float(row["evaluation_capacity"])
            + 0.08 * float(row["knowledge_infrastructure"])
            + 0.08 * float(row["implementation_authority"])
        )

        implementation_score = (
            0.18 * float(row["implementation_authority"])
            + 0.18 * float(row["budget_alignment"])
            + 0.14 * float(row["decision_pathways"])
            + 0.12 * float(row["evaluation_capacity"])
            + 0.10 * float(row["foresight_mandate"])
            + 0.10 * float(row["scenario_cycles"])
            + 0.09 * float(row["horizon_scanning"])
            + 0.09 * float(row["knowledge_infrastructure"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "foresight_capacity_strategy_score": round(score, 4),
            "implementation_authority_strategy_score": round(implementation_score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_capacity_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    profiles: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    uptake: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Foresight Capacity Scores",
        "",
    ]

    for row in profiles:
        lines.append(
            f"- **{row['foresight_model']}**: capacity {row['foresight_capacity_score']}; "
            f"gap {row['capacity_gap_score']}; class: {row['maturity_class']}."
        )

    lines.extend(["", "## Scanning Signal Priorities", ""])
    for row in signals:
        lines.append(
            f"- **{row['signal_name']}**: priority {row['scanning_signal_priority_score']}; "
            f"response gap {row['response_gap_score']}."
        )

    lines.extend(["", "## Decision Uptake Scores", ""])
    for row in uptake:
        lines.append(
            f"- **{row['decision_area']}**: uptake {row['decision_uptake_score']}; "
            f"budget influence {row['budget_influence']}; implementation influence {row['implementation_influence']}."
        )

    lines.extend(["", "## Scenario Cycle Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['foresight_stress_pressure_score']}; "
            f"opportunity {row['foresight_opportunity_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final capacity {row['final_foresight_capacity']}; "
            f"final uptake {row['final_decision_uptake']}; final legitimacy {row['final_legitimacy_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: foresight capacity strategy {row['foresight_capacity_strategy_score']}; "
            f"implementation authority strategy {row['implementation_authority_strategy_score']}."
        )

    avg_capacity = mean(float(row["foresight_capacity_score"]) for row in profiles)
    avg_signal = mean(float(row["scanning_signal_priority_score"]) for row in signals)
    avg_uptake = mean(float(row["decision_uptake_score"]) for row in uptake)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Foresight capacity profiles: {len(profiles)}.",
        f"- Scanning signals: {len(signals)}.",
        f"- Decision uptake records: {len(uptake)}.",
        f"- Scenario profiles: {len(scenarios)}.",
        f"- Average foresight capacity score: {round(avg_capacity, 4)}.",
        f"- Average scanning signal priority score: {round(avg_signal, 4)}.",
        f"- Average decision uptake score: {round(avg_uptake, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats public-sector foresight capacity as an institutional system for scanning, scenarios, participation, decision uptake, budget connection, implementation authority, knowledge infrastructure, evaluation, and learning.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "public_sector_foresight_capacity_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "foresight_capacity_profiles.csv")
    signals_raw = read_csv(DATA / "scanning_signals.csv")
    uptake_raw = read_csv(DATA / "decision_uptake_register.csv")
    scenarios_raw = read_csv(DATA / "scenario_cycle_profiles.csv")
    pathways_raw = read_csv(DATA / "adaptive_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(profiles_raw, signals_raw, uptake_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profiles = score_profiles(profiles_raw)
    signals = score_signals(signals_raw)
    uptake = score_uptake(uptake_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "foresight_capacity_scores.csv", profiles)
    write_csv(OUTPUTS / "scanning_signal_scores.csv", signals)
    write_csv(OUTPUTS / "decision_uptake_scores.csv", uptake)
    write_csv(OUTPUTS / "scenario_cycle_scores.csv", scenarios)
    write_csv(OUTPUTS / "foresight_capacity_pathways.csv", trajectories)
    write_csv(OUTPUTS / "foresight_capacity_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, profiles, signals, uptake, scenarios, pathway_summary, strategies)

    print(f"Public-sector foresight capacity workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
