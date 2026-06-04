#!/usr/bin/env python3
"""
Standard-library workflow for Security Futures and Hybrid Risk.

Outputs:
- security_profile_scores.csv
- security_scenario_scores.csv
- security_strategy_scores.csv
- hybrid_risk_priority_scores.csv
- infrastructure_cascade_scores.csv
- adaptive_security_trajectories.csv
- adaptive_security_summary.csv
- security_futures_hybrid_risk_report.md
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


def hybrid_risk_score(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["cyber_exposure"])
        + 0.13 * float(row["infrastructure_dependence"])
        + 0.13 * float(row["information_vulnerability"])
        + 0.12 * float(row["climate_security_stress"])
        + 0.10 * float(row["resource_dependence"])
        + 0.11 * (1.0 - float(row["institutional_coordination"]))
        + 0.10 * (1.0 - float(row["civilian_protection"]))
        + 0.10 * (1.0 - float(row["adaptive_resilience"]))
        + 0.05 * (1.0 - float(row["public_trust"]))
        + 0.03 * (1.0 - float(row["attribution_clarity"]))
    )


def security_resilience_score(row: dict[str, str]) -> float:
    return (
        0.20 * float(row["institutional_coordination"])
        + 0.22 * float(row["civilian_protection"])
        + 0.22 * float(row["adaptive_resilience"])
        + 0.16 * float(row["public_trust"])
        + 0.08 * float(row["attribution_clarity"])
        + 0.04 * (1.0 - float(row["cyber_exposure"]))
        + 0.04 * (1.0 - float(row["information_vulnerability"]))
        + 0.04 * (1.0 - float(row["infrastructure_dependence"]))
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    dependencies: list[dict[str, str]],
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

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Adaptive pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["cyber_exposure", "infrastructure_dependence", "information_vulnerability", "climate_security_stress", "resource_dependence", "institutional_coordination", "civilian_protection", "adaptive_resilience", "public_trust", "attribution_clarity"]),
        ("scenarios", scenarios, ["cyber_shock", "infrastructure_shock", "information_shock", "climate_shock", "resource_shock", "migration_pressure", "security_escalation", "institutional_fragmentation", "private_infrastructure_dependency", "civilian_harm_pressure"]),
        ("strategies", strategies, ["cyber_resilience_gain", "infrastructure_redundancy_gain", "information_integrity_gain", "climate_security_adaptation_gain", "resource_security_gain", "institutional_coordination_gain", "civilian_protection_gain", "deterrence_gain", "adaptive_learning_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "cascade_potential", "visibility_gap", "recovery_difficulty", "distributional_harm", "preparedness"]),
        ("dependencies", dependencies, ["dependency_weight", "disruption_sensitivity", "recovery_capacity", "public_harm_potential", "private_operator_dependency"]),
        ("pathways", pathways, ["initial_resilience", "cyber_exposure", "infrastructure_dependence", "information_vulnerability", "climate_security_stress", "resource_dependence", "institutional_coordination", "civilian_protection", "adaptive_resilience", "public_trust", "system_stress"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("dependency_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        risk = hybrid_risk_score(row)
        resilience = security_resilience_score(row)
        resilience_gap = max(0.0, risk - resilience)

        if risk >= 0.70:
            profile_class = "High hybrid security risk"
        elif resilience >= 0.65:
            profile_class = "Stronger security resilience"
        else:
            profile_class = "Mixed or transitional security future"

        rows.append({
            "profile_id": row["profile_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "hybrid_risk_score": round(risk, 4),
            "security_resilience_score": round(resilience, 4),
            "resilience_gap_score": round(resilience_gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["hybrid_risk_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.13 * float(row["cyber_shock"])
            + 0.13 * float(row["infrastructure_shock"])
            + 0.12 * float(row["information_shock"])
            + 0.12 * float(row["climate_shock"])
            + 0.10 * float(row["resource_shock"])
            + 0.08 * float(row["migration_pressure"])
            + 0.10 * float(row["security_escalation"])
            + 0.09 * float(row["institutional_fragmentation"])
            + 0.06 * float(row["private_infrastructure_dependency"])
            + 0.07 * float(row["civilian_harm_pressure"])
        )

        response_opportunity = (
            0.16 * (1.0 - float(row["institutional_fragmentation"]))
            + 0.14 * (1.0 - float(row["civilian_harm_pressure"]))
            + 0.12 * (1.0 - float(row["private_infrastructure_dependency"]))
            + 0.11 * (1.0 - float(row["information_shock"]))
            + 0.10 * (1.0 - float(row["infrastructure_shock"]))
            + 0.09 * (1.0 - float(row["cyber_shock"]))
            + 0.08 * (1.0 - float(row["climate_shock"]))
            + 0.07 * (1.0 - float(row["resource_shock"]))
            + 0.07 * (1.0 - float(row["security_escalation"]))
            + 0.06 * (1.0 - float(row["migration_pressure"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "hybrid_security_stress_score": round(stress, 4),
            "response_opportunity_score": round(response_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["hybrid_security_stress_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        value = (
            0.12 * float(row["cyber_resilience_gain"])
            + 0.12 * float(row["infrastructure_redundancy_gain"])
            + 0.12 * float(row["information_integrity_gain"])
            + 0.10 * float(row["climate_security_adaptation_gain"])
            + 0.09 * float(row["resource_security_gain"])
            + 0.12 * float(row["institutional_coordination_gain"])
            + 0.12 * float(row["civilian_protection_gain"])
            + 0.07 * float(row["deterrence_gain"])
            + 0.08 * float(row["adaptive_learning_gain"])
            + 0.03 * float(row["implementation_capacity"])
            + 0.03 * float(row["public_legitimacy_gain"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.16 * float(row["public_legitimacy_gain"])
            + 0.14 * float(row["institutional_coordination_gain"])
            + 0.12 * float(row["adaptive_learning_gain"])
            + 0.10 * float(row["civilian_protection_gain"])
            + 0.08 * float(row["cyber_resilience_gain"])
            + 0.08 * float(row["infrastructure_redundancy_gain"])
            + 0.06 * float(row["information_integrity_gain"])
            + 0.04 * float(row["climate_security_adaptation_gain"])
            + 0.02 * float(row["deterrence_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "security_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["security_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.18 * float(row["severity"])
            + 0.18 * float(row["cascade_potential"])
            + 0.10 * float(row["visibility_gap"])
            + 0.13 * float(row["recovery_difficulty"])
            + 0.17 * float(row["distributional_harm"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "hybrid_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["hybrid_risk_priority_score"]), reverse=True)
    return rows


def score_infrastructure_dependencies(dependencies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in dependencies:
        cascade = (
            float(row["dependency_weight"])
            * float(row["disruption_sensitivity"])
            * float(row["public_harm_potential"])
            * (1.0 - float(row["recovery_capacity"]))
        )

        public_private_risk = (
            0.40 * float(row["private_operator_dependency"])
            + 0.30 * float(row["public_harm_potential"])
            + 0.20 * float(row["disruption_sensitivity"])
            + 0.10 * (1.0 - float(row["recovery_capacity"]))
        )

        rows.append({
            "dependency_id": row["dependency_id"],
            "source_system": row["source_system"],
            "target_system": row["target_system"],
            "cascade_exposure_score": round(cascade, 4),
            "public_private_risk_score": round(public_private_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["cascade_exposure_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        resilience = float(row["initial_resilience"])
        cyber = float(row["cyber_exposure"])
        infra = float(row["infrastructure_dependence"])
        info = float(row["information_vulnerability"])
        climate = float(row["climate_security_stress"])
        resource = float(row["resource_dependence"])
        coordination = float(row["institutional_coordination"])
        protection = float(row["civilian_protection"])
        adaptive = float(row["adaptive_resilience"])
        trust = float(row["public_trust"])
        stress = float(row["system_stress"])
        horizon = int(row["time_horizon"])

        hybrid_risk = (
            0.16 * cyber
            + 0.15 * infra
            + 0.14 * info
            + 0.13 * climate
            + 0.10 * resource
            + 0.12 * (1.0 - coordination)
            + 0.10 * (1.0 - protection)
            + 0.10 * (1.0 - adaptive)
        )

        cascade_pressure = (
            0.26 * infra
            + 0.18 * cyber
            + 0.14 * resource
            + 0.12 * climate
            + 0.12 * (1.0 - coordination)
            + 0.10 * info
            + 0.08 * (1.0 - adaptive)
        )

        trust_state = trust

        risk_values: list[float] = []
        cascade_values: list[float] = []
        resilience_values: list[float] = []
        trust_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                ordinary_pressure = 0.04
                cyber_shock = 0.12 * cyber if t % 8 == 0 else 0.0
                infrastructure_shock = 0.10 * infra if t % 10 == 0 else 0.0
                information_shock = 0.09 * info if t % 9 == 0 else 0.0
                climate_shock = 0.11 * climate if t % 13 == 0 else 0.0
                resource_shock = 0.08 * resource if t % 11 == 0 else 0.0

                shock_total = ordinary_pressure + cyber_shock + infrastructure_shock + information_shock + climate_shock + resource_shock

                response_capacity = (
                    0.06 * coordination
                    + 0.06 * adaptive
                    + 0.04 * protection
                    + 0.03 * trust_state
                )

                cascade_pressure = clamp(
                    cascade_pressure
                    + shock_total
                    + 0.04 * infra
                    + 0.03 * cyber
                    + 0.03 * resource
                    - response_capacity,
                    0.0,
                    1.8,
                )

                hybrid_risk = clamp(
                    hybrid_risk
                    + 0.05 * cascade_pressure
                    + 0.04 * info
                    + 0.03 * climate
                    + shock_total
                    + 0.02 * stress
                    - response_capacity,
                    0.0,
                    1.8,
                )

                resilience = clamp(
                    resilience
                    + 0.04 * adaptive
                    + 0.03 * coordination
                    + 0.03 * protection
                    + 0.02 * trust_state
                    - 0.04 * hybrid_risk
                    - 0.02 * shock_total,
                    0.0,
                    1.8,
                )

                trust_state = clamp(
                    trust_state
                    + 0.04 * protection
                    + 0.03 * coordination
                    + 0.02 * adaptive
                    - 0.04 * information_shock
                    - 0.03 * hybrid_risk,
                    0.0,
                    1.8,
                )

            risk_values.append(hybrid_risk)
            cascade_values.append(cascade_pressure)
            resilience_values.append(resilience)
            trust_values.append(trust_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "hybrid_risk": round(hybrid_risk, 4),
                "cascade_pressure": round(cascade_pressure, 4),
                "security_resilience": round(resilience, 4),
                "public_trust": round(trust_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_hybrid_risk": round(risk_values[-1], 4),
            "mean_hybrid_risk": round(mean(risk_values), 4),
            "final_cascade_pressure": round(cascade_values[-1], 4),
            "final_security_resilience": round(resilience_values[-1], 4),
            "final_public_trust": round(trust_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_security_resilience"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    dependency_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Security Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['future_name']}**: hybrid risk {row['hybrid_risk_score']}; "
            f"security resilience {row['security_resilience_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: stress {row['hybrid_security_stress_score']}; "
            f"response opportunity {row['response_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['security_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Hybrid Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['hybrid_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; preparedness {row['preparedness']}."
        )

    lines.extend(["", "## Infrastructure Cascade Exposure", ""])
    for row in dependency_scores:
        lines.append(
            f"- **{row['source_system']} → {row['target_system']}**: cascade exposure {row['cascade_exposure_score']}; "
            f"public-private risk {row['public_private_risk_score']}."
        )

    lines.extend(["", "## Adaptive Security Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final hybrid risk {row['final_hybrid_risk']}; "
            f"final resilience {row['final_security_resilience']}; final public trust {row['final_public_trust']}."
        )

    avg_risk = mean(float(row["hybrid_risk_score"]) for row in profile_scores)
    avg_resilience = mean(float(row["security_resilience_score"]) for row in profile_scores)
    avg_strategy = mean(float(row["security_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Security profiles: {len(profile_scores)}.",
        f"- Scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Infrastructure dependencies: {len(dependency_scores)}.",
        f"- Average hybrid risk score: {round(avg_risk, 4)}.",
        f"- Average security resilience score: {round(avg_resilience, 4)}.",
        f"- Average strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats security futures and hybrid risk as systems shaped by cyber exposure, infrastructure dependence, information vulnerability, climate-security stress, resource dependence, institutional coordination, civilian protection, adaptive resilience, public trust, attribution clarity, and cascade exposure.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "security_futures_hybrid_risk_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "security_profiles.csv")
    scenarios_raw = read_csv(DATA / "security_scenarios.csv")
    strategies_raw = read_csv(DATA / "security_strategy_options.csv")
    risks_raw = read_csv(DATA / "security_risk_indicators.csv")
    dependencies_raw = read_csv(DATA / "infrastructure_dependencies.csv")
    pathways_raw = read_csv(DATA / "adaptive_security_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, dependencies_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    dependency_scores = score_infrastructure_dependencies(dependencies_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "security_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "security_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "security_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "hybrid_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "infrastructure_cascade_scores.csv", dependency_scores)
    write_csv(OUTPUTS / "adaptive_security_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_security_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, strategy_scores, risk_scores, dependency_scores, pathway_summary)

    print(f"Security futures and hybrid risk workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
