#!/usr/bin/env python3
"""
Standard-library workflow for Climate Futures and Environmental Change.

Outputs:
- climate_profile_scores.csv
- climate_scenario_scores.csv
- mitigation_adaptation_strategy_scores.csv
- climate_risk_priority_scores.csv
- climate_governance_capacity_scores.csv
- climate_pathways.csv
- climate_pathway_summary.csv
- climate_futures_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 3.0) -> float:
    return max(low, min(high, value))


def climate_readiness(row: dict[str, str]) -> float:
    return (
        -0.16 * float(row["emissions_intensity"])
        + 0.15 * float(row["adaptation_capacity"])
        - 0.15 * float(row["ecosystem_stress"])
        + 0.14 * float(row["governance_coordination"])
        - 0.12 * float(row["social_vulnerability"])
        + 0.10 * float(row["technology_deployment"])
        + 0.14 * float(row["transition_speed"])
        + 0.12 * float(row["justice_capacity"])
        - 0.10 * float(row["residual_loss"])
    )


def climate_fragility(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["emissions_intensity"])
        + 0.15 * float(row["ecosystem_stress"])
        + 0.14 * float(row["social_vulnerability"])
        + 0.13 * float(row["residual_loss"])
        + 0.12 * (1.0 - float(row["adaptation_capacity"]))
        + 0.12 * (1.0 - float(row["governance_coordination"]))
        + 0.10 * (1.0 - float(row["transition_speed"]))
        + 0.08 * (1.0 - float(row["justice_capacity"]))
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
        ("profiles", profiles, ["emissions_intensity", "adaptation_capacity", "ecosystem_stress", "governance_coordination", "social_vulnerability", "technology_deployment", "transition_speed", "justice_capacity", "residual_loss"]),
        ("scenarios", scenarios, ["emissions_pressure", "feedback_pressure", "physical_hazard_pressure", "ecological_degradation", "social_vulnerability_pressure", "transition_momentum", "governance_fragmentation", "adaptation_finance_gap"]),
        ("strategies", strategies, ["mitigation_effect", "adaptation_gain", "vulnerability_reduction", "ecosystem_protection", "governance_gain", "finance_capacity", "justice_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "systemic_reach", "visibility_gap", "distributional_harm", "preparedness"]),
        ("governance", governance, ["mitigation_governance", "adaptation_governance", "public_finance", "monitoring_capacity", "coordination", "participation", "justice_safeguards"]),
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
        readiness = climate_readiness(row)
        fragility = climate_fragility(row)

        if readiness >= 0.12 and fragility < 0.48:
            profile_class = "Stronger climate readiness"
        elif fragility >= 0.66:
            profile_class = "High climate fragility"
        else:
            profile_class = "Mixed or transitional climate future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "climate_readiness_score": round(readiness, 4),
            "climate_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["climate_readiness_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.15 * float(row["emissions_pressure"])
            + 0.15 * float(row["feedback_pressure"])
            + 0.15 * float(row["physical_hazard_pressure"])
            + 0.13 * float(row["ecological_degradation"])
            + 0.14 * float(row["social_vulnerability_pressure"])
            + 0.12 * float(row["governance_fragmentation"])
            + 0.10 * float(row["adaptation_finance_gap"])
            + 0.06 * (1.0 - float(row["transition_momentum"]))
        )

        transition_opportunity = (
            0.22 * float(row["transition_momentum"])
            + 0.14 * (1.0 - float(row["emissions_pressure"]))
            + 0.12 * (1.0 - float(row["governance_fragmentation"]))
            + 0.12 * (1.0 - float(row["adaptation_finance_gap"]))
            + 0.12 * (1.0 - float(row["social_vulnerability_pressure"]))
            + 0.10 * (1.0 - float(row["ecological_degradation"]))
            + 0.09 * (1.0 - float(row["feedback_pressure"]))
            + 0.09 * (1.0 - float(row["physical_hazard_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "climate_stress_score": round(stress, 4),
            "transition_opportunity_score": round(transition_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["climate_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.17 * float(row["mitigation_effect"])
            + 0.16 * float(row["adaptation_gain"])
            + 0.15 * float(row["vulnerability_reduction"])
            + 0.14 * float(row["ecosystem_protection"])
            + 0.13 * float(row["governance_gain"])
            + 0.11 * float(row["finance_capacity"])
            + 0.10 * float(row["justice_gain"])
            + 0.04 * float(row["implementation_capacity"])
        )

        readiness = (
            0.24 * float(row["implementation_capacity"])
            + 0.14 * float(row["governance_gain"])
            + 0.14 * float(row["finance_capacity"])
            + 0.12 * float(row["adaptation_gain"])
            + 0.12 * float(row["mitigation_effect"])
            + 0.10 * float(row["vulnerability_reduction"])
            + 0.08 * float(row["justice_gain"])
            + 0.06 * float(row["ecosystem_protection"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "climate_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["climate_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.17 * float(row["irreversibility"])
            + 0.16 * float(row["systemic_reach"])
            + 0.12 * float(row["visibility_gap"])
            + 0.15 * float(row["distributional_harm"])
            + 0.08 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "climate_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["climate_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.16 * float(row["mitigation_governance"])
            + 0.16 * float(row["adaptation_governance"])
            + 0.14 * float(row["public_finance"])
            + 0.14 * float(row["monitoring_capacity"])
            + 0.16 * float(row["coordination"])
            + 0.10 * float(row["participation"])
            + 0.14 * float(row["justice_safeguards"])
        )

        legitimacy_gap = (
            0.18 * (1.0 - float(row["participation"]))
            + 0.18 * (1.0 - float(row["justice_safeguards"]))
            + 0.14 * (1.0 - float(row["adaptation_governance"]))
            + 0.14 * (1.0 - float(row["coordination"]))
            + 0.12 * (1.0 - float(row["public_finance"]))
            + 0.12 * (1.0 - float(row["mitigation_governance"]))
            + 0.12 * (1.0 - float(row["monitoring_capacity"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "climate_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["climate_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        emissions = float(row["emissions"])
        sink_strength = float(row["sink_strength"])
        feedback_pressure = float(row["feedback_pressure"])
        adaptation = float(row["adaptation"])
        vulnerability_reduction = float(row["vulnerability_reduction"])
        governance_capacity = float(row["governance_capacity"])
        justice_capacity = float(row["justice_capacity"])
        climate_stress = float(row["initial_climate_stress"])
        horizon = int(row["time_horizon"])

        social_vulnerability = 0.70 - 0.35 * vulnerability_reduction + 0.10 * (1.0 - justice_capacity)
        adaptive_capacity = 0.30 + 0.35 * adaptation + 0.25 * governance_capacity + 0.15 * justice_capacity

        stress_values: list[float] = []
        vulnerability_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                feedback_event = feedback_pressure if t % 10 == 0 else feedback_pressure * 0.45

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.03 * governance_capacity
                    + 0.03 * adaptation
                    + 0.02 * justice_capacity
                    - 0.02 * feedback_event,
                    0.0,
                    1.5,
                )

                social_vulnerability = clamp(
                    social_vulnerability
                    - 0.03 * vulnerability_reduction
                    - 0.02 * governance_capacity
                    - 0.02 * justice_capacity
                    + 0.02 * climate_stress,
                    0.0,
                    1.2,
                )

                climate_stress = clamp(
                    climate_stress
                    + emissions
                    - sink_strength
                    + feedback_event
                    - 0.18 * adaptation
                    - 0.08 * governance_capacity
                    - 0.05 * justice_capacity,
                    0.0,
                    3.0,
                )

            stress_values.append(climate_stress)
            vulnerability_values.append(social_vulnerability)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "climate_stress_index": round(climate_stress, 4),
                "social_vulnerability_index": round(social_vulnerability, 4),
                "adaptive_capacity_index": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_climate_stress": round(stress_values[-1], 4),
            "mean_climate_stress": round(mean(stress_values), 4),
            "final_social_vulnerability": round(vulnerability_values[-1], 4),
            "final_adaptive_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_climate_stress"]))
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
        "## Climate Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: readiness {row['climate_readiness_score']}; "
            f"fragility {row['climate_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Climate Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: climate stress {row['climate_stress_score']}; "
            f"transition opportunity {row['transition_opportunity_score']}."
        )

    lines.extend(["", "## Mitigation and Adaptation Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: value {row['climate_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Climate Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['climate_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Climate Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['climate_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Climate Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final climate stress {row['final_climate_stress']}; "
            f"final social vulnerability {row['final_social_vulnerability']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_readiness = mean(float(row["climate_readiness_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["climate_fragility_score"]) for row in profile_scores)
    avg_final_stress = mean(float(row["final_climate_stress"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Climate future profiles: {len(profile_scores)}.",
        f"- Climate scenarios: {len(scenario_scores)}.",
        f"- Mitigation/adaptation strategies: {len(strategy_scores)}.",
        f"- Climate risk indicators: {len(risk_scores)}.",
        f"- Climate governance records: {len(governance_scores)}.",
        f"- Average climate readiness score: {round(avg_readiness, 4)}.",
        f"- Average climate fragility score: {round(avg_fragility, 4)}.",
        f"- Average final climate stress: {round(avg_final_stress, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats climate futures as social-ecological systems shaped by emissions, sinks, feedbacks, adaptation, vulnerability, governance, justice, technology, residual loss, and environmental change.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "climate_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "climate_future_profiles.csv")
    scenarios_raw = read_csv(DATA / "climate_scenarios.csv")
    strategies_raw = read_csv(DATA / "mitigation_adaptation_strategies.csv")
    risks_raw = read_csv(DATA / "climate_risk_indicators.csv")
    governance_raw = read_csv(DATA / "climate_governance_records.csv")
    pathways_raw = read_csv(DATA / "climate_pathways.csv")

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

    write_csv(OUTPUTS / "climate_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "climate_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "mitigation_adaptation_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "climate_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "climate_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "climate_pathways.csv", trajectories)
    write_csv(OUTPUTS / "climate_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Climate futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
