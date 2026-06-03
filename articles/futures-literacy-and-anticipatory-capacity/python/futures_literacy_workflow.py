#!/usr/bin/env python3
"""
Standard-library workflow for Futures Literacy and Anticipatory Capacity.

Outputs:
- anticipatory_capacity_scores.csv
- assumption_vulnerability_scores.csv
- signal_watch_scores.csv
- future_image_risk_scores.csv
- learning_cycle_scores.csv
- strategy_translation_index.csv
- futures_literacy_report.md
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
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


def score_capacity_profiles() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "capacity_profiles.csv")
    weights = {
        "scanning_capacity": 0.15,
        "interpretive_capacity": 0.15,
        "assumption_visibility": 0.17,
        "imagination_range": 0.13,
        "participatory_depth": 0.17,
        "learning_capacity": 0.13,
        "action_translation": 0.10,
    }

    output: list[dict[str, Any]] = []
    for row in rows:
        values = {key: float(row[key]) for key in weights}
        score = sum(values[key] * weight for key, weight in weights.items())
        output.append({
            "organization_type": row["organization_type"],
            "anticipatory_capacity_score": round(score, 4),
            "strongest_dimension": max(values, key=values.get),
            "weakest_dimension": min(values, key=values.get),
        })

    output.sort(key=lambda row: float(row["anticipatory_capacity_score"]), reverse=True)
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


def score_future_images() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "future_images.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        assumption_risk = float(row["assumption_risk"])
        participation_need = float(row["participation_need"])
        participation_gap = max(0.0, participation_need - 0.70)
        future_image_risk = assumption_risk * (1.0 + participation_gap)
        output.append({
            "future_image_id": row["future_image_id"],
            "actor_group": row["actor_group"],
            "future_image": row["future_image"],
            "dominant_emotion": row["dominant_emotion"],
            "time_horizon": row["time_horizon"],
            "assumption_risk": assumption_risk,
            "participation_need": participation_need,
            "future_image_risk": round(future_image_risk, 4),
        })

    output.sort(key=lambda row: float(row["future_image_risk"]), reverse=True)
    return output


def score_learning_cycles() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "learning_cycles.csv")
    output: list[dict[str, Any]] = []

    frequency_bonus = {
        "monthly": 0.12,
        "bimonthly": 0.10,
        "quarterly": 0.08,
        "semiannual": 0.04,
        "annual": 0.02,
    }

    for row in rows:
        participation = float(row["public_participation_level"])
        decision_linkage = float(row["decision_linkage"])
        learning_score = float(row["learning_score"])
        review_bonus = frequency_bonus.get(row["signal_review_frequency"], 0.0)
        institutional_learning_score = (
            0.35 * learning_score +
            0.30 * decision_linkage +
            0.25 * participation +
            review_bonus
        )
        output.append({
            "cycle_id": row["cycle_id"],
            "cycle_name": row["cycle_name"],
            "signal_review_frequency": row["signal_review_frequency"],
            "assumption_review_frequency": row["assumption_review_frequency"],
            "public_participation_level": participation,
            "decision_linkage": decision_linkage,
            "learning_score": learning_score,
            "institutional_learning_score": round(institutional_learning_score, 4),
        })

    output.sort(key=lambda row: float(row["institutional_learning_score"]), reverse=True)
    return output


def build_translation_index() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "strategy_translation.csv")
    output: list[dict[str, Any]] = []

    frequency_weight = {
        "monthly": 1.0,
        "quarterly": 0.85,
        "semiannual": 0.65,
        "annual": 0.45,
    }

    for row in rows:
        weight = frequency_weight.get(row["review_frequency"], 0.50)
        output.append({
            "insight_id": row["insight_id"],
            "decision_area": row["decision_area"],
            "insight": row["insight"],
            "action_option": row["action_option"],
            "monitoring_indicator": row["monitoring_indicator"],
            "review_frequency": row["review_frequency"],
            "translation_priority": round(weight, 4),
        })

    output.sort(key=lambda row: float(row["translation_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    capacity: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    future_images: list[dict[str, Any]],
    learning: list[dict[str, Any]],
    translation: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Anticipatory Capacity Ranking",
        "",
    ]

    for index, row in enumerate(capacity, start=1):
        lines.append(
            f"{index}. **{row['organization_type']}** — score {row['anticipatory_capacity_score']}; "
            f"strongest: {row['strongest_dimension']}; weakest: {row['weakest_dimension']}."
        )

    lines.extend(["", "## Most Vulnerable Assumptions", ""])
    for row in assumptions[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for row in signals[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['signal']} — watch score {row['watch_score']}."
        )

    lines.extend(["", "## Future Image Risk", ""])
    for row in future_images[:5]:
        lines.append(
            f"- **{row['actor_group']}**: {row['future_image']} — risk {row['future_image_risk']}."
        )

    lines.extend(["", "## Strongest Learning Cycles", ""])
    for row in learning[:5]:
        lines.append(
            f"- **{row['cycle_name']}** — institutional learning score {row['institutional_learning_score']}."
        )

    lines.extend(["", "## Strategy Translation Priorities", ""])
    for row in translation:
        lines.append(
            f"- **{row['decision_area']}**: {row['action_option']} "
            f"(monitor: {row['monitoring_indicator']}; review: {row['review_frequency']})."
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "This workflow treats futures literacy as an institutional learning capability. "
        "The goal is not to predict the future, but to make assumptions, signals, future images, "
        "participation needs, and decision links more explicit.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "futures_literacy_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    capacity = score_capacity_profiles()
    assumptions = score_assumptions()
    signals = score_signals()
    future_images = score_future_images()
    learning = score_learning_cycles()
    translation = build_translation_index()

    write_csv(OUTPUTS / "anticipatory_capacity_scores.csv", capacity)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumptions)
    write_csv(OUTPUTS / "signal_watch_scores.csv", signals)
    write_csv(OUTPUTS / "future_image_risk_scores.csv", future_images)
    write_csv(OUTPUTS / "learning_cycle_scores.csv", learning)
    write_csv(OUTPUTS / "strategy_translation_index.csv", translation)

    write_report(config, capacity, assumptions, signals, future_images, learning, translation)

    print(f"Futures literacy workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
