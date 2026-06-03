#!/usr/bin/env python3
"""
Standard-library workflow for Democratic Futures and Public Participation.

Outputs:
- participation_model_scores.csv
- representation_quality_scores.csv
- decision_uptake_scores.csv
- future_scenario_scores.csv
- democratic_futures_pathways.csv
- democratic_futures_pathway_summary.csv
- strategy_option_scores.csv
- democratic_futures_report.md
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


def democratic_capacity(row: dict[str, str]) -> float:
    return (
        0.11 * float(row["inclusion"])
        + 0.12 * float(row["deliberative_quality"])
        + 0.11 * float(row["representation"])
        + 0.14 * float(row["institutional_uptake"])
        + 0.12 * float(row["accountability"])
        + 0.12 * float(row["justice_safeguards"])
        + 0.08 * float(row["public_learning"])
        + 0.10 * float(row["decision_influence"])
        + 0.05 * float(row["accessibility"])
        + 0.05 * float(row["community_authority"])
    )


def tokenism_risk(row: dict[str, str]) -> float:
    return (
        0.18 * (1.0 - float(row["institutional_uptake"]))
        + 0.16 * (1.0 - float(row["decision_influence"]))
        + 0.14 * (1.0 - float(row["accountability"]))
        + 0.14 * (1.0 - float(row["community_authority"]))
        + 0.12 * (1.0 - float(row["justice_safeguards"]))
        + 0.10 * (1.0 - float(row["representation"]))
        + 0.08 * (1.0 - float(row["deliberative_quality"]))
        + 0.08 * (1.0 - float(row["inclusion"]))
    )


def validate_records(
    models: list[dict[str, str]],
    representation: list[dict[str, str]],
    uptake: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    model_ids = {row["model_id"] for row in models}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in representation:
        if row["model_id"] not in model_ids:
            errors.append(f"Representation record {row['representation_id']} references missing model {row['model_id']}.")

    for row in uptake:
        if row["model_id"] not in model_ids:
            errors.append(f"Uptake record {row['uptake_id']} references missing model {row['model_id']}.")

    for row in pathways:
        if row["model_id"] not in model_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing model {row['model_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("models", models, ["inclusion", "deliberative_quality", "representation", "institutional_uptake", "accountability", "justice_safeguards", "public_learning", "decision_influence", "accessibility", "community_authority"]),
        ("representation", representation, ["affectedness", "representation_quality", "barrier_reduction", "compensation", "decision_access", "trust_condition", "knowledge_recognition"]),
        ("uptake", uptake, ["response_duty", "budget_connection", "policy_influence", "regulatory_influence", "implementation_tracking", "public_reporting", "remedy_access"]),
        ("scenarios", scenarios, ["public_trust", "participation_quality", "institutional_responsiveness", "inequality_pressure", "platform_power", "climate_stress", "democratic_polarization", "civic_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("model_id") or row.get("scenario_id") or row.get("representation_id") or row.get("uptake_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_models(models: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in models:
        capacity = democratic_capacity(row)
        tokenism = tokenism_risk(row)

        if capacity >= 0.74:
            democratic_class = "Strong democratic futures capacity"
        elif tokenism >= 0.55:
            democratic_class = "High tokenism or low influence risk"
        else:
            democratic_class = "Developing participatory foresight capacity"

        rows.append({
            "model_id": row["model_id"],
            "participation_model": row["participation_model"],
            "participation_type": row["participation_type"],
            "democratic_futures_capacity_score": round(capacity, 4),
            "tokenism_risk_score": round(tokenism, 4),
            "democratic_class": democratic_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["democratic_futures_capacity_score"]), reverse=True)
    return rows


def score_representation(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        score = (
            0.20 * float(row["affectedness"])
            + 0.20 * float(row["representation_quality"])
            + 0.16 * float(row["barrier_reduction"])
            + 0.12 * float(row["compensation"])
            + 0.14 * float(row["decision_access"])
            + 0.08 * float(row["trust_condition"])
            + 0.10 * float(row["knowledge_recognition"])
        )

        rows.append({
            "representation_id": row["representation_id"],
            "model_id": row["model_id"],
            "group_name": row["group_name"],
            "representation_quality_score": round(score, 4),
            "decision_access": float(row["decision_access"]),
            "knowledge_recognition": float(row["knowledge_recognition"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["representation_quality_score"]), reverse=True)
    return rows


def score_uptake(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        score = (
            0.18 * float(row["response_duty"])
            + 0.16 * float(row["budget_connection"])
            + 0.16 * float(row["policy_influence"])
            + 0.14 * float(row["regulatory_influence"])
            + 0.14 * float(row["implementation_tracking"])
            + 0.12 * float(row["public_reporting"])
            + 0.10 * float(row["remedy_access"])
        )

        rows.append({
            "uptake_id": row["uptake_id"],
            "model_id": row["model_id"],
            "decision_area": row["decision_area"],
            "decision_uptake_score": round(score, 4),
            "budget_connection": float(row["budget_connection"]),
            "remedy_access": float(row["remedy_access"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["decision_uptake_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        stress = (
            0.16 * (1.0 - float(row["public_trust"]))
            + 0.14 * (1.0 - float(row["participation_quality"]))
            + 0.14 * (1.0 - float(row["institutional_responsiveness"]))
            + 0.14 * float(row["inequality_pressure"])
            + 0.12 * float(row["platform_power"])
            + 0.12 * float(row["climate_stress"])
            + 0.12 * float(row["democratic_polarization"])
            + 0.06 * (1.0 - float(row["civic_capacity"]))
        )

        opportunity = (
            0.20 * float(row["public_trust"])
            + 0.20 * float(row["participation_quality"])
            + 0.18 * float(row["institutional_responsiveness"])
            + 0.16 * float(row["civic_capacity"])
            + 0.10 * (1.0 - float(row["democratic_polarization"]))
            + 0.08 * (1.0 - float(row["inequality_pressure"]))
            + 0.08 * (1.0 - float(row["platform_power"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "democratic_stress_pressure_score": round(stress, 4),
            "democratic_futures_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["democratic_futures_opportunity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        inclusion = float(row["inclusion"])
        deliberation = float(row["deliberation"])
        representation = float(row["representation"])
        uptake_base = float(row["uptake"])
        accountability = float(row["accountability"])
        justice = float(row["justice"])
        learning = float(row["learning"])
        authority = float(row["authority"])
        trust = float(row["initial_trust"])
        uptake = uptake_base
        democratic_capacity_state = (
            0.14 * inclusion
            + 0.14 * deliberation
            + 0.14 * representation
            + 0.18 * uptake
            + 0.14 * accountability
            + 0.14 * justice
            + 0.12 * learning
        )
        tokenism = 1.0 - (0.50 * uptake + 0.50 * accountability)
        learning_state = learning
        horizon = int(row["time_horizon"])

        capacity_values: list[float] = []
        trust_values: list[float] = []
        uptake_values: list[float] = []
        tokenism_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                pressure = 0.14 if t % 8 == 0 else 0.05

                participation_quality = (
                    0.22 * inclusion
                    + 0.22 * deliberation
                    + 0.18 * representation
                    + 0.18 * justice
                    + 0.10 * learning_state
                    + 0.10 * accountability
                )

                institutional_response = (
                    0.36 * uptake
                    + 0.28 * accountability
                    + 0.20 * authority
                    + 0.16 * learning_state
                )

                uptake = clamp(
                    uptake
                    + 0.04 * uptake_base
                    + 0.03 * accountability
                    + 0.03 * authority
                    + 0.02 * learning_state
                    - 0.03 * pressure,
                    0.0,
                    1.4,
                )

                tokenism = clamp(
                    tokenism
                    + 0.05 * pressure
                    - 0.04 * uptake
                    - 0.04 * accountability
                    - 0.03 * justice
                    - 0.02 * authority,
                    0.0,
                    1.2,
                )

                learning_state = clamp(
                    learning_state
                    + 0.03 * learning
                    + 0.03 * deliberation
                    + 0.02 * uptake
                    - 0.02 * pressure,
                    0.0,
                    1.4,
                )

                trust = clamp(
                    trust
                    + 0.05 * uptake
                    + 0.04 * accountability
                    + 0.03 * justice
                    + 0.02 * authority
                    - 0.06 * tokenism
                    - 0.02 * pressure,
                    0.0,
                    1.4,
                )

                democratic_capacity_state = clamp(
                    democratic_capacity_state
                    + participation_quality / 7.0
                    + institutional_response / 7.0
                    + 0.04 * trust
                    - 0.08 * tokenism
                    - 0.04 * pressure,
                    0.0,
                    1.8,
                )

            capacity_values.append(democratic_capacity_state)
            trust_values.append(trust)
            uptake_values.append(uptake)
            tokenism_values.append(tokenism)
            learning_values.append(learning_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "model_id": row["model_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "democratic_futures_capacity": round(democratic_capacity_state, 4),
                "public_trust": round(trust, 4),
                "institutional_uptake": round(uptake, 4),
                "tokenism_risk": round(tokenism, 4),
                "learning_score": round(learning_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "model_id": row["model_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_democratic_futures_capacity": round(capacity_values[-1], 4),
            "mean_democratic_futures_capacity": round(mean(capacity_values), 4),
            "final_public_trust": round(trust_values[-1], 4),
            "final_institutional_uptake": round(uptake_values[-1], 4),
            "mean_tokenism_risk": round(mean(tokenism_values), 4),
            "final_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_democratic_futures_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        democratic_score = (
            0.12 * float(row["inclusion_design"])
            + 0.12 * float(row["deliberative_design"])
            + 0.12 * float(row["representation_quality"])
            + 0.14 * float(row["response_duty"])
            + 0.12 * float(row["budget_link"])
            + 0.12 * float(row["accountability_tracking"])
            + 0.12 * float(row["justice_safeguards"])
            + 0.08 * float(row["remedy_access"])
            + 0.06 * float(row["public_learning"])
        )

        influence_score = (
            0.18 * float(row["response_duty"])
            + 0.18 * float(row["budget_link"])
            + 0.16 * float(row["accountability_tracking"])
            + 0.14 * float(row["remedy_access"])
            + 0.12 * float(row["justice_safeguards"])
            + 0.10 * float(row["representation_quality"])
            + 0.08 * float(row["deliberative_design"])
            + 0.04 * float(row["public_learning"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "democratic_futures_strategy_score": round(democratic_score, 4),
            "decision_influence_strategy_score": round(influence_score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["democratic_futures_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    model_scores: list[dict[str, Any]],
    representation_scores: list[dict[str, Any]],
    uptake_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Participation Model Scores",
        "",
    ]

    for row in model_scores:
        lines.append(
            f"- **{row['participation_model']}**: democratic capacity {row['democratic_futures_capacity_score']}; "
            f"tokenism risk {row['tokenism_risk_score']}; class: {row['democratic_class']}."
        )

    lines.extend(["", "## Representation Quality Scores", ""])
    for row in representation_scores:
        lines.append(
            f"- **{row['group_name']}**: representation quality {row['representation_quality_score']}; "
            f"decision access {row['decision_access']}; knowledge recognition {row['knowledge_recognition']}."
        )

    lines.extend(["", "## Decision Uptake Scores", ""])
    for row in uptake_scores:
        lines.append(
            f"- **{row['decision_area']}**: uptake {row['decision_uptake_score']}; "
            f"budget connection {row['budget_connection']}; remedy access {row['remedy_access']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: opportunity {row['democratic_futures_opportunity_score']}; "
            f"stress {row['democratic_stress_pressure_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final democratic capacity {row['final_democratic_futures_capacity']}; "
            f"final public trust {row['final_public_trust']}; mean tokenism risk {row['mean_tokenism_risk']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: democratic futures strategy {row['democratic_futures_strategy_score']}; "
            f"decision influence strategy {row['decision_influence_strategy_score']}."
        )

    avg_capacity = mean(float(row["democratic_futures_capacity_score"]) for row in model_scores)
    avg_tokenism = mean(float(row["tokenism_risk_score"]) for row in model_scores)
    avg_uptake = mean(float(row["decision_uptake_score"]) for row in uptake_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Participation models: {len(model_scores)}.",
        f"- Representation records: {len(representation_scores)}.",
        f"- Decision uptake records: {len(uptake_scores)}.",
        f"- Future scenarios: {len(scenario_scores)}.",
        f"- Average democratic futures capacity score: {round(avg_capacity, 4)}.",
        f"- Average tokenism risk score: {round(avg_tokenism, 4)}.",
        f"- Average decision uptake score: {round(avg_uptake, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats democratic futures as an institutional and civic system for inclusion, deliberation, representation, public learning, decision influence, accountability, justice safeguards, and visible follow-through.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "democratic_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    models_raw = read_csv(DATA / "participation_models.csv")
    representation_raw = read_csv(DATA / "representation_profiles.csv")
    uptake_raw = read_csv(DATA / "decision_uptake_register.csv")
    scenarios_raw = read_csv(DATA / "future_scenarios.csv")
    pathways_raw = read_csv(DATA / "democratic_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(models_raw, representation_raw, uptake_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    model_scores = score_models(models_raw)
    representation_scores = score_representation(representation_raw)
    uptake_scores = score_uptake(uptake_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategy_scores = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "participation_model_scores.csv", model_scores)
    write_csv(OUTPUTS / "representation_quality_scores.csv", representation_scores)
    write_csv(OUTPUTS / "decision_uptake_scores.csv", uptake_scores)
    write_csv(OUTPUTS / "future_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "democratic_futures_pathways.csv", trajectories)
    write_csv(OUTPUTS / "democratic_futures_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategy_scores)

    write_report(config, model_scores, representation_scores, uptake_scores, scenario_scores, pathway_summary, strategy_scores)

    print(f"Democratic futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
