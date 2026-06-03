#!/usr/bin/env python3
"""
Standard-library workflow for Backcasting and Strategic Planning.

Outputs:
- strategic_gap_scores.csv
- pathway_viability_scores.csv
- milestone_risk_priorities.csv
- constraint_priorities.csv
- scenario_stress_burdens.csv
- monitoring_trigger_register.csv
- backcasting_report.md
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

DIMENSIONS = [
    "decarbonization",
    "equity",
    "resilience",
    "institutional_capacity",
    "public_legitimacy",
    "ecological_integrity",
]


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


def score_strategic_gaps() -> list[dict[str, Any]]:
    futures = read_csv(DATA / "desired_futures.csv")
    baselines = {row["future_id"]: row for row in read_csv(DATA / "current_baselines.csv")}
    output: list[dict[str, Any]] = []

    for future in futures:
        baseline = baselines[future["future_id"]]
        gaps: dict[str, float] = {}
        for dimension in DIMENSIONS:
            target = float(future[dimension])
            current = float(baseline[f"current_{dimension}"])
            gaps[f"{dimension}_gap"] = round(target - current, 4)

        gap_score = mean(gaps.values())

        output.append({
            "future_id": future["future_id"],
            "future_name": future["future_name"],
            "domain": future["domain"],
            "target_year": future["target_year"],
            **gaps,
            "strategic_gap_score": round(gap_score, 4),
            "baseline_note": baseline["baseline_note"],
        })

    output.sort(key=lambda row: float(row["strategic_gap_score"]), reverse=True)
    return output


def classify_pathway(score: float) -> str:
    if score >= 0.55:
        return "Strong adaptive pathway"
    if score >= 0.45:
        return "Potential pathway with constraints"
    return "Fragile or high-risk pathway"


def score_pathways() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "pathways.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        feasibility = float(row["feasibility"])
        institutional_difficulty = float(row["institutional_difficulty"])
        transition_speed = float(row["transition_speed"])
        alignment = float(row["stakeholder_alignment"])
        resilience = float(row["resilience"])
        justice = float(row["justice"])
        adaptability = float(row["adaptability"])
        friction = float(row["political_friction"])

        viability = (
            0.18 * feasibility
            - 0.16 * institutional_difficulty
            + 0.14 * transition_speed
            + 0.18 * alignment
            + 0.16 * resilience
            + 0.12 * justice
            + 0.14 * adaptability
            - 0.12 * friction
        )

        output.append({
            "pathway_id": row["pathway_id"],
            "future_id": row["future_id"],
            "pathway_name": row["pathway_name"],
            "feasibility": feasibility,
            "institutional_difficulty": institutional_difficulty,
            "transition_speed": transition_speed,
            "stakeholder_alignment": alignment,
            "resilience": resilience,
            "justice": justice,
            "adaptability": adaptability,
            "political_friction": friction,
            "pathway_viability_score": round(viability, 4),
            "pathway_class": classify_pathway(viability),
            "description": row["description"],
        })

    output.sort(key=lambda row: float(row["pathway_viability_score"]), reverse=True)
    return output


def score_milestones() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "milestones.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        completion = float(row["completion_score"])
        risk = float(row["risk_score"])
        priority = risk * (1.0 - completion)

        output.append({
            "milestone_id": row["milestone_id"],
            "pathway_id": row["pathway_id"],
            "phase_year": row["phase_year"],
            "milestone": row["milestone"],
            "dependency": row["dependency"],
            "completion_score": completion,
            "risk_score": risk,
            "milestone_risk_priority": round(priority, 4),
            "owner_role": row["owner_role"],
        })

    output.sort(key=lambda row: float(row["milestone_risk_priority"]), reverse=True)
    return output


def score_constraints() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "constraints.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        impact = float(row["impact"])
        severity = float(row["severity"])
        reversibility = float(row["reversibility"])
        priority = impact * severity * (1.0 + (1.0 - reversibility))

        output.append({
            "constraint_id": row["constraint_id"],
            "pathway_id": row["pathway_id"],
            "constraint_type": row["constraint_type"],
            "constraint": row["constraint"],
            "impact": impact,
            "severity": severity,
            "reversibility": reversibility,
            "constraint_priority": round(priority, 4),
            "mitigation": row["mitigation"],
        })

    output.sort(key=lambda row: float(row["constraint_priority"]), reverse=True)
    return output


def score_stress_tests() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "scenario_stress_tests.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        climate = float(row["climate_stress"])
        politics = float(row["political_resistance"])
        funding = float(row["funding_constraint"])
        technology = float(row["technology_uncertainty"])
        trust = float(row["public_trust"])

        burden = (
            0.22 * climate
            + 0.20 * politics
            + 0.20 * funding
            + 0.18 * technology
            + 0.20 * (1.0 - trust)
        )

        output.append({
            "stress_id": row["stress_id"],
            "pathway_id": row["pathway_id"],
            "scenario_name": row["scenario_name"],
            "climate_stress": climate,
            "political_resistance": politics,
            "funding_constraint": funding,
            "technology_uncertainty": technology,
            "public_trust": trust,
            "stress_burden_score": round(burden, 4),
            "stress_note": row["stress_note"],
        })

    output.sort(key=lambda row: float(row["stress_burden_score"]), reverse=True)
    return output


def build_trigger_register() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "monitoring_triggers.csv")
    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }
    output: list[dict[str, Any]] = []

    for row in rows:
        threshold = float(row["threshold"])
        frequency = frequency_weight.get(row["review_frequency"], 0.50)
        trigger_priority = 0.60 * threshold + 0.40 * frequency

        output.append({
            "trigger_id": row["trigger_id"],
            "pathway_id": row["pathway_id"],
            "indicator": row["indicator"],
            "threshold": threshold,
            "review_frequency": row["review_frequency"],
            "trigger_priority": round(trigger_priority, 4),
            "trigger_action": row["trigger_action"],
        })

    output.sort(key=lambda row: float(row["trigger_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    gaps: list[dict[str, Any]],
    pathways: list[dict[str, Any]],
    milestones: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
    stress_tests: list[dict[str, Any]],
    triggers: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Strategic Gap Scores",
        "",
    ]

    for row in gaps:
        lines.append(
            f"- **{row['future_name']}** ({row['target_year']}): strategic gap score {row['strategic_gap_score']}."
        )

    lines.extend(["", "## Pathway Viability Ranking", ""])
    for index, row in enumerate(pathways, start=1):
        lines.append(
            f"{index}. **{row['pathway_name']}** — viability {row['pathway_viability_score']}; "
            f"class: {row['pathway_class']}."
        )

    lines.extend(["", "## Highest-Priority Milestone Risks", ""])
    for row in milestones[:7]:
        lines.append(
            f"- **{row['phase_year']} / {row['pathway_id']}**: {row['milestone']} "
            f"— risk priority {row['milestone_risk_priority']}."
        )

    lines.extend(["", "## Highest-Priority Constraints", ""])
    for row in constraints[:7]:
        lines.append(
            f"- **{row['constraint_type']}** on {row['pathway_id']}: {row['constraint']} "
            f"— priority {row['constraint_priority']}."
        )

    lines.extend(["", "## Scenario Stress Burdens", ""])
    for row in stress_tests[:8]:
        lines.append(
            f"- **{row['scenario_name']}** on {row['pathway_id']}: stress burden {row['stress_burden_score']}."
        )

    lines.extend(["", "## Monitoring Triggers", ""])
    for row in triggers[:8]:
        lines.append(
            f"- **{row['indicator']}** on {row['pathway_id']}: threshold {row['threshold']}; "
            f"action: {row['trigger_action']}"
        )

    avg_gap = mean(float(row["strategic_gap_score"]) for row in gaps)
    avg_viability = mean(float(row["pathway_viability_score"]) for row in pathways)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average strategic gap score: {round(avg_gap, 4)}.",
        f"- Average pathway viability score: {round(avg_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats backcasting as adaptive pathway design. It starts from desired futures, compares current baselines, scores strategic gaps, evaluates pathway viability, identifies milestone and constraint risks, stress-tests pathways, and defines monitoring triggers for revision.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "backcasting_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    gaps = score_strategic_gaps()
    pathways = score_pathways()
    milestones = score_milestones()
    constraints = score_constraints()
    stress_tests = score_stress_tests()
    triggers = build_trigger_register()

    write_csv(OUTPUTS / "strategic_gap_scores.csv", gaps)
    write_csv(OUTPUTS / "pathway_viability_scores.csv", pathways)
    write_csv(OUTPUTS / "milestone_risk_priorities.csv", milestones)
    write_csv(OUTPUTS / "constraint_priorities.csv", constraints)
    write_csv(OUTPUTS / "scenario_stress_burdens.csv", stress_tests)
    write_csv(OUTPUTS / "monitoring_trigger_register.csv", triggers)

    write_report(config, gaps, pathways, milestones, constraints, stress_tests, triggers)

    print(f"Backcasting workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
