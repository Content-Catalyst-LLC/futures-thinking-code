#!/usr/bin/env python3
"""
Standard-library workflow for Uncertainty Matrices and Driver Mapping.

Outputs:
- driver_priority_scores.csv
- driver_interaction_scores.csv
- scenario_axis_candidates.csv
- signal_priority_scores.csv
- monitoring_priority_scores.csv
- assumption_fragility_scores.csv
- uncertainty_driver_mapping_report.md
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
CONFIG = ROOT / "article_config.json"
OUTPUTS.mkdir(exist_ok=True)

IMPACT_THRESHOLD = 0.80
UNCERTAINTY_THRESHOLD = 0.72


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


def classify_quadrant(impact: float, uncertainty: float) -> str:
    if impact >= IMPACT_THRESHOLD and uncertainty >= UNCERTAINTY_THRESHOLD:
        return "Critical uncertainty"
    if impact >= IMPACT_THRESHOLD and uncertainty < UNCERTAINTY_THRESHOLD:
        return "Baseline structural driver"
    if impact < IMPACT_THRESHOLD and uncertainty >= UNCERTAINTY_THRESHOLD:
        return "Watchlist uncertainty"
    return "Lower-priority factor"


def score_drivers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "driver_register.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        impact = float(row["impact"])
        uncertainty = float(row["uncertainty"])
        urgency = float(row["urgency"])
        interaction = float(row["interaction_strength"])
        burden = float(row["distributional_burden"])
        monitoring = float(row["monitoring_feasibility"])
        evidence = float(row["evidence_strength"])
        controllability = float(row["controllability"])

        priority = (
            0.22 * impact
            + 0.20 * uncertainty
            + 0.14 * urgency
            + 0.14 * interaction
            + 0.12 * burden
            + 0.08 * monitoring
            + 0.06 * evidence
            + 0.04 * (1.0 - controllability)
        )

        axis_suitability = impact * uncertainty * interaction * monitoring * evidence

        output.append({
            "driver_id": row["driver_id"],
            "driver_name": row["driver_name"],
            "domain": row["domain"],
            "driver_type": row["driver_type"],
            "impact": impact,
            "uncertainty": uncertainty,
            "urgency": urgency,
            "interaction_strength": interaction,
            "distributional_burden": burden,
            "monitoring_feasibility": monitoring,
            "evidence_strength": evidence,
            "controllability": controllability,
            "driver_priority_score": round(priority, 4),
            "matrix_quadrant": classify_quadrant(impact, uncertainty),
            "axis_suitability_score": round(axis_suitability, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["driver_priority_score"]), reverse=True)
    return output


def score_interactions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "driver_interactions.csv")
    output: list[dict[str, Any]] = []
    outgoing: dict[str, float] = defaultdict(float)
    incoming: dict[str, float] = defaultdict(float)

    for row in rows:
        weight = float(row["influence_weight"])
        delay = float(row["delay_risk"])
        cascade = float(row["cascade_potential"])
        interaction_priority = weight * (0.45 + 0.25 * delay + 0.30 * cascade)

        outgoing[row["source_driver_id"]] += weight
        incoming[row["target_driver_id"]] += weight

        output.append({
            "interaction_id": row["interaction_id"],
            "source_driver_id": row["source_driver_id"],
            "target_driver_id": row["target_driver_id"],
            "relationship_type": row["relationship_type"],
            "influence_weight": weight,
            "direction": row["direction"],
            "delay_risk": delay,
            "cascade_potential": cascade,
            "interaction_priority_score": round(interaction_priority, 4),
            "notes": row["notes"],
        })

    output.sort(key=lambda item: float(item["interaction_priority_score"]), reverse=True)

    cross_rows: list[dict[str, Any]] = []
    all_drivers = sorted(set(outgoing.keys()) | set(incoming.keys()))

    for driver_id in all_drivers:
        cross_rows.append({
            "driver_id": driver_id,
            "outgoing_influence": round(outgoing.get(driver_id, 0.0), 4),
            "incoming_influence": round(incoming.get(driver_id, 0.0), 4),
            "total_cross_impact": round(outgoing.get(driver_id, 0.0) + incoming.get(driver_id, 0.0), 4),
        })

    cross_rows.sort(key=lambda item: float(item["total_cross_impact"]), reverse=True)
    write_csv(OUTPUTS / "driver_cross_impact_scores.csv", cross_rows)

    return output


def identify_axis_candidates(drivers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [
        row for row in drivers
        if row["matrix_quadrant"] == "Critical uncertainty"
    ]

    candidates.sort(
        key=lambda item: (
            float(item["axis_suitability_score"]),
            float(item["driver_priority_score"])
        ),
        reverse=True
    )

    output: list[dict[str, Any]] = []
    for rank, row in enumerate(candidates, start=1):
        output.append({
            "axis_rank": rank,
            "driver_id": row["driver_id"],
            "driver_name": row["driver_name"],
            "domain": row["domain"],
            "impact": row["impact"],
            "uncertainty": row["uncertainty"],
            "axis_suitability_score": row["axis_suitability_score"],
            "scenario_axis_note": f"Candidate axis for scenario contrast: {row['driver_name']}",
        })

    return output


def score_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        novelty = float(row["novelty"])
        relevance = float(row["relevance"])
        urgency = float(row["urgency"])
        evidence = float(row["evidence_quality"])
        affected = float(row["affected_voice"])

        priority = (
            0.15 * novelty
            + 0.30 * relevance
            + 0.25 * urgency
            + 0.15 * evidence
            + 0.15 * affected
        )

        output.append({
            "signal_id": row["signal_id"],
            "driver_id": row["driver_id"],
            "signal_name": row["signal_name"],
            "signal_type": row["signal_type"],
            "novelty": novelty,
            "relevance": relevance,
            "urgency": urgency,
            "evidence_quality": evidence,
            "affected_voice": affected,
            "signal_priority_score": round(priority, 4),
            "interpretation": row["interpretation"],
        })

    output.sort(key=lambda item: float(item["signal_priority_score"]), reverse=True)
    return output


def score_monitoring(drivers_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = read_csv(DATA / "monitoring_indicators.csv")
    frequency = {"monthly": 1.0, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
    output: list[dict[str, Any]] = []

    for row in rows:
        driver = drivers_by_id[row["driver_id"]]
        baseline = float(row["baseline"])
        threshold = float(row["threshold"])
        gap = abs(threshold - baseline)
        review_weight = frequency.get(row["review_frequency"], 0.50)
        priority = (
            0.30 * float(driver["uncertainty"])
            + 0.20 * float(driver["urgency"])
            + 0.18 * float(driver["distributional_burden"])
            + 0.17 * gap
            + 0.15 * review_weight
        )

        output.append({
            "indicator_id": row["indicator_id"],
            "driver_id": row["driver_id"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "threshold": threshold,
            "monitoring_gap": round(gap, 4),
            "review_frequency": row["review_frequency"],
            "review_weight": review_weight,
            "monitoring_priority_score": round(priority, 4),
            "assumption_risk": row["assumption_risk"],
            "trigger_rule": row["trigger_rule"],
            "decision_response": row["decision_response"],
        })

    output.sort(key=lambda item: float(item["monitoring_priority_score"]), reverse=True)
    return output


def score_assumptions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "assumption_register.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        confidence = float(row["confidence"])
        fragility = float(row["fragility"])
        failure_risk = (1.0 - confidence) * 0.45 + fragility * 0.55

        output.append({
            "assumption_id": row["assumption_id"],
            "driver_id": row["driver_id"],
            "assumption_name": row["assumption_name"],
            "confidence": confidence,
            "fragility": fragility,
            "assumption_failure_risk": round(failure_risk, 4),
            "monitoring_signal": row["monitoring_signal"],
            "revision_rule": row["revision_rule"],
            "assumption_text": row["assumption_text"],
        })

    output.sort(key=lambda item: float(item["assumption_failure_risk"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    drivers: list[dict[str, Any]],
    interactions: list[dict[str, Any]],
    axes: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    monitoring: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Driver Priority Scores",
        "",
    ]

    for row in drivers:
        lines.append(
            f"- **{row['driver_name']}** ({row['matrix_quadrant']}): priority {row['driver_priority_score']}; "
            f"axis suitability {row['axis_suitability_score']}."
        )

    lines.extend(["", "## Scenario-Axis Candidates", ""])
    for row in axes:
        lines.append(
            f"- **{row['driver_name']}**: axis rank {row['axis_rank']}; suitability {row['axis_suitability_score']}."
        )

    lines.extend(["", "## Highest-Priority Driver Interactions", ""])
    for row in interactions[:10]:
        lines.append(
            f"- **{row['source_driver_id']} → {row['target_driver_id']}** ({row['relationship_type']}): "
            f"priority {row['interaction_priority_score']}."
        )

    lines.extend(["", "## Signal Priorities", ""])
    for row in signals[:10]:
        lines.append(
            f"- **{row['signal_name']}**: priority {row['signal_priority_score']}; interpretation: {row['interpretation']}"
        )

    lines.extend(["", "## Monitoring Priorities", ""])
    for row in monitoring[:10]:
        lines.append(
            f"- **{row['indicator_name']}**: priority {row['monitoring_priority_score']}; response: {row['decision_response']}"
        )

    lines.extend(["", "## Assumption Fragility", ""])
    for row in assumptions:
        lines.append(
            f"- **{row['assumption_name']}**: failure risk {row['assumption_failure_risk']}; revision rule: {row['revision_rule']}"
        )

    critical_count = sum(1 for row in drivers if row["matrix_quadrant"] == "Critical uncertainty")
    baseline_count = sum(1 for row in drivers if row["matrix_quadrant"] == "Baseline structural driver")
    avg_priority = mean(float(row["driver_priority_score"]) for row in drivers)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Critical uncertainties identified: {critical_count}.",
        f"- Baseline structural drivers identified: {baseline_count}.",
        f"- Average driver priority score: {round(avg_priority, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats uncertainty matrices and driver mapping as structured foresight intelligence. It ranks drivers, classifies matrix quadrants, identifies candidate scenario axes, maps cross-driver interactions, tracks signals, and connects assumptions to monitoring triggers.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "uncertainty_driver_mapping_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    drivers = score_drivers()
    drivers_by_id = {row["driver_id"]: row for row in drivers}

    interactions = score_interactions()
    axes = identify_axis_candidates(drivers)
    signals = score_signals()
    monitoring = score_monitoring(drivers_by_id)
    assumptions = score_assumptions()

    write_csv(OUTPUTS / "driver_priority_scores.csv", drivers)
    write_csv(OUTPUTS / "driver_interaction_scores.csv", interactions)
    write_csv(OUTPUTS / "scenario_axis_candidates.csv", axes)
    write_csv(OUTPUTS / "signal_priority_scores.csv", signals)
    write_csv(OUTPUTS / "monitoring_priority_scores.csv", monitoring)
    write_csv(OUTPUTS / "assumption_fragility_scores.csv", assumptions)

    write_report(config, drivers, interactions, axes, signals, monitoring, assumptions)

    print(f"Uncertainty driver mapping workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
