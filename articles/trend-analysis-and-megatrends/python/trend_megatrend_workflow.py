#!/usr/bin/env python3
"""
Standard-library workflow for Trend Analysis and Megatrends.

Outputs:
- trend_megatrend_profiles.csv
- megatrend_interaction_priorities.csv
- signal_watch_scores.csv
- indicator_movement_scores.csv
- assumption_vulnerability_scores.csv
- strategy_translation_priorities.csv
- trend_megatrend_report.md
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


def classify_profile(score: float) -> str:
    if score >= 0.55:
        return "Megatrend-level structural force"
    if score >= 0.48:
        return "Megatrend candidate"
    if score >= 0.42:
        return "Established strategic trend"
    return "Emerging or domain-specific trend"


def score_trends() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "trend_profiles.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        momentum = float(row["momentum"])
        structural_depth = float(row["structural_depth"])
        cross_system = float(row["cross_system_influence"])
        reversibility = float(row["reversibility"])
        uncertainty = float(row["uncertainty"])
        distribution = float(row["distributional_sensitivity"])

        profile = (
            0.20 * momentum
            + 0.22 * structural_depth
            + 0.22 * cross_system
            - 0.12 * reversibility
            - 0.14 * uncertainty
            + 0.10 * distribution
        )

        output.append({
            "trend_id": row["trend_id"],
            "pattern_type": row["pattern_type"],
            "domain": row["domain"],
            "source_pattern_class": row["pattern_class"],
            "momentum": momentum,
            "structural_depth": structural_depth,
            "cross_system_influence": cross_system,
            "reversibility": reversibility,
            "uncertainty": uncertainty,
            "distributional_sensitivity": distribution,
            "long_term_change_profile": round(profile, 4),
            "classification": classify_profile(profile),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["long_term_change_profile"]), reverse=True)
    return output


def score_interactions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "megatrend_interactions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        strength = float(row["interaction_strength"])
        risk = float(row["systemic_risk"])
        priority = strength * risk

        output.append({
            "interaction_id": row["interaction_id"],
            "source_trend": row["source_trend"],
            "target_trend": row["target_trend"],
            "interaction_type": row["interaction_type"],
            "interaction_strength": strength,
            "systemic_risk": risk,
            "interaction_priority": round(priority, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["interaction_priority"]), reverse=True)
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
            "related_trend": row["related_trend"],
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


def score_indicators() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "indicators.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        current = float(row["current_value"])
        baseline = float(row["baseline_value"])
        confidence = float(row["confidence"])
        movement_score = (current - baseline) * confidence

        output.append({
            "indicator_id": row["indicator_id"],
            "indicator_name": row["indicator_name"],
            "domain": row["domain"],
            "trend_id": row["trend_id"],
            "current_value": current,
            "baseline_value": baseline,
            "trend_direction": row["trend_direction"],
            "confidence": confidence,
            "movement_score": round(movement_score, 4),
            "review_frequency": row["review_frequency"],
        })

    output.sort(key=lambda item: float(item["movement_score"]), reverse=True)
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


def score_strategy_implications() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "strategy_implications.csv")
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
            "implication_id": row["implication_id"],
            "trend_id": row["trend_id"],
            "decision_area": row["decision_area"],
            "strategic_implication": row["strategic_implication"],
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
    trends: list[dict[str, Any]],
    interactions: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    indicators: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    strategy: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Trend and Megatrend Profile Ranking",
        "",
    ]

    for index, row in enumerate(trends, start=1):
        lines.append(
            f"{index}. **{row['pattern_type']}** — profile {row['long_term_change_profile']}; "
            f"classification: {row['classification']}."
        )

    lines.extend(["", "## Highest-Priority Megatrend Interactions", ""])
    for row in interactions[:6]:
        lines.append(
            f"- **{row['source_trend']} → {row['target_trend']}** ({row['interaction_type']}): "
            f"priority {row['interaction_priority']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for row in signals[:6]:
        lines.append(
            f"- **{row['domain']}**: {row['signal']} — watch score {row['watch_score']}."
        )

    lines.extend(["", "## Indicator Movement Scores", ""])
    for row in indicators[:6]:
        lines.append(
            f"- **{row['indicator_name']}**: movement score {row['movement_score']} "
            f"({row['review_frequency']} review)."
        )

    lines.extend(["", "## Most Vulnerable Assumptions", ""])
    for row in assumptions[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend(["", "## Strategy Translation Priorities", ""])
    for row in strategy[:8]:
        lines.append(
            f"- **{row['decision_area']}**: {row['action_option']} "
            f"(priority {row['translation_priority']})."
        )

    avg_profile = mean(float(row["long_term_change_profile"]) for row in trends)
    avg_signal = mean(float(row["watch_score"]) for row in signals)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average long-term change profile: {round(avg_profile, 4)}.",
        f"- Average signal watch score: {round(avg_signal, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats trend analysis as a structured interpretation system. It distinguishes movement from momentum, ordinary trends from structural forces, and isolated patterns from interacting megatrend environments. It is designed to support scenario planning, monitoring, and strategic decision-making rather than deterministic prediction.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "trend_megatrend_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    trends = score_trends()
    interactions = score_interactions()
    signals = score_signals()
    indicators = score_indicators()
    assumptions = score_assumptions()
    strategy = score_strategy_implications()

    write_csv(OUTPUTS / "trend_megatrend_profiles.csv", trends)
    write_csv(OUTPUTS / "megatrend_interaction_priorities.csv", interactions)
    write_csv(OUTPUTS / "signal_watch_scores.csv", signals)
    write_csv(OUTPUTS / "indicator_movement_scores.csv", indicators)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumptions)
    write_csv(OUTPUTS / "strategy_translation_priorities.csv", strategy)

    write_report(config, trends, interactions, signals, indicators, assumptions, strategy)

    print(f"Trend and megatrend workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
