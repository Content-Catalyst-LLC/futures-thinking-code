#!/usr/bin/env python3
"""
Research-grade standard-library workflow for Futures Thinking article directories.

This script performs:
- forecast error diagnostics
- driver priority scoring
- signal watch scoring
- assumption vulnerability scoring
- strategy robustness analysis
- regret analysis
- practice profile scoring
- markdown report generation

It requires only the Python standard library.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
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


def forecast_error_summary() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "forecast_observations.csv")
    by_metric: dict[str, list[dict[str, float]]] = defaultdict(list)

    for row in rows:
        observed = float(row["observed_value"])
        forecast = float(row["forecast_value"])
        error = observed - forecast
        abs_error = abs(error)
        pct_error = abs_error / observed if observed != 0 else 0.0
        by_metric[row["metric"]].append(
            {
                "observed": observed,
                "forecast": forecast,
                "error": error,
                "abs_error": abs_error,
                "pct_error": pct_error,
            }
        )

    output: list[dict[str, Any]] = []
    for metric, values in by_metric.items():
        mae = mean(v["abs_error"] for v in values)
        rmse = math.sqrt(mean(v["error"] ** 2 for v in values))
        mape = mean(v["pct_error"] for v in values)
        bias = mean(v["error"] for v in values)
        output.append(
            {
                "metric": metric,
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
                "mape": round(mape, 4),
                "bias": round(bias, 4),
                "diagnostic": "underforecast" if bias > 0 else "overforecast" if bias < 0 else "balanced",
            }
        )

    output.sort(key=lambda row: float(row["rmse"]), reverse=True)
    return output


def driver_priority() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "drivers.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        velocity = float(row["velocity"])
        priority = uncertainty * impact * velocity
        output.append(
            {
                "driver_id": row["driver_id"],
                "domain": row["domain"],
                "driver_name": row["driver_name"],
                "uncertainty": uncertainty,
                "impact": impact,
                "velocity": velocity,
                "driver_priority": round(priority, 4),
                "description": row["description"],
            }
        )

    output.sort(key=lambda row: float(row["driver_priority"]), reverse=True)
    return output


def signal_watch_scores() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        novelty = float(row["novelty"])
        score = 0.35 * uncertainty + 0.40 * impact + 0.25 * novelty
        output.append(
            {
                "signal_id": row["signal_id"],
                "domain": row["domain"],
                "signal": row["signal"],
                "source_type": row["source_type"],
                "uncertainty": uncertainty,
                "impact": impact,
                "novelty": novelty,
                "watch_score": round(score, 4),
                "monitoring_priority": row["monitoring_priority"],
            }
        )

    output.sort(key=lambda row: float(row["watch_score"]), reverse=True)
    return output


def assumption_vulnerability() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "assumptions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        confidence = float(row["confidence"])
        exposure = float(row["exposure"])
        reversibility = float(row["reversibility"])
        vulnerability = exposure * (1.0 - confidence) * (1.0 + (1.0 - reversibility))
        output.append(
            {
                "assumption_id": row["assumption_id"],
                "domain": row["domain"],
                "assumption_text": row["assumption_text"],
                "confidence": confidence,
                "exposure": exposure,
                "reversibility": reversibility,
                "vulnerability_score": round(vulnerability, 4),
                "monitoring_signal": row["monitoring_signal"],
            }
        )

    output.sort(key=lambda row: float(row["vulnerability_score"]), reverse=True)
    return output


def strategy_robustness() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    performance = read_csv(DATA / "strategy_performance.csv")
    strategies = {row["strategy_id"]: row for row in read_csv(DATA / "strategies.csv")}
    scenarios = {row["scenario_id"]: row for row in read_csv(DATA / "scenarios.csv")}

    by_strategy: dict[str, list[float]] = defaultdict(list)
    by_scenario: dict[str, list[tuple[str, float]]] = defaultdict(list)

    for row in performance:
        strategy_id = row["strategy_id"]
        scenario_id = row["scenario_id"]
        score = float(row["performance"])
        by_strategy[strategy_id].append(score)
        by_scenario[scenario_id].append((strategy_id, score))

    best_by_scenario = {
        scenario_id: max(items, key=lambda item: item[1])[1]
        for scenario_id, items in by_scenario.items()
    }

    regret_rows: list[dict[str, Any]] = []
    regrets_by_strategy: dict[str, list[float]] = defaultdict(list)

    for row in performance:
        strategy_id = row["strategy_id"]
        scenario_id = row["scenario_id"]
        score = float(row["performance"])
        regret = best_by_scenario[scenario_id] - score
        regrets_by_strategy[strategy_id].append(regret)
        regret_rows.append(
            {
                "strategy_id": strategy_id,
                "strategy_name": strategies[strategy_id]["strategy_name"],
                "scenario_id": scenario_id,
                "scenario_name": scenarios[scenario_id]["scenario_name"],
                "performance": round(score, 4),
                "best_scenario_performance": round(best_by_scenario[scenario_id], 4),
                "regret": round(regret, 4),
                "notes": row["notes"],
            }
        )

    summary: list[dict[str, Any]] = []
    for strategy_id, values in by_strategy.items():
        strategy = strategies[strategy_id]
        avg = mean(values)
        worst = min(values)
        best = max(values)
        volatility = pstdev(values) if len(values) > 1 else 0.0
        adaptability = float(strategy["adaptability"])
        equity = float(strategy["equity_sensitivity"])
        implementation_difficulty = float(strategy["implementation_difficulty"])
        robustness = (
            0.45 * worst
            + 0.30 * avg
            + 0.15 * adaptability
            + 0.10 * equity
            - 0.15 * volatility
            - 0.05 * implementation_difficulty
        )
        summary.append(
            {
                "strategy_id": strategy_id,
                "strategy_name": strategy["strategy_name"],
                "strategy_type": strategy["strategy_type"],
                "mean_performance": round(avg, 4),
                "worst_case": round(worst, 4),
                "best_case": round(best, 4),
                "volatility": round(volatility, 4),
                "adaptability": adaptability,
                "equity_sensitivity": equity,
                "implementation_difficulty": implementation_difficulty,
                "robustness_score": round(robustness, 4),
                "mean_regret": round(mean(regrets_by_strategy[strategy_id]), 4),
                "max_regret": round(max(regrets_by_strategy[strategy_id]), 4),
            }
        )

    summary.sort(key=lambda row: float(row["robustness_score"]), reverse=True)
    regret_rows.sort(key=lambda row: float(row["regret"]), reverse=True)
    return summary, regret_rows


def practice_profile_scores() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "practice_profiles.csv")
    weights = {
        "predictive_emphasis": 0.04,
        "uncertainty_plurality": 0.20,
        "assumption_visibility": 0.18,
        "participatory_depth": 0.14,
        "strategic_readiness": 0.20,
        "critical_reflection": 0.14,
        "reproducibility": 0.10,
    }
    output: list[dict[str, Any]] = []

    for row in rows:
        values = {key: float(row[key]) for key in weights}
        score = sum(values[key] * weight for key, weight in weights.items())
        output.append(
            {
                "practice": row["practice"],
                "anticipatory_capacity_score": round(score, 4),
                "strongest_dimension": max(values, key=values.get),
                "weakest_dimension": min(values, key=values.get),
            }
        )

    output.sort(key=lambda row: float(row["anticipatory_capacity_score"]), reverse=True)
    return output


def write_markdown_report(
    config: dict[str, Any],
    forecast_rows: list[dict[str, Any]],
    driver_rows: list[dict[str, Any]],
    signal_rows: list[dict[str, Any]],
    assumption_rows: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
    regret_rows: list[dict[str, Any]],
    practice_rows: list[dict[str, Any]],
) -> None:
    lines: list[str] = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Top Forecast Error Diagnostics",
        "",
    ]

    for row in forecast_rows[:4]:
        lines.append(
            f"- **{row['metric']}**: RMSE {row['rmse']}, MAE {row['mae']}, "
            f"MAPE {row['mape']}, diagnostic: {row['diagnostic']}."
        )

    lines.extend(["", "## Highest-Priority Drivers", ""])
    for row in driver_rows[:5]:
        lines.append(
            f"- **{row['driver_name']}** ({row['domain']}): priority {row['driver_priority']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for row in signal_rows[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['signal']} — watch score {row['watch_score']}."
        )

    lines.extend(["", "## Most Vulnerable Assumptions", ""])
    for row in assumption_rows[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend(["", "## Strategy Robustness Ranking", ""])
    for i, row in enumerate(strategy_rows, start=1):
        lines.append(
            f"{i}. **{row['strategy_name']}** — robustness {row['robustness_score']}, "
            f"worst case {row['worst_case']}, max regret {row['max_regret']}."
        )

    lines.extend(["", "## Largest Strategic Regrets", ""])
    for row in regret_rows[:6]:
        lines.append(
            f"- **{row['strategy_name']}** in **{row['scenario_name']}**: regret {row['regret']}."
        )

    lines.extend(["", "## Future-Oriented Practice Profile", ""])
    for row in practice_rows:
        lines.append(
            f"- **{row['practice']}**: score {row['anticipatory_capacity_score']}; "
            f"strongest dimension: {row['strongest_dimension']}; weakest dimension: {row['weakest_dimension']}."
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The workflow is designed to support disciplined anticipatory judgment, not prediction certainty. "
            "The rankings identify brittle strategies, vulnerable assumptions, high-priority signals, and drivers that deserve monitoring.",
            "",
            f"Repository URL: {config['repository_url']}",
        ]
    )

    (OUTPUTS / "research_workflow_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    forecast_rows = forecast_error_summary()
    driver_rows = driver_priority()
    signal_rows = signal_watch_scores()
    assumption_rows = assumption_vulnerability()
    strategy_rows, regret_rows = strategy_robustness()
    practice_rows = practice_profile_scores()

    write_csv(OUTPUTS / "forecast_error_summary.csv", forecast_rows)
    write_csv(OUTPUTS / "driver_priority_scores.csv", driver_rows)
    write_csv(OUTPUTS / "signal_watch_scores.csv", signal_rows)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumption_rows)
    write_csv(OUTPUTS / "strategy_robustness_summary.csv", strategy_rows)
    write_csv(OUTPUTS / "strategy_regret_analysis.csv", regret_rows)
    write_csv(OUTPUTS / "practice_profile_scores.csv", practice_rows)

    write_markdown_report(
        config,
        forecast_rows,
        driver_rows,
        signal_rows,
        assumption_rows,
        strategy_rows,
        regret_rows,
        practice_rows,
    )

    print(f"Research workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
