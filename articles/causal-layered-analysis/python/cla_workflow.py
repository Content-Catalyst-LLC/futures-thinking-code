#!/usr/bin/env python3
"""
Standard-library workflow for Causal Layered Analysis.

Outputs:
- cla_issue_depth_scores.csv
- layer_transformation_priorities.csv
- metaphor_reframing_scores.csv
- reframing_depth_scores.csv
- power_legitimacy_audit_scores.csv
- scenario_translation_register.csv
- cla_report.md
"""

from __future__ import annotations

import csv
import json
from collections import Counter
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


def classify_cla(score: float) -> str:
    if score >= 0.86:
        return "High-depth reframing opportunity"
    if score >= 0.80:
        return "Strong layered analysis candidate"
    return "Moderate CLA candidate"


def score_issues() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "cla_issues.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        litany = float(row["litany_visibility"])
        systemic = float(row["systemic_explanation"])
        worldview = float(row["worldview_challenge"])
        metaphor = float(row["myth_metaphor_depth"])
        reframe = float(row["reframing_potential"])
        power = float(row["power_sensitivity"])
        relevance = float(row["strategic_relevance"])

        depth = (
            0.10 * litany
            + 0.18 * systemic
            + 0.22 * worldview
            + 0.20 * metaphor
            + 0.16 * reframe
            + 0.08 * power
            + 0.06 * relevance
        )

        output.append({
            "issue_id": row["issue_id"],
            "issue_title": row["issue_title"],
            "domain": row["domain"],
            "time_horizon": row["time_horizon"],
            "litany_visibility": litany,
            "systemic_explanation": systemic,
            "worldview_challenge": worldview,
            "myth_metaphor_depth": metaphor,
            "reframing_potential": reframe,
            "power_sensitivity": power,
            "strategic_relevance": relevance,
            "cla_depth_score": round(depth, 4),
            "cla_class": classify_cla(depth),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["cla_depth_score"]), reverse=True)
    return output


def score_layers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "layer_codes.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        diagnostic = float(row["diagnostic_weight"])
        transformation = float(row["transformation_need"])
        priority = diagnostic * transformation

        output.append({
            "code_id": row["code_id"],
            "issue_id": row["issue_id"],
            "layer_level": int(row["layer_level"]),
            "layer_label": row["layer_label"],
            "statement": row["statement"],
            "diagnostic_weight": diagnostic,
            "transformation_need": transformation,
            "layer_priority": round(priority, 4),
            "notes": row["notes"],
        })

    output.sort(key=lambda item: float(item["layer_priority"]), reverse=True)
    return output


def score_metaphors() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "metaphor_map.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        shift = float(row["metaphor_shift_score"])
        ethical = float(row["ethical_relevance"])
        score = 0.60 * shift + 0.40 * ethical

        output.append({
            "metaphor_id": row["metaphor_id"],
            "issue_id": row["issue_id"],
            "dominant_metaphor": row["dominant_metaphor"],
            "alternative_metaphor": row["alternative_metaphor"],
            "dominant_effect": row["dominant_effect"],
            "alternative_effect": row["alternative_effect"],
            "metaphor_shift_score": shift,
            "ethical_relevance": ethical,
            "metaphor_reframing_score": round(score, 4),
        })

    output.sort(key=lambda item: float(item["metaphor_reframing_score"]), reverse=True)
    return output


def score_reframes() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "reframing_profiles.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        litany = float(row["litany_change"])
        systemic = float(row["systemic_change"])
        worldview = float(row["worldview_change"])
        metaphor = float(row["metaphor_change"])
        power = float(row["power_awareness"])
        coherence = float(row["strategic_coherence"])

        depth = (
            0.12 * litany
            + 0.20 * systemic
            + 0.22 * worldview
            + 0.22 * metaphor
            + 0.12 * power
            + 0.12 * coherence
        )

        output.append({
            "reframe_id": row["reframe_id"],
            "issue_id": row["issue_id"],
            "old_litany": row["old_litany"],
            "new_litany": row["new_litany"],
            "old_worldview": row["old_worldview"],
            "new_worldview": row["new_worldview"],
            "old_metaphor": row["old_metaphor"],
            "new_metaphor": row["new_metaphor"],
            "litany_change": litany,
            "systemic_change": systemic,
            "worldview_change": worldview,
            "metaphor_change": metaphor,
            "power_awareness": power,
            "strategic_coherence": coherence,
            "reframing_depth_score": round(depth, 4),
        })

    output.sort(key=lambda item: float(item["reframing_depth_score"]), reverse=True)
    return output


