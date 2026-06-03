#!/usr/bin/env python3
"""
Standard-library workflow for Early Warning Systems and Futures Intelligence.

Outputs:
- signal_warning_scores.csv
- threshold_trigger_scores.csv
- assumption_failure_scores.csv
- scenario_monitor_scores.csv
- cross_system_cascade_scores.csv
- response_protocol_priorities.csv
- early_warning_futures_intelligence_report.md
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


def warning_level(score: float) -> str:
    if score >= 0.82:
        return "Escalate"
    if score >= 0.76:
        return "Watch closely"
    return "Monitor"


def review_weight(freq: str) -> float:
    return {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }.get(freq, 0.50)


def score_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        novelty = float(row["novelty"])
        relevance = float(row["relevance"])
        urgency = float(row["urgency"])
        evidence = float(row["evidence_quality"])
        affected = float(row["affected_voice"])
        vulnerability = float(row["vulnerability"])
        lead_time = float(row["lead_time_value"])

        score = (
            0.12 * novelty
            + 0.22 * relevance
            + 0.20 * urgency
            + 0.13 * evidence
            + 0.11 * affected
            + 0.13 * vulnerability
            + 0.09 * lead_time
        )

        output.append({
            "signal_id": row["signal_id"],
            "signal_name": row["signal_name"],
            "domain": row["domain"],
            "signal_type": row["signal_type"],
            "novelty": novelty,
            "relevance": relevance,
            "urgency": urgency,
            "evidence_quality": evidence,
            "affected_voice": affected,
            "vulnerability": vulnerability,
            "lead_time_value": lead_time,
            "warning_score": round(score, 4),
            "warning_level": warning_level(score),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["warning_score"]), reverse=True)
    return output


def score_indicators() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "indicators.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        baseline = float(row["baseline"])
        current = float(row["current_value"])
        threshold = float(row["threshold_value"])
        gap = current - threshold
        breach = 1.0 if current >= threshold else 0.0
        positive_gap = max(0.0, gap)
        rw = review_weight(row["review_frequency"])

        priority = (
            0.45 * breach
            + 0.25 * current
            + 0.20 * positive_gap
            + 0.10 * rw
        )

        output.append({
            "indicator_id": row["indicator_id"],
            "domain": row["domain"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "current_value": current,
            "threshold_value": threshold,
            "threshold_gap": round(gap, 4),
            "threshold_breached": bool(breach),
            "review_frequency": row["review_frequency"],
            "review_weight": rw,
            "warning_owner": row["warning_owner"],
            "trigger_priority_score": round(priority, 4),
            "trigger_rule": row["trigger_rule"],
            "response_protocol_id": row["response_protocol_id"],
        })

    output.sort(key=lambda item: float(item["trigger_priority_score"]), reverse=True)
    return output


def score_assumptions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "assumptions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        confidence = float(row["confidence"])
        fragility = float(row["fragility"])
        risk = 0.45 * (1.0 - confidence) + 0.55 * fragility

        output.append({
            "assumption_id": row["assumption_id"],
            "domain": row["domain"],
            "assumption_name": row["assumption_name"],
            "confidence": confidence,
            "fragility": fragility,
            "assumption_failure_risk": round(risk, 4),
            "linked_indicator": row["linked_indicator"],
            "revision_rule": row["revision_rule"],
            "assumption_text": row["assumption_text"],
        })

    output.sort(key=lambda item: float(item["assumption_failure_risk"]), reverse=True)
    return output


def score_scenario_monitors() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "scenario_monitors.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        relevance = float(row["scenario_relevance"])
        weight = float(row["monitoring_weight"])
        score = relevance * weight

        output.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "indicator_name": row["indicator_name"],
            "signal_direction": row["signal_direction"],
            "scenario_relevance": relevance,
            "monitoring_weight": weight,
            "scenario_monitor_score": round(score, 4),
            "interpretation": row["interpretation"],
        })

    output.sort(key=lambda item: float(item["scenario_monitor_score"]), reverse=True)
    return output


def score_cascades() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "cross_system_interactions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        influence = float(row["influence_weight"])
        delay = float(row["delay_risk"])
        cascade = float(row["cascade_potential"])
        score = influence * (0.40 + 0.25 * delay + 0.35 * cascade)

        output.append({
            "interaction_id": row["interaction_id"],
            "source_domain": row["source_domain"],
            "target_domain": row["target_domain"],
            "relationship_type": row["relationship_type"],
            "influence_weight": influence,
            "delay_risk": delay,
            "cascade_potential": cascade,
            "cascade_warning_score": round(score, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["cascade_warning_score"]), reverse=True)
    return output


def score_response_protocols(trigger_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    protocols = read_csv(DATA / "response_protocols.csv")
    trigger_by_protocol = {
        row["response_protocol_id"]: float(row["trigger_priority_score"])
        for row in trigger_scores
    }

    action_weight = {
        "escalate": 1.00,
        "pause": 0.96,
        "prepare": 0.72,
        "watch": 0.54,
    }

    output: list[dict[str, Any]] = []

    for row in protocols:
        trigger_score = trigger_by_protocol.get(row["response_protocol_id"], 0.0)
        public_required = 1.0 if row["public_communication_required"].lower() == "yes" else 0.0
        accountability_required = 1.0 if row["accountability_review_required"].lower() == "yes" else 0.0
        action = action_weight.get(row["action_level"], 0.50)

        priority = (
            0.55 * trigger_score
            + 0.20 * action
            + 0.15 * public_required
            + 0.10 * accountability_required
        )

        output.append({
            "response_protocol_id": row["response_protocol_id"],
            "response_name": row["response_name"],
            "response_type": row["response_type"],
            "lead_agency": row["lead_agency"],
            "action_level": row["action_level"],
            "public_communication_required": row["public_communication_required"],
            "accountability_review_required": row["accountability_review_required"],
            "linked_trigger_priority": round(trigger_score, 4),
            "response_priority_score": round(priority, 4),
            "response_description": row["response_description"],
        })

    output.sort(key=lambda item: float(item["response_priority_score"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    signals: list[dict[str, Any]],
    indicators: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    cascades: list[dict[str, Any]],
    protocols: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Signal Warning Scores",
        "",
    ]

    for row in signals:
        lines.append(
            f"- **{row['signal_name']}** ({row['domain']}): warning score {row['warning_score']}; "
            f"level: {row['warning_level']}."
        )

    lines.extend(["", "## Threshold and Trigger Scores", ""])
    for row in indicators:
        breach_text = "breached" if row["threshold_breached"] else "not breached"
        lines.append(
            f"- **{row['indicator_name']}**: trigger priority {row['trigger_priority_score']}; "
            f"threshold {breach_text}; owner: {row['warning_owner']}."
        )

    lines.extend(["", "## Assumption Failure Risks", ""])
    for row in assumptions:
        lines.append(
            f"- **{row['assumption_name']}**: failure risk {row['assumption_failure_risk']}; "
            f"revision rule: {row['revision_rule']}"
        )

    lines.extend(["", "## Scenario Monitoring", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: monitor score {row['scenario_monitor_score']}; "
            f"indicator: {row['indicator_name']}."
        )

    lines.extend(["", "## Cross-System Cascade Scores", ""])
    for row in cascades[:10]:
        lines.append(
            f"- **{row['source_domain']} → {row['target_domain']}**: cascade score {row['cascade_warning_score']}; "
            f"type: {row['relationship_type']}."
        )

    lines.extend(["", "## Response Protocol Priorities", ""])
    for row in protocols:
        lines.append(
            f"- **{row['response_name']}**: response priority {row['response_priority_score']}; "
            f"lead: {row['lead_agency']}."
        )

    escalations = sum(1 for row in signals if row["warning_level"] == "Escalate")
    breached = sum(1 for row in indicators if row["threshold_breached"])
    avg_warning = mean(float(row["warning_score"]) for row in signals)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Escalation-level signals: {escalations}.",
        f"- Threshold breaches: {breached}.",
        f"- Average warning score: {round(avg_warning, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats early warning as a full intelligence-and-governance system. It scores signals, checks thresholds, tracks fragile assumptions, monitors scenario movement, identifies cross-system cascades, and links warning indicators to response protocols.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "early_warning_futures_intelligence_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    signals = score_signals()
    indicators = score_indicators()
    assumptions = score_assumptions()
    scenario_monitors = score_scenario_monitors()
    cascades = score_cascades()
    protocols = score_response_protocols(indicators)

    write_csv(OUTPUTS / "signal_warning_scores.csv", signals)
    write_csv(OUTPUTS / "threshold_trigger_scores.csv", indicators)
    write_csv(OUTPUTS / "assumption_failure_scores.csv", assumptions)
    write_csv(OUTPUTS / "scenario_monitor_scores.csv", scenario_monitors)
    write_csv(OUTPUTS / "cross_system_cascade_scores.csv", cascades)
    write_csv(OUTPUTS / "response_protocol_priorities.csv", protocols)

    write_report(config, signals, indicators, assumptions, scenario_monitors, cascades, protocols)

    print(f"Early warning futures intelligence workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
