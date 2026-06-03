#!/usr/bin/env python3
"""
Standard-library workflow for Scenario Planning.

Outputs:
- strategy_robustness_summary.csv
- strategy_regret_analysis.csv
- driver_uncertainty_scores.csv
- signal_watch_scores.csv
- assumption_vulnerability_scores.csv
- scenario_planning_report.md
"""

from __future__ import annotations

import csv
import json
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


def score_drivers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "drivers_uncertainties.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        velocity = float(row["velocity"])
        criticality = uncertainty * impact * velocity
        output.append({
            "driver_id": row["driver_id"],
            "domain": row["domain"],
            "driver_or_uncertainty": row["driver_or_uncertainty"],
            "driver_type": row["driver_type"],
            "uncertainty": uncertainty,
            "impact": impact,
            "velocity": velocity,
            "criticality_score": round(criticality, 4),
            "description": row["description"],
        })

    output.sort(key=lambda row: float(row["criticality_score"]), reverse=True)
    return output


def score_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        novelty = float(row["novelty"])
        watch_score = 0.35 * uncertainty + 0.40 * impact + 0.25 * novelty
        output.append({
            "signal_id": row["signal_id"],
            "domain": row["domain"],
            "signal": row["signal"],
            "uncertainty": uncertainty,
            "impact": impact,
            "novelty": novelty,
            "watch_score": round(watch_score, 4),
            "source_type": row["source_type"],
            "monitoring_priority": row["monitoring_priority"],
        })

    output.sort(key=lambda row: float(row["watch_score"]), reverse=True)
    return output


def score_assumptions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "assumptions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        confidence = float(row["confidence"])
        exposure = float(row["exposure"])
        reversibility = float(row["reversibility"])
        vulnerability = exposure * (1.0 - confidence) * (1.0 + (1.0 - reversibility))
        output.append({
            "assumption_id": row["assumption_id"],
            "domain": row["domain"],
            "assumption_text": row["assumption_text"],
            "confidence": confidence,
            "exposure": exposure,
            "reversibility": reversibility,
            "vulnerability_score": round(vulnerability, 4),
            "monitoring_signal": row["monitoring_signal"],
        })

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
        regret_rows.append({
            "strategy_id": strategy_id,
            "strategy": strategies[strategy_id]["strategy"],
            "scenario_id": scenario_id,
            "scenario_name": scenarios[scenario_id]["scenario_name"],
            "performance": round(score, 4),
            "best_scenario_performance": round(best_by_scenario[scenario_id], 4),
            "regret": round(regret, 4),
            "notes": row["notes"],
        })

    summary: list[dict[str, Any]] = []

    for strategy_id, values in by_strategy.items():
        strategy = strategies[strategy_id]
        avg = mean(values)
        worst = min(values)
        best = max(values)
        volatility = pstdev(values) if len(values) > 1 else 0.0
        adaptability = float(strategy["adaptability"])
        equity = float(strategy["equity_sensitivity"])
        difficulty = float(strategy["implementation_difficulty"])
        robustness = (
            0.45 * worst
            + 0.30 * avg
            + 0.15 * adaptability
            + 0.10 * equity
            - 0.15 * volatility
            - 0.05 * difficulty
        )
        summary.append({
            "strategy_id": strategy_id,
            "strategy": strategy["strategy"],
            "strategy_type": strategy["strategy_type"],
            "mean_performance": round(avg, 4),
            "worst_case": round(worst, 4),
            "best_case": round(best, 4),
            "volatility": round(volatility, 4),
            "adaptability": adaptability,
            "equity_sensitivity": equity,
            "implementation_difficulty": difficulty,
            "robustness_score": round(robustness, 4),
            "mean_regret": round(mean(regrets_by_strategy[strategy_id]), 4),
            "max_regret": round(max(regrets_by_strategy[strategy_id]), 4),
        })

    summary.sort(key=lambda row: float(row["robustness_score"]), reverse=True)
    regret_rows.sort(key=lambda row: float(row["regret"]), reverse=True)
    return summary, regret_rows


def write_report(
    config: dict[str, Any],
    strategy_rows: list[dict[str, Any]],
    regret_rows: list[dict[str, Any]],
    driver_rows: list[dict[str, Any]],
    signal_rows: list[dict[str, Any]],
    assumption_rows: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Strategy Robustness Ranking",
        "",
    ]

    for index, row in enumerate(strategy_rows, start=1):
        lines.append(
            f"{index}. **{row['strategy']}** — robustness {row['robustness_score']}; "
            f"worst case {row['worst_case']}; max regret {row['max_regret']}."
        )

    lines.extend(["", "## Largest Strategic Regrets", ""])
    for row in regret_rows[:8]:
        lines.append(
            f"- **{row['strategy']}** in **{row['scenario_name']}**: regret {row['regret']}."
        )

    lines.extend(["", "## Highest-Criticality Drivers and Uncertainties", ""])
    for row in driver_rows[:6]:
        lines.append(
            f"- **{row['driver_or_uncertainty']}** ({row['domain']}): criticality {row['criticality_score']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for row in signal_rows[:6]:
        lines.append(
            f"- **{row['domain']}**: {row['signal']} — watch score {row['watch_score']}."
        )

    lines.extend(["", "## Most Vulnerable Assumptions", ""])
    for row in assumption_rows[:6]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "The workflow demonstrates scenario planning as a strategy-under-uncertainty practice. It does not predict which scenario will occur. It compares strategies across plausible futures, identifies brittle assumptions, and creates monitoring outputs for institutional learning.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "scenario_planning_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    driver_rows = score_drivers()
    signal_rows = score_signals()
    assumption_rows = score_assumptions()
    strategy_rows, regret_rows = strategy_robustness()

    write_csv(OUTPUTS / "driver_uncertainty_scores.csv", driver_rows)
    write_csv(OUTPUTS / "signal_watch_scores.csv", signal_rows)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumption_rows)
    write_csv(OUTPUTS / "strategy_robustness_summary.csv", strategy_rows)
    write_csv(OUTPUTS / "strategy_regret_analysis.csv", regret_rows)

    write_report(config, strategy_rows, regret_rows, driver_rows, signal_rows, assumption_rows)

    print(f"Scenario planning workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
