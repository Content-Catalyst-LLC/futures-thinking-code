#!/usr/bin/env python3
"""
Standard-library workflow for Future Generations and Long-Term Responsibility.

Outputs:
- intergenerational_profile_scores.csv
- future_generation_scenario_scores.csv
- intergenerational_strategy_scores.csv
- long_term_risk_priority_scores.csv
- inheritance_record_scores.csv
- adaptive_long_term_trajectories.csv
- adaptive_long_term_summary.csv
- future_generations_long_term_responsibility_report.md
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


def clamp(value: float, low: float = 0.0, high: float = 1.8) -> float:
    return max(low, min(high, value))


def inherited_burden_score(row: dict[str, str]) -> float:
    return (
        0.18 * float(row["climate_burden"])
        + 0.14 * float(row["debt_without_assets"])
        + 0.16 * float(row["infrastructure_decay"])
        + 0.18 * float(row["ecological_damage"])
        + 0.14 * float(row["technological_lock_in"])
        + 0.10 * (1.0 - float(row["institutional_capacity"]))
        + 0.06 * (1.0 - float(row["adaptive_capacity"]))
        + 0.04 * (1.0 - float(row["future_representation"]))
    )


def future_freedom_score(row: dict[str, str]) -> float:
    return (
        0.20 * float(row["institutional_capacity"])
        + 0.20 * float(row["adaptive_capacity"])
        + 0.16 * float(row["future_representation"])
        + 0.14 * (1.0 - float(row["technological_lock_in"]))
        + 0.12 * (1.0 - float(row["infrastructure_decay"]))
        + 0.10 * (1.0 - float(row["ecological_damage"]))
        + 0.05 * (1.0 - float(row["climate_burden"]))
        + 0.03 * (1.0 - float(row["debt_without_assets"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    records: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing profile {row['profile_id']}.")

    for row in risks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Risk indicator {row['risk_id']} references missing scenario {row['scenario_id']}.")

    for row in records:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Inheritance record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["climate_burden", "debt_without_assets", "infrastructure_decay", "ecological_damage", "institutional_capacity", "technological_lock_in", "adaptive_capacity", "future_representation", "reparative_continuity", "public_legitimacy"]),
        ("scenarios", scenarios, ["short_term_pressure", "climate_delay", "ecological_threshold_risk", "debt_transfer", "maintenance_deferral", "technology_lock_in", "institutional_fragility", "future_representation_gap", "reparative_gap", "adaptive_learning_capacity"]),
        ("strategies", strategies, ["future_generation_review_gain", "climate_budgeting_gain", "maintenance_accounting_gain", "ecological_restoration_gain", "public_investment_gain", "youth_participation_gain", "technology_accountability_gain", "reparative_finance_gain", "adaptive_governance_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "visibility_gap", "distributional_harm", "future_generation_harm", "preparedness"]),
        ("records", records, ["inherited_burden", "future_freedom", "institutional_capacity", "ecological_damage", "adaptive_capacity", "future_representation", "reparative_continuity", "public_legitimacy"]),
        ("pathways", pathways, ["inherited_burden", "future_freedom", "institutional_capacity", "ecological_damage", "adaptive_capacity", "future_representation", "reparative_continuity", "public_legitimacy"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in profiles:
        burden = inherited_burden_score(row)
        freedom = future_freedom_score(row)
        stewardship = (
            0.18 * freedom
            + 0.18 * float(row["institutional_capacity"])
            + 0.18 * float(row["adaptive_capacity"])
            + 0.14 * float(row["future_representation"])
            + 0.12 * float(row["reparative_continuity"])
            + 0.10 * float(row["public_legitimacy"])
            - 0.06 * burden
            - 0.04 * float(row["ecological_damage"])
        )
        gap = max(0.0, burden - freedom)

        if burden >= 0.70:
            profile_class = "High inherited burden"
        elif freedom >= 0.70:
            profile_class = "Stronger long-term stewardship"
        else:
            profile_class = "Mixed intergenerational pathway"

        rows.append({
            "profile_id": row["profile_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "inherited_burden_score": round(burden, 4),
            "future_freedom_score": round(freedom, 4),
            "stewardship_score": round(stewardship, 4),
            "intergenerational_gap_score": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["stewardship_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        long_term_risk = (
            0.13 * float(row["short_term_pressure"])
            + 0.14 * float(row["climate_delay"])
            + 0.14 * float(row["ecological_threshold_risk"])
            + 0.11 * float(row["debt_transfer"])
            + 0.12 * float(row["maintenance_deferral"])
            + 0.11 * float(row["technology_lock_in"])
            + 0.11 * float(row["institutional_fragility"])
            + 0.07 * float(row["future_representation_gap"])
            + 0.05 * float(row["reparative_gap"])
            + 0.02 * (1.0 - float(row["adaptive_learning_capacity"]))
        )

        stewardship_opportunity = (
            0.16 * (1.0 - float(row["short_term_pressure"]))
            + 0.14 * (1.0 - float(row["climate_delay"]))
            + 0.13 * (1.0 - float(row["ecological_threshold_risk"]))
            + 0.12 * (1.0 - float(row["maintenance_deferral"]))
            + 0.11 * (1.0 - float(row["technology_lock_in"]))
            + 0.10 * (1.0 - float(row["institutional_fragility"]))
            + 0.09 * (1.0 - float(row["future_representation_gap"]))
            + 0.08 * (1.0 - float(row["reparative_gap"]))
            + 0.05 * float(row["adaptive_learning_capacity"])
            + 0.02 * (1.0 - float(row["debt_transfer"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "long_term_risk_score": round(long_term_risk, 4),
            "stewardship_opportunity_score": round(stewardship_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["long_term_risk_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        value = (
            0.13 * float(row["future_generation_review_gain"])
            + 0.13 * float(row["climate_budgeting_gain"])
            + 0.12 * float(row["maintenance_accounting_gain"])
            + 0.12 * float(row["ecological_restoration_gain"])
            + 0.11 * float(row["public_investment_gain"])
            + 0.10 * float(row["youth_participation_gain"])
            + 0.10 * float(row["technology_accountability_gain"])
            + 0.09 * float(row["reparative_finance_gain"])
            + 0.07 * float(row["adaptive_governance_gain"])
            + 0.02 * float(row["implementation_capacity"])
            + 0.01 * float(row["public_legitimacy_gain"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.16 * float(row["public_legitimacy_gain"])
            + 0.12 * float(row["future_generation_review_gain"])
            + 0.11 * float(row["adaptive_governance_gain"])
            + 0.10 * float(row["maintenance_accounting_gain"])
            + 0.09 * float(row["climate_budgeting_gain"])
            + 0.08 * float(row["public_investment_gain"])
            + 0.06 * float(row["youth_participation_gain"])
            + 0.04 * float(row["technology_accountability_gain"])
            + 0.04 * float(row["reparative_finance_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "intergenerational_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["intergenerational_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.16 * float(row["severity"])
            + 0.15 * float(row["irreversibility"])
            + 0.10 * float(row["visibility_gap"])
            + 0.18 * float(row["distributional_harm"])
            + 0.18 * float(row["future_generation_harm"])
            + 0.09 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "long_term_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "future_generation_harm": float(row["future_generation_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["long_term_risk_priority_score"]), reverse=True)
    return rows


def score_inheritance_records(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        burden = float(row["inherited_burden"])
        freedom = float(row["future_freedom"])
        institution = float(row["institutional_capacity"])
        ecology = float(row["ecological_damage"])
        adaptive = float(row["adaptive_capacity"])
        representation = float(row["future_representation"])
        repair = float(row["reparative_continuity"])
        legitimacy = float(row["public_legitimacy"])

        stewardship = (
            0.18 * freedom
            + 0.18 * institution
            + 0.18 * adaptive
            + 0.14 * representation
            + 0.12 * repair
            + 0.10 * legitimacy
            - 0.06 * burden
            - 0.04 * ecology
        )

        burden_gap = max(0.0, burden + ecology - freedom - adaptive)

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "inherited_burden_score": round(burden, 4),
            "future_freedom_score": round(freedom, 4),
            "stewardship_capacity_score": round(stewardship, 4),
            "burden_gap_score": round(burden_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["stewardship_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        burden = float(row["inherited_burden"])
        freedom = float(row["future_freedom"])
        institution = float(row["institutional_capacity"])
        ecology = float(row["ecological_damage"])
        adaptive = float(row["adaptive_capacity"])
        representation = float(row["future_representation"])
        repair = float(row["reparative_continuity"])
        legitimacy = float(row["public_legitimacy"])
        horizon = int(row["time_horizon"])

        stewardship = (
            0.18 * freedom
            + 0.18 * institution
            + 0.18 * adaptive
            + 0.14 * representation
            + 0.12 * repair
            + 0.10 * legitimacy
            - 0.06 * burden
            - 0.04 * ecology
        )

        burden_values: list[float] = []
        freedom_values: list[float] = []
        institution_values: list[float] = []
        ecology_values: list[float] = []
        adaptive_values: list[float] = []
        representation_values: list[float] = []
        stewardship_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                short_term_pressure = 0.010 if t % 6 == 0 else 0.0
                climate_shock = 0.014 if t % 10 == 0 else 0.0
                repair_window = 0.012 if t % 12 == 0 else 0.0
                institutional_shock = 0.010 if t % 17 == 0 else 0.0

                burden = clamp(
                    burden
                    + short_term_pressure
                    + 0.010 * ecology
                    + 0.006 * institutional_shock
                    - 0.012 * adaptive
                    - 0.010 * representation
                    - 0.008 * repair,
                    0.0,
                    1.8,
                )

                ecology = clamp(
                    ecology
                    + climate_shock
                    + 0.008 * burden
                    - 0.014 * adaptive
                    - 0.010 * institution
                    - 0.008 * repair,
                    0.0,
                    1.8,
                )

                institution = clamp(
                    institution
                    + 0.010 * representation
                    + 0.008 * adaptive
                    + 0.006 * legitimacy
                    - 0.008 * burden
                    - 0.006 * short_term_pressure
                    - 0.006 * institutional_shock,
                    0.0,
                    1.8,
                )

                adaptive = clamp(
                    adaptive
                    + 0.010 * institution
                    + 0.008 * representation
                    + repair_window
                    - 0.010 * ecology
                    - 0.006 * burden,
                    0.0,
                    1.8,
                )

                representation = clamp(
                    representation
                    + 0.008 * institution
                    + 0.008 * legitimacy
                    + repair_window
                    - 0.006 * short_term_pressure,
                    0.0,
                    1.8,
                )

                repair = clamp(
                    repair
                    + 0.010 * representation
                    + 0.008 * institution
                    + repair_window
                    - 0.006 * burden
                    - 0.004 * ecology,
                    0.0,
                    1.8,
                )

                legitimacy = clamp(
                    legitimacy
                    + 0.008 * representation
                    + 0.007 * institution
                    + 0.006 * repair
                    - 0.006 * burden
                    - 0.005 * ecology,
                    0.0,
                    1.8,
                )

                freedom = clamp(
                    freedom
                    + 0.010 * adaptive
                    + 0.008 * institution
                    + 0.006 * representation
                    + 0.006 * repair
                    - 0.012 * burden
                    - 0.010 * ecology,
                    0.0,
                    1.8,
                )

                stewardship = clamp(
                    0.18 * freedom
                    + 0.18 * institution
                    + 0.18 * adaptive
                    + 0.14 * representation
                    + 0.12 * repair
                    + 0.10 * legitimacy
                    - 0.06 * burden
                    - 0.04 * ecology,
                    -1.0,
                    1.8,
                )

            burden_values.append(burden)
            freedom_values.append(freedom)
            institution_values.append(institution)
            ecology_values.append(ecology)
            adaptive_values.append(adaptive)
            representation_values.append(representation)
            stewardship_values.append(stewardship)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "inherited_burden": round(burden, 4),
                "future_freedom": round(freedom, 4),
                "institutional_capacity": round(institution, 4),
                "ecological_damage": round(ecology, 4),
                "adaptive_capacity": round(adaptive, 4),
                "future_representation": round(representation, 4),
                "reparative_continuity": round(repair, 4),
                "public_legitimacy": round(legitimacy, 4),
                "stewardship_score": round(stewardship, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_inherited_burden": round(burden_values[-1], 4),
            "final_future_freedom": round(freedom_values[-1], 4),
            "final_institutional_capacity": round(institution_values[-1], 4),
            "final_ecological_damage": round(ecology_values[-1], 4),
            "final_adaptive_capacity": round(adaptive_values[-1], 4),
            "final_future_representation": round(representation_values[-1], 4),
            "final_stewardship_score": round(stewardship_values[-1], 4),
            "mean_stewardship_score": round(mean(stewardship_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_stewardship_score"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    record_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Intergenerational Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['scenario_name']}**: inherited burden {row['inherited_burden_score']}; "
            f"future freedom {row['future_freedom_score']}; stewardship {row['stewardship_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Future Generation Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: long-term risk {row['long_term_risk_score']}; "
            f"stewardship opportunity {row['stewardship_opportunity_score']}."
        )

    lines.extend(["", "## Intergenerational Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['intergenerational_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Long-Term Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['long_term_risk_priority_score']}; "
            f"future-generation harm {row['future_generation_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Inheritance Record Scores", ""])
    for row in record_scores:
        lines.append(
            f"- **{row['record_name']}**: burden {row['inherited_burden_score']}; "
            f"future freedom {row['future_freedom_score']}; stewardship capacity {row['stewardship_capacity_score']}."
        )

    lines.extend(["", "## Adaptive Long-Term Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final stewardship {row['final_stewardship_score']}; "
            f"final inherited burden {row['final_inherited_burden']}; final future freedom {row['final_future_freedom']}."
        )

    avg_burden = mean(float(row["inherited_burden_score"]) for row in profile_scores)
    avg_freedom = mean(float(row["future_freedom_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["intergenerational_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Intergenerational profiles: {len(profile_scores)}.",
        f"- Future-generation scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Inheritance records: {len(record_scores)}.",
        f"- Average inherited burden score: {round(avg_burden, 4)}.",
        f"- Average future freedom score: {round(avg_freedom, 4)}.",
        f"- Average strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats future generations and long-term responsibility as systems shaped by inherited burden, future freedom, ecological inheritance, public institutions, technological lock-in, adaptive capacity, representation, repair, and legitimacy.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "future_generations_long_term_responsibility_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "intergenerational_responsibility_profiles.csv")
    scenarios_raw = read_csv(DATA / "future_generation_scenarios.csv")
    strategies_raw = read_csv(DATA / "intergenerational_strategy_options.csv")
    risks_raw = read_csv(DATA / "long_term_risk_indicators.csv")
    records_raw = read_csv(DATA / "inheritance_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_long_term_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, records_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    record_scores = score_inheritance_records(records_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "intergenerational_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "future_generation_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "intergenerational_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "long_term_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "inheritance_record_scores.csv", record_scores)
    write_csv(OUTPUTS / "adaptive_long_term_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_long_term_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, record_scores, pathway_summary)

    print(f"Future generations workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
