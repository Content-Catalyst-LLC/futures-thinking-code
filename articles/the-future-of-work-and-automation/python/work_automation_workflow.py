#!/usr/bin/env python3
"""
Standard-library workflow for The Future of Work and Automation.

Outputs:
- occupation_future_scores.csv
- task_exposure_scores.csv
- work_scenario_scores.csv
- algorithmic_management_risk_scores.csv
- social_protection_scores.csv
- work_automation_paths.csv
- work_automation_summary.csv
- strategy_option_scores.csv
- work_automation_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 1.5) -> float:
    return max(low, min(high, value))


def validate_records(
    occupations: list[dict[str, str]],
    tasks: list[dict[str, str]],
    risks: list[dict[str, str]],
    protections: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    occupation_ids = {row["occupation_id"] for row in occupations}

    for dataset_name, rows in [
        ("task_exposure_matrix", tasks),
        ("algorithmic_management_risks", risks),
        ("social_protection_indicators", protections),
        ("pathway_parameters", pathways),
    ]:
        for row in rows:
            if row["occupation_id"] not in occupation_ids:
                errors.append(f"{dataset_name} record references missing occupation {row['occupation_id']}.")

    numeric_specs = [
        ("occupations", occupations, ["employment_scale", "wage_security", "task_exposure", "augmentation_capacity", "worker_voice", "training_access", "social_protection", "surveillance_intensity", "initial_job_quality"]),
        ("tasks", tasks, ["task_weight", "ai_exposure", "robotics_exposure", "monitoring_exposure", "augmentation_potential", "human_context_requirement"]),
        ("risks", risks, ["probability", "severity", "detection_difficulty", "worker_voice_gap", "due_process_gap", "privacy_exposure", "mitigation_capacity"]),
        ("protections", protections, ["training_access", "income_support", "portable_benefits", "wage_floor", "appeal_rights", "collective_bargaining_access", "public_investment"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("occupation_id") or row.get("task_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_occupations(occupations: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in occupations:
        task_exposure = float(row["task_exposure"])
        augmentation = float(row["augmentation_capacity"])
        voice = float(row["worker_voice"])
        training = float(row["training_access"])
        protection = float(row["social_protection"])
        surveillance = float(row["surveillance_intensity"])
        wage_security = float(row["wage_security"])
        job_quality = float(row["initial_job_quality"])

        exposure_pressure = (
            0.34 * task_exposure
            + 0.22 * surveillance
            + 0.18 * (1.0 - voice)
            + 0.14 * (1.0 - training)
            + 0.12 * (1.0 - protection)
        )

        worker_centered_capacity = (
            0.20 * augmentation
            + 0.20 * voice
            + 0.16 * training
            + 0.16 * protection
            + 0.14 * wage_security
            + 0.14 * (1.0 - surveillance)
        )

        transition_risk = task_exposure * (1.0 - training) * (1.0 - protection + surveillance / 2.0)

        adjusted_job_quality = (
            0.28 * job_quality
            + 0.18 * wage_security
            + 0.18 * voice
            + 0.16 * protection
            + 0.12 * training
            + 0.08 * (1.0 - surveillance)
        )

        rows.append({
            "occupation_id": row["occupation_id"],
            "occupation_name": row["occupation_name"],
            "sector": row["sector"],
            "exposure_pressure_score": round(exposure_pressure, 4),
            "worker_centered_capacity_score": round(worker_centered_capacity, 4),
            "transition_risk_score": round(transition_risk, 4),
            "adjusted_job_quality_score": round(adjusted_job_quality, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["transition_risk_score"]), reverse=True)
    return rows


def score_tasks(tasks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in tasks:
        weight = float(row["task_weight"])
        ai = float(row["ai_exposure"])
        robotics = float(row["robotics_exposure"])
        monitoring = float(row["monitoring_exposure"])
        augmentation = float(row["augmentation_potential"])
        context = float(row["human_context_requirement"])

        automation_exposure = weight * (0.42 * ai + 0.28 * robotics + 0.18 * monitoring + 0.12 * (1.0 - context))
        augmentation_score = weight * (0.60 * augmentation + 0.25 * context + 0.15 * ai)
        substitution_pressure = automation_exposure - augmentation_score / 2.0

        rows.append({
            "task_id": row["task_id"],
            "occupation_id": row["occupation_id"],
            "task_name": row["task_name"],
            "task_category": row["task_category"],
            "weighted_automation_exposure": round(automation_exposure, 4),
            "weighted_augmentation_score": round(augmentation_score, 4),
            "task_substitution_pressure": round(substitution_pressure, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["task_substitution_pressure"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        automation = float(row["automation_intensity"])
        augmentation = float(row["augmentation_capacity"])
        voice = float(row["worker_voice"])
        quality = float(row["job_quality"])
        surveillance = float(row["surveillance_intensity"])
        support = float(row["transition_support"])
        mobility = float(row["skill_mobility"])
        protection = float(row["social_protection"])

        worker_centered = (
            0.18 * augmentation
            + 0.18 * voice
            + 0.18 * quality
            + 0.14 * support
            + 0.14 * mobility
            + 0.12 * protection
            + 0.06 * (1.0 - surveillance)
        )

        displacement_pressure = (
            0.30 * automation
            + 0.22 * surveillance
            + 0.18 * (1.0 - support)
            + 0.16 * (1.0 - mobility)
            + 0.14 * (1.0 - protection)
        )

        if worker_centered >= 0.75:
            scenario_class = "High worker-centered capacity"
        elif displacement_pressure >= 0.65:
            scenario_class = "High displacement and control risk"
        else:
            scenario_class = "Contested transition pathway"

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "worker_centered_capacity_score": round(worker_centered, 4),
            "displacement_control_pressure_score": round(displacement_pressure, 4),
            "scenario_class": scenario_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["worker_centered_capacity_score"]), reverse=True)
    return rows


def score_algorithmic_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        probability = float(row["probability"])
        severity = float(row["severity"])
        detection = float(row["detection_difficulty"])
        voice_gap = float(row["worker_voice_gap"])
        due_process = float(row["due_process_gap"])
        privacy = float(row["privacy_exposure"])
        mitigation = float(row["mitigation_capacity"])

        risk_score = (
            0.18 * probability
            + 0.20 * severity
            + 0.14 * detection
            + 0.16 * voice_gap
            + 0.16 * due_process
            + 0.10 * privacy
            + 0.06 * (1.0 - mitigation)
        )

        rows.append({
            "risk_id": row["risk_id"],
            "occupation_id": row["occupation_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "algorithmic_management_risk_score": round(risk_score, 4),
            "mitigation_capacity": mitigation,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["algorithmic_management_risk_score"]), reverse=True)
    return rows


def score_social_protection(protections: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in protections:
        training = float(row["training_access"])
        income = float(row["income_support"])
        portable = float(row["portable_benefits"])
        wage_floor = float(row["wage_floor"])
        appeals = float(row["appeal_rights"])
        bargaining = float(row["collective_bargaining_access"])
        investment = float(row["public_investment"])

        readiness = (
            0.16 * training
            + 0.16 * income
            + 0.14 * portable
            + 0.14 * wage_floor
            + 0.14 * appeals
            + 0.14 * bargaining
            + 0.12 * investment
        )

        rows.append({
            "protection_id": row["protection_id"],
            "occupation_id": row["occupation_id"],
            "protection_name": row["protection_name"],
            "social_protection_readiness_score": round(readiness, 4),
            "social_protection_gap_score": round(1.0 - readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["social_protection_gap_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        task_exposure = float(row["task_exposure"])
        augmentation = float(row["augmentation_capacity"])
        voice = float(row["worker_voice"])
        training = float(row["training_access"])
        protection = float(row["social_protection"])
        surveillance = float(row["surveillance_intensity"])
        job_quality = float(row["initial_job_quality"])
        transition_risk = task_exposure * (1.0 - training)
        skill_mobility = training
        horizon = int(row["time_horizon"])

        quality_values: list[float] = []
        risk_values: list[float] = []
        mobility_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                automation_pressure = 0.05 + 0.10 * task_exposure
                augmentation_gain = 0.08 * augmentation
                voice_buffer = 0.06 * voice
                protection_buffer = 0.05 * protection
                surveillance_penalty = 0.07 * surveillance
                shock = 0.08 if t % 10 == 0 else 0.02

                transition_risk = clamp(
                    transition_risk * 0.90
                    + automation_pressure
                    + shock
                    - 0.06 * training
                    - 0.05 * protection,
                    0.0,
                    1.5,
                )

                skill_mobility = clamp(
                    skill_mobility + 0.04 * training + 0.03 * augmentation - 0.02 * surveillance,
                    0.0,
                    1.2,
                )

                job_quality = clamp(
                    job_quality
                    + augmentation_gain
                    + voice_buffer
                    + protection_buffer
                    - automation_pressure / 2.0
                    - surveillance_penalty
                    - shock / 2.0,
                    0.0,
                    1.5,
                )

            quality_values.append(job_quality)
            risk_values.append(transition_risk)
            mobility_values.append(skill_mobility)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "occupation_id": row["occupation_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "job_quality": round(job_quality, 4),
                "transition_risk": round(transition_risk, 4),
                "skill_mobility": round(skill_mobility, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "occupation_id": row["occupation_id"],
            "pathway_name": row["pathway_name"],
            "final_job_quality": round(quality_values[-1], 4),
            "mean_transition_risk": round(mean(risk_values), 4),
            "final_skill_mobility": round(mobility_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_job_quality"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        automation_governance = float(row["automation_governance"])
        voice = float(row["worker_voice"])
        training = float(row["training_commitment"])
        protection = float(row["social_protection"])
        quality = float(row["job_quality_commitment"])
        privacy = float(row["privacy_protection"])
        productivity = float(row["productivity_sharing"])
        care = float(row["care_investment"])

        worker_centered_strategy = (
            0.16 * automation_governance
            + 0.18 * voice
            + 0.14 * training
            + 0.14 * protection
            + 0.14 * quality
            + 0.10 * privacy
            + 0.08 * productivity
            + 0.06 * care
        )

        shared_prosperity = (
            0.14 * voice
            + 0.14 * protection
            + 0.14 * quality
            + 0.16 * productivity
            + 0.14 * care
            + 0.14 * training
            + 0.14 * automation_governance
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "worker_centered_strategy_score": round(worker_centered_strategy, 4),
            "shared_prosperity_score": round(shared_prosperity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["worker_centered_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    occupations: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    protections: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Occupation Future Scores",
        "",
    ]

    for row in occupations:
        lines.append(
            f"- **{row['occupation_name']}**: exposure pressure {row['exposure_pressure_score']}; "
            f"transition risk {row['transition_risk_score']}; worker-centered capacity {row['worker_centered_capacity_score']}."
        )

    lines.extend(["", "## Highest Task Substitution Pressures", ""])
    for row in tasks[:8]:
        lines.append(
            f"- **{row['task_name']}**: substitution pressure {row['task_substitution_pressure']}; "
            f"automation exposure {row['weighted_automation_exposure']}."
        )

    lines.extend(["", "## Work Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: worker-centered capacity {row['worker_centered_capacity_score']}; "
            f"displacement/control pressure {row['displacement_control_pressure_score']}; class: {row['scenario_class']}."
        )

    lines.extend(["", "## Algorithmic Management Risks", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk score {row['algorithmic_management_risk_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Social Protection Gaps", ""])
    for row in protections:
        lines.append(
            f"- **{row['protection_name']}**: readiness {row['social_protection_readiness_score']}; "
            f"gap {row['social_protection_gap_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final job quality {row['final_job_quality']}; "
            f"mean transition risk {row['mean_transition_risk']}; final skill mobility {row['final_skill_mobility']}."
        )

    lines.extend(["", "## Strategy Option Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: worker-centered score {row['worker_centered_strategy_score']}; "
            f"shared prosperity score {row['shared_prosperity_score']}."
        )

    avg_risk = mean(float(row["transition_risk_score"]) for row in occupations)
    avg_protection_gap = mean(float(row["social_protection_gap_score"]) for row in protections)
    avg_worker_capacity = mean(float(row["worker_centered_capacity_score"]) for row in occupations)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Occupations: {len(occupations)}.",
        f"- Task records: {len(tasks)}.",
        f"- Work scenarios: {len(scenarios)}.",
        f"- Algorithmic management risks: {len(risks)}.",
        f"- Social protection records: {len(protections)}.",
        f"- Average transition risk score: {round(avg_risk, 4)}.",
        f"- Average social protection gap score: {round(avg_protection_gap, 4)}.",
        f"- Average worker-centered capacity score: {round(avg_worker_capacity, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats the future of work and automation as a task-level and institution-level transformation problem. It compares exposure, augmentation, worker voice, social protection, surveillance, job quality, skill mobility, transition risk, algorithmic management, and strategy options. Scores support transparent futures analysis rather than deterministic prediction.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "work_automation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    occupations_raw = read_csv(DATA / "occupation_profiles.csv")
    tasks_raw = read_csv(DATA / "task_exposure_matrix.csv")
    scenarios_raw = read_csv(DATA / "work_scenarios.csv")
    risks_raw = read_csv(DATA / "algorithmic_management_risks.csv")
    protections_raw = read_csv(DATA / "social_protection_indicators.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(occupations_raw, tasks_raw, risks_raw, protections_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    occupations = score_occupations(occupations_raw)
    tasks = score_tasks(tasks_raw)
    scenarios = score_scenarios(scenarios_raw)
    risks = score_algorithmic_risks(risks_raw)
    protections = score_social_protection(protections_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "occupation_future_scores.csv", occupations)
    write_csv(OUTPUTS / "task_exposure_scores.csv", tasks)
    write_csv(OUTPUTS / "work_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "algorithmic_management_risk_scores.csv", risks)
    write_csv(OUTPUTS / "social_protection_scores.csv", protections)
    write_csv(OUTPUTS / "work_automation_paths.csv", trajectories)
    write_csv(OUTPUTS / "work_automation_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, occupations, tasks, scenarios, risks, protections, pathway_summary, strategies)

    print(f"Work automation workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
