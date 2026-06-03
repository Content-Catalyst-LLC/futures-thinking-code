#!/usr/bin/env python3
"""
Standard-library workflow for Anticipatory Governance.

Outputs:
- governance_profile_scores.csv
- weak_signal_scores.csv
- emerging_risk_scores.csv
- scenario_profile_scores.csv
- anticipatory_governance_pathways.csv
- anticipatory_governance_pathway_summary.csv
- strategy_option_scores.csv
- anticipatory_governance_report.md
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


def anticipatory_capacity(row: dict[str, str]) -> float:
    return (
        0.12 * float(row["detection_capacity"])
        + 0.12 * float(row["interpretation_capacity"])
        + 0.12 * float(row["scenario_capacity"])
        + 0.12 * float(row["preparedness_capacity"])
        + 0.12 * float(row["legitimacy"])
        + 0.10 * float(row["coordination_capacity"])
        + 0.10 * float(row["adaptive_authority"])
        + 0.08 * float(row["equity_safeguards"])
        + 0.07 * float(row["learning_capacity"])
        + 0.05 * float(row["implementation_connection"])
    )


def fragility_pressure(row: dict[str, str]) -> float:
    return (
        0.16 * (1.0 - float(row["detection_capacity"]))
        + 0.14 * (1.0 - float(row["preparedness_capacity"]))
        + 0.14 * (1.0 - float(row["adaptive_authority"]))
        + 0.14 * (1.0 - float(row["coordination_capacity"]))
        + 0.14 * (1.0 - float(row["legitimacy"]))
        + 0.12 * (1.0 - float(row["equity_safeguards"]))
        + 0.08 * (1.0 - float(row["learning_capacity"]))
        + 0.08 * (1.0 - float(row["implementation_connection"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    signals: list[dict[str, str]],
    risks: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    governance_ids = {row["governance_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["governance_id"] not in governance_ids:
            errors.append(f"Risk {row['risk_id']} references missing governance profile {row['governance_id']}.")

    for row in pathways:
        if row["governance_id"] not in governance_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing governance profile {row['governance_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["detection_capacity", "interpretation_capacity", "scenario_capacity", "preparedness_capacity", "legitimacy", "coordination_capacity", "adaptive_authority", "equity_safeguards", "learning_capacity", "implementation_connection"]),
        ("signals", signals, ["signal_strength", "novelty", "uncertainty", "system_relevance", "justice_relevance", "detection_difficulty", "response_readiness"]),
        ("risks", risks, ["probability", "severity", "uncertainty", "detection_difficulty", "justice_exposure", "governance_gap", "mitigation_capacity"]),
        ("scenarios", scenarios, ["technology_acceleration", "climate_stress", "public_trust", "geopolitical_volatility", "fiscal_pressure", "institutional_capacity", "participation_quality", "crisis_frequency"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("governance_id") or row.get("scenario_id") or row.get("risk_id") or row.get("signal_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        capacity = anticipatory_capacity(row)
        fragility = fragility_pressure(row)

        if capacity >= 0.72:
            governance_class = "Strong anticipatory governance profile"
        elif fragility >= 0.55:
            governance_class = "High anticipatory fragility"
        else:
            governance_class = "Contested anticipatory capacity"

        rows.append({
            "governance_id": row["governance_id"],
            "governance_strategy": row["governance_strategy"],
            "governance_type": row["governance_type"],
            "anticipatory_capacity_score": round(capacity, 4),
            "anticipatory_fragility_pressure_score": round(fragility, 4),
            "governance_class": governance_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["anticipatory_capacity_score"]), reverse=True)
    return rows


def score_signals(signals: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in signals:
        priority = (
            0.16 * float(row["signal_strength"])
            + 0.14 * float(row["novelty"])
            + 0.12 * float(row["uncertainty"])
            + 0.18 * float(row["system_relevance"])
            + 0.16 * float(row["justice_relevance"])
            + 0.12 * float(row["detection_difficulty"])
            + 0.12 * (1.0 - float(row["response_readiness"]))
        )

        rows.append({
            "signal_id": row["signal_id"],
            "signal_name": row["signal_name"],
            "domain": row["domain"],
            "weak_signal_priority_score": round(priority, 4),
            "response_gap_score": round(1.0 - float(row["response_readiness"]), 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["weak_signal_priority_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.16 * float(row["probability"])
            + 0.18 * float(row["severity"])
            + 0.14 * float(row["uncertainty"])
            + 0.14 * float(row["detection_difficulty"])
            + 0.14 * float(row["justice_exposure"])
            + 0.14 * float(row["governance_gap"])
            + 0.10 * (1.0 - float(row["mitigation_capacity"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "governance_id": row["governance_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "emerging_risk_priority_score": round(priority, 4),
            "mitigation_capacity": float(row["mitigation_capacity"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["emerging_risk_priority_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.16 * float(row["technology_acceleration"])
            + 0.18 * float(row["climate_stress"])
            + 0.14 * (1.0 - float(row["public_trust"]))
            + 0.14 * float(row["geopolitical_volatility"])
            + 0.12 * float(row["fiscal_pressure"])
            + 0.10 * (1.0 - float(row["institutional_capacity"]))
            + 0.08 * (1.0 - float(row["participation_quality"]))
            + 0.08 * float(row["crisis_frequency"])
        )

        opportunity = (
            0.22 * float(row["institutional_capacity"])
            + 0.22 * float(row["participation_quality"])
            + 0.20 * float(row["public_trust"])
            + 0.12 * (1.0 - float(row["fiscal_pressure"]))
            + 0.10 * (1.0 - float(row["crisis_frequency"]))
            + 0.08 * (1.0 - float(row["geopolitical_volatility"]))
            + 0.06 * (1.0 - float(row["climate_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "future_stress_pressure_score": round(stress, 4),
            "democratic_anticipatory_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_stress_pressure_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        detection = float(row["detection"])
        interpretation = float(row["interpretation"])
        preparedness = float(row["preparedness"])
        legitimacy = float(row["legitimacy"])
        coordination = float(row["coordination"])
        adaptive_authority = float(row["adaptive_authority"])
        equity = float(row["equity"])
        learning = float(row["learning"])
        capacity = float(row["initial_capacity"])
        legitimacy_state = legitimacy
        learning_state = 0.5 * interpretation + 0.5 * adaptive_authority
        risk_pressure = 0.55
        horizon = int(row["time_horizon"])

        capacity_values: list[float] = []
        legitimacy_values: list[float] = []
        learning_values: list[float] = []
        risk_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                shock = 0.16 if t % 8 == 0 else 0.06

                warning_effect = 0.22 * detection + 0.18 * interpretation
                response_effect = 0.20 * preparedness + 0.18 * coordination + 0.16 * adaptive_authority
                democratic_effect = 0.14 * legitimacy_state + 0.12 * equity
                learning_effect = 0.12 * learning_state

                risk_pressure = clamp(
                    risk_pressure
                    + shock
                    - 0.10 * warning_effect
                    - 0.08 * response_effect,
                    0.0,
                    1.5,
                )

                learning_state = clamp(
                    learning_state
                    + 0.04 * interpretation
                    + 0.04 * adaptive_authority
                    + 0.02 * coordination
                    + 0.02 * learning
                    - 0.03 * shock,
                    0.0,
                    1.4,
                )

                legitimacy_state = clamp(
                    legitimacy_state
                    + 0.04 * legitimacy
                    + 0.03 * equity
                    + 0.02 * preparedness
                    - 0.04 * risk_pressure,
                    0.0,
                    1.4,
                )

                capacity = clamp(
                    capacity
                    + warning_effect / 5.0
                    + response_effect / 5.0
                    + democratic_effect / 6.0
                    + learning_effect / 6.0
                    - 0.10 * risk_pressure,
                    0.0,
                    1.8,
                )

            capacity_values.append(capacity)
            legitimacy_values.append(legitimacy_state)
            learning_values.append(learning_state)
            risk_values.append(risk_pressure)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "governance_id": row["governance_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "anticipatory_capacity": round(capacity, 4),
                "legitimacy_score": round(legitimacy_state, 4),
                "learning_score": round(learning_state, 4),
                "risk_pressure": round(risk_pressure, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "governance_id": row["governance_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_anticipatory_capacity": round(capacity_values[-1], 4),
            "mean_anticipatory_capacity": round(mean(capacity_values), 4),
            "final_legitimacy_score": round(legitimacy_values[-1], 4),
            "final_learning_score": round(learning_values[-1], 4),
            "mean_risk_pressure": round(mean(risk_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_anticipatory_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        institutionalization = (
            0.12 * float(row["horizon_scanning"])
            + 0.12 * float(row["scenario_planning"])
            + 0.14 * float(row["early_warning"])
            + 0.14 * float(row["adaptive_regulation"])
            + 0.14 * float(row["public_participation"])
            + 0.12 * float(row["budget_alignment"])
            + 0.10 * float(row["evaluation_capacity"])
            + 0.08 * float(row["equity_safeguards"])
            + 0.04 * float(row["implementation_authority"])
        )

        operational = (
            0.18 * float(row["implementation_authority"])
            + 0.16 * float(row["budget_alignment"])
            + 0.14 * float(row["early_warning"])
            + 0.14 * float(row["adaptive_regulation"])
            + 0.12 * float(row["evaluation_capacity"])
            + 0.10 * float(row["horizon_scanning"])
            + 0.08 * float(row["scenario_planning"])
            + 0.08 * float(row["public_participation"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "anticipatory_governance_strategy_score": round(institutionalization, 4),
            "operational_authority_strategy_score": round(operational, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["anticipatory_governance_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    profiles: list[dict[str, Any]],
    signals: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Governance Profile Scores",
        "",
    ]

    for row in profiles:
        lines.append(
            f"- **{row['governance_strategy']}**: anticipatory capacity {row['anticipatory_capacity_score']}; "
            f"fragility pressure {row['anticipatory_fragility_pressure_score']}; class: {row['governance_class']}."
        )

    lines.extend(["", "## Weak Signal Priorities", ""])
    for row in signals:
        lines.append(
            f"- **{row['signal_name']}**: priority {row['weak_signal_priority_score']}; "
            f"response gap {row['response_gap_score']}."
        )

    lines.extend(["", "## Emerging Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['emerging_risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: future stress {row['future_stress_pressure_score']}; "
            f"democratic opportunity {row['democratic_anticipatory_opportunity_score']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final capacity {row['final_anticipatory_capacity']}; "
            f"final legitimacy {row['final_legitimacy_score']}; mean risk pressure {row['mean_risk_pressure']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: anticipatory strategy {row['anticipatory_governance_strategy_score']}; "
            f"operational authority {row['operational_authority_strategy_score']}."
        )

    avg_capacity = mean(float(row["anticipatory_capacity_score"]) for row in profiles)
    avg_signal = mean(float(row["weak_signal_priority_score"]) for row in signals)
    avg_risk = mean(float(row["emerging_risk_priority_score"]) for row in risks)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Governance profiles: {len(profiles)}.",
        f"- Weak signals: {len(signals)}.",
        f"- Emerging risks: {len(risks)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- Average anticipatory capacity score: {round(avg_capacity, 4)}.",
        f"- Average weak signal priority score: {round(avg_signal, 4)}.",
        f"- Average emerging risk priority score: {round(avg_risk, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats anticipatory governance as an institutional capacity for detecting weak signals interpreting uncertainty preparing for multiple futures connecting foresight to authority learning from feedback and preserving democratic legitimacy under uncertainty.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "anticipatory_governance_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "governance_profiles.csv")
    signals_raw = read_csv(DATA / "weak_signal_register.csv")
    risks_raw = read_csv(DATA / "emerging_risk_register.csv")
    scenarios_raw = read_csv(DATA / "scenario_profiles.csv")
    pathways_raw = read_csv(DATA / "adaptive_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(profiles_raw, signals_raw, risks_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profiles = score_profiles(profiles_raw)
    signals = score_signals(signals_raw)
    risks = score_risks(risks_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "governance_profile_scores.csv", profiles)
    write_csv(OUTPUTS / "weak_signal_scores.csv", signals)
    write_csv(OUTPUTS / "emerging_risk_scores.csv", risks)
    write_csv(OUTPUTS / "scenario_profile_scores.csv", scenarios)
    write_csv(OUTPUTS / "anticipatory_governance_pathways.csv", trajectories)
    write_csv(OUTPUTS / "anticipatory_governance_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, profiles, signals, risks, scenarios, pathway_summary, strategies)

    print(f"Anticipatory governance workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
