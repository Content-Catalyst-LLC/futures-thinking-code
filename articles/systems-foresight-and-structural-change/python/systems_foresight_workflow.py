#!/usr/bin/env python3
"""
Standard-library workflow for Systems Foresight and Structural Change.

Outputs:
- structural_pressure_scores.csv
- feedback_loop_priority_scores.csv
- leverage_point_scores.csv
- signal_pressure_scores.csv
- structural_change_pathways.csv
- structural_change_summary.csv
- monitoring_trigger_scores.csv
- systems_foresight_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def pressure_class(score: float) -> str:
    if score >= 0.78:
        return "High structural pressure"
    if score >= 0.68:
        return "Significant structural pressure"
    return "Moderate structural pressure"


def score_structural_pressure() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "system_domains.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        stress = float(row["system_stress"])
        capacity = float(row["adaptive_capacity"])
        trust = float(row["public_trust"])
        interdependence = float(row["interdependence"])
        vulnerability = float(row["distributional_vulnerability"])
        fragmentation = float(row["institutional_fragmentation"])
        lock_in = float(row["structural_lock_in"])

        pressure = (
            0.22 * stress
            + 0.16 * (1.0 - capacity)
            + 0.14 * (1.0 - trust)
            + 0.16 * interdependence
            + 0.14 * vulnerability
            + 0.09 * fragmentation
            + 0.09 * lock_in
        )

        output.append({
            "system_id": row["system_id"],
            "system_domain": row["system_domain"],
            "domain_type": row["domain_type"],
            "system_stress": stress,
            "adaptive_capacity": capacity,
            "public_trust": trust,
            "interdependence": interdependence,
            "distributional_vulnerability": vulnerability,
            "institutional_fragmentation": fragmentation,
            "structural_lock_in": lock_in,
            "structural_pressure_score": round(pressure, 4),
            "pressure_class": pressure_class(pressure),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["structural_pressure_score"]), reverse=True)
    return output


def score_feedback_loops() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "feedback_loops.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        strength = float(row["feedback_strength"])
        delay = float(row["delay_risk"])
        visibility = float(row["visibility"])
        control = float(row["institutional_control"])

        priority = strength * (
            0.40 * delay
            + 0.30 * (1.0 - visibility)
            + 0.30 * (1.0 - control)
        )

        if row["loop_polarity"] == "beneficial":
            loop_action = "protect and strengthen"
        else:
            loop_action = "interrupt or redirect"

        output.append({
            "loop_id": row["loop_id"],
            "system_id": row["system_id"],
            "loop_name": row["loop_name"],
            "loop_type": row["loop_type"],
            "loop_polarity": row["loop_polarity"],
            "feedback_strength": strength,
            "delay_risk": delay,
            "visibility": visibility,
            "institutional_control": control,
            "feedback_priority_score": round(priority, 4),
            "recommended_action": loop_action,
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["feedback_priority_score"]), reverse=True)
    return output


def score_leverage_points() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "leverage_points.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        depth = float(row["intervention_depth"])
        reach = float(row["system_reach"])
        feasibility = float(row["political_feasibility"])
        legitimacy = float(row["legitimacy_quality"])
        equity = float(row["equity_quality"])
        readiness = float(row["implementation_readiness"])

        score = depth * reach * feasibility * legitimacy * equity * readiness

        if score >= 0.26:
            leverage_class = "High-leverage structural pathway"
        elif score >= 0.20:
            leverage_class = "Promising leverage pathway"
        else:
            leverage_class = "Important but constrained pathway"

        output.append({
            "leverage_id": row["leverage_id"],
            "system_id": row["system_id"],
            "intervention": row["intervention"],
            "intervention_level": row["intervention_level"],
            "intervention_depth": depth,
            "system_reach": reach,
            "political_feasibility": feasibility,
            "legitimacy_quality": legitimacy,
            "equity_quality": equity,
            "implementation_readiness": readiness,
            "leverage_score": round(score, 4),
            "leverage_class": leverage_class,
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["leverage_score"]), reverse=True)
    return output


def score_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals_pressure.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        novelty = float(row["novelty"])
        relevance = float(row["structural_relevance"])
        urgency = float(row["urgency"])
        visibility = float(row["visibility"])
        affected_voice = float(row["affected_voice"])

        priority = (
            0.15 * novelty
            + 0.30 * relevance
            + 0.25 * urgency
            + 0.15 * visibility
            + 0.15 * affected_voice
        )

        output.append({
            "signal_id": row["signal_id"],
            "system_id": row["system_id"],
            "signal_name": row["signal_name"],
            "signal_type": row["signal_type"],
            "novelty": novelty,
            "structural_relevance": relevance,
            "urgency": urgency,
            "visibility": visibility,
            "affected_voice": affected_voice,
            "signal_priority_score": round(priority, 4),
            "interpretation": row["interpretation"],
        })

    output.sort(key=lambda item: float(item["signal_priority_score"]), reverse=True)
    return output


def structural_pressure_value(stress: float, capacity: float, trust: float, interdependence: float, vulnerability: float) -> float:
    return (
        0.26 * stress
        + 0.22 * (1.0 - capacity)
        + 0.18 * (1.0 - trust)
        + 0.18 * interdependence
        + 0.16 * vulnerability
    )


def simulate_strategy_pathways() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    strategies = read_csv(DATA / "strategy_pathways.csv")
    paths: list[dict[str, Any]] = []
    summary: list[dict[str, Any]] = []

    for strategy in strategies:
        stress = 0.84
        capacity = 0.42
        trust = 0.46
        interdependence = 0.86
        vulnerability = 0.88

        stress_reduction = float(strategy["stress_reduction"])
        capacity_gain = float(strategy["capacity_gain"])
        trust_gain = float(strategy["trust_gain"])
        vulnerability_reduction = float(strategy["vulnerability_reduction"])
        structural_depth = float(strategy["structural_depth"])
        complexity = float(strategy["implementation_complexity"])
        dependency = float(strategy["governance_dependency"])

        for t in TIME_STEPS:
            shock = 0.08 if t % 10 == 0 else 0.02
            learning_effect = structural_depth * max(0.0, 0.75 - capacity) * 0.010
            implementation_drag = complexity * 0.002
            coordination_bonus = dependency * structural_depth * 0.0015

            stress = clamp(stress + shock - stress_reduction - learning_effect - coordination_bonus)
            capacity = clamp(capacity + capacity_gain + learning_effect - implementation_drag)
            trust = clamp(trust + trust_gain - 0.020 * shock + 0.003 * structural_depth)
            vulnerability = clamp(vulnerability - vulnerability_reduction + 0.010 * shock - 0.002 * structural_depth)

            pressure = structural_pressure_value(
                stress=stress,
                capacity=capacity,
                trust=trust,
                interdependence=interdependence,
                vulnerability=vulnerability,
            )

            paths.append({
                "strategy_id": strategy["strategy_id"],
                "strategy_name": strategy["strategy_name"],
                "strategy_type": strategy["strategy_type"],
                "time_step": t,
                "stress": round(stress, 4),
                "adaptive_capacity": round(capacity, 4),
                "trust": round(trust, 4),
                "interdependence": round(interdependence, 4),
                "distributional_vulnerability": round(vulnerability, 4),
                "structural_depth": structural_depth,
                "structural_pressure": round(pressure, 4),
            })

        rows = [row for row in paths if row["strategy_id"] == strategy["strategy_id"]]
        final = rows[-1]
        pressures = [float(row["structural_pressure"]) for row in rows]
        change_score = (
            0.30 * (1.0 - float(final["structural_pressure"]))
            + 0.25 * float(final["adaptive_capacity"])
            + 0.20 * float(final["trust"])
            + 0.25 * (1.0 - float(final["distributional_vulnerability"]))
        )

        summary.append({
            "strategy_id": strategy["strategy_id"],
            "strategy_name": strategy["strategy_name"],
            "strategy_type": strategy["strategy_type"],
            "final_pressure": final["structural_pressure"],
            "mean_pressure": round(mean(pressures), 4),
            "max_pressure": round(max(pressures), 4),
            "final_capacity": final["adaptive_capacity"],
            "final_trust": final["trust"],
            "final_vulnerability": final["distributional_vulnerability"],
            "structural_change_score": round(change_score, 4),
        })

    summary.sort(key=lambda item: float(item["structural_change_score"]), reverse=True)
    return paths, summary


def score_monitoring_triggers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "monitoring_triggers.csv")
    frequency = {"monthly": 1.0, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
    output: list[dict[str, Any]] = []

    for row in rows:
        baseline = float(row["baseline"])
        threshold = float(row["threshold"])
        gap = abs(threshold - baseline)
        review_weight = frequency.get(row["review_frequency"], 0.50)
        priority = 0.70 * gap + 0.30 * review_weight

        output.append({
            "trigger_id": row["trigger_id"],
            "system_id": row["system_id"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "threshold": threshold,
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
    pressure: list[dict[str, Any]],
    feedback: list[dict[str, Any]],
    leverage: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    strategy_summary: list[dict[str, Any]],
    monitoring: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Structural Pressure Scores",
        "",
    ]

    for row in pressure:
        lines.append(
            f"- **{row['system_domain']}**: pressure {row['structural_pressure_score']}; "
            f"class: {row['pressure_class']}."
        )

    lines.extend(["", "## Feedback Loop Priorities", ""])
    for row in feedback[:8]:
        lines.append(
            f"- **{row['loop_name']}** ({row['loop_polarity']}): priority {row['feedback_priority_score']}; "
            f"recommended action: {row['recommended_action']}."
        )

    lines.extend(["", "## Leverage Point Scores", ""])
    for row in leverage:
        lines.append(
            f"- **{row['intervention']}**: leverage {row['leverage_score']}; class: {row['leverage_class']}."
        )

    lines.extend(["", "## Signal Pressure Priorities", ""])
    for row in signals:
        lines.append(
            f"- **{row['signal_name']}**: priority {row['signal_priority_score']}; interpretation: {row['interpretation']}"
        )

    lines.extend(["", "## Structural Change Strategy Pathways", ""])
    for row in strategy_summary:
        lines.append(
            f"- **{row['strategy_name']}**: structural change score {row['structural_change_score']}; "
            f"final pressure {row['final_pressure']}."
        )

    lines.extend(["", "## Monitoring Triggers", ""])
    for row in monitoring[:8]:
        lines.append(
            f"- **{row['indicator_name']}**: monitoring priority {row['monitoring_priority']}; "
            f"response: {row['decision_response']}"
        )

    best_strategy = strategy_summary[0]
    avg_pressure = mean(float(row["structural_pressure_score"]) for row in pressure)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average structural pressure score: {round(avg_pressure, 4)}.",
        f"- Highest-scoring structural strategy: {best_strategy['strategy_name']} with score {best_strategy['structural_change_score']}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats systems foresight as structural diagnosis and adaptive strategy design. It scores system pressure, feedback loops, leverage points, signals, strategy pathways, and monitoring triggers so future-oriented strategy can address the structures that produce recurring outcomes.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "systems_foresight_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    pressure = score_structural_pressure()
    feedback = score_feedback_loops()
    leverage = score_leverage_points()
    signals = score_signals()
    strategy_paths, strategy_summary = simulate_strategy_pathways()
    monitoring = score_monitoring_triggers()

    write_csv(OUTPUTS / "structural_pressure_scores.csv", pressure)
    write_csv(OUTPUTS / "feedback_loop_priority_scores.csv", feedback)
    write_csv(OUTPUTS / "leverage_point_scores.csv", leverage)
    write_csv(OUTPUTS / "signal_pressure_scores.csv", signals)
    write_csv(OUTPUTS / "structural_change_pathways.csv", strategy_paths)
    write_csv(OUTPUTS / "structural_change_summary.csv", strategy_summary)
    write_csv(OUTPUTS / "monitoring_trigger_scores.csv", monitoring)

    write_report(config, pressure, feedback, leverage, signals, strategy_summary, monitoring)

    print(f"Systems foresight workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
