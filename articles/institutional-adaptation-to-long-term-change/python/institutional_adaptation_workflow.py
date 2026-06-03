#!/usr/bin/env python3
"""
Standard-library workflow for Institutional Adaptation to Long-Term Change.

Outputs:
- institutional_profile_scores.csv
- adaptation_risk_scores.csv
- feedback_capacity_scores.csv
- adaptation_scenario_scores.csv
- institutional_adaptation_pathways.csv
- institutional_adaptation_pathway_summary.csv
- strategy_option_scores.csv
- institutional_adaptation_report.md
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


def adaptive_profile(row: dict[str, str]) -> float:
    return (
        0.18 * float(row["learning_capacity"])
        + 0.16 * float(row["structural_flexibility"])
        + 0.16 * float(row["coordination_capacity"])
        + 0.14 * float(row["legitimacy"])
        + 0.14 * float(row["feedback_sensitivity"])
        + 0.10 * float(row["resource_mobility"])
        + 0.08 * float(row["shock_responsiveness"])
        - 0.10 * float(row["rigidity"])
        + 0.04 * float(row["intergenerational_responsibility"])
    )


def fragility_pressure(row: dict[str, str]) -> float:
    return (
        0.20 * float(row["rigidity"])
        + 0.16 * (1.0 - float(row["learning_capacity"]))
        + 0.16 * (1.0 - float(row["structural_flexibility"]))
        + 0.14 * (1.0 - float(row["coordination_capacity"]))
        + 0.12 * (1.0 - float(row["legitimacy"]))
        + 0.12 * (1.0 - float(row["feedback_sensitivity"]))
        + 0.10 * (1.0 - float(row["resource_mobility"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    risks: list[dict[str, str]],
    feedback: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    institution_ids = {row["institution_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["institution_id"] not in institution_ids:
            errors.append(f"Risk {row['risk_id']} references missing institution {row['institution_id']}.")

    for row in feedback:
        if row["institution_id"] not in institution_ids:
            errors.append(f"Feedback record {row['feedback_id']} references missing institution {row['institution_id']}.")

    for row in pathways:
        if row["institution_id"] not in institution_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing institution {row['institution_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["learning_capacity", "structural_flexibility", "coordination_capacity", "legitimacy", "feedback_sensitivity", "resource_mobility", "shock_responsiveness", "rigidity", "intergenerational_responsibility"]),
        ("risks", risks, ["probability", "severity", "detection_difficulty", "governance_gap", "legitimacy_exposure", "implementation_exposure", "mitigation_capacity"]),
        ("feedback", feedback, ["signal_detection", "interpretation_capacity", "evaluation_quality", "memory_retention", "revision_authority", "community_feedback", "public_reporting"]),
        ("scenarios", scenarios, ["environmental_pressure", "technological_change", "demographic_pressure", "fiscal_constraint", "public_trust", "coordination_demand", "crisis_frequency"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("institution_id") or row.get("scenario_id") or row.get("risk_id") or row.get("feedback_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        profile = adaptive_profile(row)
        fragility = fragility_pressure(row)

        if profile >= 0.58:
            adaptation_class = "Strong adaptive profile"
        elif fragility >= 0.55:
            adaptation_class = "High institutional fragility"
        else:
            adaptation_class = "Contested adaptation profile"

        rows.append({
            "institution_id": row["institution_id"],
            "institution_name": row["institution_name"],
            "institution_type": row["institution_type"],
            "adaptive_profile_score": round(profile, 4),
            "fragility_pressure_score": round(fragility, 4),
            "adaptation_class": adaptation_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["adaptive_profile_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.18 * float(row["probability"])
            + 0.20 * float(row["severity"])
            + 0.14 * float(row["detection_difficulty"])
            + 0.16 * float(row["governance_gap"])
            + 0.12 * float(row["legitimacy_exposure"])
            + 0.12 * float(row["implementation_exposure"])
            + 0.08 * (1.0 - float(row["mitigation_capacity"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "institution_id": row["institution_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "adaptation_risk_priority_score": round(priority, 4),
            "mitigation_capacity": float(row["mitigation_capacity"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["adaptation_risk_priority_score"]), reverse=True)
    return rows


def score_feedback(feedback_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in feedback_rows:
        score = (
            0.18 * float(row["signal_detection"])
            + 0.16 * float(row["interpretation_capacity"])
            + 0.16 * float(row["evaluation_quality"])
            + 0.14 * float(row["memory_retention"])
            + 0.14 * float(row["revision_authority"])
            + 0.12 * float(row["community_feedback"])
            + 0.10 * float(row["public_reporting"])
        )

        rows.append({
            "feedback_id": row["feedback_id"],
            "institution_id": row["institution_id"],
            "feedback_dimension": row["feedback_dimension"],
            "feedback_capacity_score": round(score, 4),
            "feedback_gap_score": round(1.0 - score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["feedback_capacity_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.18 * float(row["environmental_pressure"])
            + 0.18 * float(row["technological_change"])
            + 0.14 * float(row["demographic_pressure"])
            + 0.14 * float(row["fiscal_constraint"])
            + 0.12 * (1.0 - float(row["public_trust"]))
            + 0.12 * float(row["coordination_demand"])
            + 0.12 * float(row["crisis_frequency"])
        )

        opportunity = (
            0.24 * float(row["public_trust"])
            + 0.22 * (1.0 - float(row["fiscal_constraint"]))
            + 0.18 * (1.0 - float(row["crisis_frequency"]))
            + 0.14 * (1.0 - float(row["environmental_pressure"]))
            + 0.12 * (1.0 - float(row["technological_change"]))
            + 0.10 * float(row["coordination_demand"])
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "institutional_stress_pressure_score": round(stress, 4),
            "adaptation_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["institutional_stress_pressure_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        learning = float(row["learning"])
        flexibility = float(row["flexibility"])
        coordination = float(row["coordination"])
        legitimacy = float(row["legitimacy"])
        feedback = float(row["feedback"])
        resources = float(row["resources"])
        rigidity = float(row["rigidity"])
        viability = float(row["initial_viability"])
        legitimacy_state = legitimacy
        learning_state = learning
        horizon = int(row["time_horizon"])

        viability_values: list[float] = []
        legitimacy_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.18 if t % 7 == 0 else 0.08

                adaptation_gain = (
                    0.20 * learning_state
                    + 0.18 * flexibility
                    + 0.18 * coordination
                    + 0.16 * feedback
                    + 0.14 * resources
                    + 0.10 * legitimacy_state
                    - 0.18 * rigidity
                )

                legitimacy_state = clamp(
                    legitimacy_state
                    + 0.04 * legitimacy
                    + 0.03 * feedback
                    + 0.02 * coordination
                    - 0.04 * disruption
                    - 0.03 * rigidity,
                    0.0,
                    1.4,
                )

                learning_state = clamp(
                    learning_state
                    + 0.04 * feedback
                    + 0.03 * learning
                    + 0.02 * coordination
                    - 0.03 * rigidity
                    - 0.02 * disruption,
                    0.0,
                    1.4,
                )

                viability = clamp(
                    viability
                    - disruption
                    + adaptation_gain
                    + 0.04 * learning_state
                    - 0.04 * (1.0 - legitimacy_state),
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            legitimacy_values.append(legitimacy_state)
            learning_values.append(learning_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "institution_id": row["institution_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "institutional_viability": round(viability, 4),
                "legitimacy_score": round(legitimacy_state, 4),
                "learning_score": round(learning_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "institution_id": row["institution_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_institutional_viability": round(viability_values[-1], 4),
            "mean_institutional_viability": round(mean(viability_values), 4),
            "final_legitimacy_score": round(legitimacy_values[-1], 4),
            "final_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_institutional_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        adaptation = (
            0.16 * float(row["learning_systems"])
            + 0.14 * float(row["adaptive_legal_design"])
            + 0.14 * float(row["cross_agency_coordination"])
            + 0.14 * float(row["participatory_governance"])
            + 0.12 * float(row["long_term_budgeting"])
            + 0.12 * float(row["feedback_infrastructure"])
            + 0.10 * float(row["accountability_safeguards"])
            + 0.05 * float(row["resource_mobility"])
            + 0.03 * float(row["power_analysis"])
        )

        legitimacy = (
            0.18 * float(row["participatory_governance"])
            + 0.16 * float(row["accountability_safeguards"])
            + 0.14 * float(row["power_analysis"])
            + 0.12 * float(row["feedback_infrastructure"])
            + 0.12 * float(row["learning_systems"])
            + 0.10 * float(row["cross_agency_coordination"])
            + 0.10 * float(row["long_term_budgeting"])
            + 0.08 * float(row["adaptive_legal_design"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "institutional_adaptation_strategy_score": round(adaptation, 4),
            "legitimacy_and_accountability_strategy_score": round(legitimacy, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["institutional_adaptation_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    profiles: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    feedback: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Institutional Profile Scores",
        "",
    ]

    for row in profiles:
        lines.append(
            f"- **{row['institution_name']}**: adaptive profile {row['adaptive_profile_score']}; "
            f"fragility pressure {row['fragility_pressure_score']}; class: {row['adaptation_class']}."
        )

    lines.extend(["", "## Adaptation Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['adaptation_risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Feedback Capacity Scores", ""])
    for row in feedback:
        lines.append(
            f"- **{row['feedback_dimension']}**: feedback capacity {row['feedback_capacity_score']}; "
            f"gap {row['feedback_gap_score']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: institutional stress {row['institutional_stress_pressure_score']}; "
            f"adaptation opportunity {row['adaptation_opportunity_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_institutional_viability']}; "
            f"final legitimacy {row['final_legitimacy_score']}; final learning {row['final_learning_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: adaptation strategy {row['institutional_adaptation_strategy_score']}; "
            f"legitimacy and accountability strategy {row['legitimacy_and_accountability_strategy_score']}."
        )

    avg_profile = mean(float(row["adaptive_profile_score"]) for row in profiles)
    avg_risk = mean(float(row["adaptation_risk_priority_score"]) for row in risks)
    avg_feedback = mean(float(row["feedback_capacity_score"]) for row in feedback)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Institutions: {len(profiles)}.",
        f"- Risk records: {len(risks)}.",
        f"- Feedback records: {len(feedback)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- Average adaptive profile score: {round(avg_profile, 4)}.",
        f"- Average adaptation risk priority score: {round(avg_risk, 4)}.",
        f"- Average feedback capacity score: {round(avg_feedback, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats institutional adaptation as a systems-governance challenge. It compares learning capacity, structural flexibility, coordination, legitimacy, feedback sensitivity, resource mobility, shock responsiveness, rigidity, risk exposure, and adaptive pathway performance.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "institutional_adaptation_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "institutional_profiles.csv")
    risks_raw = read_csv(DATA / "adaptation_risk_register.csv")
    feedback_raw = read_csv(DATA / "feedback_indicators.csv")
    scenarios_raw = read_csv(DATA / "adaptation_scenarios.csv")
    pathways_raw = read_csv(DATA / "adaptive_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(profiles_raw, risks_raw, feedback_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profiles = score_profiles(profiles_raw)
    risks = score_risks(risks_raw)
    feedback = score_feedback(feedback_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "institutional_profile_scores.csv", profiles)
    write_csv(OUTPUTS / "adaptation_risk_scores.csv", risks)
    write_csv(OUTPUTS / "feedback_capacity_scores.csv", feedback)
    write_csv(OUTPUTS / "adaptation_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "institutional_adaptation_pathways.csv", trajectories)
    write_csv(OUTPUTS / "institutional_adaptation_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, profiles, risks, feedback, scenarios, pathway_summary, strategies)

    print(f"Institutional adaptation workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
