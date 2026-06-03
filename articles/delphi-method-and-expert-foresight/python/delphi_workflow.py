#!/usr/bin/env python3
"""
Standard-library workflow for Delphi Method and Expert Foresight.

Outputs:
- panel_diversity_audit.csv
- delphi_round_metrics.csv
- expert_judgment_profiles.csv
- issue_priority_scores.csv
- rationale_theme_summary.csv
- foresight_translation_register.csv
- delphi_report.md
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median, pstdev
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


def quantile(values: list[float], q: float) -> float:
    values_sorted = sorted(values)
    if not values_sorted:
        return 0.0
    position = (len(values_sorted) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(values_sorted) - 1)
    fraction = position - lower
    return values_sorted[lower] * (1 - fraction) + values_sorted[upper] * fraction


def audit_panel() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "expert_panel.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        formal = 1.0 if bool_text(row["formal_expert"]) else 0.0
        practice = 1.0 if bool_text(row["practice_expert"]) else 0.0
        community = 1.0 if bool_text(row["community_expert"]) else 0.0
        ethics = 1.0 if bool_text(row["ethics_expert"]) else 0.0
        panel_weight = float(row["panel_weight"])
        blind_spot = float(row["blind_spot_risk"])

        diversity_score = mean([formal, practice, community, ethics]) * panel_weight * (1.0 - blind_spot)

        output.append({
            "expert_id": row["expert_id"],
            "expertise_domain": row["expertise_domain"],
            "sector": row["sector"],
            "formal_expert": row["formal_expert"],
            "practice_expert": row["practice_expert"],
            "community_expert": row["community_expert"],
            "ethics_expert": row["ethics_expert"],
            "years_experience": int(row["years_experience"]),
            "panel_weight": panel_weight,
            "blind_spot_risk": blind_spot,
            "panel_diversity_score": round(diversity_score, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["panel_diversity_score"]), reverse=True)
    return output


def score_expert_judgments() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "delphi_responses.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        likelihood = float(row["likelihood"])
        impact = float(row["impact"])
        urgency = float(row["urgency"])
        feasibility = float(row["feasibility"])
        low = float(row["low_estimate"])
        high = float(row["high_estimate"])

        profile = (
            0.25 * likelihood
            + 0.35 * impact
            + 0.25 * urgency
            + 0.15 * feasibility
        )

        output.append({
            "response_id": row["response_id"],
            "expert_id": row["expert_id"],
            "round": int(row["round"]),
            "issue_id": row["issue_id"],
            "issue_title": row["issue_title"],
            "likelihood": likelihood,
            "impact": impact,
            "urgency": urgency,
            "feasibility": feasibility,
            "confidence": float(row["confidence"]),
            "uncertainty_range": round(high - low, 4),
            "judgment_profile": round(profile, 4),
            "rationale_code": row["rationale_code"],
        })

    output.sort(key=lambda item: (item["round"], item["expert_id"]))
    return output


def round_metrics() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "delphi_responses.csv")
    grouped: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        grouped[(row["issue_id"], int(row["round"]))].append(row)

    output: list[dict[str, Any]] = []
    previous_medians: dict[str, float] = {}

    for (issue_id, round_number), group_rows in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        profiles = []
        likelihood_values = []
        impact_values = []
        urgency_values = []
        uncertainty_values = []

        for row in group_rows:
            likelihood = float(row["likelihood"])
            impact = float(row["impact"])
            urgency = float(row["urgency"])
            feasibility = float(row["feasibility"])
            high = float(row["high_estimate"])
            low = float(row["low_estimate"])

            profile = 0.25 * likelihood + 0.35 * impact + 0.25 * urgency + 0.15 * feasibility
            profiles.append(profile)
            likelihood_values.append(likelihood)
            impact_values.append(impact)
            urgency_values.append(urgency)
            uncertainty_values.append(high - low)

        med = median(profiles)
        q1 = quantile(profiles, 0.25)
        q3 = quantile(profiles, 0.75)
        dispersion = q3 - q1
        previous = previous_medians.get(issue_id)
        stability_shift = None if previous is None else abs(med - previous)
        previous_medians[issue_id] = med

        output.append({
            "issue_id": issue_id,
            "round": round_number,
            "respondent_count": len(group_rows),
            "median_judgment_profile": round(med, 4),
            "mean_judgment_profile": round(mean(profiles), 4),
            "std_judgment_profile": round(pstdev(profiles), 4),
            "lower_quartile": round(q1, 4),
            "upper_quartile": round(q3, 4),
            "interquartile_range": round(dispersion, 4),
            "median_likelihood": round(median(likelihood_values), 4),
            "median_impact": round(median(impact_values), 4),
            "median_urgency": round(median(urgency_values), 4),
            "mean_uncertainty_range": round(mean(uncertainty_values), 4),
            "stability_shift": "" if stability_shift is None else round(stability_shift, 4),
        })

    return output


def score_issue_priorities() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "issue_priorities.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        likelihood = float(row["likelihood"])
        impact = float(row["impact"])
        uncertainty = float(row["uncertainty"])
        urgency = float(row["urgency"])
        governance = float(row["governance_relevance"])
        monitoring = float(row["monitoring_need"])

        priority = (
            0.25 * likelihood
            + 0.30 * impact
            + 0.20 * urgency
            + 0.15 * governance
            + 0.10 * monitoring
        )

        uncertainty_adjusted_priority = priority * (1.0 + 0.20 * uncertainty)

        output.append({
            "issue_id": row["issue_id"],
            "issue_title": row["issue_title"],
            "domain": row["domain"],
            "likelihood": likelihood,
            "impact": impact,
            "uncertainty": uncertainty,
            "urgency": urgency,
            "governance_relevance": governance,
            "monitoring_need": monitoring,
            "priority_score": round(priority, 4),
            "uncertainty_adjusted_priority": round(uncertainty_adjusted_priority, 4),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["uncertainty_adjusted_priority"]), reverse=True)
    return output


def summarize_rationales() -> list[dict[str, Any]]:
    responses = read_csv(DATA / "delphi_responses.csv")
    rationales = {row["rationale_code"]: row for row in read_csv(DATA / "qualitative_rationales.csv")}
    counts = Counter(row["rationale_code"] for row in responses)

    output: list[dict[str, Any]] = []
    for code, count in counts.most_common():
        row = rationales[code]
        output.append({
            "rationale_code": code,
            "theme": row["theme"],
            "response_count": count,
            "interpretive_summary": row["interpretive_summary"],
            "decision_implication": row["decision_implication"],
        })

    return output


def build_translation_register() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "foresight_outputs.csv")
    output: list[dict[str, Any]] = []

    frequency_weight = {
        "monthly": 1.00,
        "quarterly": 0.88,
        "semiannual": 0.68,
        "annual": 0.48,
    }

    for row in rows:
        review_weight = frequency_weight.get(row["review_frequency"], 0.50)
        output.append({
            "output_id": row["output_id"],
            "issue_id": row["issue_id"],
            "output_type": row["output_type"],
            "output_title": row["output_title"],
            "decision_use": row["decision_use"],
            "monitoring_indicator": row["monitoring_indicator"],
            "review_frequency": row["review_frequency"],
            "review_weight": review_weight,
        })

    return output


def write_report(
    config: dict[str, Any],
    panel: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    judgments: list[dict[str, Any]],
    priorities: list[dict[str, Any]],
    rationales: list[dict[str, Any]],
    translations: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Panel Diversity Audit",
        "",
    ]

    for row in panel[:8]:
        lines.append(
            f"- **{row['expert_id']}** ({row['expertise_domain']}): diversity score {row['panel_diversity_score']}; "
            f"blind-spot risk {row['blind_spot_risk']}."
        )

    lines.extend(["", "## Delphi Round Metrics", ""])
    for row in metrics:
        shift = row["stability_shift"] if row["stability_shift"] != "" else "baseline"
        lines.append(
            f"- **Round {row['round']} / {row['issue_id']}**: median profile {row['median_judgment_profile']}; "
            f"IQR {row['interquartile_range']}; stability shift {shift}."
        )

    lines.extend(["", "## Highest Issue Priorities", ""])
    for row in priorities[:6]:
        lines.append(
            f"- **{row['issue_title']}**: priority {row['priority_score']}; "
            f"uncertainty-adjusted {row['uncertainty_adjusted_priority']}."
        )

    lines.extend(["", "## Dominant Qualitative Rationales", ""])
    for row in rationales[:8]:
        lines.append(
            f"- **{row['theme']}** ({row['response_count']} responses): {row['decision_implication']}"
        )

    lines.extend(["", "## Foresight Translation Register", ""])
    for row in translations:
        lines.append(
            f"- **{row['output_title']}** ({row['output_type']}): {row['decision_use']}; "
            f"monitor: {row['monitoring_indicator']}."
        )

    final_round = [row for row in metrics if row["round"] == max(int(item["round"]) for item in metrics)]
    avg_final_iqr = mean(float(row["interquartile_range"]) for row in final_round)
    avg_priority = mean(float(row["priority_score"]) for row in priorities)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Average final-round interquartile range: {round(avg_final_iqr, 4)}.",
        f"- Average issue priority score: {round(avg_priority, 4)}.",
        f"- Expert response records analyzed: {len(judgments)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats Delphi as structured expert judgment rather than a consensus machine. It tracks panel composition, judgment profiles, dispersion, stability, uncertainty ranges, qualitative rationales, issue priorities, and translation of expert foresight into policy, scenario, research, and monitoring outputs.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "delphi_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    panel = audit_panel()
    judgments = score_expert_judgments()
    metrics = round_metrics()
    priorities = score_issue_priorities()
    rationales = summarize_rationales()
    translations = build_translation_register()

    write_csv(OUTPUTS / "panel_diversity_audit.csv", panel)
    write_csv(OUTPUTS / "expert_judgment_profiles.csv", judgments)
    write_csv(OUTPUTS / "delphi_round_metrics.csv", metrics)
    write_csv(OUTPUTS / "issue_priority_scores.csv", priorities)
    write_csv(OUTPUTS / "rationale_theme_summary.csv", rationales)
    write_csv(OUTPUTS / "foresight_translation_register.csv", translations)

    write_report(config, panel, metrics, judgments, priorities, rationales, translations)

    print(f"Delphi workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
