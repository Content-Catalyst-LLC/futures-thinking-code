#!/usr/bin/env python3
"""
Standard-library workflow for Digital Platform Futures.

Outputs:
- platform_profile_scores.csv
- platform_risk_scores.csv
- platform_accountability_scores.csv
- platform_scenario_scores.csv
- digital_platform_pathways.csv
- digital_platform_pathway_summary.csv
- strategy_option_scores.csv
- digital_platform_futures_report.md
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


def public_interest_capacity(
    platform_power: float,
    data_advantage: float,
    interoperability: float,
    worker_protection: float,
    public_accountability: float,
    user_rights: float,
    ecological_responsibility: float,
    digital_public_value: float,
) -> float:
    return (
        0.18 * interoperability
        + 0.18 * public_accountability
        + 0.16 * user_rights
        + 0.14 * worker_protection
        + 0.14 * digital_public_value
        + 0.10 * ecological_responsibility
        + 0.05 * (1.0 - platform_power)
        + 0.05 * (1.0 - data_advantage)
    )


def dependency_pressure(
    platform_power: float,
    data_advantage: float,
    interoperability: float,
    user_rights: float,
    public_accountability: float,
    worker_protection: float,
) -> float:
    return (
        0.24 * platform_power
        + 0.20 * data_advantage
        + 0.18 * (1.0 - interoperability)
        + 0.14 * (1.0 - user_rights)
        + 0.14 * (1.0 - public_accountability)
        + 0.10 * (1.0 - worker_protection)
    )


def validate_records(
    platforms: list[dict[str, str]],
    risks: list[dict[str, str]],
    accountability: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    platform_ids = {row["platform_id"] for row in platforms}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["platform_id"] not in platform_ids:
            errors.append(f"Risk {row['risk_id']} references missing platform {row['platform_id']}.")

    for row in accountability:
        if row["platform_id"] not in platform_ids:
            errors.append(f"Accountability indicator {row['accountability_id']} references missing platform {row['platform_id']}.")

    for row in pathways:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("platforms", platforms, ["network_effect_strength", "data_advantage", "gatekeeping_power", "lock_in", "interoperability", "public_accountability", "user_rights", "worker_protection", "ecological_responsibility", "digital_public_value"]),
        ("risks", risks, ["probability", "severity", "detection_difficulty", "accountability_gap", "dependency_exposure", "public_harm_relevance", "mitigation_capacity"]),
        ("accountability", accountability, ["transparency", "auditability", "contestability", "enforceability", "researcher_access", "remedy_capacity", "public_participation"]),
        ("scenarios", scenarios, ["platform_power", "data_advantage", "interoperability", "worker_protection", "public_accountability", "user_rights", "ecological_responsibility", "digital_public_value"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("platform_id") or row.get("scenario_id") or row.get("risk_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_platforms(platforms: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in platforms:
        network = float(row["network_effect_strength"])
        data = float(row["data_advantage"])
        gatekeeping = float(row["gatekeeping_power"])
        lock_in = float(row["lock_in"])
        interoperability = float(row["interoperability"])
        accountability = float(row["public_accountability"])
        rights = float(row["user_rights"])
        worker = float(row["worker_protection"])
        ecology = float(row["ecological_responsibility"])
        public_value = float(row["digital_public_value"])

        platform_power = 0.26 * network + 0.24 * data + 0.22 * gatekeeping + 0.16 * lock_in + 0.12 * (1.0 - interoperability)
        capacity = public_interest_capacity(platform_power, data, interoperability, worker, accountability, rights, ecology, public_value)
        dependency = dependency_pressure(platform_power, data, interoperability, rights, accountability, worker)

        rows.append({
            "platform_id": row["platform_id"],
            "platform_name": row["platform_name"],
            "platform_type": row["platform_type"],
            "market_role": row["market_role"],
            "platform_power_score": round(platform_power, 4),
            "public_interest_platform_capacity_score": round(capacity, 4),
            "platform_dependency_pressure_score": round(dependency, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["platform_dependency_pressure_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        probability = float(row["probability"])
        severity = float(row["severity"])
        detection = float(row["detection_difficulty"])
        accountability_gap = float(row["accountability_gap"])
        dependency = float(row["dependency_exposure"])
        public_harm = float(row["public_harm_relevance"])
        mitigation = float(row["mitigation_capacity"])

        priority = (
            0.18 * probability
            + 0.20 * severity
            + 0.16 * detection
            + 0.16 * accountability_gap
            + 0.14 * dependency
            + 0.10 * public_harm
            + 0.06 * (1.0 - mitigation)
        )

        rows.append({
            "risk_id": row["risk_id"],
            "platform_id": row["platform_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "platform_risk_priority_score": round(priority, 4),
            "mitigation_capacity": mitigation,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["platform_risk_priority_score"]), reverse=True)
    return rows


def score_accountability(accountability_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in accountability_rows:
        transparency = float(row["transparency"])
        auditability = float(row["auditability"])
        contestability = float(row["contestability"])
        enforceability = float(row["enforceability"])
        researcher = float(row["researcher_access"])
        remedy = float(row["remedy_capacity"])
        participation = float(row["public_participation"])

        capacity = (
            0.18 * transparency
            + 0.16 * auditability
            + 0.18 * contestability
            + 0.18 * enforceability
            + 0.10 * researcher
            + 0.12 * remedy
            + 0.08 * participation
        )

        rows.append({
            "accountability_id": row["accountability_id"],
            "platform_id": row["platform_id"],
            "accountability_dimension": row["accountability_dimension"],
            "accountability_capacity_score": round(capacity, 4),
            "accountability_gap_score": round(1.0 - capacity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["accountability_gap_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        power = float(row["platform_power"])
        data = float(row["data_advantage"])
        interoperability = float(row["interoperability"])
        worker = float(row["worker_protection"])
        accountability = float(row["public_accountability"])
        rights = float(row["user_rights"])
        ecology = float(row["ecological_responsibility"])
        public_value = float(row["digital_public_value"])

        capacity = public_interest_capacity(power, data, interoperability, worker, accountability, rights, ecology, public_value)
        dependency = dependency_pressure(power, data, interoperability, rights, accountability, worker)

        if capacity >= 0.75:
            scenario_class = "High public-interest platform capacity"
        elif dependency >= 0.68:
            scenario_class = "High platform dependency pressure"
        else:
            scenario_class = "Contested platform transition"

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "public_interest_platform_capacity_score": round(capacity, 4),
            "platform_dependency_pressure_score": round(dependency, 4),
            "scenario_class": scenario_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_platform_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        power = float(row["platform_power"])
        data = float(row["data_advantage"])
        interoperability = float(row["interoperability"])
        accountability = float(row["public_accountability"])
        rights = float(row["user_rights"])
        worker = float(row["worker_protection"])
        public_value_base = float(row["digital_public_value"])
        public_value = float(row["initial_public_value"])
        dependency = 0.35 + 0.25 * power + 0.20 * data
        accountability_capacity = accountability
        horizon = int(row["time_horizon"])

        public_value_values: list[float] = []
        dependency_values: list[float] = []
        accountability_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.08 if t % 10 == 0 else 0.03

                enclosure_force = (
                    0.24 * power
                    + 0.20 * data
                    + 0.18 * (1.0 - interoperability)
                    + 0.14 * (1.0 - rights)
                    + 0.12 * (1.0 - worker)
                )

                public_governance_force = (
                    0.22 * accountability
                    + 0.20 * rights
                    + 0.18 * interoperability
                    + 0.16 * worker
                    + 0.14 * public_value_base
                )

                accountability_capacity = clamp(
                    accountability_capacity
                    + 0.04 * accountability
                    + 0.03 * rights
                    + 0.03 * interoperability
                    - 0.04 * power,
                    0.0,
                    1.4,
                )

                dependency = clamp(
                    dependency * 0.90
                    + enclosure_force
                    + disruption
                    - 0.10 * interoperability
                    - 0.08 * accountability,
                    0.0,
                    1.8,
                )

                public_value = clamp(
                    public_value
                    + public_governance_force / 4.0
                    - enclosure_force / 4.0
                    + 0.04 * accountability_capacity
                    - 0.03 * dependency,
                    0.0,
                    1.6,
                )

            public_value_values.append(public_value)
            dependency_values.append(dependency)
            accountability_values.append(accountability_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "digital_public_value": round(public_value, 4),
                "platform_dependency_pressure": round(dependency, 4),
                "accountability_capacity": round(accountability_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_public_value": round(public_value_values[-1], 4),
            "mean_dependency_pressure": round(mean(dependency_values), 4),
            "final_accountability_capacity": round(accountability_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_public_value"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        interoperability = float(row["interoperability"])
        rights = float(row["user_rights"])
        worker = float(row["worker_protection"])
        accountability = float(row["public_accountability"])
        researcher = float(row["researcher_access"])
        competition = float(row["competition_enforcement"])
        public_infrastructure = float(row["public_infrastructure"])
        ecology = float(row["ecological_standards"])
        remedy = float(row["remedy_capacity"])

        public_interest = (
            0.16 * interoperability
            + 0.14 * rights
            + 0.14 * worker
            + 0.16 * accountability
            + 0.10 * researcher
            + 0.10 * competition
            + 0.10 * public_infrastructure
            + 0.08 * ecology
            + 0.02 * remedy
        )

        accountability_strategy = (
            0.16 * accountability
            + 0.16 * remedy
            + 0.14 * rights
            + 0.12 * worker
            + 0.12 * researcher
            + 0.12 * competition
            + 0.10 * interoperability
            + 0.08 * public_infrastructure
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "public_interest_platform_strategy_score": round(public_interest, 4),
            "accountability_strategy_score": round(accountability_strategy, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_platform_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    platforms: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    accountability: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Platform Profile Scores",
        "",
    ]

    for row in platforms:
        lines.append(
            f"- **{row['platform_name']}**: platform power {row['platform_power_score']}; "
            f"dependency pressure {row['platform_dependency_pressure_score']}; public-interest capacity {row['public_interest_platform_capacity_score']}."
        )

    lines.extend(["", "## Platform Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['platform_risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Accountability Gaps", ""])
    for row in accountability:
        lines.append(
            f"- **{row['accountability_dimension']}**: accountability capacity {row['accountability_capacity_score']}; "
            f"gap {row['accountability_gap_score']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: public-interest capacity {row['public_interest_platform_capacity_score']}; "
            f"dependency pressure {row['platform_dependency_pressure_score']}; class: {row['scenario_class']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final public value {row['final_public_value']}; "
            f"mean dependency pressure {row['mean_dependency_pressure']}; final accountability capacity {row['final_accountability_capacity']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: public-interest strategy score {row['public_interest_platform_strategy_score']}; "
            f"accountability strategy score {row['accountability_strategy_score']}."
        )

    avg_dependency = mean(float(row["platform_dependency_pressure_score"]) for row in platforms)
    avg_accountability_gap = mean(float(row["accountability_gap_score"]) for row in accountability)
    avg_public_capacity = mean(float(row["public_interest_platform_capacity_score"]) for row in scenarios)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Platforms: {len(platforms)}.",
        f"- Risk records: {len(risks)}.",
        f"- Accountability indicators: {len(accountability)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- Average platform dependency pressure: {round(avg_dependency, 4)}.",
        f"- Average accountability gap: {round(avg_accountability_gap, 4)}.",
        f"- Average scenario public-interest platform capacity: {round(avg_public_capacity, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats digital platform futures as a systems-governance challenge. It compares platform power, data advantage, gatekeeping, lock-in, interoperability, user rights, worker protection, public accountability, ecological responsibility, digital public value, platform dependency pressure, and public-interest strategy options.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "digital_platform_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    platforms_raw = read_csv(DATA / "platform_profiles.csv")
    risks_raw = read_csv(DATA / "platform_risk_register.csv")
    accountability_raw = read_csv(DATA / "accountability_indicators.csv")
    scenarios_raw = read_csv(DATA / "platform_scenarios.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(platforms_raw, risks_raw, accountability_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    platforms = score_platforms(platforms_raw)
    risks = score_risks(risks_raw)
    accountability = score_accountability(accountability_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "platform_profile_scores.csv", platforms)
    write_csv(OUTPUTS / "platform_risk_scores.csv", risks)
    write_csv(OUTPUTS / "platform_accountability_scores.csv", accountability)
    write_csv(OUTPUTS / "platform_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "digital_platform_pathways.csv", trajectories)
    write_csv(OUTPUTS / "digital_platform_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, platforms, risks, accountability, scenarios, pathway_summary, strategies)

    print(f"Digital platform futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