def score_power() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "power_audit.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        power_risk = float(row["power_risk"])
        exclusion = float(row["exclusion_risk"])
        legitimacy = float(row["legitimacy_need"])
        score = 0.40 * power_risk + 0.30 * exclusion + 0.30 * legitimacy

        output.append({
            "audit_id": row["audit_id"],
            "issue_id": row["issue_id"],
            "dominant_voice": row["dominant_voice"],
            "excluded_voice": row["excluded_voice"],
            "power_risk": power_risk,
            "exclusion_risk": exclusion,
            "legitimacy_need": legitimacy,
            "power_legitimacy_score": round(score, 4),
            "counter_narrative": row["counter_narrative"],
        })

    output.sort(key=lambda item: float(item["power_legitimacy_score"]), reverse=True)
    return output


def build_scenario_register() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "scenario_translation.csv")
    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }
    output: list[dict[str, Any]] = []

    for row in rows:
        output.append({
            "scenario_id": row["scenario_id"],
            "issue_id": row["issue_id"],
            "reframed_scenario": row["reframed_scenario"],
            "scenario_logic": row["scenario_logic"],
            "backcasting_target": row["backcasting_target"],
            "monitoring_indicator": row["monitoring_indicator"],
            "review_frequency": row["review_frequency"],
            "review_weight": frequency_weight.get(row["review_frequency"], 0.50),
        })

    return output


def write_report(
    config: dict[str, Any],
    issues: list[dict[str, Any]],
    layers: list[dict[str, Any]],
    metaphors: list[dict[str, Any]],
    reframes: list[dict[str, Any]],
    power: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
) -> None:
    layer_counts = Counter(row["layer_label"] for row in layers)

    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## CLA Issue Depth Scores",
        "",
    ]

    for row in issues:
        lines.append(
            f"- **{row['issue_title']}**: CLA depth {row['cla_depth_score']}; class: {row['cla_class']}."
        )

    lines.extend(["", "## Highest Layer Transformation Priorities", ""])
    for row in layers[:8]:
        lines.append(
            f"- **{row['issue_id']} / {row['layer_label']}**: priority {row['layer_priority']}; {row['statement']}"
        )

    lines.extend(["", "## Strongest Metaphor Reframes", ""])
    for row in metaphors[:6]:
        lines.append(
            f"- **{row['dominant_metaphor']} → {row['alternative_metaphor']}**: "
            f"score {row['metaphor_reframing_score']}."
        )

    lines.extend(["", "## Reframing Depth Scores", ""])
    for row in reframes:
        lines.append(
            f"- **{row['issue_id']}**: {row['old_metaphor']} → {row['new_metaphor']} "
            f"with depth score {row['reframing_depth_score']}."
        )

    lines.extend(["", "## Power and Legitimacy Audit", ""])
    for row in power:
        lines.append(
            f"- **{row['issue_id']}**: score {row['power_legitimacy_score']}; "
            f"counter-narrative: {row['counter_narrative']}"
        )

    lines.extend(["", "## Scenario Translation Register", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['reframed_scenario']}**: {row['backcasting_target']}; "
            f"monitor: {row['monitoring_indicator']}."
        )

    avg_depth = mean(float(row["cla_depth_score"]) for row in issues)
    avg_reframe = mean(float(row["reframing_depth_score"]) for row in reframes)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average CLA depth score: {round(avg_depth, 4)}.",
        f"- Average reframing depth score: {round(avg_reframe, 4)}.",
        f"- Layer code counts: {dict(layer_counts)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats Causal Layered Analysis as structured layered interpretation. It scores issue depth, layer-level transformation need, metaphor reframing, power and legitimacy risk, and translation from reframed narratives into scenario and backcasting use.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "cla_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    issues = score_issues()
    layers = score_layers()
    metaphors = score_metaphors()
    reframes = score_reframes()
    power = score_power()
    scenarios = build_scenario_register()

    write_csv(OUTPUTS / "cla_issue_depth_scores.csv", issues)
    write_csv(OUTPUTS / "layer_transformation_priorities.csv", layers)
    write_csv(OUTPUTS / "metaphor_reframing_scores.csv", metaphors)
    write_csv(OUTPUTS / "reframing_depth_scores.csv", reframes)
    write_csv(OUTPUTS / "power_legitimacy_audit_scores.csv", power)
    write_csv(OUTPUTS / "scenario_translation_register.csv", scenarios)

    write_report(config, issues, layers, metaphors, reframes, power, scenarios)

    print(f"CLA workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
