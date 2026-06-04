#!/usr/bin/env python3
"""
Standard-library workflow for Future Directions in Strategic Foresight.

Outputs:
- foresight_capability_scores.csv
- foresight_system_scenario_scores.csv
- foresight_strategy_scores.csv
- foresight_risk_priority_scores.csv
- foresight_signal_priority_scores.csv
- adaptive_strategy_trajectories.csv
- adaptive_strategy_summary.csv
- future_directions_strategic_foresight_report.md
"""

from __future__ import annotations

import csv
import json
import math
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


def capability_score(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["signal_detection"])
        + 0.16 * float(row["scenario_capability"])
        + 0.14 * float(row["learning_capacity"])
        + 0.14 * float(row["governance_integration"])
        + 0.12 * float(row["adaptive_flexibility"])
        + 0.10 * float(row["participatory_legitimacy"])
        + 0.10 * float(row["ethical_accountability"])
        + 0.08 * float(row["data_infrastructure"])
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    signals: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    institution_ids = {row["institution_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in strategies:
        if row["institution_id"] not in institution_ids:
            errors.append(f"Strategy {row['strategy_id']} references missing institution {row['institution_id']}.")

    for row in risks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Risk indicator {row['risk_id']} references missing scenario {row['scenario_id']}.")

    for row in pathways:
        if row["institution_id"] not in institution_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing institution {row['institution_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["signal_detection", "scenario_capability", "learning_capacity", "governance_integration", "adaptive_flexibility", "participatory_legitimacy", "ethical_accountability", "data_infrastructure", "ai_readiness", "public_legitimacy"]),
        ("scenarios", scenarios, ["signal_velocity", "uncertainty_load", "data_quality", "ai_dependence", "governance_authority", "participatory_depth", "ethical_risk", "institutional_learning", "coordination_complexity"]),
        ("strategies", strategies, ["signal_pipeline_gain", "scenario_update_gain", "governance_integration_gain", "data_system_gain", "participatory_legitimacy_gain", "ethical_accountability_gain", "adaptive_strategy_gain", "ai_audit_gain", "learning_capacity_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "visibility_gap", "governance_gap", "legitimacy_gap", "preparedness"]),
        ("signals", signals, ["signal_strength", "signal_velocity", "novelty", "relevance", "source_quality", "interpretive_confidence", "uncertainty"]),
        ("pathways", pathways, ["signal_detection", "scenario_capability", "learning_capacity", "governance_integration", "adaptive_flexibility", "participatory_legitimacy", "ethical_accountability", "data_infrastructure"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("institution_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("signal_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in profiles:
        capability = capability_score(row)
        technical = (
            0.35 * float(row["signal_detection"])
            + 0.35 * float(row["scenario_capability"])
            + 0.30 * float(row["data_infrastructure"])
        )
        governance = (
            0.45 * float(row["governance_integration"])
            + 0.30 * float(row["adaptive_flexibility"])
            + 0.25 * float(row["learning_capacity"])
        )
        legitimacy = (
            0.40 * float(row["participatory_legitimacy"])
            + 0.35 * float(row["ethical_accountability"])
            + 0.25 * float(row["public_legitimacy"])
        )
        capability_gap = max(0.0, technical - ((governance + legitimacy) / 2.0))

        if capability >= 0.70:
            maturity = "High integrated foresight capability"
        elif capability_gap >= 0.18:
            maturity = "Technically capable but weakly integrated"
        elif float(row["governance_integration"]) < 0.50:
            maturity = "Governance integration gap"
        elif float(row["participatory_legitimacy"]) < 0.50:
            maturity = "Participation and legitimacy gap"
        else:
            maturity = "Developing foresight capability"

        rows.append({
            "institution_id": row["institution_id"],
            "institution_type": row["institution_type"],
            "sector": row["sector"],
            "foresight_capability_score": round(capability, 4),
            "technical_capability_score": round(technical, 4),
            "governance_capability_score": round(governance, 4),
            "legitimacy_capability_score": round(legitimacy, 4),
            "capability_gap_score": round(capability_gap, 4),
            "maturity_class": maturity,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_capability_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        system_risk = (
            0.12 * float(row["signal_velocity"])
            + 0.16 * float(row["uncertainty_load"])
            + 0.10 * (1.0 - float(row["data_quality"]))
            + 0.10 * float(row["ai_dependence"])
            + 0.16 * (1.0 - float(row["governance_authority"]))
            + 0.10 * (1.0 - float(row["participatory_depth"]))
            + 0.12 * float(row["ethical_risk"])
            + 0.08 * (1.0 - float(row["institutional_learning"]))
            + 0.06 * float(row["coordination_complexity"])
        )

        transformation_opportunity = (
            0.14 * float(row["data_quality"])
            + 0.14 * float(row["governance_authority"])
            + 0.14 * float(row["participatory_depth"])
            + 0.14 * float(row["institutional_learning"])
            + 0.12 * (1.0 - float(row["ethical_risk"]))
            + 0.10 * (1.0 - float(row["uncertainty_load"]))
            + 0.08 * (1.0 - float(row["coordination_complexity"]))
            + 0.08 * float(row["signal_velocity"])
            + 0.04 * (1.0 - float(row["ai_dependence"]))
            + 0.02 * float(row["data_quality"])
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "foresight_system_risk_score": round(system_risk, 4),
            "transformation_opportunity_score": round(transformation_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_system_risk_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        capability_gain = (
            0.11 * float(row["signal_pipeline_gain"])
            + 0.12 * float(row["scenario_update_gain"])
            + 0.14 * float(row["governance_integration_gain"])
            + 0.10 * float(row["data_system_gain"])
            + 0.11 * float(row["participatory_legitimacy_gain"])
            + 0.11 * float(row["ethical_accountability_gain"])
            + 0.12 * float(row["adaptive_strategy_gain"])
            + 0.07 * float(row["ai_audit_gain"])
            + 0.08 * float(row["learning_capacity_gain"])
            + 0.02 * float(row["implementation_capacity"])
            + 0.02 * float(row["public_legitimacy_gain"])
        )

        implementation_readiness = (
            0.22 * float(row["implementation_capacity"])
            + 0.14 * float(row["public_legitimacy_gain"])
            + 0.12 * float(row["governance_integration_gain"])
            + 0.10 * float(row["data_system_gain"])
            + 0.10 * float(row["learning_capacity_gain"])
            + 0.09 * float(row["adaptive_strategy_gain"])
            + 0.08 * float(row["signal_pipeline_gain"])
            + 0.07 * float(row["scenario_update_gain"])
            + 0.04 * float(row["participatory_legitimacy_gain"])
            + 0.04 * float(row["ethical_accountability_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "institution_id": row["institution_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "foresight_capability_gain_score": round(capability_gain, 4),
            "implementation_readiness_score": round(implementation_readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_capability_gain_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.17 * float(row["severity"])
            + 0.12 * float(row["irreversibility"])
            + 0.12 * float(row["visibility_gap"])
            + 0.18 * float(row["governance_gap"])
            + 0.17 * float(row["legitimacy_gap"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "foresight_risk_priority_score": round(priority, 4),
            "governance_gap": float(row["governance_gap"]),
            "legitimacy_gap": float(row["legitimacy_gap"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_risk_priority_score"]), reverse=True)
    return rows


def score_signals(signals: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in signals:
        attention = (
            0.16 * float(row["signal_strength"])
            + 0.14 * float(row["signal_velocity"])
            + 0.10 * float(row["novelty"])
            + 0.20 * float(row["relevance"])
            + 0.14 * float(row["source_quality"])
            + 0.14 * float(row["interpretive_confidence"])
            + 0.12 * float(row["uncertainty"])
        )

        ambiguity = float(row["uncertainty"]) * (1.0 - float(row["interpretive_confidence"]))

        rows.append({
            "signal_id": row["signal_id"],
            "domain": row["domain"],
            "signal_name": row["signal_name"],
            "strategic_attention_score": round(attention, 4),
            "ambiguity_score": round(ambiguity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["strategic_attention_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        signal = float(row["signal_detection"])
        scenario = float(row["scenario_capability"])
        learning = float(row["learning_capacity"])
        governance = float(row["governance_integration"])
        adaptive = float(row["adaptive_flexibility"])
        participation = float(row["participatory_legitimacy"])
        ethics = float(row["ethical_accountability"])
        data = float(row["data_infrastructure"])
        horizon = int(row["time_horizon"])

        capability_values: list[float] = []
        governance_values: list[float] = []
        learning_values: list[float] = []
        adaptive_values: list[float] = []
        legitimacy_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                signal_shock = 0.012 if t % 6 == 0 else 0.0
                crisis_pressure = 0.014 if t % 10 == 0 else 0.0
                review_cycle = 0.014 if t % 12 == 0 else 0.0
                governance_drift = 0.010 if t % 17 == 0 else 0.0

                signal = clamp(signal + signal_shock + 0.006 * data + 0.004 * learning - 0.004 * crisis_pressure, 0.0, 1.8)
                scenario = clamp(scenario + 0.008 * signal + 0.006 * learning + review_cycle - 0.006 * governance_drift, 0.0, 1.8)
                learning = clamp(learning + 0.008 * scenario + 0.006 * governance + review_cycle - 0.005 * crisis_pressure, 0.0, 1.8)
                governance = clamp(governance + 0.007 * learning + 0.006 * participation + 0.005 * ethics - governance_drift - 0.004 * crisis_pressure, 0.0, 1.8)
                adaptive = clamp(adaptive + 0.008 * learning + 0.007 * governance + 0.006 * scenario - 0.006 * crisis_pressure, 0.0, 1.8)
                participation = clamp(participation + 0.006 * governance + 0.005 * ethics + review_cycle - 0.004 * governance_drift, 0.0, 1.8)
                ethics = clamp(ethics + 0.006 * participation + 0.006 * governance + 0.004 * learning - 0.004 * crisis_pressure, 0.0, 1.8)
                data = clamp(data + 0.006 * signal + 0.005 * scenario + 0.004 * learning - 0.003 * governance_drift, 0.0, 1.8)

            capability = (
                0.16 * signal
                + 0.16 * scenario
                + 0.14 * learning
                + 0.14 * governance
                + 0.12 * adaptive
                + 0.10 * participation
                + 0.10 * ethics
                + 0.08 * data
            )
            legitimacy = (0.40 * participation + 0.35 * ethics + 0.25 * governance)

            capability_values.append(capability)
            governance_values.append(governance)
            learning_values.append(learning)
            adaptive_values.append(adaptive)
            legitimacy_values.append(legitimacy)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "institution_id": row["institution_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "signal_detection": round(signal, 4),
                "scenario_capability": round(scenario, 4),
                "learning_capacity": round(learning, 4),
                "governance_integration": round(governance, 4),
                "adaptive_flexibility": round(adaptive, 4),
                "participatory_legitimacy": round(participation, 4),
                "ethical_accountability": round(ethics, 4),
                "data_infrastructure": round(data, 4),
                "foresight_capability_score": round(capability, 4),
                "legitimacy_score": round(legitimacy, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "institution_id": row["institution_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_foresight_capability_score": round(capability_values[-1], 4),
            "mean_foresight_capability_score": round(mean(capability_values), 4),
            "final_governance_integration": round(governance_values[-1], 4),
            "final_learning_capacity": round(learning_values[-1], 4),
            "final_adaptive_flexibility": round(adaptive_values[-1], 4),
            "final_legitimacy_score": round(legitimacy_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_foresight_capability_score"]), reverse=True)
    return trajectory_rows, summary_rows


def generate_dynamic_scenario_update() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for t in range(1, 61):
        signal_a = max(0.0, min(1.0, 0.30 + (0.48 * (t - 1) / 59.0) + 0.025 * math.sin(t / 3.0)))
        signal_b = max(0.0, min(1.0, 0.52 - (0.14 * (t - 1) / 59.0) + 0.020 * math.cos(t / 4.0)))
        signal_c = max(0.0, min(1.0, 0.22 + (0.40 * (t - 1) / 59.0) + 0.030 * math.sin(t / 5.0)))

        total = signal_a + signal_b + signal_c
        wa = signal_a / total
        wb = signal_b / total
        wc = signal_c / total

        uncertainty_load = 1.0 - max(wa, wb, wc)
        learning_capacity = max(0.0, min(1.0, 0.42 + 0.006 * t + 0.015 * math.sin(t / 6.0)))

        rows.append({
            "time_step": t,
            "scenario_a_weight": round(wa, 4),
            "scenario_b_weight": round(wb, 4),
            "scenario_c_weight": round(wc, 4),
            "uncertainty_load": round(uncertainty_load, 4),
            "learning_capacity": round(learning_capacity, 4),
        })

    return rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    signal_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Foresight Capability Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['institution_type']}**: capability {row['foresight_capability_score']}; "
            f"technical {row['technical_capability_score']}; governance {row['governance_capability_score']}; "
            f"legitimacy {row['legitimacy_capability_score']}; class: {row['maturity_class']}."
        )

    lines.extend(["", "## Foresight System Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: system risk {row['foresight_system_risk_score']}; "
            f"transformation opportunity {row['transformation_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: capability gain {row['foresight_capability_gain_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['foresight_risk_priority_score']}; "
            f"governance gap {row['governance_gap']}; legitimacy gap {row['legitimacy_gap']}."
        )

    lines.extend(["", "## Signal Priority Scores", ""])
    for row in signal_scores:
        lines.append(
            f"- **{row['signal_name']}**: attention {row['strategic_attention_score']}; "
            f"ambiguity {row['ambiguity_score']}."
        )

    lines.extend(["", "## Adaptive Strategy Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final capability {row['final_foresight_capability_score']}; "
            f"final governance {row['final_governance_integration']}; final legitimacy {row['final_legitimacy_score']}."
        )

    avg_capability = mean(float(row["foresight_capability_score"]) for row in profile_scores)
    avg_risk = mean(float(row["foresight_risk_priority_score"]) for row in risk_scores)
    avg_strategy = mean(float(row["foresight_capability_gain_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Institutional profiles: {len(profile_scores)}.",
        f"- Foresight scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Signal records: {len(signal_scores)}.",
        f"- Average foresight capability score: {round(avg_capability, 4)}.",
        f"- Average risk priority score: {round(avg_risk, 4)}.",
        f"- Average strategy capability gain score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats next-generation foresight as an integrated capability that combines signal detection, scenario infrastructure, learning, governance, participation, ethics, data systems, AI readiness, and adaptive strategy.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "future_directions_strategic_foresight_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "foresight_capability_profiles.csv")
    scenarios_raw = read_csv(DATA / "foresight_system_scenarios.csv")
    strategies_raw = read_csv(DATA / "foresight_strategy_options.csv")
    risks_raw = read_csv(DATA / "foresight_risk_indicators.csv")
    signals_raw = read_csv(DATA / "foresight_signal_records.csv")
    pathways_raw = read_csv(DATA / "adaptive_strategy_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, signals_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    signal_scores = score_signals(signals_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    dynamic_update = generate_dynamic_scenario_update()

    write_csv(OUTPUTS / "foresight_capability_scores.csv", profile_scores)
    write_csv(OUTPUTS / "foresight_system_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "foresight_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "foresight_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "foresight_signal_priority_scores.csv", signal_scores)
    write_csv(OUTPUTS / "adaptive_strategy_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_strategy_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "dynamic_scenario_updating.csv", dynamic_update)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, signal_scores, pathway_summary)

    print(f"Future directions strategic foresight workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
