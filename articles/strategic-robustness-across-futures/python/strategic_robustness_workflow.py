#!/usr/bin/env python3
"""
Standard-library workflow for Strategic Robustness Across Futures.

Outputs:
- scenario_strategy_performance.csv
- strategy_robustness_scores.csv
- scenario_strategy_regret.csv
- strategy_regret_summary.csv
- adaptive_trigger_scores.csv
- vulnerability_scores.csv
- assumption_fragility_scores.csv
- strategic_robustness_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def load_weights() -> dict[str, float]:
    return {
        row["criterion_name"]: float(row["weight"])
        for row in read_csv(DATA / "performance_criteria.csv")
    }


def score_performance() -> list[dict[str, Any]]:
    scenarios = read_csv(DATA / "scenarios.csv")
    strategies = read_csv(DATA / "strategies.csv")
    weights = load_weights()

    rows: list[dict[str, Any]] = []

    for scenario in scenarios:
        disruption = float(scenario["disruption_level"])
        public_trust = float(scenario["public_trust"])
        fiscal = float(scenario["fiscal_capacity"])
        implementation_capacity = float(scenario["implementation_capacity"])
        ecological = float(scenario["ecological_stress"])
        technology = float(scenario["technology_volatility"])
        distributional = float(scenario["distributional_pressure"])

        for strategy in strategies:
            baseline = float(strategy["baseline_effectiveness"])
            shock_absorption = float(strategy["shock_absorption"])
            equity_quality = float(strategy["equity_quality"])
            adaptability = float(strategy["adaptability"])
            complexity = float(strategy["implementation_complexity"])
            legitimacy_design = float(strategy["legitimacy_design"])
            transformability = float(strategy["transformability"])

            effectiveness = clamp(
                baseline
                - 0.22 * disruption
                + 0.26 * shock_absorption
                - 0.08 * ecological
                - 0.05 * technology * (1.0 - adaptability)
            )

            feasibility = clamp(
                implementation_capacity
                + 0.18 * fiscal
                - 0.30 * complexity
                - 0.05 * disruption
            )

            legitimacy = clamp(
                0.40 * public_trust
                + 0.25 * legitimacy_design
                + 0.20 * equity_quality
                + 0.15 * adaptability
                - 0.05 * distributional
            )

            equity = clamp(
                equity_quality
                - 0.30 * distributional
                + 0.15 * legitimacy_design
                + 0.10 * transformability
            )

            adaptability_score = clamp(
                0.70 * adaptability
                + 0.30 * implementation_capacity
                - 0.05 * technology * (1.0 - shock_absorption)
            )

            transformability_score = clamp(
                0.70 * transformability
                + 0.30 * legitimacy_design
                - 0.06 * complexity
            )

            viability = clamp(
                weights["effectiveness"] * effectiveness
                + weights["feasibility"] * feasibility
                + weights["legitimacy"] * legitimacy
                + weights["equity"] * equity
                + weights["adaptability"] * adaptability_score
                + weights["transformability"] * transformability_score
            )

            rows.append({
                "scenario_id": scenario["scenario_id"],
                "scenario_name": scenario["scenario_name"],
                "scenario_family": scenario["scenario_family"],
                "strategy_id": strategy["strategy_id"],
                "strategy_name": strategy["strategy_name"],
                "strategy_type": strategy["strategy_type"],
                "effectiveness": round(effectiveness, 4),
                "feasibility": round(feasibility, 4),
                "legitimacy": round(legitimacy, 4),
                "equity": round(equity, 4),
                "adaptability_score": round(adaptability_score, 4),
                "transformability_score": round(transformability_score, 4),
                "viability_score": round(viability, 4),
            })

    return rows


def robustness_summary(performance: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in performance:
        grouped.setdefault(row["strategy_id"], []).append(row)

    output: list[dict[str, Any]] = []

    for strategy_id, rows in grouped.items():
        scores = [float(row["viability_score"]) for row in rows]
        threshold_failures = sum(score < 0.50 for score in scores)
        low_legitimacy_cases = sum(float(row["legitimacy"]) < 0.50 for row in rows)
        low_equity_cases = sum(float(row["equity"]) < 0.50 for row in rows)

        output.append({
            "strategy_id": strategy_id,
            "strategy_name": rows[0]["strategy_name"],
            "strategy_type": rows[0]["strategy_type"],
            "worst_case_viability": round(min(scores), 4),
            "mean_viability": round(mean(scores), 4),
            "best_case_viability": round(max(scores), 4),
            "viability_range": round(max(scores) - min(scores), 4),
            "threshold_failures": threshold_failures,
            "low_legitimacy_cases": low_legitimacy_cases,
            "low_equity_cases": low_equity_cases,
        })

    output.sort(
        key=lambda item: (
            float(item["worst_case_viability"]),
            float(item["mean_viability"]),
            -int(item["threshold_failures"])
        ),
        reverse=True
    )
    return output


def regret_analysis(performance: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    best_by_scenario: dict[str, float] = {}

    for row in performance:
        scenario_id = row["scenario_id"]
        score = float(row["viability_score"])
        best_by_scenario[scenario_id] = max(best_by_scenario.get(scenario_id, score), score)

    regret_rows: list[dict[str, Any]] = []

    for row in performance:
        best = best_by_scenario[row["scenario_id"]]
        score = float(row["viability_score"])
        regret_rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "viability_score": round(score, 4),
            "best_scenario_viability": round(best, 4),
            "regret": round(best - score, 4),
        })

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in regret_rows:
        grouped.setdefault(row["strategy_id"], []).append(row)

    summary_rows: list[dict[str, Any]] = []
    for strategy_id, rows in grouped.items():
        regrets = [float(row["regret"]) for row in rows]
        summary_rows.append({
            "strategy_id": strategy_id,
            "strategy_name": rows[0]["strategy_name"],
            "max_regret": round(max(regrets), 4),
            "mean_regret": round(mean(regrets), 4),
        })

    regret_rows.sort(key=lambda item: float(item["regret"]), reverse=True)
    summary_rows.sort(key=lambda item: (float(item["max_regret"]), float(item["mean_regret"])))

    return regret_rows, summary_rows


def score_triggers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "adaptive_triggers.csv")
    frequency = {"monthly": 1.0, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
    output: list[dict[str, Any]] = []

    for row in rows:
        baseline = float(row["baseline"])
        threshold = float(row["threshold_value"])
        gap = abs(threshold - baseline)
        review_weight = frequency.get(row["review_frequency"], 0.50)
        priority = 0.45 * gap + 0.35 * threshold + 0.20 * review_weight

        output.append({
            "trigger_id": row["trigger_id"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "threshold_value": threshold,
            "monitoring_gap": round(gap, 4),
            "review_frequency": row["review_frequency"],
            "review_weight": review_weight,
            "linked_scenario": row["linked_scenario"],
            "trigger_priority_score": round(priority, 4),
            "trigger_rule": row["trigger_rule"],
            "decision_response": row["decision_response"],
        })

    output.sort(key=lambda item: float(item["trigger_priority_score"]), reverse=True)
    return output


def score_vulnerabilities() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "vulnerability_conditions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        severity = float(row["severity"])
        detectability = float(row["detectability"])
        mitigation = float(row["mitigation_capacity"])
        score = 0.50 * severity + 0.25 * (1.0 - detectability) + 0.25 * (1.0 - mitigation)

        output.append({
            "vulnerability_id": row["vulnerability_id"],
            "strategy_id": row["strategy_id"],
            "scenario_id": row["scenario_id"],
            "vulnerability_name": row["vulnerability_name"],
            "severity": severity,
            "detectability": detectability,
            "mitigation_capacity": mitigation,
            "vulnerability_priority_score": round(score, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["vulnerability_priority_score"]), reverse=True)
    return output


def score_assumptions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "assumption_register.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        confidence = float(row["confidence"])
        fragility = float(row["fragility"])
        failure_risk = 0.45 * (1.0 - confidence) + 0.55 * fragility

        output.append({
            "assumption_id": row["assumption_id"],
            "strategy_id": row["strategy_id"],
            "assumption_name": row["assumption_name"],
            "confidence": confidence,
            "fragility": fragility,
            "assumption_failure_risk": round(failure_risk, 4),
            "monitoring_indicator": row["monitoring_indicator"],
            "revision_rule": row["revision_rule"],
            "assumption_text": row["assumption_text"],
        })

    output.sort(key=lambda item: float(item["assumption_failure_risk"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    robustness: list[dict[str, Any]],
    regret_summary: list[dict[str, Any]],
    triggers: list[dict[str, Any]],
    vulnerabilities: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Strategy Robustness Ranking",
        "",
    ]

    for row in robustness:
        lines.append(
            f"- **{row['strategy_name']}**: worst-case viability {row['worst_case_viability']}; "
            f"mean viability {row['mean_viability']}; threshold failures {row['threshold_failures']}."
        )

    lines.extend(["", "## Regret Summary", ""])
    for row in regret_summary:
        lines.append(
            f"- **{row['strategy_name']}**: max regret {row['max_regret']}; mean regret {row['mean_regret']}."
        )

    lines.extend(["", "## Adaptive Trigger Priorities", ""])
    for row in triggers:
        lines.append(
            f"- **{row['indicator_name']}**: trigger priority {row['trigger_priority_score']}; "
            f"response: {row['decision_response']}"
        )

    lines.extend(["", "## Vulnerability Priorities", ""])
    for row in vulnerabilities:
        lines.append(
            f"- **{row['vulnerability_name']}**: priority {row['vulnerability_priority_score']}; "
            f"description: {row['description']}"
        )

    lines.extend(["", "## Assumption Failure Risks", ""])
    for row in assumptions:
        lines.append(
            f"- **{row['assumption_name']}**: failure risk {row['assumption_failure_risk']}; "
            f"revision rule: {row['revision_rule']}"
        )

    best = robustness[0]
    low_regret = regret_summary[0]

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Best worst-case strategy: {best['strategy_name']} with worst-case viability {best['worst_case_viability']}.",
        f"- Lowest maximum-regret strategy: {low_regret['strategy_name']} with max regret {low_regret['max_regret']}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats strategic robustness as cross-scenario survivability rather than expected-case optimization. It compares strategies across plausible futures, identifies worst-case viability, calculates regret, diagnoses failure modes, and links monitoring triggers to adaptive decision responses.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "strategic_robustness_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    performance = score_performance()
    robustness = robustness_summary(performance)
    regret_rows, regret_summary = regret_analysis(performance)
    triggers = score_triggers()
    vulnerabilities = score_vulnerabilities()
    assumptions = score_assumptions()

    write_csv(OUTPUTS / "scenario_strategy_performance.csv", performance)
    write_csv(OUTPUTS / "strategy_robustness_scores.csv", robustness)
    write_csv(OUTPUTS / "scenario_strategy_regret.csv", regret_rows)
    write_csv(OUTPUTS / "strategy_regret_summary.csv", regret_summary)
    write_csv(OUTPUTS / "adaptive_trigger_scores.csv", triggers)
    write_csv(OUTPUTS / "vulnerability_scores.csv", vulnerabilities)
    write_csv(OUTPUTS / "assumption_fragility_scores.csv", assumptions)

    write_report(config, robustness, regret_summary, triggers, vulnerabilities, assumptions)

    print(f"Strategic robustness workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
