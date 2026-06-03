#!/usr/bin/env python3
"""
Standard-library workflow for Futures Thinking in Business Strategy.

Outputs:
- strategy_profile_scores.csv
- strategic_option_scores.csv
- capability_priority_scores.csv
- early_warning_indicator_scores.csv
- scenario_stress_test_scores.csv
- dynamic_capability_paths.csv
- dynamic_capability_summary.csv
- business_strategy_futures_report.md
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


def futures_readiness(row: dict[str, str]) -> float:
    return (
        0.14 * float(row["innovation_capacity"])
        - 0.10 * float(row["uncertainty_exposure"])
        + 0.15 * float(row["resilience"])
        + 0.14 * float(row["strategic_flexibility"])
        + 0.10 * float(row["organizational_alignment"])
        + 0.12 * float(row["sensing_capability"])
        + 0.08 * float(row["capital_flexibility"])
        + 0.09 * float(row["legitimacy_trust"])
        + 0.08 * float(row["transition_readiness"])
    )


def strategic_fragility(row: dict[str, str]) -> float:
    return (
        0.18 * float(row["uncertainty_exposure"])
        + 0.14 * (1.0 - float(row["resilience"]))
        + 0.14 * (1.0 - float(row["strategic_flexibility"]))
        + 0.13 * (1.0 - float(row["sensing_capability"]))
        + 0.11 * (1.0 - float(row["capital_flexibility"]))
        + 0.10 * (1.0 - float(row["organizational_alignment"]))
        + 0.10 * (1.0 - float(row["legitimacy_trust"]))
        + 0.10 * (1.0 - float(row["transition_readiness"]))
    )


def validate_records(
    strategies: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    options: list[dict[str, str]],
    capabilities: list[dict[str, str]],
    indicators: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    strategy_ids = {row["strategy_id"] for row in strategies}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in options:
        if row["strategy_id"] not in strategy_ids:
            errors.append(f"Option {row['option_id']} references missing strategy {row['strategy_id']}.")

    for row in capabilities:
        if row["strategy_id"] not in strategy_ids:
            errors.append(f"Capability {row['capability_id']} references missing strategy {row['strategy_id']}.")

    for row in indicators:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Indicator {row['indicator_id']} references missing scenario {row['scenario_id']}.")

    for row in pathways:
        if row["strategy_id"] not in strategy_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing strategy {row['strategy_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("strategies", strategies, ["innovation_capacity", "uncertainty_exposure", "resilience", "strategic_flexibility", "organizational_alignment", "sensing_capability", "capital_flexibility", "legitimacy_trust", "transition_readiness"]),
        ("scenarios", scenarios, ["market_growth", "technology_acceleration", "regulatory_pressure", "climate_stress", "supply_chain_stability", "capital_availability", "labor_availability", "consumer_trust_pressure", "geopolitical_fragmentation"]),
        ("options", options, ["learning_value", "upside_potential", "cost_to_maintain", "reversibility", "scalability", "strategic_fit", "signal_sensitivity"]),
        ("capabilities", capabilities, ["current_strength", "future_importance", "development_difficulty", "coordination_requirement", "investment_need", "learning_rate"]),
        ("indicators", indicators, ["baseline_value", "current_signal_strength", "strategic_relevance", "lead_time", "monitoring_difficulty", "trigger_threshold"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("strategy_id") or row.get("scenario_id") or row.get("option_id") or row.get("capability_id") or row.get("indicator_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_strategy_profiles(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        readiness = futures_readiness(row)
        fragility = strategic_fragility(row)

        if readiness >= 0.62 and fragility < 0.48:
            strategy_class = "Strong futures-ready strategy profile"
        elif fragility >= 0.55:
            strategy_class = "High strategic fragility"
        else:
            strategy_class = "Developing futures-ready strategy profile"

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "business_futures_readiness_score": round(readiness, 4),
            "strategic_fragility_score": round(fragility, 4),
            "strategy_class": strategy_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["business_futures_readiness_score"]), reverse=True)
    return rows


def score_options(options: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in options:
        option_value = (
            0.22 * float(row["learning_value"])
            + 0.20 * float(row["upside_potential"])
            + 0.15 * float(row["reversibility"])
            + 0.15 * float(row["scalability"])
            + 0.14 * float(row["strategic_fit"])
            + 0.14 * float(row["signal_sensitivity"])
            - 0.20 * float(row["cost_to_maintain"])
        )

        option_quality = (
            0.18 * float(row["learning_value"])
            + 0.18 * float(row["strategic_fit"])
            + 0.16 * float(row["signal_sensitivity"])
            + 0.14 * float(row["reversibility"])
            + 0.14 * float(row["scalability"])
            + 0.12 * float(row["upside_potential"])
            + 0.08 * (1.0 - float(row["cost_to_maintain"]))
        )

        rows.append({
            "option_id": row["option_id"],
            "strategy_id": row["strategy_id"],
            "option_name": row["option_name"],
            "option_type": row["option_type"],
            "net_strategic_option_value": round(option_value, 4),
            "option_quality_score": round(option_quality, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["net_strategic_option_value"]), reverse=True)
    return rows


def score_capabilities(capabilities: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in capabilities:
        gap = max(0.0, float(row["future_importance"]) - float(row["current_strength"]))
        priority = (
            0.34 * float(row["future_importance"])
            + 0.20 * float(row["development_difficulty"])
            + 0.18 * float(row["coordination_requirement"])
            + 0.14 * float(row["investment_need"])
            + 0.14 * (1.0 - float(row["current_strength"]))
        )

        rows.append({
            "capability_id": row["capability_id"],
            "strategy_id": row["strategy_id"],
            "capability_name": row["capability_name"],
            "capability_type": row["capability_type"],
            "future_capability_gap": round(gap, 4),
            "capability_investment_priority": round(priority, 4),
            "learning_rate": float(row["learning_rate"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["capability_investment_priority"]), reverse=True)
    return rows


def score_indicators(indicators: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in indicators:
        trigger_gap = float(row["trigger_threshold"]) - float(row["current_signal_strength"])
        trigger_proximity = 1.0 - max(0.0, trigger_gap)
        urgency = (
            0.25 * float(row["current_signal_strength"])
            + 0.22 * float(row["strategic_relevance"])
            + 0.16 * float(row["lead_time"])
            + 0.12 * (1.0 - float(row["monitoring_difficulty"]))
            + 0.25 * trigger_proximity
        )

        rows.append({
            "indicator_id": row["indicator_id"],
            "scenario_id": row["scenario_id"],
            "indicator_name": row["indicator_name"],
            "indicator_domain": row["indicator_domain"],
            "trigger_proximity": round(trigger_proximity, 4),
            "strategic_signal_urgency": round(urgency, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["strategic_signal_urgency"]), reverse=True)
    return rows


def stress_test_scenarios(strategies: list[dict[str, str]], scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for strategy in strategies:
        for scenario in scenarios:
            opportunity = (
                0.18 * float(scenario["market_growth"])
                + 0.16 * float(scenario["technology_acceleration"]) * float(strategy["innovation_capacity"])
                + 0.14 * float(scenario["capital_availability"]) * float(strategy["capital_flexibility"])
                + 0.14 * float(scenario["consumer_trust_pressure"]) * float(strategy["legitimacy_trust"])
                + 0.12 * float(strategy["sensing_capability"])
                + 0.12 * float(strategy["strategic_flexibility"])
                + 0.14 * float(strategy["transition_readiness"])
            )

            pressure = (
                0.16 * float(scenario["regulatory_pressure"]) * (1.0 - float(strategy["transition_readiness"]))
                + 0.16 * float(scenario["climate_stress"]) * (1.0 - float(strategy["resilience"]))
                + 0.14 * (1.0 - float(scenario["supply_chain_stability"])) * (1.0 - float(strategy["resilience"]))
                + 0.14 * (1.0 - float(scenario["capital_availability"])) * (1.0 - float(strategy["capital_flexibility"]))
                + 0.14 * float(scenario["geopolitical_fragmentation"]) * (1.0 - float(strategy["strategic_flexibility"]))
                + 0.12 * float(scenario["consumer_trust_pressure"]) * (1.0 - float(strategy["legitimacy_trust"]))
                + 0.14 * float(strategy["uncertainty_exposure"])
            )

            viability = clamp(0.65 + opportunity - pressure, 0.0, 1.5)

            rows.append({
                "strategy_id": strategy["strategy_id"],
                "strategy_name": strategy["strategy_name"],
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "scenario_opportunity_score": round(opportunity, 4),
                "scenario_pressure_score": round(pressure, 4),
                "cross_scenario_viability": round(viability, 4),
            })

    rows.sort(key=lambda item: (item["strategy_id"], -float(item["cross_scenario_viability"])))
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        sensing = float(row["sensing"])
        innovation = float(row["innovation"])
        resilience = float(row["resilience"])
        flexibility = float(row["flexibility"])
        alignment = float(row["alignment"])
        capital = float(row["capital_flexibility"])
        trust = float(row["trust"])
        transition = float(row["transition_readiness"])
        viability = float(row["initial_viability"])
        horizon = int(row["time_horizon"])

        option_value = 0.28 * flexibility + 0.22 * sensing + 0.18 * capital + 0.18 * innovation + 0.14 * transition
        fragility = 1.0 - (0.28 * resilience + 0.20 * flexibility + 0.18 * trust + 0.18 * capital + 0.16 * alignment)
        learning = 0.35 * sensing + 0.25 * innovation + 0.22 * alignment + 0.18 * transition

        viability_values: list[float] = []
        option_values: list[float] = []
        fragility_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.18 if t % 8 == 0 else 0.06

                response_gain = (
                    0.18 * innovation
                    + 0.20 * resilience
                    + 0.20 * flexibility
                    + 0.16 * sensing
                    + 0.10 * capital
                    + 0.08 * trust
                    + 0.08 * transition
                )

                option_value = clamp(
                    option_value
                    + 0.03 * flexibility
                    + 0.03 * sensing
                    + 0.02 * capital
                    + 0.02 * innovation
                    - 0.04 * disruption,
                    0.0,
                    1.5,
                )

                fragility = clamp(
                    fragility
                    + 0.06 * disruption
                    - 0.03 * resilience
                    - 0.03 * flexibility
                    - 0.02 * trust
                    - 0.02 * alignment
                    - 0.02 * transition,
                    0.0,
                    1.4,
                )

                learning = clamp(
                    learning
                    + 0.03 * sensing
                    + 0.03 * alignment
                    + 0.02 * innovation
                    + 0.02 * transition
                    - 0.02 * disruption,
                    0.0,
                    1.4,
                )

                viability = clamp(
                    viability
                    - disruption
                    - 0.04 * fragility
                    + response_gain / 4.0
                    + 0.05 * option_value
                    + 0.03 * learning,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            option_values.append(option_value)
            fragility_values.append(fragility)
            learning_values.append(learning)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "strategy_id": row["strategy_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "strategic_viability": round(viability, 4),
                "strategic_option_value": round(option_value, 4),
                "fragility_score": round(fragility, 4),
                "learning_score": round(learning, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "strategy_id": row["strategy_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_strategic_viability": round(viability_values[-1], 4),
            "mean_strategic_viability": round(mean(viability_values), 4),
            "final_option_value": round(option_values[-1], 4),
            "mean_fragility_score": round(mean(fragility_values), 4),
            "final_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_strategic_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    strategy_scores: list[dict[str, Any]],
    option_scores: list[dict[str, Any]],
    capability_scores: list[dict[str, Any]],
    indicator_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Strategy Profile Scores",
        "",
    ]

    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: futures readiness {row['business_futures_readiness_score']}; "
            f"fragility {row['strategic_fragility_score']}; class: {row['strategy_class']}."
        )

    lines.extend(["", "## Strategic Option Scores", ""])
    for row in option_scores:
        lines.append(
            f"- **{row['option_name']}**: net option value {row['net_strategic_option_value']}; "
            f"option quality {row['option_quality_score']}."
        )

    lines.extend(["", "## Capability Investment Priorities", ""])
    for row in capability_scores:
        lines.append(
            f"- **{row['capability_name']}**: gap {row['future_capability_gap']}; "
            f"priority {row['capability_investment_priority']}."
        )

    lines.extend(["", "## Early Warning Indicator Urgency", ""])
    for row in indicator_scores:
        lines.append(
            f"- **{row['indicator_name']}**: trigger proximity {row['trigger_proximity']}; "
            f"signal urgency {row['strategic_signal_urgency']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_strategic_viability']}; "
            f"mean fragility {row['mean_fragility_score']}; final option value {row['final_option_value']}."
        )

    avg_readiness = mean(float(row["business_futures_readiness_score"]) for row in strategy_scores)
    avg_fragility = mean(float(row["strategic_fragility_score"]) for row in strategy_scores)
    avg_viability = mean(float(row["cross_scenario_viability"]) for row in scenario_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Strategy profiles: {len(strategy_scores)}.",
        f"- Strategic options: {len(option_scores)}.",
        f"- Capabilities: {len(capability_scores)}.",
        f"- Early warning indicators: {len(indicator_scores)}.",
        f"- Scenario stress-test records: {len(scenario_scores)}.",
        f"- Average business futures readiness score: {round(avg_readiness, 4)}.",
        f"- Average strategic fragility score: {round(avg_fragility, 4)}.",
        f"- Average cross-scenario viability: {round(avg_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats futures thinking in business strategy as an integrated strategic system for sensing change, testing assumptions, building options, strengthening resilience, preserving legitimacy, and adapting under uncertainty.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "business_strategy_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    strategies_raw = read_csv(DATA / "strategy_profiles.csv")
    scenarios_raw = read_csv(DATA / "future_scenarios.csv")
    options_raw = read_csv(DATA / "strategic_options.csv")
    capabilities_raw = read_csv(DATA / "capability_register.csv")
    indicators_raw = read_csv(DATA / "early_warning_indicators.csv")
    pathways_raw = read_csv(DATA / "dynamic_capability_pathways.csv")

    errors = validate_records(strategies_raw, scenarios_raw, options_raw, capabilities_raw, indicators_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    strategy_scores = score_strategy_profiles(strategies_raw)
    option_scores = score_options(options_raw)
    capability_scores = score_capabilities(capabilities_raw)
    indicator_scores = score_indicators(indicators_raw)
    scenario_scores = stress_test_scenarios(strategies_raw, scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "strategy_profile_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "strategic_option_scores.csv", option_scores)
    write_csv(OUTPUTS / "capability_priority_scores.csv", capability_scores)
    write_csv(OUTPUTS / "early_warning_indicator_scores.csv", indicator_scores)
    write_csv(OUTPUTS / "scenario_stress_test_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "dynamic_capability_paths.csv", trajectories)
    write_csv(OUTPUTS / "dynamic_capability_summary.csv", pathway_summary)

    write_report(config, strategy_scores, option_scores, capability_scores, indicator_scores, scenario_scores, pathway_summary)

    print(f"Business strategy futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
