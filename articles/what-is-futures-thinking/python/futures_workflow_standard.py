#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def analyze_strategy_performance() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = read_csv(DATA / "strategy_performance.csv")
    by_strategy: dict[str, list[float]] = defaultdict(list)
    by_future: dict[str, list[tuple[str, float]]] = defaultdict(list)

    for row in rows:
        strategy = row["strategy"]
        future = row["future"]
        performance = float(row["performance"])
        by_strategy[strategy].append(performance)
        by_future[future].append((strategy, performance))

    best_by_future = {
        future: max(items, key=lambda item: item[1])[1]
        for future, items in by_future.items()
    }

    regret_rows: list[dict[str, object]] = []
    regrets_by_strategy: dict[str, list[float]] = defaultdict(list)

    for row in rows:
        strategy = row["strategy"]
        future = row["future"]
        performance = float(row["performance"])
        best = best_by_future[future]
        regret = best - performance
        regrets_by_strategy[strategy].append(regret)
        regret_rows.append({
            "strategy": strategy,
            "future": future,
            "performance": round(performance, 4),
            "best_future_performance": round(best, 4),
            "regret": round(regret, 4),
        })

    summary_rows: list[dict[str, object]] = []

    for strategy, values in by_strategy.items():
        avg = mean(values)
        worst = min(values)
        best = max(values)
        volatility = pstdev(values) if len(values) > 1 else 0.0
        robustness_score = 0.45 * worst + 0.35 * avg - 0.20 * volatility
        summary_rows.append({
            "strategy": strategy,
            "mean_performance": round(avg, 4),
            "worst_case": round(worst, 4),
            "best_case": round(best, 4),
            "volatility": round(volatility, 4),
            "robustness_score": round(robustness_score, 4),
            "mean_regret": round(mean(regrets_by_strategy[strategy]), 4),
            "max_regret": round(max(regrets_by_strategy[strategy]), 4),
        })

    summary_rows.sort(key=lambda row: float(row["robustness_score"]), reverse=True)
    return summary_rows, regret_rows


def analyze_practice_profiles() -> list[dict[str, object]]:
    rows = read_csv(DATA / "practice_profiles.csv")
    weights = {
        "predictive_emphasis": 0.05,
        "uncertainty_plurality": 0.22,
        "assumption_visibility": 0.18,
        "participatory_depth": 0.15,
        "strategic_readiness": 0.25,
        "critical_reflection": 0.15,
    }

    output: list[dict[str, object]] = []
    for row in rows:
        values = {key: float(row[key]) for key in weights}
        weighted_score = sum(values[key] * weight for key, weight in weights.items())
        output.append({
            "practice": row["practice"],
            "anticipatory_capacity_score": round(weighted_score, 4),
            "strongest_dimension": max(values, key=values.get),
            "weakest_dimension": min(values, key=values.get),
        })

    output.sort(key=lambda row: float(row["anticipatory_capacity_score"]), reverse=True)
    return output


def analyze_signals() -> list[dict[str, object]]:
    rows = read_csv(DATA / "signals.csv")
    output: list[dict[str, object]] = []

    for row in rows:
        uncertainty = float(row["uncertainty"])
        impact = float(row["impact"])
        output.append({
            "signal_id": row["signal_id"],
            "domain": row["domain"],
            "signal": row["signal"],
            "uncertainty": uncertainty,
            "impact": impact,
            "watch_score": round(0.5 * uncertainty + 0.5 * impact, 4),
            "monitoring_priority": row["monitoring_priority"],
        })

    output.sort(key=lambda row: float(row["watch_score"]), reverse=True)
    return output


def write_markdown_summary(strategy_summary, practice_scores, signal_scores) -> None:
    lines = ["# Futures Diagnostics Summary", "", "## Strategy Robustness Ranking", ""]
    for index, row in enumerate(strategy_summary, start=1):
        lines.append(
            f"{index}. **{row['strategy']}** — robustness score: "
            f"{row['robustness_score']}; worst case: {row['worst_case']}; "
            f"max regret: {row['max_regret']}."
        )

    lines.extend(["", "## Future-Oriented Practice Scores", ""])
    for index, row in enumerate(practice_scores, start=1):
        lines.append(
            f"{index}. **{row['practice']}** — anticipatory capacity score: "
            f"{row['anticipatory_capacity_score']}; strongest dimension: "
            f"{row['strongest_dimension']}; weakest dimension: {row['weakest_dimension']}."
        )

    lines.extend(["", "## Highest-Priority Signals", ""])
    for index, row in enumerate(signal_scores[:5], start=1):
        lines.append(
            f"{index}. **{row['domain']}** — {row['signal']} "
            f"(watch score: {row['watch_score']})."
        )

    (OUTPUTS / "futures_diagnostics_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    strategy_summary, regret_rows = analyze_strategy_performance()
    practice_scores = analyze_practice_profiles()
    signal_scores = analyze_signals()

    write_csv(OUTPUTS / "strategy_summary_standard.csv", strategy_summary)
    write_csv(OUTPUTS / "strategy_regret_standard.csv", regret_rows)
    write_csv(OUTPUTS / "practice_profile_scores_standard.csv", practice_scores)
    write_csv(OUTPUTS / "signal_watch_scores_standard.csv", signal_scores)
    write_markdown_summary(strategy_summary, practice_scores, signal_scores)

    print("Standard workflow complete.")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
