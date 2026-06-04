#!/usr/bin/env python3
"""
Standard-library workflow for Futures Thinking and Risk Analysis.

Outputs:
- risk_profile_scores.csv
- risk_scenario_scores.csv
- strategy_robustness_scores.csv
- risk_indicator_priority_scores.csv
- risk_governance_capacity_scores.csv
- adaptive_pathway_trajectories.csv
- adaptive_pathway_summary.csv
- futures_risk_analysis_report.md
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


def futures_risk_score(row: dict[str, str]) -> float:
    return (
        0.12 * (1.0 - float(row["probability_confidence"]))
        + 0.16 * float(row["structural_uncertainty"])
        + 0.14 * float(row["interdependence"])
        + 0.15 * float(row["vulnerability"])
        - 0.11 * float(row["resilience_capacity"])
        - 0.10 * float(row["governance_capacity"])
        - 0.08 * float(row["signal_visibility"])
        + 0.12 * float(row["tail_risk_severity"])
        + 0.10 * float(row["distributional_harm"])
        - 0.02 * float(row["adaptive_capacity"])
    )


def preparedness_gap(row: dict[str, str]) -> float:
    return (
        0.18 * (1.0 - float(row["resilience_capacity"]))
        + 0.18 * (1.0 - float(row["governance_capacity"]))
        + 0.15 * (1.0 - float(row["signal_visibility"]))
        + 0.15 * float(row["structural_uncertainty"])
        + 0.12 * float(row["vulnerability"])
        + 0.10 * float(row["tail_risk_severity"])
        + 0.08 * float(row["distributional_harm"])
        + 0.04 * (1.0 - float(row["adaptive_capacity"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    indicators: list[dict[str, str]],
    governance: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing profile {row['profile_id']}.")

    for row in indicators:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Indicator {row['indicator_id']} references missing scenario {row['scenario_id']}.")

    for row in governance:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Governance record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["probability_confidence", "structural_uncertainty", "interdependence", "vulnerability", "resilience_capacity", "governance_capacity", "signal_visibility", "tail_risk_severity", "distributional_harm", "adaptive_capacity"]),
        ("scenarios", scenarios, ["model_uncertainty", "data_uncertainty", "nonstationarity", "cascade_potential", "tail_risk_pressure", "exposure_pressure", "vulnerability_pressure", "governance_stress", "legitimacy_stress", "early_warning_gap"]),
        ("strategies", strategies, ["baseline_performance", "technology_disruption_performance", "climate_stress_performance", "geopolitical_fragmentation_performance", "financial_contagion_performance", "institutional_breakdown_performance", "systemic_cascade_performance", "monitoring_capacity", "adaptability", "implementation_capacity", "public_legitimacy"]),
        ("indicators", indicators, ["signal_strength", "visibility_gap", "lead_time", "systemic_relevance", "cascade_potential", "tail_severity", "preparedness_gap", "distributional_harm"]),
        ("governance", governance, ["monitoring_capacity", "scenario_refresh_capacity", "cross_sector_coordination", "public_legitimacy", "learning_capacity", "flexible_finance", "accountability_capacity", "distributional_review_capacity"]),
        ("pathways", pathways, ["initial_preparedness", "monitoring_capacity", "trigger_sensitivity", "learning_capacity", "governance_capacity", "resilience_capacity", "vulnerability_pressure", "cascade_pressure", "tail_pressure", "public_legitimacy"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("indicator_id") or row.get("record_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        risk = futures_risk_score(row)
        gap = preparedness_gap(row)

        if risk >= 0.45:
            profile_class = "High futures risk"
        elif risk >= 0.30:
            profile_class = "Moderate futures risk"
        else:
            profile_class = "Lower futures risk"

        rows.append({
            "profile_id": row["profile_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "futures_risk_profile_score": round(risk, 4),
            "preparedness_gap_score": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["futures_risk_profile_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.12 * float(row["model_uncertainty"])
            + 0.09 * float(row["data_uncertainty"])
            + 0.13 * float(row["nonstationarity"])
            + 0.15 * float(row["cascade_potential"])
            + 0.12 * float(row["tail_risk_pressure"])
            + 0.10 * float(row["exposure_pressure"])
            + 0.10 * float(row["vulnerability_pressure"])
            + 0.08 * float(row["governance_stress"])
            + 0.06 * float(row["legitimacy_stress"])
            + 0.05 * float(row["early_warning_gap"])
        )

        adaptive_opportunity = (
            0.16 * (1.0 - float(row["governance_stress"]))
            + 0.15 * (1.0 - float(row["early_warning_gap"]))
            + 0.13 * (1.0 - float(row["legitimacy_stress"]))
            + 0.11 * (1.0 - float(row["vulnerability_pressure"]))
            + 0.10 * (1.0 - float(row["cascade_potential"]))
            + 0.09 * (1.0 - float(row["tail_risk_pressure"]))
            + 0.09 * (1.0 - float(row["model_uncertainty"]))
            + 0.07 * (1.0 - float(row["data_uncertainty"]))
            + 0.05 * (1.0 - float(row["nonstationarity"]))
            + 0.05 * (1.0 - float(row["exposure_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "systemic_risk_stress_score": round(stress, 4),
            "adaptive_opportunity_score": round(adaptive_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["systemic_risk_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    performance_fields = [
        "baseline_performance",
        "technology_disruption_performance",
        "climate_stress_performance",
        "geopolitical_fragmentation_performance",
        "financial_contagion_performance",
        "institutional_breakdown_performance",
        "systemic_cascade_performance",
    ]

    scenario_labels = [
        "Stable Baseline",
        "Technological Disruption",
        "Climate Stress",
        "Geopolitical Fragmentation",
        "Financial Contagion",
        "Institutional Breakdown",
        "Systemic Cascade",
    ]

    best_by_field = {
        field: max(float(row[field]) for row in strategies)
        for field in performance_fields
    }

    performance_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in strategies:
        values = [float(row[field]) for field in performance_fields]
        regrets = [best_by_field[field] - float(row[field]) for field in performance_fields]

        for scenario, field, value, regret in zip(scenario_labels, performance_fields, values, regrets):
            performance_rows.append({
                "strategy_id": row["strategy_id"],
                "strategy_name": row["strategy_name"],
                "scenario": scenario,
                "performance": round(value, 4),
                "regret": round(regret, 4),
            })

        mean_performance = mean(values)
        worst_case = min(values)
        best_case = max(values)
        maximum_regret = max(regrets)
        mean_regret = mean(regrets)
        governance_quality = (
            0.30 * float(row["monitoring_capacity"])
            + 0.30 * float(row["adaptability"])
            + 0.20 * float(row["implementation_capacity"])
            + 0.20 * float(row["public_legitimacy"])
        )
        robustness = (
            0.42 * worst_case
            + 0.28 * mean_performance
            - 0.20 * maximum_regret
            + 0.10 * governance_quality
        )

        summary_rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "mean_performance": round(mean_performance, 4),
            "worst_case": round(worst_case, 4),
            "best_case": round(best_case, 4),
            "maximum_regret": round(maximum_regret, 4),
            "mean_regret": round(mean_regret, 4),
            "governance_quality": round(governance_quality, 4),
            "robustness_score": round(robustness, 4),
            "description": row["description"],
        })

    summary_rows.sort(key=lambda item: float(item["robustness_score"]), reverse=True)
    return performance_rows, summary_rows


def score_indicators(indicators: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in indicators:
        priority = (
            0.13 * float(row["signal_strength"])
            + 0.11 * float(row["visibility_gap"])
            + 0.09 * (1.0 - float(row["lead_time"]))
            + 0.15 * float(row["systemic_relevance"])
            + 0.16 * float(row["cascade_potential"])
            + 0.15 * float(row["tail_severity"])
            + 0.11 * float(row["preparedness_gap"])
            + 0.10 * float(row["distributional_harm"])
        )

        rows.append({
            "indicator_id": row["indicator_id"],
            "scenario_id": row["scenario_id"],
            "indicator_name": row["indicator_name"],
            "indicator_domain": row["indicator_domain"],
            "risk_indicator_priority_score": round(priority, 4),
            "preparedness_gap": float(row["preparedness_gap"]),
            "distributional_harm": float(row["distributional_harm"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["risk_indicator_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.15 * float(row["monitoring_capacity"])
            + 0.14 * float(row["scenario_refresh_capacity"])
            + 0.14 * float(row["cross_sector_coordination"])
            + 0.13 * float(row["public_legitimacy"])
            + 0.14 * float(row["learning_capacity"])
            + 0.10 * float(row["flexible_finance"])
            + 0.10 * float(row["accountability_capacity"])
            + 0.10 * float(row["distributional_review_capacity"])
        )

        legitimacy_gap = (
            0.16 * (1.0 - float(row["public_legitimacy"]))
            + 0.15 * (1.0 - float(row["accountability_capacity"]))
            + 0.14 * (1.0 - float(row["distributional_review_capacity"]))
            + 0.13 * (1.0 - float(row["cross_sector_coordination"]))
            + 0.12 * (1.0 - float(row["monitoring_capacity"]))
            + 0.11 * (1.0 - float(row["scenario_refresh_capacity"]))
            + 0.10 * (1.0 - float(row["learning_capacity"]))
            + 0.09 * (1.0 - float(row["flexible_finance"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "risk_governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["risk_governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        preparedness = float(row["initial_preparedness"])
        monitoring = float(row["monitoring_capacity"])
        trigger = float(row["trigger_sensitivity"])
        learning = float(row["learning_capacity"])
        governance = float(row["governance_capacity"])
        resilience = float(row["resilience_capacity"])
        vulnerability = float(row["vulnerability_pressure"])
        cascade = float(row["cascade_pressure"])
        tail = float(row["tail_pressure"])
        legitimacy = float(row["public_legitimacy"])
        horizon = int(row["time_horizon"])

        system_stress = (
            0.22 * vulnerability
            + 0.26 * cascade
            + 0.22 * tail
            + 0.12 * (1.0 - governance)
            + 0.10 * (1.0 - monitoring)
            + 0.08 * (1.0 - legitimacy)
        )

        adaptive_capacity = (
            0.20 * monitoring
            + 0.18 * trigger
            + 0.24 * learning
            + 0.18 * governance
            + 0.10 * resilience
            + 0.10 * legitimacy
        )

        preparedness_values: list[float] = []
        stress_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.16 if t % 8 == 0 else 0.05
                tail_event = 0.12 * tail if t % 13 == 0 else 0.0
                cascade_event = 0.10 * cascade if t % 10 == 0 else 0.0

                warning_response = (
                    0.05 * monitoring
                    + 0.04 * trigger
                    + 0.04 * learning
                    + 0.03 * governance
                    + 0.02 * legitimacy
                )

                system_stress = clamp(
                    system_stress
                    + 0.06 * shock
                    + tail_event
                    + cascade_event
                    + 0.03 * vulnerability
                    - warning_response,
                    0.0,
                    1.6,
                )

                adaptive_capacity = clamp(
                    adaptive_capacity
                    + 0.04 * learning
                    + 0.03 * monitoring
                    + 0.03 * trigger
                    + 0.02 * governance
                    + 0.02 * legitimacy
                    - 0.03 * shock
                    - 0.02 * system_stress,
                    0.0,
                    1.6,
                )

                preparedness = clamp(
                    preparedness
                    + 0.04 * adaptive_capacity
                    + 0.03 * resilience
                    + 0.02 * governance
                    + 0.02 * legitimacy
                    - 0.05 * system_stress
                    - 0.03 * shock
                    - 0.02 * tail_event
                    - 0.02 * cascade_event,
                    0.0,
                    1.6,
                )

            preparedness_values.append(preparedness)
            stress_values.append(system_stress)
            capacity_values.append(adaptive_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "preparedness": round(preparedness, 4),
                "system_stress": round(system_stress, 4),
                "adaptive_capacity": round(adaptive_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_preparedness": round(preparedness_values[-1], 4),
            "mean_preparedness": round(mean(preparedness_values), 4),
            "mean_system_stress": round(mean(stress_values), 4),
            "final_adaptive_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_preparedness"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    indicator_scores: list[dict[str, Any]],
    governance_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Futures Risk Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['scenario_name']}**: risk profile {row['futures_risk_profile_score']}; "
            f"preparedness gap {row['preparedness_gap_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Stress Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['systemic_risk_stress_score']}; "
            f"adaptive opportunity {row['adaptive_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Robustness Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: robustness {row['robustness_score']}; "
            f"worst case {row['worst_case']}; maximum regret {row['maximum_regret']}."
        )

    lines.extend(["", "## Risk Indicator Priority Scores", ""])
    for row in indicator_scores:
        lines.append(
            f"- **{row['indicator_name']}**: priority {row['risk_indicator_priority_score']}; "
            f"preparedness gap {row['preparedness_gap']}; distributional harm {row['distributional_harm']}."
        )

    lines.extend(["", "## Risk Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['risk_governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Adaptive Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final preparedness {row['final_preparedness']}; "
            f"mean stress {row['mean_system_stress']}; final adaptive capacity {row['final_adaptive_capacity']}."
        )

    avg_risk = mean(float(row["futures_risk_profile_score"]) for row in profile_scores)
    avg_gap = mean(float(row["preparedness_gap_score"]) for row in profile_scores)
    avg_robustness = mean(float(row["robustness_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Risk profiles: {len(profile_scores)}.",
        f"- Scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(indicator_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average futures risk profile score: {round(avg_risk, 4)}.",
        f"- Average preparedness gap score: {round(avg_gap, 4)}.",
        f"- Average strategy robustness score: {round(avg_robustness, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats risk analysis as a futures-oriented practice shaped by probability confidence, structural uncertainty, interdependence, vulnerability, resilience capacity, governance capacity, signal visibility, tail-risk severity, distributional harm, adaptive capacity, strategy robustness, and public legitimacy.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "futures_risk_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "risk_profiles.csv")
    scenarios_raw = read_csv(DATA / "risk_scenarios.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")
    indicators_raw = read_csv(DATA / "risk_indicators.csv")
    governance_raw = read_csv(DATA / "governance_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, indicators_raw, governance_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    performance_rows, strategy_scores = score_strategies(strategies_raw)
    indicator_scores = score_indicators(indicators_raw)
    governance_scores = score_governance(governance_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "risk_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "risk_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "strategy_scenario_performance.csv", performance_rows)
    write_csv(OUTPUTS / "strategy_robustness_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "risk_indicator_priority_scores.csv", indicator_scores)
    write_csv(OUTPUTS / "risk_governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "adaptive_pathway_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, indicator_scores, governance_scores, pathway_summary)

    print(f"Futures risk analysis workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
