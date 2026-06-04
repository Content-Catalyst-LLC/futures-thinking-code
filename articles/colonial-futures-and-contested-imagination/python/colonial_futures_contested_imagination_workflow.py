#!/usr/bin/env python3
"""
Standard-library workflow for Colonial Futures and Contested Imagination.

Outputs:
- colonial_future_profile_scores.csv
- colonial_future_scenario_scores.csv
- reparative_strategy_scores.csv
- coloniality_risk_priority_scores.csv
- extraction_voice_scores.csv
- adaptive_colonial_future_trajectories.csv
- adaptive_colonial_future_summary.csv
- colonial_futures_contested_imagination_report.md
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


def coloniality_risk_score(row: dict[str, str]) -> float:
    return (
        0.12 * float(row["agenda_setting_power"])
        + 0.12 * (1.0 - float(row["consent_quality"]))
        + 0.12 * float(row["land_exposure"])
        + 0.12 * float(row["external_control"])
        + 0.11 * (1.0 - float(row["epistemic_justice"]))
        + 0.10 * (1.0 - float(row["local_benefit"]))
        + 0.10 * float(row["ecological_harm"])
        + 0.09 * (1.0 - float(row["reparative_capacity"]))
        + 0.07 * (1.0 - float(row["sovereignty_recognition"]))
        + 0.03 * (1.0 - float(row["data_sovereignty"]))
        + 0.02 * (1.0 - float(row["labor_protection"]))
    )


def reparative_future_score(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["consent_quality"])
        + 0.15 * float(row["epistemic_justice"])
        + 0.14 * float(row["local_benefit"])
        + 0.16 * float(row["reparative_capacity"])
        + 0.14 * float(row["sovereignty_recognition"])
        + 0.08 * float(row["data_sovereignty"])
        + 0.07 * float(row["labor_protection"])
        + 0.05 * (1.0 - float(row["external_control"]))
        + 0.03 * (1.0 - float(row["land_exposure"]))
        + 0.02 * (1.0 - float(row["ecological_harm"]))
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
            errors.append(f"Extraction/voice record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["agenda_setting_power", "consent_quality", "land_exposure", "external_control", "epistemic_justice", "local_benefit", "ecological_harm", "reparative_capacity", "sovereignty_recognition", "data_sovereignty", "labor_protection"]),
        ("scenarios", scenarios, ["extraction_pressure", "external_control_pressure", "consent_gap", "land_risk", "knowledge_erasure", "data_extraction", "security_drift", "ecological_harm", "reparative_opening", "community_voice"]),
        ("strategies", strategies, ["land_return_gain", "consent_quality_gain", "community_ownership_gain", "epistemic_justice_gain", "data_sovereignty_gain", "labor_rights_gain", "ecological_restoration_gain", "reparative_finance_gain", "accountability_gain", "implementation_capacity", "legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "visibility_gap", "distributional_harm", "rights_risk", "preparedness"]),
        ("records", records, ["extraction_burden", "community_voice", "external_control", "ecological_harm", "local_benefit", "reparative_capacity", "consent_quality", "sovereignty_recognition"]),
        ("pathways", pathways, ["extraction_burden", "community_voice", "external_control", "ecological_harm", "local_benefit", "reparative_capacity", "consent_quality", "sovereignty_recognition"]),
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
        risk = coloniality_risk_score(row)
        repair = reparative_future_score(row)
        gap = max(0.0, risk - repair)

        if risk >= 0.70:
            profile_class = "High coloniality risk"
        elif repair >= 0.65:
            profile_class = "Stronger reparative future capacity"
        else:
            profile_class = "Mixed or contested future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "coloniality_risk_score": round(risk, 4),
            "reparative_future_score": round(repair, 4),
            "reparative_gap_score": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["coloniality_risk_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        colonial_pressure = (
            0.14 * float(row["extraction_pressure"])
            + 0.14 * float(row["external_control_pressure"])
            + 0.13 * float(row["consent_gap"])
            + 0.12 * float(row["land_risk"])
            + 0.12 * float(row["knowledge_erasure"])
            + 0.10 * float(row["data_extraction"])
            + 0.09 * float(row["security_drift"])
            + 0.08 * float(row["ecological_harm"])
            + 0.05 * (1.0 - float(row["reparative_opening"]))
            + 0.03 * (1.0 - float(row["community_voice"]))
        )

        decolonial_opportunity = (
            0.18 * float(row["reparative_opening"])
            + 0.17 * float(row["community_voice"])
            + 0.12 * (1.0 - float(row["consent_gap"]))
            + 0.11 * (1.0 - float(row["external_control_pressure"]))
            + 0.10 * (1.0 - float(row["knowledge_erasure"]))
            + 0.09 * (1.0 - float(row["extraction_pressure"]))
            + 0.08 * (1.0 - float(row["land_risk"]))
            + 0.06 * (1.0 - float(row["data_extraction"]))
            + 0.05 * (1.0 - float(row["security_drift"]))
            + 0.04 * (1.0 - float(row["ecological_harm"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "colonial_pressure_score": round(colonial_pressure, 4),
            "decolonial_opportunity_score": round(decolonial_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["colonial_pressure_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        value = (
            0.13 * float(row["land_return_gain"])
            + 0.13 * float(row["consent_quality_gain"])
            + 0.12 * float(row["community_ownership_gain"])
            + 0.12 * float(row["epistemic_justice_gain"])
            + 0.10 * float(row["data_sovereignty_gain"])
            + 0.10 * float(row["labor_rights_gain"])
            + 0.10 * float(row["ecological_restoration_gain"])
            + 0.09 * float(row["reparative_finance_gain"])
            + 0.07 * float(row["accountability_gain"])
            + 0.02 * float(row["implementation_capacity"])
            + 0.02 * float(row["legitimacy_gain"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.16 * float(row["legitimacy_gain"])
            + 0.14 * float(row["accountability_gain"])
            + 0.12 * float(row["consent_quality_gain"])
            + 0.10 * float(row["community_ownership_gain"])
            + 0.08 * float(row["epistemic_justice_gain"])
            + 0.07 * float(row["reparative_finance_gain"])
            + 0.05 * float(row["labor_rights_gain"])
            + 0.04 * float(row["land_return_gain"])
            + 0.04 * float(row["ecological_restoration_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "reparative_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["reparative_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.17 * float(row["severity"])
            + 0.15 * float(row["irreversibility"])
            + 0.10 * float(row["visibility_gap"])
            + 0.20 * float(row["distributional_harm"])
            + 0.14 * float(row["rights_risk"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "coloniality_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "rights_risk": float(row["rights_risk"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["coloniality_risk_priority_score"]), reverse=True)
    return rows


def score_extraction_voice(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in records:
        extraction_burden = float(row["extraction_burden"])
        voice = float(row["community_voice"])
        external = float(row["external_control"])
        harm = float(row["ecological_harm"])
        benefit = float(row["local_benefit"])
        repair = float(row["reparative_capacity"])
        consent = float(row["consent_quality"])
        sovereignty = float(row["sovereignty_recognition"])

        legitimacy = (
            0.18 * voice
            + 0.16 * benefit
            + 0.16 * repair
            + 0.16 * consent
            + 0.14 * sovereignty
            - 0.08 * extraction_burden
            - 0.07 * external
            - 0.05 * harm
        )

        reparative_gap = max(0.0, extraction_burden + external + harm - benefit - repair - consent)

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "extraction_burden_score": round(extraction_burden, 4),
            "future_making_legitimacy_score": round(legitimacy, 4),
            "reparative_gap_score": round(reparative_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["reparative_gap_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        extraction = float(row["extraction_burden"])
        voice = float(row["community_voice"])
        external = float(row["external_control"])
        harm = float(row["ecological_harm"])
        benefit = float(row["local_benefit"])
        repair = float(row["reparative_capacity"])
        consent = float(row["consent_quality"])
        sovereignty = float(row["sovereignty_recognition"])
        horizon = int(row["time_horizon"])

        legitimacy = (
            0.18 * voice
            + 0.16 * benefit
            + 0.16 * repair
            + 0.16 * consent
            + 0.14 * sovereignty
            - 0.08 * extraction
            - 0.07 * external
            - 0.05 * harm
        )

        extraction_values: list[float] = []
        voice_values: list[float] = []
        external_values: list[float] = []
        harm_values: list[float] = []
        repair_values: list[float] = []
        legitimacy_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                extraction_push = 0.018 if t % 7 == 0 else 0.0
                resistance_cycle = 0.020 if t % 9 == 0 else 0.0
                repair_window = 0.018 if t % 11 == 0 else 0.0
                backlash = 0.010 if t % 13 == 0 else 0.0

                extraction = clamp(
                    extraction + extraction_push + 0.012 * external - 0.014 * voice - 0.012 * repair - 0.008 * consent,
                    0.0,
                    1.8,
                )

                voice = clamp(
                    voice + resistance_cycle + 0.014 * repair + 0.010 * sovereignty - 0.010 * external - 0.006 * extraction - backlash,
                    0.0,
                    1.8,
                )

                external = clamp(
                    external + 0.010 * extraction + backlash - 0.014 * voice - 0.010 * repair - 0.008 * sovereignty,
                    0.0,
                    1.8,
                )

                harm = clamp(
                    harm + 0.012 * extraction + 0.006 * external - 0.014 * repair - 0.008 * consent,
                    0.0,
                    1.8,
                )

                benefit = clamp(
                    benefit + 0.012 * voice + 0.010 * repair + repair_window - 0.006 * external,
                    0.0,
                    1.8,
                )

                repair = clamp(
                    repair + 0.014 * voice + 0.010 * consent + 0.010 * sovereignty + repair_window - 0.008 * external - 0.006 * extraction,
                    0.0,
                    1.8,
                )

                consent = clamp(
                    consent + 0.012 * voice + 0.008 * sovereignty + 0.006 * repair - 0.008 * external,
                    0.0,
                    1.8,
                )

                sovereignty = clamp(
                    sovereignty + 0.010 * voice + 0.008 * consent + 0.008 * repair - 0.008 * external,
                    0.0,
                    1.8,
                )

                legitimacy = clamp(
                    0.18 * voice
                    + 0.16 * benefit
                    + 0.16 * repair
                    + 0.16 * consent
                    + 0.14 * sovereignty
                    - 0.08 * extraction
                    - 0.07 * external
                    - 0.05 * harm,
                    -1.0,
                    1.8,
                )

            extraction_values.append(extraction)
            voice_values.append(voice)
            external_values.append(external)
            harm_values.append(harm)
            repair_values.append(repair)
            legitimacy_values.append(legitimacy)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "extraction_burden": round(extraction, 4),
                "community_voice": round(voice, 4),
                "external_control": round(external, 4),
                "ecological_harm": round(harm, 4),
                "local_benefit": round(benefit, 4),
                "reparative_capacity": round(repair, 4),
                "consent_quality": round(consent, 4),
                "sovereignty_recognition": round(sovereignty, 4),
                "legitimacy": round(legitimacy, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_extraction_burden": round(extraction_values[-1], 4),
            "final_community_voice": round(voice_values[-1], 4),
            "final_external_control": round(external_values[-1], 4),
            "final_ecological_harm": round(harm_values[-1], 4),
            "final_reparative_capacity": round(repair_values[-1], 4),
            "final_legitimacy": round(legitimacy_values[-1], 4),
            "mean_legitimacy": round(mean(legitimacy_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_legitimacy"]), reverse=True)
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
        "## Colonial Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: coloniality risk {row['coloniality_risk_score']}; "
            f"reparative capacity {row['reparative_future_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: colonial pressure {row['colonial_pressure_score']}; "
            f"decolonial opportunity {row['decolonial_opportunity_score']}."
        )

    lines.extend(["", "## Reparative Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: reparative value {row['reparative_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Coloniality Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['coloniality_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; rights risk {row['rights_risk']}."
        )

    lines.extend(["", "## Extraction, Voice, and Legitimacy Scores", ""])
    for row in record_scores:
        lines.append(
            f"- **{row['record_name']}**: extraction {row['extraction_burden_score']}; "
            f"legitimacy {row['future_making_legitimacy_score']}; reparative gap {row['reparative_gap_score']}."
        )

    lines.extend(["", "## Adaptive Colonial Future Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final legitimacy {row['final_legitimacy']}; "
            f"final extraction {row['final_extraction_burden']}; final reparative capacity {row['final_reparative_capacity']}."
        )

    avg_risk = mean(float(row["coloniality_risk_score"]) for row in profile_scores)
    avg_repair = mean(float(row["reparative_future_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["reparative_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Colonial future profiles: {len(profile_scores)}.",
        f"- Scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Extraction/voice records: {len(record_scores)}.",
        f"- Average coloniality risk score: {round(avg_risk, 4)}.",
        f"- Average reparative future score: {round(avg_repair, 4)}.",
        f"- Average reparative strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats colonial futures and contested imagination as systems shaped by agenda-setting power, consent, land exposure, external control, epistemic justice, local benefit, ecological harm, reparative capacity, sovereignty, data governance, labor protection, and legitimacy.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "colonial_futures_contested_imagination_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "colonial_future_profiles.csv")
    scenarios_raw = read_csv(DATA / "colonial_future_scenarios.csv")
    strategies_raw = read_csv(DATA / "reparative_strategy_options.csv")
    risks_raw = read_csv(DATA / "coloniality_risk_indicators.csv")
    records_raw = read_csv(DATA / "extraction_voice_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_colonial_future_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, records_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    record_scores = score_extraction_voice(records_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "colonial_future_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "colonial_future_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "reparative_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "coloniality_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "extraction_voice_scores.csv", record_scores)
    write_csv(OUTPUTS / "adaptive_colonial_future_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_colonial_future_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, record_scores, pathway_summary)

    print(f"Colonial futures and contested imagination workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
