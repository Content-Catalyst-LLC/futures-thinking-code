#!/usr/bin/env python3
"""
Standard-library workflow for Horizon Scanning.

Outputs:
- horizon_signal_profiles.csv
- source_diversity_audit.csv
- signal_cluster_priorities.csv
- assumption_vulnerability_scores.csv
- watchlist_priorities.csv
- institutional_scanning_effectiveness.csv
- horizon_scanning_report.md
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


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


def classify_signal(score: float) -> str:
    if score >= 0.72:
        return "High-priority watchlist"
    if score >= 0.62:
        return "Monitor and cluster"
    if score >= 0.54:
        return "Exploratory monitoring"
    return "Low-priority or background noise"


def score_signals() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        visibility = float(row["visibility"])
        ambiguity = float(row["ambiguity"])
        structural = float(row["structural_connection"])
        domain_diversity = float(row["domain_diversity"])
        source_diversity = float(row["source_diversity"])
        assumption_challenge = float(row["assumption_challenge"])
        relevance = float(row["strategic_relevance"])

        profile = (
            0.10 * visibility
            - 0.08 * ambiguity
            + 0.22 * structural
            + 0.18 * domain_diversity
            + 0.14 * source_diversity
            + 0.14 * assumption_challenge
            + 0.30 * relevance
        )

        output.append({
            "signal_id": row["signal_id"],
            "signal_title": row["signal_title"],
            "domain": row["domain"],
            "signal_type": row["signal_type"],
            "visibility": visibility,
            "ambiguity": ambiguity,
            "structural_connection": structural,
            "domain_diversity": domain_diversity,
            "source_diversity": source_diversity,
            "assumption_challenge": assumption_challenge,
            "strategic_relevance": relevance,
            "horizon_scanning_profile": round(profile, 4),
            "priority_class": classify_signal(profile),
            "affected_groups": row["affected_groups"],
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["horizon_scanning_profile"]), reverse=True)
    return output


def audit_sources() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "sources.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        reliability = float(row["reliability"])
        blind_spot_risk = float(row["blind_spot_risk"])
        community = 1.0 if bool_text(row["community_source"]) else 0.0
        scientific = 1.0 if bool_text(row["scientific_source"]) else 0.0
        policy = 1.0 if bool_text(row["policy_source"]) else 0.0
        cultural = 1.0 if bool_text(row["cultural_source"]) else 0.0
        elite = 1.0 if bool_text(row["elite_source"]) else 0.0

        source_value = (
            reliability * (1.0 - blind_spot_risk)
            + 0.20 * community
            + 0.10 * scientific
            + 0.10 * policy
            + 0.08 * cultural
            - 0.08 * elite * blind_spot_risk
        )

        output.append({
            "source_id": row["source_id"],
            "source_name": row["source_name"],
            "source_type": row["source_type"],
            "domain": row["domain"],
            "elite_source": row["elite_source"],
            "community_source": row["community_source"],
            "scientific_source": row["scientific_source"],
            "policy_source": row["policy_source"],
            "cultural_source": row["cultural_source"],
            "reliability": reliability,
            "blind_spot_risk": blind_spot_risk,
            "source_value_score": round(source_value, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["source_value_score"]), reverse=True)
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


def score_institutions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "institutional_profiles.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        signal = float(row["signal_strength"])
        ambiguity = float(row["ambiguity"])
        filtering = float(row["filtering_quality"])
        source_diversity = float(row["source_diversity"])
        uptake = float(row["institutional_uptake"])
        resistance = float(row["resistance"])

        effectiveness = (
            0.20 * signal
            - 0.16 * ambiguity
            + 0.24 * filtering
            + 0.22 * source_diversity
            + 0.22 * uptake
            - 0.16 * resistance
        )

        output.append({
            "profile_id": row["profile_id"],
            "profile_name": row["profile_name"],
            "signal_strength": signal,
            "ambiguity": ambiguity,
            "filtering_quality": filtering,
            "source_diversity": source_diversity,
            "institutional_uptake": uptake,
            "resistance": resistance,
            "scanning_effectiveness_score": round(effectiveness, 4),
        })

    output.sort(key=lambda item: float(item["scanning_effectiveness_score"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    signals: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    watchlist: list[dict[str, Any]],
    institutions: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Highest-Priority Horizon Scanning Signals",
        "",
    ]

    for index, row in enumerate(signals[:8], start=1):
        lines.append(
            f"{index}. **{row['signal_title']}** — profile {row['horizon_scanning_profile']}; "
            f"class: {row['priority_class']}."
        )

    lines.extend(["", "## Source Diversity Audit", ""])
    for row in sources[:6]:
        lines.append(
            f"- **{row['source_name']}** ({row['source_type']}): value score {row['source_value_score']}; "
            f"blind-spot risk {row['blind_spot_risk']}."
        )

    lines.extend(["", "## Signal Cluster Priorities", ""])
    for row in clusters:
        lines.append(
            f"- **{row['cluster_name']}**: cluster priority {row['cluster_priority']} "
            f"({row['monitoring_priority']} monitoring)."
        )

    lines.extend(["", "## Most Vulnerable Scanning Assumptions", ""])
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

    lines.extend(["", "## Institutional Scanning Effectiveness", ""])
    for index, row in enumerate(institutions, start=1):
        lines.append(
            f"{index}. **{row['profile_name']}** — effectiveness score {row['scanning_effectiveness_score']}."
        )

    avg_signal = mean(float(row["horizon_scanning_profile"]) for row in signals)
    avg_effectiveness = mean(float(row["scanning_effectiveness_score"]) for row in institutions)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average horizon scanning signal profile: {round(avg_signal, 4)}.",
        f"- Average institutional scanning effectiveness score: {round(avg_effectiveness, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats horizon scanning as a disciplined practice of attention under uncertainty. It distinguishes access to information from scanning capacity, and it shows how source diversity, filtering quality, clustering, assumption challenge, and institutional uptake shape whether weak signals become usable foresight.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "horizon_scanning_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    signals = score_signals()
    sources = audit_sources()
    clusters = score_clusters()
    assumptions = score_assumptions()
    watchlist = score_watchlist()
    institutions = score_institutions()

    write_csv(OUTPUTS / "horizon_signal_profiles.csv", signals)
    write_csv(OUTPUTS / "source_diversity_audit.csv", sources)
    write_csv(OUTPUTS / "signal_cluster_priorities.csv", clusters)
    write_csv(OUTPUTS / "assumption_vulnerability_scores.csv", assumptions)
    write_csv(OUTPUTS / "watchlist_priorities.csv", watchlist)
    write_csv(OUTPUTS / "institutional_scanning_effectiveness.csv", institutions)

    write_report(config, signals, sources, clusters, assumptions, watchlist, institutions)

    print(f"Horizon scanning workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
