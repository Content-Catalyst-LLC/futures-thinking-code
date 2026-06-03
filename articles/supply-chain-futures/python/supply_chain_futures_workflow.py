#!/usr/bin/env python3
"""
Standard-library workflow for Supply Chain Futures.

Outputs:
- supply_chain_profile_scores.csv
- supply_chain_scenario_scores.csv
- resilience_strategy_scores.csv
- chokepoint_priority_scores.csv
- procurement_circularity_scores.csv
- disruption_pathways.csv
- disruption_pathway_summary.csv
- supply_chain_futures_report.md
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


def resilience_score(row: dict[str, str]) -> float:
    return (
        0.10 * float(row["cost_efficiency"])
        + 0.16 * float(row["supplier_diversification"])
        + 0.14 * float(row["inventory_buffer"])
        + 0.14 * float(row["supply_visibility"])
        + 0.12 * float(row["labor_accountability"])
        + 0.13 * float(row["climate_adaptation"])
        + 0.09 * float(row["digital_traceability"])
        + 0.06 * float(row["circularity"])
        + 0.04 * float(row["regulatory_readiness"])
        + 0.02 * float(row["recovery_capacity"])
    )


def fragility_score(row: dict[str, str]) -> float:
    return (
        0.16 * (1.0 - float(row["supplier_diversification"]))
        + 0.16 * (1.0 - float(row["inventory_buffer"]))
        + 0.14 * (1.0 - float(row["supply_visibility"]))
        + 0.14 * (1.0 - float(row["climate_adaptation"]))
        + 0.12 * (1.0 - float(row["labor_accountability"]))
        + 0.10 * (1.0 - float(row["recovery_capacity"]))
        + 0.08 * (1.0 - float(row["regulatory_readiness"]))
        + 0.06 * (1.0 - float(row["digital_traceability"]))
        + 0.04 * (1.0 - float(row["circularity"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    chokepoints: list[dict[str, str]],
    procurement_records: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing profile {row['profile_id']}.")

    for row in chokepoints:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Chokepoint {row['chokepoint_id']} references missing scenario {row['scenario_id']}.")

    for row in procurement_records:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Procurement/circularity record {row['record_id']} references missing profile {row['profile_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["cost_efficiency", "supplier_diversification", "inventory_buffer", "supply_visibility", "labor_accountability", "climate_adaptation", "digital_traceability", "circularity", "regulatory_readiness", "recovery_capacity"]),
        ("scenarios", scenarios, ["trade_fragmentation", "climate_disruption", "technology_acceleration", "critical_minerals_pressure", "labor_stress", "transport_chokepoint_pressure", "regulatory_pressure", "demand_volatility"]),
        ("strategies", strategies, ["supplier_diversification_gain", "buffer_gain", "visibility_gain", "labor_accountability_gain", "climate_adaptation_gain", "circularity_gain", "implementation_capacity", "cost_burden"]),
        ("chokepoints", chokepoints, ["dependency_concentration", "substitution_difficulty", "disruption_probability", "systemic_reach", "recovery_difficulty", "visibility_gap"]),
        ("procurement_records", procurement_records, ["public_value", "resilience_support", "labor_standard_strength", "environmental_performance", "traceability_quality", "circular_material_capacity", "implementation_readiness"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("chokepoint_id") or row.get("record_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        resilience = resilience_score(row)
        fragility = fragility_score(row)

        if resilience >= 0.66 and fragility < 0.45:
            profile_class = "Stronger resilience profile"
        elif fragility >= 0.62:
            profile_class = "High supply chain fragility"
        else:
            profile_class = "Mixed or transitional supply chain profile"

        rows.append({
            "profile_id": row["profile_id"],
            "supply_chain_name": row["supply_chain_name"],
            "supply_chain_type": row["supply_chain_type"],
            "supply_chain_resilience_score": round(resilience, 4),
            "supply_chain_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["supply_chain_resilience_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        disruption_pressure = (
            0.16 * float(row["trade_fragmentation"])
            + 0.18 * float(row["climate_disruption"])
            + 0.14 * float(row["critical_minerals_pressure"])
            + 0.12 * float(row["labor_stress"])
            + 0.14 * float(row["transport_chokepoint_pressure"])
            + 0.10 * float(row["regulatory_pressure"])
            + 0.10 * float(row["demand_volatility"])
            + 0.06 * float(row["technology_acceleration"])
        )

        adaptation_opportunity = (
            0.16 * float(row["technology_acceleration"])
            + 0.16 * float(row["regulatory_pressure"])
            + 0.14 * float(row["climate_disruption"])
            + 0.14 * float(row["critical_minerals_pressure"])
            + 0.12 * float(row["demand_volatility"])
            + 0.10 * float(row["trade_fragmentation"])
            + 0.10 * float(row["labor_stress"])
            + 0.08 * float(row["transport_chokepoint_pressure"])
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "disruption_pressure_score": round(disruption_pressure, 4),
            "adaptation_opportunity_score": round(adaptation_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["disruption_pressure_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        resilience_gain = (
            0.18 * float(row["supplier_diversification_gain"])
            + 0.16 * float(row["buffer_gain"])
            + 0.16 * float(row["visibility_gain"])
            + 0.14 * float(row["labor_accountability_gain"])
            + 0.16 * float(row["climate_adaptation_gain"])
            + 0.10 * float(row["circularity_gain"])
            + 0.10 * float(row["implementation_capacity"])
            - 0.10 * float(row["cost_burden"])
        )

        implementation_risk = (
            0.28 * (1.0 - float(row["implementation_capacity"]))
            + 0.18 * float(row["cost_burden"])
            + 0.10 * (1.0 - float(row["supplier_diversification_gain"]))
            + 0.10 * (1.0 - float(row["buffer_gain"]))
            + 0.10 * (1.0 - float(row["visibility_gain"]))
            + 0.10 * (1.0 - float(row["labor_accountability_gain"]))
            + 0.08 * (1.0 - float(row["climate_adaptation_gain"]))
            + 0.06 * (1.0 - float(row["circularity_gain"]))
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "resilience_gain_score": round(resilience_gain, 4),
            "implementation_risk_score": round(implementation_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["resilience_gain_score"]), reverse=True)
    return rows


def score_chokepoints(chokepoints: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in chokepoints:
        priority = (
            0.18 * float(row["dependency_concentration"])
            + 0.17 * float(row["substitution_difficulty"])
            + 0.16 * float(row["disruption_probability"])
            + 0.18 * float(row["systemic_reach"])
            + 0.17 * float(row["recovery_difficulty"])
            + 0.14 * float(row["visibility_gap"])
        )

        rows.append({
            "chokepoint_id": row["chokepoint_id"],
            "scenario_id": row["scenario_id"],
            "chokepoint_name": row["chokepoint_name"],
            "chokepoint_type": row["chokepoint_type"],
            "chokepoint_priority_score": round(priority, 4),
            "visibility_gap": float(row["visibility_gap"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["chokepoint_priority_score"]), reverse=True)
    return rows


def score_procurement_circularity(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in records:
        public_interest_score = (
            0.18 * float(row["public_value"])
            + 0.18 * float(row["resilience_support"])
            + 0.14 * float(row["labor_standard_strength"])
            + 0.14 * float(row["environmental_performance"])
            + 0.14 * float(row["traceability_quality"])
            + 0.12 * float(row["circular_material_capacity"])
            + 0.10 * float(row["implementation_readiness"])
        )

        rows.append({
            "record_id": row["record_id"],
            "profile_id": row["profile_id"],
            "record_name": row["record_name"],
            "record_type": row["record_type"],
            "public_interest_supply_governance_score": round(public_interest_score, 4),
            "implementation_readiness": float(row["implementation_readiness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_supply_governance_score"]), reverse=True)
    return rows


def simulate_disruption(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        cost_efficiency = float(row["cost_efficiency"])
        diversification = float(row["diversification"])
        buffer = float(row["buffer"])
        visibility = float(row["visibility"])
        labor = float(row["labor_accountability"])
        climate = float(row["climate_adaptation"])
        traceability = float(row["traceability"])
        recovery_capacity = float(row["recovery_capacity"])
        viability = float(row["initial_viability"])
        horizon = int(row["time_horizon"])

        exposure = (
            0.22 * (1.0 - diversification)
            + 0.20 * (1.0 - buffer)
            + 0.18 * (1.0 - visibility)
            + 0.16 * (1.0 - climate)
            + 0.12 * (1.0 - labor)
            + 0.12 * (1.0 - recovery_capacity)
        )
        recovery = (
            0.24 * recovery_capacity
            + 0.20 * visibility
            + 0.18 * buffer
            + 0.16 * diversification
            + 0.12 * traceability
            + 0.10 * labor
        )

        viability_values: list[float] = []
        exposure_values: list[float] = []
        recovery_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.20 if t % 8 == 0 else 0.06

                adaptive_capacity = (
                    0.20 * diversification
                    + 0.18 * buffer
                    + 0.18 * visibility
                    + 0.16 * recovery_capacity
                    + 0.12 * climate
                    + 0.10 * traceability
                    + 0.06 * labor
                )

                exposure = clamp(
                    exposure
                    + 0.06 * disruption
                    - 0.03 * diversification
                    - 0.03 * buffer
                    - 0.03 * visibility
                    - 0.03 * climate
                    - 0.02 * labor,
                    0.0,
                    1.4,
                )

                recovery = clamp(
                    recovery
                    + 0.03 * recovery_capacity
                    + 0.03 * visibility
                    + 0.02 * buffer
                    + 0.02 * traceability
                    - 0.04 * disruption,
                    0.0,
                    1.5,
                )

                viability = clamp(
                    viability
                    + 0.04 * cost_efficiency
                    + 0.08 * adaptive_capacity
                    + 0.05 * recovery
                    - disruption
                    - 0.05 * exposure,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            exposure_values.append(exposure)
            recovery_values.append(recovery)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "supply_chain_viability": round(viability, 4),
                "disruption_exposure": round(exposure, 4),
                "recovery_score": round(recovery, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_viability": round(viability_values[-1], 4),
            "mean_viability": round(mean(viability_values), 4),
            "mean_disruption_exposure": round(mean(exposure_values), 4),
            "final_recovery_score": round(recovery_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    chokepoint_scores: list[dict[str, Any]],
    procurement_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Supply Chain Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['supply_chain_name']}**: resilience {row['supply_chain_resilience_score']}; "
            f"fragility {row['supply_chain_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: disruption pressure {row['disruption_pressure_score']}; "
            f"adaptation opportunity {row['adaptation_opportunity_score']}."
        )

    lines.extend(["", "## Resilience Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: resilience gain {row['resilience_gain_score']}; "
            f"implementation risk {row['implementation_risk_score']}."
        )

    lines.extend(["", "## Chokepoint Risk Priority Scores", ""])
    for row in chokepoint_scores:
        lines.append(
            f"- **{row['chokepoint_name']}**: priority {row['chokepoint_priority_score']}; "
            f"visibility gap {row['visibility_gap']}."
        )

    lines.extend(["", "## Procurement and Circularity Scores", ""])
    for row in procurement_scores:
        lines.append(
            f"- **{row['record_name']}**: public-interest governance score {row['public_interest_supply_governance_score']}; "
            f"implementation readiness {row['implementation_readiness']}."
        )

    lines.extend(["", "## Disruption Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_viability']}; "
            f"mean disruption exposure {row['mean_disruption_exposure']}; final recovery score {row['final_recovery_score']}."
        )

    avg_resilience = mean(float(row["supply_chain_resilience_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["supply_chain_fragility_score"]) for row in profile_scores)
    avg_viability = mean(float(row["final_viability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Supply chain profiles: {len(profile_scores)}.",
        f"- Supply chain scenarios: {len(scenario_scores)}.",
        f"- Resilience strategies: {len(strategy_scores)}.",
        f"- Chokepoint records: {len(chokepoint_scores)}.",
        f"- Procurement/circularity records: {len(procurement_scores)}.",
        f"- Average resilience score: {round(avg_resilience, 4)}.",
        f"- Average fragility score: {round(avg_fragility, 4)}.",
        f"- Average final viability: {round(avg_viability, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats supply chains as complex adaptive systems shaped by cost, diversification, buffers, visibility, labor accountability, climate adaptation, digital traceability, circularity, governance, and recovery capacity.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "supply_chain_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "supply_chain_profiles.csv")
    scenarios_raw = read_csv(DATA / "supply_chain_scenarios.csv")
    strategies_raw = read_csv(DATA / "resilience_strategies.csv")
    chokepoints_raw = read_csv(DATA / "chokepoint_risk_register.csv")
    procurement_raw = read_csv(DATA / "procurement_circularity_records.csv")
    pathways_raw = read_csv(DATA / "disruption_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, chokepoints_raw, procurement_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    chokepoint_scores = score_chokepoints(chokepoints_raw)
    procurement_scores = score_procurement_circularity(procurement_raw)
    trajectories, pathway_summary = simulate_disruption(pathways_raw)

    write_csv(OUTPUTS / "supply_chain_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "supply_chain_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "resilience_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "chokepoint_priority_scores.csv", chokepoint_scores)
    write_csv(OUTPUTS / "procurement_circularity_scores.csv", procurement_scores)
    write_csv(OUTPUTS / "disruption_pathways.csv", trajectories)
    write_csv(OUTPUTS / "disruption_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, chokepoint_scores, procurement_scores, pathway_summary)

    print(f"Supply chain futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
