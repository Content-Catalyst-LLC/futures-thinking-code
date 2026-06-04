#!/usr/bin/env python3
"""
Standard-library workflow for Futures Thinking and Sustainability.

Outputs:
- sustainability_profile_scores.csv
- sustainability_scenario_scores.csv
- transition_strategy_scores.csv
- sustainability_risk_priority_scores.csv
- governance_capacity_scores.csv
- transition_pathways.csv
- transition_pathway_summary.csv
- sustainability_futures_report.md
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


def sustainability_viability(row: dict[str, str]) -> float:
    return (
        0.17 * float(row["ecological_integrity"])
        + 0.15 * float(row["social_equity"])
        + 0.14 * float(row["adaptive_capacity"])
        + 0.10 * float(row["technological_responsibility"])
        + 0.14 * float(row["governance_coordination"])
        + 0.10 * float(row["public_finance_capacity"])
        + 0.10 * float(row["resilience_capacity"])
        + 0.10 * float(row["justice_legitimacy"])
        - 0.08 * float(row["degradation_pressure"])
    )


def sustainability_fragility(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["degradation_pressure"])
        + 0.15 * (1.0 - float(row["ecological_integrity"]))
        + 0.14 * (1.0 - float(row["social_equity"]))
        + 0.13 * (1.0 - float(row["governance_coordination"]))
        + 0.12 * (1.0 - float(row["adaptive_capacity"]))
        + 0.11 * (1.0 - float(row["public_finance_capacity"]))
        + 0.10 * (1.0 - float(row["resilience_capacity"]))
        + 0.09 * (1.0 - float(row["justice_legitimacy"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    governance: list[dict[str, str]],
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

    for row in governance:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Governance record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["ecological_integrity", "social_equity", "adaptive_capacity", "technological_responsibility", "governance_coordination", "public_finance_capacity", "resilience_capacity", "justice_legitimacy", "degradation_pressure"]),
        ("scenarios", scenarios, ["climate_stress", "biodiversity_pressure", "resource_constraint", "inequality_pressure", "technology_change", "governance_fragmentation", "public_finance_stress", "transition_momentum"]),
        ("strategies", strategies, ["ecological_gain", "equity_gain", "adaptive_capacity_gain", "governance_gain", "finance_gain", "resilience_gain", "justice_gain", "implementation_capacity"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "systemic_reach", "visibility_gap", "distributional_harm", "preparedness"]),
        ("governance", governance, ["participation", "accountability", "coordination", "monitoring_capacity", "adaptive_learning", "public_investment", "justice_safeguards"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        viability = sustainability_viability(row)
        fragility = sustainability_fragility(row)

        if viability >= 0.62 and fragility < 0.42:
            profile_class = "Stronger sustainability pathway"
        elif fragility >= 0.62:
            profile_class = "High sustainability fragility"
        else:
            profile_class = "Mixed or transitional sustainability future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "sustainability_viability_score": round(viability, 4),
            "sustainability_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["sustainability_viability_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.17 * float(row["climate_stress"])
            + 0.15 * float(row["biodiversity_pressure"])
            + 0.13 * float(row["resource_constraint"])
            + 0.15 * float(row["inequality_pressure"])
            + 0.12 * float(row["governance_fragmentation"])
            + 0.12 * float(row["public_finance_stress"])
            + 0.08 * (1.0 - float(row["transition_momentum"]))
            + 0.08 * float(row["technology_change"])
        )

        transition_opportunity = (
            0.20 * float(row["transition_momentum"])
            + 0.14 * float(row["technology_change"])
            + 0.12 * (1.0 - float(row["governance_fragmentation"]))
            + 0.12 * (1.0 - float(row["public_finance_stress"]))
            + 0.12 * (1.0 - float(row["inequality_pressure"]))
            + 0.10 * (1.0 - float(row["climate_stress"]))
            + 0.10 * (1.0 - float(row["biodiversity_pressure"]))
            + 0.10 * (1.0 - float(row["resource_constraint"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "sustainability_stress_score": round(stress, 4),
            "transition_opportunity_score": round(transition_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["sustainability_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        gain = (
            0.16 * float(row["ecological_gain"])
            + 0.16 * float(row["equity_gain"])
            + 0.14 * float(row["adaptive_capacity_gain"])
            + 0.14 * float(row["governance_gain"])
            + 0.12 * float(row["finance_gain"])
            + 0.12 * float(row["resilience_gain"])
            + 0.12 * float(row["justice_gain"])
            + 0.04 * float(row["implementation_capacity"])
        )

        readiness = (
            0.24 * float(row["implementation_capacity"])
            + 0.14 * float(row["governance_gain"])
            + 0.14 * float(row["finance_gain"])
            + 0.14 * float(row["adaptive_capacity_gain"])
            + 0.12 * float(row["resilience_gain"])
            + 0.10 * float(row["justice_gain"])
            + 0.08 * float(row["ecological_gain"])
            + 0.04 * float(row["equity_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "sustainability_gain_score": round(gain, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["sustainability_gain_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.17 * float(row["irreversibility"])
            + 0.16 * float(row["systemic_reach"])
            + 0.12 * float(row["visibility_gap"])
            + 0.15 * float(row["distributional_harm"])
            + 0.08 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "sustainability_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["sustainability_risk_priority_score"]), reverse=True)
    return rows


def score_governance(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        capacity = (
            0.14 * float(row["participation"])
            + 0.14 * float(row["accountability"])
            + 0.16 * float(row["coordination"])
            + 0.14 * float(row["monitoring_capacity"])
            + 0.16 * float(row["adaptive_learning"])
            + 0.12 * float(row["public_investment"])
            + 0.14 * float(row["justice_safeguards"])
        )

        legitimacy_gap = (
            0.18 * (1.0 - float(row["participation"]))
            + 0.18 * (1.0 - float(row["accountability"]))
            + 0.16 * (1.0 - float(row["justice_safeguards"]))
            + 0.14 * (1.0 - float(row["coordination"]))
            + 0.12 * (1.0 - float(row["adaptive_learning"]))
            + 0.12 * (1.0 - float(row["public_investment"]))
            + 0.10 * (1.0 - float(row["monitoring_capacity"]))
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "governance_capacity_score": round(capacity, 4),
            "legitimacy_gap_score": round(legitimacy_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["governance_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        ecology = float(row["ecology"])
        governance = float(row["governance"])
        adaptation = float(row["adaptation"])
        public_finance = float(row["public_finance"])
        resilience = float(row["resilience"])
        justice = float(row["justice"])
        degradation = float(row["degradation_pressure"])
        viability = float(row["initial_viability"])
        horizon = int(row["time_horizon"])

        exposure = (
            0.22 * degradation
            + 0.18 * (1.0 - ecology)
            + 0.16 * (1.0 - resilience)
            + 0.16 * (1.0 - governance)
            + 0.12 * (1.0 - public_finance)
            + 0.08 * (1.0 - adaptation)
            + 0.08 * (1.0 - justice)
        )

        institutional_capacity = (
            0.24 * governance
            + 0.22 * adaptation
            + 0.18 * public_finance
            + 0.18 * resilience
            + 0.18 * justice
        )

        viability_values: list[float] = []
        exposure_values: list[float] = []
        capacity_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                stress = 0.16 if t % 9 == 0 else 0.06

                response_gain = (
                    0.20 * ecology
                    + 0.18 * governance
                    + 0.18 * adaptation
                    + 0.14 * public_finance
                    + 0.16 * resilience
                    + 0.14 * justice
                )

                exposure = clamp(
                    exposure
                    + 0.05 * stress
                    + 0.03 * degradation
                    - 0.03 * ecology
                    - 0.03 * resilience
                    - 0.02 * governance
                    - 0.02 * justice,
                    0.0,
                    1.4,
                )

                institutional_capacity = clamp(
                    institutional_capacity
                    + 0.03 * governance
                    + 0.03 * adaptation
                    + 0.02 * public_finance
                    + 0.02 * justice
                    - 0.04 * stress,
                    0.0,
                    1.5,
                )

                viability = clamp(
                    viability
                    + 0.07 * response_gain
                    + 0.04 * institutional_capacity
                    - stress
                    - 0.05 * exposure
                    - 0.03 * degradation,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            exposure_values.append(exposure)
            capacity_values.append(institutional_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "sustainability_viability": round(viability, 4),
                "stress_exposure": round(exposure, 4),
                "institutional_capacity": round(institutional_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_viability": round(viability_values[-1], 4),
            "mean_viability": round(mean(viability_values), 4),
            "mean_stress_exposure": round(mean(exposure_values), 4),
            "final_institutional_capacity": round(capacity_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    governance_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Sustainability Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: viability {row['sustainability_viability_score']}; "
            f"fragility {row['sustainability_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Sustainability Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['sustainability_stress_score']}; "
            f"transition opportunity {row['transition_opportunity_score']}."
        )

    lines.extend(["", "## Transition Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: sustainability gain {row['sustainability_gain_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Sustainability Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['sustainability_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Governance Capacity Scores", ""])
    for row in governance_scores:
        lines.append(
            f"- **{row['record_name']}**: governance capacity {row['governance_capacity_score']}; "
            f"legitimacy gap {row['legitimacy_gap_score']}."
        )

    lines.extend(["", "## Transition Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_viability']}; "
            f"mean stress exposure {row['mean_stress_exposure']}; final institutional capacity {row['final_institutional_capacity']}."
        )

    avg_viability = mean(float(row["sustainability_viability_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["sustainability_fragility_score"]) for row in profile_scores)
    avg_pathway_viability = mean(float(row["final_viability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Sustainability future profiles: {len(profile_scores)}.",
        f"- Sustainability scenarios: {len(scenario_scores)}.",
        f"- Transition strategies: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Governance records: {len(governance_scores)}.",
        f"- Average sustainability viability score: {round(avg_viability, 4)}.",
        f"- Average sustainability fragility score: {round(avg_fragility, 4)}.",
        f"- Average final pathway viability: {round(avg_pathway_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats sustainability futures as complex systems shaped by ecological integrity, social equity, adaptive capacity, governance, public finance, resilience, justice, degradation pressure, and institutional learning.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "sustainability_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "sustainability_future_profiles.csv")
    scenarios_raw = read_csv(DATA / "sustainability_scenarios.csv")
    strategies_raw = read_csv(DATA / "transition_strategies.csv")
    risks_raw = read_csv(DATA / "sustainability_risk_indicators.csv")
    governance_raw = read_csv(DATA / "governance_capacity_records.csv")
    pathways_raw = read_csv(DATA / "transition_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, governance_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    governance_scores = score_governance(governance_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "sustainability_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "sustainability_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "transition_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "sustainability_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "governance_capacity_scores.csv", governance_scores)
    write_csv(OUTPUTS / "transition_pathways.csv", trajectories)
    write_csv(OUTPUTS / "transition_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, governance_scores, pathway_summary)

    print(f"Sustainability futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
