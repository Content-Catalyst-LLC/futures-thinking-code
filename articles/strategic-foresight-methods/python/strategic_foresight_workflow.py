#!/usr/bin/env python3
"""
Standard-library workflow for Strategic Foresight Methods.

Outputs:
- foresight_method_profiles.csv
- foresight_method_risks.csv
- pipeline_actionable_foresight_scores.csv
- signal_watch_scores.csv
- driver_uncertainty_scores.csv
- assumption_vulnerability_scores.csv
- strategy_translation_index.csv
- strategic_foresight_report.md
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


def score_methods() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = read_csv(DATA / "foresight_methods.csv")
    profile_rows: list[dict[str, Any]] = []
    risk_rows: list[dict[str, Any]] = []

    for row in rows:
        detection = float(row["detection_power"])
        ambiguity = float(row["ambiguity_tolerance"])
        structural = float(row["structural_depth"])
        actionability = float(row["actionability"])
        participation = float(row["participatory_depth"])
        fit = float(row["institutional_fit"])
        learning = float(row["learning_value"])
        technocratic = float(row["technocratic_risk"])

        profile = (
            0.16 * detection
            + 0.14 * ambiguity
            + 0.16 * structural
            + 0.18 * actionability
            + 0.14 * participation
            + 0.10 * fit
            + 0.12 * learning
        )

        risk = technocratic * (1.0 - participation) * (1.0 - learning)

        profile_rows.append({
            "method_id": row["method_id"],
            "method": row["method"],
            "primary_function": row["primary_function"],
            "detection_power": detection,
            "ambiguity_tolerance": ambiguity,
            "structural_depth": structural,
            "actionability": actionability,
            "participatory_depth": participation,
            "institutional_fit": fit,
            "learning_value": learning,
            "method_profile_score": round(profile, 4),
        })

        risk_rows.append({
            "method_id": row["method_id"],
            "method": row["method"],
            "primary_function": row["primary_function"],
            "technocratic_risk": technocratic,
            "participatory_depth": participation,
            "learning_value": learning,
            "method_risk_score": round(risk, 4),
            "risk_note": "High method-risk attention" if risk >= 0.12 else "Manageable if integrated carefully",
        })

    profile_rows.sort(key=lambda item: float(item["method_profile_score"]), reverse=True)
    risk_rows.sort(key=lambda item: float(item["method_risk_score"]), reverse=True)
    return profile_rows, risk_rows


def score_pipelines() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "pipeline_profiles.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        detection = float(row["detection"])
        interpretation = float(row["interpretation"])
        pattern = float(row["pattern_formation"])
        uncertainty = float(row["uncertainty_structuring"])
        strategic = float(row["strategic_design"])
        legitimacy = float(row["legitimacy"])
        uptake = float(row["uptake"])
        resistance = float(row["resistance"])

        method_gain = (
            0.14 * detection
            + 0.15 * interpretation
            + 0.14 * pattern
            + 0.16 * uncertainty
            + 0.16 * strategic
            + 0.12 * legitimacy
            + 0.13 * uptake
        )

        actionable = method_gain + 0.15 * legitimacy + 0.15 * uptake - 0.20 * resistance

        output.append({
            "pipeline_id": row["pipeline_id"],
            "pipeline_name": row["pipeline_name"],
            "method_gain": round(method_gain, 4),
            "legitimacy": legitimacy,
            "uptake": uptake,
            "resistance": resistance,
            "actionable_foresight_score": round(actionable, 4),
        })

    output.sort(key=lambda item: float(item["actionable_foresight_score"]), reverse=True)
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

    output.sort(key=lambda item: float(item["watch_score"]), reverse=True)
    return output


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

    output.sort(key=lambda item: float(item["criticality_score"]), reverse=True)
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

    output.sort(key=lambda item: float(item["vulnerability_score"]), reverse=True)
    return output


def build_translation_index() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "strategy_translation.csv")
    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }

    output: list[dict[str, Any]] = []

    for row in rows:
        linkage = float(row["decision_linkage"])
        frequency = frequency_weight.get(row["review_frequency"], 0.50)
        priority = 0.70 * linkage + 0.30 * frequency

        output.append({
            "insight_id": row["insight_id"],
            "decision_area": row["decision_area"],
            "foresight_insight": row["foresight_insight"],
            "action_option": row["action_option"],
            "monitoring_indicator": row["monitoring_indicator"],
            "review_frequency": row["review_frequency"],
            "decision_linkage": linkage,
            "translation_priority": round(priority, 4),
        })

    output.sort(key=lambda item: float(item["translation_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    method_profiles: list[dict[str, Any]],
    method_risks: list[dict[str, Any]],
    pipelines: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    translation: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Highest-Scoring Foresight Method Profiles",
        "",
    ]

    for row in method_profiles[:10]:
        lines.append(
            f"- **{row['method']}** ({row['primary_function']}): profile score {row['method_profile_score']}."
        )

    lines.extend(["", "## Method Risk Attention", ""])
    for row in method_risks[:6]:
        lines.append(
            f"- **{row['method']}**: risk score {row['method_risk_score']} — {row['risk_note']}."
        )

    lines.extend(["", "## Institutional Pipeline Scores", ""])
    for index, row in enumerate(pipelines, start=1):
        lines.append(
            f"{index}. **{row['pipeline_name']}** — actionable foresight score {row['actionable_foresight_score']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for row in signals[:6]:
        lines.append(f"- **{row['domain']}**: {row['signal']} — watch score {row['watch_score']}.")

    lines.extend(["", "## Highest-Criticality Drivers and Uncertainties", ""])
    for row in drivers[:6]:
        lines.append(
            f"- **{row['driver_or_uncertainty']}** ({row['domain']}): criticality {row['criticality_score']}."
        )

    lines.extend(["", "## Most Vulnerable Foresight Assumptions", ""])
    for row in assumptions[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend(["", "## Strategy Translation Priorities", ""])
    for row in translation:
        lines.append(
            f"- **{row['decision_area']}**: {row['action_option']} "
            f"(monitor: {row['monitoring_indicator']}; review: {row['review_frequency']})."
        )

    avg_profile = mean(float(row["method_profile_score"]) for row in method_profiles)
    avg_pipeline = mean(float(row["actionable_foresight_score"]) for row in pipelines)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average method profile score: {round(avg_profile, 4)}.",
        f"- Average actionable foresight pipeline score: {round(avg_pipeline, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats strategic foresight as a layered system of detection, interpretation, pattern formation, uncertainty structuring, strategic design, legitimacy, uptake, and learning. The goal is not to predict the future, but to make foresight methods, institutional constraints, assumptions, signals, and strategy translation more explicit.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "strategic_foresight_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    method_profiles, method_risks = score_methods()
    pipelines = score_pipelines()
    signals = score_signals()
    drivers = score_drivers()
    assumptions = score_assumptions()
    translation = build_translation_index()

    write_csv(OUTPUTS / "foresight_method_profiles.csv", method_profiles)
    write_csv(OUTPUTS / "foresight_method_risks.csv", method_risks)
    write_csv(OUTPUTS / "pipeline_actionable_foresight_scores.csv", pipelines)
    write_csv(OUTPUTS / "signal_watch_scores.csv", signals)
    write_csv(OUTPUTS / "driver_uncertainty_scores.csv", drivers)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumptions)
    write_csv(OUTPUTS / "strategy_translation_index.csv", translation)

    write_report(config, method_profiles, method_risks, pipelines, signals, drivers, assumptions, translation)

    print(f"Strategic foresight workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
