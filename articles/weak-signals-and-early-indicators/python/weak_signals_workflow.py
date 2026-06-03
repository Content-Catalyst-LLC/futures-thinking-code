#!/usr/bin/env python3
"""
Standard-library workflow for Weak Signals and Early Indicators.

Outputs:
- weak_signal_profiles.csv
- early_indicator_scores.csv
- signal_cluster_priorities.csv
- propagation_pathway_scores.csv
- assumption_vulnerability_scores.csv
- watchlist_priorities.csv
- weak_signals_report.md
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
    if score >= 0.72:
        return "High-priority watchlist"
    if score >= 0.62:
        return "Monitor and cluster"
    if score >= 0.54:
        return "Exploratory monitoring"
    return "Low-priority or background noise"


def score_weak_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "weak_signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        visibility = float(row["visibility"])
        ambiguity = float(row["ambiguity"])
        systemic = float(row["systemic_connection"])
        propagation = float(row["propagation_potential"])
        recognition = float(row["institutional_recognition"])
        distribution = float(row["distributional_relevance"])
        urgency = float(row["monitoring_urgency"])

        profile = (
            0.10 * visibility
            - 0.08 * ambiguity
            + 0.24 * systemic
            + 0.22 * propagation
            + 0.12 * recognition
            + 0.12 * distribution
            + 0.20 * urgency
        )

        output.append({
            "signal_id": row["signal_id"],
            "signal_title": row["signal_title"],
            "domain": row["domain"],
            "signal_type": row["signal_type"],
            "visibility": visibility,
            "ambiguity": ambiguity,
            "systemic_connection": systemic,
            "propagation_potential": propagation,
            "institutional_recognition": recognition,
            "distributional_relevance": distribution,
            "monitoring_urgency": urgency,
            "weak_signal_profile": round(profile, 4),
            "priority_class": classify_profile(profile),
            "affected_groups": row["affected_groups"],
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["weak_signal_profile"]), reverse=True)
    return output


def score_early_indicators() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "early_indicators.csv")
    output: list[dict[str, Any]] = []

    max_evidence = max(float(row["evidence_count"]) for row in rows) if rows else 1.0

    for row in rows:
        evidence_index = float(row["evidence_count"]) / max_evidence
        repetition = float(row["repetition_score"])
        clarity = float(row["clarity_score"])
        measurement = float(row["measurement_quality"])
        policy = float(row["policy_attention"])

        score = (
            0.25 * repetition
            + 0.25 * clarity
            + 0.20 * measurement
            + 0.20 * policy
            + 0.10 * evidence_index
        )

        output.append({
            "indicator_id": row["indicator_id"],
            "signal_id": row["signal_id"],
            "indicator_name": row["indicator_name"],
            "evidence_count": int(row["evidence_count"]),
            "evidence_index": round(evidence_index, 4),
            "repetition_score": repetition,
            "clarity_score": clarity,
            "measurement_quality": measurement,
            "policy_attention": policy,
            "early_indicator_score": round(score, 4),
            "indicator_status": row["indicator_status"],
            "review_frequency": row["review_frequency"],
        })

    output.sort(key=lambda item: float(item["early_indicator_score"]), reverse=True)
    return output


def score_clusters() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signal_clusters.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        coherence = float(row["coherence"])
        concern = float(row["strategic_concern"])
        priority = coherence * concern

        output.append({
            "cluster_id": row["cluster_id"],
            "cluster_name": row["cluster_name"],
            "related_signals": row["related_signals"],
            "domain": row["domain"],
            "coherence": coherence,
            "strategic_concern": concern,
            "cluster_priority": round(priority, 4),
            "monitoring_priority": row["monitoring_priority"],
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["cluster_priority"]), reverse=True)
    return output


def score_propagation() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "propagation_pathways.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        adoption = float(row["adoption"])
        feedback = float(row["feedback"])
        recognition = float(row["institutional_recognition"])
        friction = float(row["friction"])
        legitimacy = float(row["legitimacy"])

        strength = (
            0.25 * adoption
            + 0.25 * feedback
            + 0.20 * recognition
            + 0.15 * legitimacy
            - 0.20 * friction
        )

        output.append({
            "pathway_id": row["pathway_id"],
            "signal_id": row["signal_id"],
            "pathway_type": row["pathway_type"],
            "adoption": adoption,
            "feedback": feedback,
            "institutional_recognition": recognition,
            "friction": friction,
            "legitimacy": legitimacy,
            "propagation_strength": round(strength, 4),
            "scaling_condition": row["scaling_condition"],
        })

    output.sort(key=lambda item: float(item["propagation_strength"]), reverse=True)
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


def score_watchlist() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "watchlist.csv")
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
            "watch_id": row["watch_id"],
            "signal_id": row["signal_id"],
            "watch_reason": row["watch_reason"],
            "owner_role": row["owner_role"],
            "review_frequency": row["review_frequency"],
            "decision_linkage": linkage,
            "watch_priority": round(priority, 4),
            "trigger_condition": row["trigger_condition"],
        })

    output.sort(key=lambda item: float(item["watch_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    signals: list[dict[str, Any]],
    indicators: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    watchlist: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Highest-Priority Weak Signals",
        "",
    ]

    for index, row in enumerate(signals[:8], start=1):
        lines.append(
            f"{index}. **{row['signal_title']}** — profile {row['weak_signal_profile']}; "
            f"class: {row['priority_class']}."
        )

    lines.extend(["", "## Strongest Early Indicator Scores", ""])
    for row in indicators[:6]:
        lines.append(
            f"- **{row['indicator_name']}** ({row['indicator_status']}): "
            f"score {row['early_indicator_score']}."
        )

    lines.extend(["", "## Signal Cluster Priorities", ""])
    for row in clusters:
        lines.append(
            f"- **{row['cluster_name']}**: cluster priority {row['cluster_priority']} "
            f"({row['monitoring_priority']} monitoring)."
        )

    lines.extend(["", "## Propagation Pathway Scores", ""])
    for row in propagation[:6]:
        lines.append(
            f"- **{row['signal_id']}** via {row['pathway_type']}: "
            f"propagation strength {row['propagation_strength']}."
        )

    lines.extend(["", "## Most Vulnerable Assumptions", ""])
    for row in assumptions[:5]:
        lines.append(
            f"- **{row['domain']}**: {row['assumption_text']} — vulnerability {row['vulnerability_score']}."
        )

    lines.extend(["", "## Watchlist Priorities", ""])
    for row in watchlist:
        lines.append(
            f"- **{row['signal_id']}**: {row['watch_reason']} "
            f"(owner: {row['owner_role']}; review: {row['review_frequency']}; priority {row['watch_priority']})."
        )

    avg_signal = mean(float(row["weak_signal_profile"]) for row in signals)
    avg_indicator = mean(float(row["early_indicator_score"]) for row in indicators)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average weak signal profile: {round(avg_signal, 4)}.",
        f"- Average early indicator score: {round(avg_indicator, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats weak signal analysis as disciplined interpretation under ambiguity. It distinguishes weak signals from early indicators, scores signal profiles, clusters related signals, models propagation conditions, identifies vulnerable assumptions, and creates watchlist priorities for monitoring and strategic review.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "weak_signals_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    signals = score_weak_signals()
    indicators = score_early_indicators()
    clusters = score_clusters()
    propagation = score_propagation()
    assumptions = score_assumptions()
    watchlist = score_watchlist()

    write_csv(OUTPUTS / "weak_signal_profiles.csv", signals)
    write_csv(OUTPUTS / "early_indicator_scores.csv", indicators)
    write_csv(OUTPUTS / "signal_cluster_priorities.csv", clusters)
    write_csv(OUTPUTS / "propagation_pathway_scores.csv", propagation)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumptions)
    write_csv(OUTPUTS / "watchlist_priorities.csv", watchlist)

    write_report(config, signals, indicators, clusters, propagation, assumptions, watchlist)

    print(f"Weak signal workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
