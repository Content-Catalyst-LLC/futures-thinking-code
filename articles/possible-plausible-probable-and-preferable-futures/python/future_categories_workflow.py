#!/usr/bin/env python3
"""
Standard-library workflow for Possible, Plausible, Probable, and Preferable Futures.

Outputs:
- future_category_classification.csv
- strategy_category_fit.csv
- category_shift_monitor.csv
- driver_priority_scores.csv
- future_categories_report.md
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


def classify_future(row: dict[str, Any]) -> str:
    plausible = row["plausibility_score"] >= 0.65
    probable = row["probability_score"] >= 0.65
    preferable = row["preference_score"] >= 0.65

    if plausible and probable and preferable:
        return "Probable and Preferable"
    if plausible and probable and not preferable:
        return "Probable but Not Preferable"
    if plausible and not probable and preferable:
        return "Preferable but Not Yet Probable"
    if preferable and not plausible:
        return "Preferable but Needs Pathway"
    if plausible and not probable:
        return "Plausible Strategic Scenario"
    return "Possible or Emerging"


def score_candidate_futures() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "candidate_futures.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        driver_support = float(row["driver_support"])
        pathway_coherence = float(row["pathway_coherence"])
        constraint_fit = float(row["constraint_fit"])
        current_trend_strength = float(row["current_trend_strength"])
        justice = float(row["justice_value"])
        sustainability = float(row["sustainability_value"])
        resilience = float(row["resilience_value"])
        legitimacy = float(row["legitimacy_value"])
        participation_need = float(row["participation_need"])

        plausibility = 0.40 * driver_support + 0.35 * pathway_coherence + 0.25 * constraint_fit
        probability = 0.70 * current_trend_strength + 0.30 * driver_support
        preference = 0.30 * justice + 0.25 * sustainability + 0.25 * resilience + 0.20 * legitimacy
        strategic_priority = 0.35 * plausibility + 0.25 * probability + 0.40 * preference
        participation_risk = max(0.0, participation_need - legitimacy)

        scored = {
            "future_id": row["future_id"],
            "future": row["future"],
            "plausibility_score": round(plausibility, 4),
            "probability_score": round(probability, 4),
            "preference_score": round(preference, 4),
            "strategic_priority": round(strategic_priority, 4),
            "participation_need": participation_need,
            "participation_risk": round(participation_risk, 4),
        }
        scored["classification"] = classify_future(scored)
        output.append(scored)

    output.sort(key=lambda row: float(row["strategic_priority"]), reverse=True)
    return output


def score_strategies() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "strategies.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        probable_fit = float(row["probable_fit"])
        plausible_fit = float(row["plausible_fit"])
        preferable_fit = float(row["preferable_fit"])
        adaptive_capacity = float(row["adaptive_capacity"])
        difficulty = float(row["implementation_difficulty"])
        equity = float(row["equity_sensitivity"])

        score = (
            0.20 * probable_fit
            + 0.30 * plausible_fit
            + 0.30 * preferable_fit
            + 0.20 * adaptive_capacity
            - 0.05 * difficulty
            + 0.05 * equity
        )

        output.append({
            "strategy_id": row["strategy_id"],
            "strategy": row["strategy"],
            "probable_fit": probable_fit,
            "plausible_fit": plausible_fit,
            "preferable_fit": preferable_fit,
            "adaptive_capacity": adaptive_capacity,
            "implementation_difficulty": difficulty,
            "equity_sensitivity": equity,
            "category_fit_score": round(score, 4),
        })

    output.sort(key=lambda row: float(row["category_fit_score"]), reverse=True)
    return output


def monitor_category_shifts() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "category_shifts.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        strength = float(row["shift_strength"])
        output.append({
            "shift_id": row["shift_id"],
            "future_id": row["future_id"],
            "previous_category": row["previous_category"],
            "current_category": row["current_category"],
            "signal": row["signal"],
            "shift_strength": strength,
            "monitoring_priority": row["monitoring_priority"],
            "review_priority_score": round(strength * (1.2 if row["monitoring_priority"] == "high" else 1.0), 4),
        })

    output.sort(key=lambda row: float(row["review_priority_score"]), reverse=True)
    return output


def score_drivers() -> list[dict[str, Any]]:
    rows = read_csv(DATA / "driver_notes.csv")
    output: list[dict[str, Any]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        velocity = float(row["velocity"])
        priority = uncertainty * impact * velocity
        output.append({
            "driver_id": row["driver_id"],
            "domain": row["domain"],
            "driver": row["driver"],
            "uncertainty": uncertainty,
            "impact": impact,
            "velocity": velocity,
            "driver_priority": round(priority, 4),
        })

    output.sort(key=lambda row: float(row["driver_priority"]), reverse=True)
    return output


def write_report(
    config: dict[str, Any],
    futures: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
    shifts: list[dict[str, Any]],
    drivers: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Future Category Classification",
        "",
    ]

    for row in futures:
        lines.append(
            f"- **{row['future']}** — {row['classification']} "
            f"(plausibility {row['plausibility_score']}, probability {row['probability_score']}, "
            f"preference {row['preference_score']}, priority {row['strategic_priority']})."
        )

    lines.extend(["", "## Strategy Category Fit", ""])
    for index, row in enumerate(strategies, start=1):
        lines.append(
            f"{index}. **{row['strategy']}** — fit score {row['category_fit_score']}."
        )

    lines.extend(["", "## Category Shift Monitor", ""])
    for row in shifts[:6]:
        lines.append(
            f"- **{row['future_id']}** shifted from {row['previous_category']} to "
            f"{row['current_category']} — review priority {row['review_priority_score']}."
        )

    lines.extend(["", "## High-Priority Drivers", ""])
    for row in drivers[:5]:
        lines.append(
            f"- **{row['driver']}** ({row['domain']}) — driver priority {row['driver_priority']}."
        )

    probable_not_preferable = [r for r in futures if r["classification"] == "Probable but Not Preferable"]
    preferable_not_probable = [r for r in futures if r["classification"] in ("Preferable but Not Yet Probable", "Preferable but Needs Pathway")]

    lines.extend(["", "## Diagnostic Flags", ""])
    if probable_not_preferable:
        lines.append("### Probable but Not Preferable")
        for row in probable_not_preferable:
            lines.append(f"- {row['future']}")
    if preferable_not_probable:
        lines.append("### Preferable but Not Yet Probable or Needs Pathway")
        for row in preferable_not_probable:
            lines.append(f"- {row['future']}")

    lines.extend([
        "",
        "## Interpretation",
        "",
        "This workflow clarifies future-category logic. Possible futures expand imagination; plausible futures require credible pathways; probable futures depend on evidence and assumptions; preferable futures require explicit values and participation. The model helps identify where strategy must prevent, prepare, backcast, or monitor.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "future_categories_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    futures = score_candidate_futures()
    strategies = score_strategies()
    shifts = monitor_category_shifts()
    drivers = score_drivers()

    write_csv(OUTPUTS / "future_category_classification.csv", futures)
    write_csv(OUTPUTS / "strategy_category_fit.csv", strategies)
    write_csv(OUTPUTS / "category_shift_monitor.csv", shifts)
    write_csv(OUTPUTS / "driver_priority_scores.csv", drivers)

    write_report(config, futures, strategies, shifts, drivers)

    print(f"Future category workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
