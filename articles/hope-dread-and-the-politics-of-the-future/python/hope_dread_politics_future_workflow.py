#!/usr/bin/env python3
"""
Standard-library workflow for Hope, Dread, and the Politics of the Future.

Outputs:
- future_emotion_profile_scores.csv
- future_politics_scenario_scores.csv
- future_emotion_strategy_scores.csv
- future_emotion_risk_priority_scores.csv
- future_emotion_record_scores.csv
- adaptive_future_emotion_trajectories.csv
- adaptive_future_emotion_summary.csv
- hope_dread_politics_future_report.md
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


def mobilization_score(row: dict[str, str]) -> float:
    return float(row["agency"]) * (float(row["hope"]) + 0.55 * float(row["dread"])) * float(row["trust"])


def paralysis_risk(row: dict[str, str]) -> float:
    return float(row["dread"]) * (1.0 - float(row["agency"])) * (1.0 - float(row["trust"]))


def disciplined_hope_score(row: dict[str, str]) -> float:
    return (
        0.18 * float(row["hope"])
        + 0.18 * float(row["agency"])
        + 0.16 * float(row["trust"])
        + 0.16 * float(row["institutional_capacity"])
        + 0.14 * float(row["narrative_accountability"])
        + 0.12 * float(row["repair_capacity"])
        - 0.04 * float(row["future_fatigue"])
        - 0.02 * float(row["polarization"])
    )


def fear_politics_risk(row: dict[str, str]) -> float:
    return (
        0.24 * float(row["dread"])
        + 0.22 * float(row["polarization"])
        + 0.18 * (1.0 - float(row["trust"]))
        + 0.16 * (1.0 - float(row["agency"]))
        + 0.12 * float(row["future_fatigue"])
        + 0.08 * (1.0 - float(row["narrative_accountability"]))
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
            errors.append(f"Future-emotion record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["hope", "dread", "agency", "trust", "polarization", "institutional_capacity", "future_fatigue", "narrative_accountability", "repair_capacity", "democratic_imagination"]),
        ("scenarios", scenarios, ["threat_intensity", "agency_pathways", "institutional_trust", "scapegoating_intensity", "false_reassurance", "crisis_fatigue", "narrative_accountability", "democratic_participation", "repair_orientation", "learning_capacity"]),
        ("strategies", strategies, ["agency_pathway_gain", "trust_repair_gain", "narrative_accountability_gain", "participatory_foresight_gain", "climate_truth_action_gain", "youth_representation_gain", "media_literacy_gain", "repair_capacity_gain", "fear_politics_resistance_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "visibility_gap", "distributional_harm", "democratic_harm", "preparedness"]),
        ("records", records, ["hope", "dread", "agency", "trust", "future_fatigue", "repair_capacity", "polarization", "narrative_accountability"]),
        ("pathways", pathways, ["hope", "dread", "agency", "trust", "future_fatigue", "repair_capacity", "polarization", "narrative_accountability"]),
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
        mobilization = mobilization_score(row)
        paralysis = paralysis_risk(row)
        disciplined = disciplined_hope_score(row)
        fear = fear_politics_risk(row)

        if disciplined >= 0.65:
            profile_class = "Stronger disciplined hope"
        elif fear >= 0.65:
            profile_class = "High fear-politics risk"
        elif paralysis >= 0.35:
            profile_class = "High paralysis risk"
        else:
            profile_class = "Mixed future-emotion profile"

        rows.append({
            "profile_id": row["profile_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "mobilization_score": round(mobilization, 4),
            "paralysis_risk_score": round(paralysis, 4),
            "disciplined_hope_score": round(disciplined, 4),
            "fear_politics_risk_score": round(fear, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["disciplined_hope_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        affective_risk = (
            0.14 * float(row["threat_intensity"])
            + 0.12 * (1.0 - float(row["agency_pathways"]))
            + 0.12 * (1.0 - float(row["institutional_trust"]))
            + 0.14 * float(row["scapegoating_intensity"])
            + 0.12 * float(row["false_reassurance"])
            + 0.12 * float(row["crisis_fatigue"])
            + 0.09 * (1.0 - float(row["narrative_accountability"]))
            + 0.07 * (1.0 - float(row["democratic_participation"]))
            + 0.05 * (1.0 - float(row["repair_orientation"]))
            + 0.03 * (1.0 - float(row["learning_capacity"]))
        )

        agency_opportunity = (
            0.16 * float(row["agency_pathways"])
            + 0.15 * float(row["institutional_trust"])
            + 0.14 * float(row["narrative_accountability"])
            + 0.13 * float(row["democratic_participation"])
            + 0.12 * float(row["repair_orientation"])
            + 0.10 * float(row["learning_capacity"])
            + 0.08 * (1.0 - float(row["scapegoating_intensity"]))
            + 0.06 * (1.0 - float(row["false_reassurance"]))
            + 0.04 * (1.0 - float(row["crisis_fatigue"]))
            + 0.02 * (1.0 - float(row["threat_intensity"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "future_politics_risk_score": round(affective_risk, 4),
            "agency_opportunity_score": round(agency_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_politics_risk_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        value = (
            0.13 * float(row["agency_pathway_gain"])
            + 0.12 * float(row["trust_repair_gain"])
            + 0.13 * float(row["narrative_accountability_gain"])
            + 0.11 * float(row["participatory_foresight_gain"])
            + 0.11 * float(row["climate_truth_action_gain"])
            + 0.10 * float(row["youth_representation_gain"])
            + 0.08 * float(row["media_literacy_gain"])
            + 0.10 * float(row["repair_capacity_gain"])
            + 0.08 * float(row["fear_politics_resistance_gain"])
            + 0.02 * float(row["implementation_capacity"])
            + 0.02 * float(row["public_legitimacy_gain"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.16 * float(row["public_legitimacy_gain"])
            + 0.12 * float(row["agency_pathway_gain"])
            + 0.11 * float(row["trust_repair_gain"])
            + 0.10 * float(row["narrative_accountability_gain"])
            + 0.09 * float(row["participatory_foresight_gain"])
            + 0.08 * float(row["climate_truth_action_gain"])
            + 0.06 * float(row["youth_representation_gain"])
            + 0.04 * float(row["media_literacy_gain"])
            + 0.04 * float(row["fear_politics_resistance_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "future_emotion_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_emotion_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.16 * float(row["severity"])
            + 0.12 * float(row["irreversibility"])
            + 0.12 * float(row["visibility_gap"])
            + 0.16 * float(row["distributional_harm"])
            + 0.20 * float(row["democratic_harm"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "future_emotion_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "democratic_harm": float(row["democratic_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_emotion_risk_priority_score"]), reverse=True)
    return rows


def score_records(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        hope = float(row["hope"])
        dread = float(row["dread"])
        agency = float(row["agency"])
        trust = float(row["trust"])
        fatigue = float(row["future_fatigue"])
        repair = float(row["repair_capacity"])
        polarization = float(row["polarization"])
        accountability = float(row["narrative_accountability"])

        mobilization = agency * (hope + 0.55 * dread) * trust
        paralysis = dread * (1.0 - agency) * (1.0 - trust)
        disciplined = 0.22 * hope + 0.22 * agency + 0.18 * trust + 0.18 * repair + 0.12 * accountability - 0.05 * fatigue - 0.03 * polarization
        false_hope_risk = max(0.0, hope - accountability - repair)

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "mobilization_score": round(mobilization, 4),
            "paralysis_risk_score": round(paralysis, 4),
            "disciplined_hope_score": round(disciplined, 4),
            "false_hope_risk_score": round(false_hope_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["disciplined_hope_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        hope = float(row["hope"])
        dread = float(row["dread"])
        agency = float(row["agency"])
        trust = float(row["trust"])
        fatigue = float(row["future_fatigue"])
        repair = float(row["repair_capacity"])
        polarization = float(row["polarization"])
        accountability = float(row["narrative_accountability"])
        horizon = int(row["time_horizon"])

        hope_values: list[float] = []
        dread_values: list[float] = []
        agency_values: list[float] = []
        trust_values: list[float] = []
        fatigue_values: list[float] = []
        mobilization_values: list[float] = []
        paralysis_values: list[float] = []
        disciplined_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                crisis_spike = 0.018 if t % 8 == 0 else 0.0
                progress_signal = 0.015 if t % 10 == 0 else 0.0
                institutional_failure = 0.014 if t % 13 == 0 else 0.0
                backlash = 0.012 if t % 17 == 0 else 0.0

                dread = clamp(
                    dread + crisis_spike + 0.010 * fatigue + 0.006 * polarization - 0.010 * agency - 0.008 * trust,
                    0.0,
                    1.8,
                )

                trust = clamp(
                    trust + progress_signal + 0.010 * repair + 0.006 * accountability - institutional_failure - 0.006 * fatigue,
                    0.0,
                    1.8,
                )

                agency = clamp(
                    agency + 0.010 * trust + 0.012 * repair + progress_signal - 0.010 * fatigue - 0.006 * dread,
                    0.0,
                    1.8,
                )

                fatigue = clamp(
                    fatigue + 0.010 * dread + institutional_failure - 0.012 * agency - 0.010 * trust,
                    0.0,
                    1.8,
                )

                repair = clamp(
                    repair + 0.010 * agency + 0.008 * trust + progress_signal - 0.006 * fatigue,
                    0.0,
                    1.8,
                )

                accountability = clamp(
                    accountability + 0.008 * trust + 0.008 * agency + progress_signal - 0.006 * institutional_failure,
                    0.0,
                    1.8,
                )

                polarization = clamp(
                    polarization + backlash + 0.006 * dread - 0.010 * trust - 0.008 * accountability,
                    0.0,
                    1.8,
                )

                hope = clamp(
                    hope + 0.012 * agency + 0.010 * trust + 0.010 * repair + 0.006 * accountability - 0.008 * fatigue - 0.004 * dread,
                    0.0,
                    1.8,
                )

            mobilization = clamp(agency * (hope + 0.55 * dread) * trust, 0.0, 2.5)
            paralysis = clamp(dread * (1.0 - min(agency, 1.0)) * (1.0 - min(trust, 1.0)), 0.0, 1.8)
            disciplined = clamp(
                0.22 * hope + 0.22 * agency + 0.18 * trust + 0.18 * repair + 0.12 * accountability - 0.05 * fatigue - 0.03 * polarization,
                -1.0,
                1.8,
            )
            fear_politics = clamp(
                0.24 * dread + 0.22 * polarization + 0.18 * (1.0 - min(trust, 1.0)) + 0.16 * (1.0 - min(agency, 1.0)) + 0.12 * fatigue + 0.08 * (1.0 - min(accountability, 1.0)),
                0.0,
                1.8,
            )

            hope_values.append(hope)
            dread_values.append(dread)
            agency_values.append(agency)
            trust_values.append(trust)
            fatigue_values.append(fatigue)
            mobilization_values.append(mobilization)
            paralysis_values.append(paralysis)
            disciplined_values.append(disciplined)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "hope": round(hope, 4),
                "dread": round(dread, 4),
                "agency": round(agency, 4),
                "trust": round(trust, 4),
                "future_fatigue": round(fatigue, 4),
                "repair_capacity": round(repair, 4),
                "polarization": round(polarization, 4),
                "narrative_accountability": round(accountability, 4),
                "mobilization_score": round(mobilization, 4),
                "paralysis_risk_score": round(paralysis, 4),
                "disciplined_hope_score": round(disciplined, 4),
                "fear_politics_risk_score": round(fear_politics, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_hope": round(hope_values[-1], 4),
            "final_dread": round(dread_values[-1], 4),
            "final_agency": round(agency_values[-1], 4),
            "final_trust": round(trust_values[-1], 4),
            "final_future_fatigue": round(fatigue_values[-1], 4),
            "final_mobilization_score": round(mobilization_values[-1], 4),
            "final_paralysis_risk_score": round(paralysis_values[-1], 4),
            "final_disciplined_hope_score": round(disciplined_values[-1], 4),
            "mean_disciplined_hope_score": round(mean(disciplined_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_disciplined_hope_score"]), reverse=True)
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
        "## Future-Emotion Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['scenario_name']}**: disciplined hope {row['disciplined_hope_score']}; "
            f"mobilization {row['mobilization_score']}; paralysis risk {row['paralysis_risk_score']}; "
            f"fear-politics risk {row['fear_politics_risk_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Future-Politics Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: future-politics risk {row['future_politics_risk_score']}; "
            f"agency opportunity {row['agency_opportunity_score']}."
        )

    lines.extend(["", "## Future-Emotion Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['future_emotion_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Future-Emotion Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['future_emotion_risk_priority_score']}; "
            f"democratic harm {row['democratic_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Future-Emotion Record Scores", ""])
    for row in record_scores:
        lines.append(
            f"- **{row['record_name']}**: disciplined hope {row['disciplined_hope_score']}; "
            f"mobilization {row['mobilization_score']}; false-hope risk {row['false_hope_risk_score']}."
        )

    lines.extend(["", "## Adaptive Future-Emotion Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final disciplined hope {row['final_disciplined_hope_score']}; "
            f"final mobilization {row['final_mobilization_score']}; final paralysis risk {row['final_paralysis_risk_score']}."
        )

    avg_disciplined = mean(float(row["disciplined_hope_score"]) for row in profile_scores)
    avg_paralysis = mean(float(row["paralysis_risk_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["future_emotion_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Future-emotion profiles: {len(profile_scores)}.",
        f"- Future-politics scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Future-emotion records: {len(record_scores)}.",
        f"- Average disciplined hope score: {round(avg_disciplined, 4)}.",
        f"- Average paralysis risk score: {round(avg_paralysis, 4)}.",
        f"- Average strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats hope, dread, and future politics as systems shaped by agency, trust, fatigue, repair capacity, polarization, narrative accountability, democratic imagination, mobilization, paralysis, and fear-politics risk.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "hope_dread_politics_future_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "future_emotion_profiles.csv")
    scenarios_raw = read_csv(DATA / "future_politics_scenarios.csv")
    strategies_raw = read_csv(DATA / "future_emotion_strategy_options.csv")
    risks_raw = read_csv(DATA / "future_emotion_risk_indicators.csv")
    records_raw = read_csv(DATA / "future_emotion_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_future_emotion_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, records_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    record_scores = score_records(records_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "future_emotion_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "future_politics_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "future_emotion_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "future_emotion_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "future_emotion_record_scores.csv", record_scores)
    write_csv(OUTPUTS / "adaptive_future_emotion_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_future_emotion_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, record_scores, pathway_summary)

    print(f"Hope, dread, and future-politics workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
