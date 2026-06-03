#!/usr/bin/env python3
"""
Standard-library workflow for The History of Futures Thinking.

Outputs:
- historical_tradition_scores.csv
- institutional_development_scores.csv
- method_genealogy_scores.csv
- historical_risk_priorities.csv
- timeline_summary.csv
- history_futures_report.md
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


def score_traditions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "historical_traditions.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        methodological = float(row["methodological_discipline"])
        institutional_power = float(row["institutional_power"])
        participation = float(row["participatory_depth"])
        ethics = float(row["ethical_reflection"])
        systems = float(row["systems_orientation"])

        reflective_score = 0.25 * methodological + 0.25 * participation + 0.25 * ethics + 0.25 * systems
        power_risk = institutional_power * (1.0 - participation) * (1.0 - ethics)

        output.append({
            "tradition_id": row["tradition_id"],
            "tradition": row["tradition"],
            "period": row["period"],
            "methodological_discipline": methodological,
            "institutional_power": institutional_power,
            "participatory_depth": participation,
            "ethical_reflection": ethics,
            "systems_orientation": systems,
            "reflective_foresight_score": round(reflective_score, 4),
            "power_risk_score": round(power_risk, 4),
            "interpretive_note": (
                "High institutional power risk"
                if power_risk >= 0.25
                else "Lower power risk or stronger reflective safeguards"
            ),
            "description": row["description"],
        })

    output.sort(key=lambda item: float(item["reflective_foresight_score"]), reverse=True)
    return output


def score_institutions() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "institutional_developments.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        influence = float(row["method_influence"])
        accountability = float(row["public_accountability"])
        balance = 0.50 * influence + 0.50 * accountability

        output.append({
            "institution_id": row["institution_id"],
            "institution_or_development": row["institution_or_development"],
            "year": int(row["year"]),
            "domain": row["domain"],
            "method_influence": influence,
            "public_accountability": accountability,
            "institutional_balance_score": round(balance, 4),
            "significance": row["significance"],
        })

    output.sort(key=lambda item: (int(item["year"]), item["institution_or_development"]))
    return output


def score_methods() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "method_genealogy.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        participation = float(row["participatory_potential"])
        technocratic = float(row["technocratic_risk"])
        ethics = float(row["ethical_sensitivity"])
        method_risk = technocratic * (1.0 - participation) * (1.0 - ethics)
        reflective_method_score = 0.34 * participation + 0.33 * ethics + 0.33 * (1.0 - technocratic)

        output.append({
            "method_id": row["method_id"],
            "method": row["method"],
            "origin_tradition": row["origin_tradition"],
            "primary_use": row["primary_use"],
            "participatory_potential": participation,
            "technocratic_risk": technocratic,
            "ethical_sensitivity": ethics,
            "method_risk_score": round(method_risk, 4),
            "reflective_method_score": round(reflective_method_score, 4),
        })

    output.sort(key=lambda item: float(item["reflective_method_score"]), reverse=True)
    return output


def score_historical_risks() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "historical_risks.csv")
    priority_weight = {"high": 1.20, "medium": 1.00, "low": 0.80}
    output: list[dict[str, Any]] = []

    for row in rows:
        severity = float(row["severity"])
        weighted = severity * priority_weight.get(row["mitigation_priority"], 1.0)
        output.append({
            "risk_id": row["risk_id"],
            "risk_name": row["risk_name"],
            "description": row["description"],
            "affected_traditions": row["affected_traditions"],
            "severity": severity,
            "mitigation_priority": row["mitigation_priority"],
            "weighted_risk_priority": round(weighted, 4),
        })

    output.sort(key=lambda item: float(item["weighted_risk_priority"]), reverse=True)
    return output


def summarize_timeline() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "timeline_periods.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        output.append({
            "period_id": row["period_id"],
            "period": row["period"],
            "approx_start": int(row["approx_start"]),
            "approx_end": int(row["approx_end"]),
            "dominant_future_logic": row["dominant_future_logic"],
            "key_development": row["key_development"],
            "ethical_risk": row["ethical_risk"],
        })

    output.sort(key=lambda item: int(item["approx_start"]))
    return output


def write_report(
    config: dict[str, Any],
    traditions: list[dict[str, Any]],
    institutions: list[dict[str, Any]],
    methods: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    timeline: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Historical Traditions by Reflective Foresight Score",
        "",
    ]

    for index, row in enumerate(traditions, start=1):
        lines.append(
            f"{index}. **{row['tradition']}** — reflective score {row['reflective_foresight_score']}; "
            f"power risk {row['power_risk_score']}; note: {row['interpretive_note']}."
        )

    lines.extend(["", "## Institutional Developments", ""])
    for row in institutions:
        lines.append(
            f"- **{row['year']} — {row['institution_or_development']}** ({row['domain']}): "
            f"balance score {row['institutional_balance_score']}."
        )

    lines.extend(["", "## Method Genealogy Scores", ""])
    for row in methods:
        lines.append(
            f"- **{row['method']}** from {row['origin_tradition']}: reflective method score "
            f"{row['reflective_method_score']}; risk {row['method_risk_score']}."
        )

    lines.extend(["", "## Highest Historical Risks", ""])
    for row in risks[:6]:
        lines.append(
            f"- **{row['risk_name']}** — weighted priority {row['weighted_risk_priority']}."
        )

    lines.extend(["", "## Timeline Summary", ""])
    for row in timeline:
        lines.append(
            f"- **{row['period']}** ({row['approx_start']}–{row['approx_end']}): "
            f"{row['dominant_future_logic']}."
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "The workflow treats the history of futures thinking as a layered field shaped by methods, institutions, values, and power. It is designed to support historically aware foresight practice rather than reduce history to simple metrics.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "history_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    traditions = score_traditions()
    institutions = score_institutions()
    methods = score_methods()
    risks = score_historical_risks()
    timeline = summarize_timeline()

    write_csv(OUTPUTS / "historical_tradition_scores.csv", traditions)
    write_csv(OUTPUTS / "institutional_development_scores.csv", institutions)
    write_csv(OUTPUTS / "method_genealogy_scores.csv", methods)
    write_csv(OUTPUTS / "historical_risk_priorities.csv", risks)
    write_csv(OUTPUTS / "timeline_summary.csv", timeline)

    write_report(config, traditions, institutions, methods, risks, timeline)

    print(f"History workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
