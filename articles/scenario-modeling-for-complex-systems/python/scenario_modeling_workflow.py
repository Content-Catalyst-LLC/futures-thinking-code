#!/usr/bin/env python3
"""
Standard-library workflow for Scenario Modeling for Complex Systems.

Outputs:
- scenario_strategy_paths.csv
- scenario_strategy_summary.csv
- scenario_strategy_robustness.csv
- scenario_strategy_regret.csv
- driver_priority_scores.csv
- monitoring_trigger_scores.csv
- scenario_modeling_report.md
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

TIME_STEPS = list(range(1, 41))


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


def clamp(value: float, low: float = 0.0, high: float = 2.0) -> float:
    return max(low, min(high, value))


def simulate_path(scenario: dict[str, str], strategy: dict[str, str]) -> list[dict[str, Any]]:
    growth_rate = float(scenario["growth_rate"])
    shock_level = float(scenario["shock_level"])
    adaptation_gain = float(scenario["adaptation_gain"])
    feedback_strength = float(scenario["feedback_strength"])
    learning_gain = float(scenario["learning_gain"])
    governance_capacity = float(scenario["governance_capacity"])
    public_trust = float(scenario["public_trust"])
    distributional_pressure = float(scenario["distributional_pressure"])

    baseline_boost = float(strategy["baseline_boost"])
    shock_absorption = float(strategy["shock_absorption"])
    adaptation_boost = float(strategy["adaptation_boost"])
    equity_weight = float(strategy["equity_weight"])
    implementation_complexity = float(strategy["implementation_complexity"])
    governance_dependency = float(strategy["governance_dependency"])

    governance_effect = governance_capacity * governance_dependency * 0.015
    legitimacy_effect = public_trust * 0.010
    equity_penalty = max(0.0, distributional_pressure - equity_weight) * 0.035
    complexity_penalty = implementation_complexity * 0.006

    state = 1.0 + baseline_boost
    adaptive_capacity = adaptation_gain + adaptation_boost
    rows: list[dict[str, Any]] = []

    for t in TIME_STEPS:
        if t > 1:
            periodic_shock = shock_level if t % 8 == 0 else shock_level / 3.0
            absorbed_shock = max(0.0, periodic_shock - shock_absorption)
            stress = max(0.0, 1.0 - state)
            stress_feedback = feedback_strength * stress
            adaptive_capacity = min(
                0.30,
                adaptive_capacity
                + learning_gain * stress
                + 0.002 * adaptation_boost
                + governance_effect
            )
            state = clamp(
                state
                + growth_rate
                - absorbed_shock
                - stress_feedback
                + adaptive_capacity
                + legitimacy_effect
                - equity_penalty
                - complexity_penalty
            )

        rows.append({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "strategy_id": strategy["strategy_id"],
            "strategy_name": strategy["strategy_name"],
            "time_step": t,
            "system_state": round(state, 4),
            "adaptive_capacity": round(adaptive_capacity, 4),
            "governance_capacity": governance_capacity,
            "public_trust": public_trust,
            "distributional_pressure": distributional_pressure,
        })

    return rows


def summarize_paths(paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for row in paths:
        key = (row["scenario_id"], row["strategy_id"])
        grouped.setdefault(key, []).append(row)

    summary: list[dict[str, Any]] = []

    for (scenario_id, strategy_id), rows in sorted(grouped.items()):
        states = [float(row["system_state"]) for row in rows]
        capacities = [float(row["adaptive_capacity"]) for row in rows]
        scenario_name = rows[0]["scenario_name"]
        strategy_name = rows[0]["strategy_name"]

        final_state = states[-1]
        min_state = min(states)
        mean_state = mean(states)
        final_capacity = capacities[-1]

        viability = (
            0.35 * final_state
            + 0.30 * min_state
            + 0.20 * mean_state
            + 0.15 * final_capacity
        )

        if viability >= 1.35 and min_state >= 0.90:
            viability_class = "Strong cross-scenario pathway"
        elif viability >= 1.05:
            viability_class = "Viable but vulnerable pathway"
        else:
            viability_class = "Fragile pathway"

        summary.append({
            "scenario_id": scenario_id,
            "scenario_name": scenario_name,
            "strategy_id": strategy_id,
            "strategy_name": strategy_name,
            "final_state": round(final_state, 4),
            "min_state": round(min_state, 4),
            "mean_state": round(mean_state, 4),
            "max_state": round(max(states), 4),
            "final_adaptive_capacity": round(final_capacity, 4),
            "viability_score": round(viability, 4),
            "viability_class": viability_class,
        })

    return summary


def robustness(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}

    for row in summary:
        grouped.setdefault(row["strategy_id"], []).append(row)

    rows_out: list[dict[str, Any]] = []

    for strategy_id, rows in grouped.items():
        scores = [float(row["viability_score"]) for row in rows]
        rows_out.append({
            "strategy_id": strategy_id,
            "strategy_name": rows[0]["strategy_name"],
            "worst_case_viability": round(min(scores), 4),
            "mean_viability": round(mean(scores), 4),
            "best_case_viability": round(max(scores), 4),
            "viability_range": round(max(scores) - min(scores), 4),
        })

    rows_out.sort(key=lambda item: (float(item["worst_case_viability"]), float(item["mean_viability"])), reverse=True)
    return rows_out


def regret(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_by_scenario: dict[str, float] = {}

    for row in summary:
        score = float(row["viability_score"])
        scenario_id = row["scenario_id"]
        best_by_scenario[scenario_id] = max(best_by_scenario.get(scenario_id, score), score)

    rows_out: list[dict[str, Any]] = []

    for row in summary:
        best = best_by_scenario[row["scenario_id"]]
        score = float(row["viability_score"])
        rows_out.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "viability_score": round(score, 4),
            "best_scenario_viability": round(best, 4),
            "regret": round(best - score, 4),
        })

    rows_out.sort(key=lambda item: float(item["regret"]), reverse=True)
    return rows_out


def score_drivers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "driver_register.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        impact = float(row["impact_level"])
        uncertainty = float(row["uncertainty_level"])
        interaction = float(row["interaction_strength"])
        sensitivity = float(row["time_sensitivity"])
        monitoring = float(row["monitoring_need"])

        priority = (
            0.25 * impact
            + 0.25 * uncertainty
            + 0.20 * interaction
            + 0.15 * sensitivity
            + 0.15 * monitoring
        )

        output.append({
            "driver_id": row["driver_id"],
            "driver_name": row["driver_name"],
            "domain": row["domain"],
            "impact_level": impact,
            "uncertainty_level": uncertainty,
            "interaction_strength": interaction,
            "time_sensitivity": sensitivity,
            "monitoring_need": monitoring,
            "driver_priority_score": round(priority, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["driver_priority_score"]), reverse=True)
    return output


def score_monitoring() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "monitoring_indicators.csv")
    frequency = {"monthly": 1.0, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
    output: list[dict[str, Any]] = []

    for row in rows:
        baseline = float(row["baseline"])
        threshold = float(row["target_or_threshold"])
        gap = abs(threshold - baseline)
        review_weight = frequency.get(row["review_frequency"], 0.50)
        priority = 0.70 * gap + 0.30 * review_weight

        output.append({
            "indicator_id": row["indicator_id"],
            "driver_id": row["driver_id"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "target_or_threshold": threshold,
            "monitoring_gap": round(gap, 4),
            "review_frequency": row["review_frequency"],
            "review_weight": review_weight,
            "monitoring_priority": round(priority, 4),
            "trigger_rule": row["trigger_rule"],
            "decision_response": row["decision_response"],
        })

    output.sort(key=lambda item: float(item["monitoring_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    summary: list[dict[str, Any]],
    robustness_rows: list[dict[str, Any]],
    regret_rows: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    monitoring: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Strategy Robustness Ranking",
        "",
    ]

    for row in robustness_rows:
        lines.append(
            f"- **{row['strategy_name']}**: worst-case viability {row['worst_case_viability']}; "
            f"mean viability {row['mean_viability']}; range {row['viability_range']}."
        )

    lines.extend(["", "## Scenario-Strategy Viability Highlights", ""])
    for row in sorted(summary, key=lambda item: float(item["viability_score"]), reverse=True)[:10]:
        lines.append(
            f"- **{row['scenario_name']} / {row['strategy_name']}**: viability {row['viability_score']}; "
            f"class: {row['viability_class']}."
        )

    lines.extend(["", "## Highest Regret Cases", ""])
    for row in regret_rows[:10]:
        lines.append(
            f"- **{row['scenario_name']} / {row['strategy_name']}**: regret {row['regret']}."
        )

    lines.extend(["", "## Driver Priority Scores", ""])
    for row in drivers:
        lines.append(
            f"- **{row['driver_name']}** ({row['domain']}): priority {row['driver_priority_score']}."
        )

    lines.extend(["", "## Monitoring Trigger Priorities", ""])
    for row in monitoring[:8]:
        lines.append(
            f"- **{row['indicator_name']}**: priority {row['monitoring_priority']}; response: {row['decision_response']}"
        )

    worst = robustness_rows[0]
    avg_viability = mean(float(row["viability_score"]) for row in summary)
    max_regret = max(float(row["regret"]) for row in regret_rows)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Best worst-case strategy: {worst['strategy_name']} with worst-case viability {worst['worst_case_viability']}.",
        f"- Average scenario-strategy viability score: {round(avg_viability, 4)}.",
        f"- Maximum observed regret: {round(max_regret, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats scenario modeling as structured exploration rather than prediction. It simulates alternative system pathways, compares strategy performance across scenarios, evaluates robustness and regret, ranks drivers by monitoring need, and links indicators to adaptive decision responses.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "scenario_modeling_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    scenarios = read_csv(DATA / "scenario_assumptions.csv")
    strategies = read_csv(DATA / "strategy_portfolio.csv")

    paths: list[dict[str, Any]] = []
    for scenario in scenarios:
        for strategy in strategies:
            paths.extend(simulate_path(scenario, strategy))

    summary = summarize_paths(paths)
    robustness_rows = robustness(summary)
    regret_rows = regret(summary)
    drivers = score_drivers()
    monitoring = score_monitoring()

    write_csv(OUTPUTS / "scenario_strategy_paths.csv", paths)
    write_csv(OUTPUTS / "scenario_strategy_summary.csv", summary)
    write_csv(OUTPUTS / "scenario_strategy_robustness.csv", robustness_rows)
    write_csv(OUTPUTS / "scenario_strategy_regret.csv", regret_rows)
    write_csv(OUTPUTS / "driver_priority_scores.csv", drivers)
    write_csv(OUTPUTS / "monitoring_trigger_scores.csv", monitoring)

    write_report(config, summary, robustness_rows, regret_rows, drivers, monitoring)

    print(f"Scenario modeling workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
