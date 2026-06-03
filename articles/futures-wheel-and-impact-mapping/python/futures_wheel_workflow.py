#!/usr/bin/env python3
"""
Standard-library workflow for Futures Wheel and Impact Mapping.

Outputs:
- consequence_priority_scores.csv
- edge_influence_scores.csv
- actor_leverage_scores.csv
- impact_pathway_scores.csv
- intervention_usefulness_scores.csv
- monitoring_gap_scores.csv
- distributional_risk_scores.csv
- futures_wheel_impact_report.md
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
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


def priority_class(score: float) -> str:
    if score >= 0.82:
        return "High-priority cascade"
    if score >= 0.74:
        return "Monitor and prepare"
    return "Context-dependent priority"


def score_consequences() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "consequence_nodes.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        likelihood = float(row["likelihood"])
        severity = float(row["severity"])
        uncertainty = float(row["uncertainty"])
        burden = float(row["distributional_burden"])
        actionability = float(row["actionability"])

        priority = (
            0.22 * likelihood
            + 0.26 * severity
            + 0.14 * uncertainty
            + 0.22 * burden
            + 0.16 * actionability
        )

        output.append({
            "node_id": row["node_id"],
            "focal_id": row["focal_id"],
            "parent_node_id": row["parent_node_id"],
            "consequence_order": int(row["consequence_order"]),
            "consequence": row["consequence"],
            "domain": row["domain"],
            "likelihood": likelihood,
            "severity": severity,
            "uncertainty": uncertainty,
            "distributional_burden": burden,
            "actionability": actionability,
            "priority_score": round(priority, 4),
            "priority_class": priority_class(priority),
            "affected_groups": row["affected_groups"],
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["priority_score"]), reverse=True)
    return output


def score_edges() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "consequence_edges.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        influence = float(row["influence_strength"])
        feedback = float(row["feedback_potential"])
        score = influence * (1.0 + feedback)

        output.append({
            "edge_id": row["edge_id"],
            "source_node_id": row["source_node_id"],
            "target_node_id": row["target_node_id"],
            "relationship_type": row["relationship_type"],
            "influence_strength": influence,
            "feedback_potential": feedback,
            "edge_priority": round(score, 4),
            "notes": row["notes"],
        })

    output.sort(key=lambda item: float(item["edge_priority"]), reverse=True)
    return output


def score_actors() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "actors.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        decision = float(row["decision_power"])
        implementation = float(row["implementation_role"])
        affectedness = float(row["affectedness"])
        knowledge = float(row["knowledge_value"])

        leverage = (
            0.30 * decision
            + 0.25 * implementation
            + 0.20 * affectedness
            + 0.25 * knowledge
        )

        output.append({
            "actor_id": row["actor_id"],
            "actor_name": row["actor_name"],
            "actor_type": row["actor_type"],
            "domain": row["domain"],
            "decision_power": decision,
            "implementation_role": implementation,
            "affectedness": affectedness,
            "knowledge_value": knowledge,
            "actor_leverage_score": round(leverage, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["actor_leverage_score"]), reverse=True)
    return output


def score_impact_pathways() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "impact_pathways.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        trace = float(row["traceability_score"])
        equity = float(row["equity_relevance"])
        feasibility = float(row["implementation_feasibility"])
        score = 0.40 * trace + 0.30 * equity + 0.30 * feasibility

        output.append({
            "pathway_id": row["pathway_id"],
            "focal_id": row["focal_id"],
            "goal": row["goal"],
            "actor_id": row["actor_id"],
            "desired_impact": row["desired_impact"],
            "deliverable": row["deliverable"],
            "indicator": row["indicator"],
            "traceability_score": trace,
            "equity_relevance": equity,
            "implementation_feasibility": feasibility,
            "impact_pathway_score": round(score, 4),
        })

    output.sort(key=lambda item: float(item["impact_pathway_score"]), reverse=True)
    return output


def score_interventions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "interventions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        cost = float(row["cost_complexity"])
        time_to_impact = float(row["time_to_impact"])
        dependency = float(row["institutional_dependency"])
        risk_reduction = float(row["risk_reduction"])
        usefulness = (
            0.40 * risk_reduction
            + 0.25 * time_to_impact
            + 0.20 * (1.0 - cost)
            + 0.15 * (1.0 - dependency)
        )

        output.append({
            "intervention_id": row["intervention_id"],
            "pathway_id": row["pathway_id"],
            "intervention_type": row["intervention_type"],
            "intervention_name": row["intervention_name"],
            "cost_complexity": cost,
            "time_to_impact": time_to_impact,
            "institutional_dependency": dependency,
            "risk_reduction": risk_reduction,
            "intervention_usefulness_score": round(usefulness, 4),
            "notes": row["notes"],
        })

    output.sort(key=lambda item: float(item["intervention_usefulness_score"]), reverse=True)
    return output


def score_monitoring() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "monitoring_indicators.csv")
    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }
    output: list[dict[str, Any]] = []

    for row in rows:
        baseline = float(row["baseline"])
        target = float(row["target"])
        gap = abs(target - baseline)
        review = frequency_weight.get(row["review_frequency"], 0.50)
        urgency = 0.70 * gap + 0.30 * review

        output.append({
            "indicator_id": row["indicator_id"],
            "pathway_id": row["pathway_id"],
            "indicator_name": row["indicator_name"],
            "baseline": baseline,
            "target": target,
            "monitoring_gap": round(gap, 4),
            "review_frequency": row["review_frequency"],
            "review_weight": review,
            "monitoring_priority": round(urgency, 4),
            "decision_trigger": row["decision_trigger"],
        })

    output.sort(key=lambda item: float(item["monitoring_priority"]), reverse=True)
    return output


def score_distributional_risk() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "distributional_audit.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        exposure = float(row["exposure"])
        capacity = float(row["adaptive_capacity"])
        voice = float(row["decision_voice"])
        burden = float(row["burden_shift_risk"])

        risk = (
            0.35 * exposure
            + 0.30 * (1.0 - capacity)
            + 0.20 * (1.0 - voice)
            + 0.15 * burden
        )

        output.append({
            "audit_id": row["audit_id"],
            "node_id": row["node_id"],
            "affected_group": row["affected_group"],
            "exposure": exposure,
            "adaptive_capacity": capacity,
            "decision_voice": voice,
            "burden_shift_risk": burden,
            "distributional_risk_score": round(risk, 4),
            "priority_note": row["priority_note"],
        })

    output.sort(key=lambda item: float(item["distributional_risk_score"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    consequences: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    actors: list[dict[str, Any]],
    pathways: list[dict[str, Any]],
    interventions: list[dict[str, Any]],
    monitoring: list[dict[str, Any]],
    distribution: list[dict[str, Any]],
) -> None:
    order_counts = Counter(row["consequence_order"] for row in consequences)
    domain_scores: dict[str, list[float]] = defaultdict(list)

    for row in consequences:
        if row["consequence_order"] > 0:
            domain_scores[row["domain"]].append(float(row["priority_score"]))

    domain_summary = sorted(
        ((domain, mean(scores)) for domain, scores in domain_scores.items()),
        key=lambda item: item[1],
        reverse=True,
    )

    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Highest-Priority Consequence Cascades",
        "",
    ]

    for row in consequences[:10]:
        if row["consequence_order"] == 0:
            continue
        lines.append(
            f"- **{row['consequence']}** ({row['domain']}, order {row['consequence_order']}): "
            f"priority {row['priority_score']}; class: {row['priority_class']}."
        )

    lines.extend(["", "## Strongest Consequence Edges", ""])
    for row in edges[:8]:
        lines.append(
            f"- **{row['source_node_id']} → {row['target_node_id']}** ({row['relationship_type']}): "
            f"edge priority {row['edge_priority']}."
        )

    lines.extend(["", "## Actor Leverage Scores", ""])
    for row in actors[:8]:
        lines.append(
            f"- **{row['actor_name']}** ({row['actor_type']}): leverage {row['actor_leverage_score']}."
        )

    lines.extend(["", "## Impact Pathway Scores", ""])
    for row in pathways[:8]:
        lines.append(
            f"- **{row['actor_id']} / {row['deliverable']}**: impact pathway score {row['impact_pathway_score']}."
        )

    lines.extend(["", "## Intervention Usefulness Scores", ""])
    for row in interventions[:8]:
        lines.append(
            f"- **{row['intervention_name']}**: usefulness {row['intervention_usefulness_score']}."
        )

    lines.extend(["", "## Monitoring Priorities", ""])
    for row in monitoring[:8]:
        lines.append(
            f"- **{row['indicator_name']}**: monitoring gap {row['monitoring_gap']}; "
            f"priority {row['monitoring_priority']}."
        )

    lines.extend(["", "## Distributional Risk Audit", ""])
    for row in distribution[:8]:
        lines.append(
            f"- **{row['affected_group']} / {row['node_id']}**: distributional risk {row['distributional_risk_score']}."
        )

    lines.extend(["", "## Domain Summary", ""])
    for domain, score in domain_summary:
        lines.append(f"- **{domain}**: average consequence priority {round(score, 4)}.")

    avg_consequence = mean(float(row["priority_score"]) for row in consequences if row["consequence_order"] > 0)
    avg_impact = mean(float(row["impact_pathway_score"]) for row in pathways)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Consequence order counts: {dict(order_counts)}.",
        f"- Average consequence priority score: {round(avg_consequence, 4)}.",
        f"- Average impact pathway score: {round(avg_impact, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats Futures Wheel and Impact Mapping as a consequence-to-impact system. It maps cascading consequences, scores consequence priority, evaluates actor leverage, links goals to actor-specific impacts and deliverables, audits distributional risk, and ties monitoring indicators to decision triggers.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "futures_wheel_impact_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    consequences = score_consequences()
    edges = score_edges()
    actors = score_actors()
    pathways = score_impact_pathways()
    interventions = score_interventions()
    monitoring = score_monitoring()
    distribution = score_distributional_risk()

    write_csv(OUTPUTS / "consequence_priority_scores.csv", consequences)
    write_csv(OUTPUTS / "edge_influence_scores.csv", edges)
    write_csv(OUTPUTS / "actor_leverage_scores.csv", actors)
    write_csv(OUTPUTS / "impact_pathway_scores.csv", pathways)
    write_csv(OUTPUTS / "intervention_usefulness_scores.csv", interventions)
    write_csv(OUTPUTS / "monitoring_gap_scores.csv", monitoring)
    write_csv(OUTPUTS / "distributional_risk_scores.csv", distribution)

    write_report(config, consequences, edges, actors, pathways, interventions, monitoring, distribution)

    print(f"Futures Wheel workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
