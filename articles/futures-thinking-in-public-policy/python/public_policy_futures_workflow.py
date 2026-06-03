#!/usr/bin/env python3
"""
Standard-library workflow for Futures Thinking in Public Policy.

Outputs:
- policy_option_scores.csv
- scenario_profile_scores.csv
- institutional_capacity_scores.csv
- policy_risk_scores.csv
- adaptive_policy_pathways.csv
- adaptive_policy_pathway_summary.csv
- strategy_option_scores.csv
- public_policy_futures_report.md
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


def policy_futures_profile(row: dict[str, str]) -> float:
    robustness = float(row["robustness"])
    equity = float(row["equity"])
    adaptability = float(row["adaptability"])
    coordination = float(row["coordination"])
    legitimacy = float(row["legitimacy"])
    implementation = float(row["implementation_capacity"])
    learning = float(row["learning_capacity"])
    intergenerational = float(row["intergenerational_responsibility"])

    return (
        0.20 * robustness
        + 0.16 * equity
        + 0.18 * adaptability
        + 0.14 * coordination
        + 0.14 * legitimacy
        + 0.08 * implementation
        + 0.06 * learning
        + 0.04 * intergenerational
    )


def policy_fragility_pressure(row: dict[str, str]) -> float:
    robustness = float(row["robustness"])
    equity = float(row["equity"])
    adaptability = float(row["adaptability"])
    coordination = float(row["coordination"])
    legitimacy = float(row["legitimacy"])
    implementation = float(row["implementation_capacity"])
    learning = float(row["learning_capacity"])

    return (
        0.20 * (1.0 - robustness)
        + 0.18 * (1.0 - adaptability)
        + 0.16 * (1.0 - coordination)
        + 0.14 * (1.0 - legitimacy)
        + 0.12 * (1.0 - equity)
        + 0.10 * (1.0 - learning)
        + 0.10 * (1.0 - implementation)
    )


def validate_records(
    policies: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    capacity: list[dict[str, str]],
    risks: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    policy_ids = {row["policy_id"] for row in policies}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["policy_id"] not in policy_ids:
            errors.append(f"Risk {row['risk_id']} references missing policy {row['policy_id']}.")

    for row in pathways:
        if row["policy_id"] not in policy_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing policy {row['policy_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("policies", policies, ["robustness", "equity", "adaptability", "coordination", "legitimacy", "implementation_capacity", "political_feasibility", "learning_capacity", "intergenerational_responsibility"]),
        ("scenarios", scenarios, ["economic_volatility", "technological_disruption", "climate_stress", "demographic_pressure", "geopolitical_instability", "public_trust", "institutional_capacity", "fiscal_space"]),
        ("capacity", capacity, ["detection_capacity", "learning_capacity", "coordination_quality", "budget_alignment", "implementation_capacity", "public_participation", "data_infrastructure", "accountability_capacity"]),
        ("risks", risks, ["probability", "severity", "detection_difficulty", "governance_gap", "equity_exposure", "implementation_exposure", "mitigation_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("policy_id") or row.get("scenario_id") or row.get("capacity_id") or row.get("risk_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_policies(policies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in policies:
        profile = policy_futures_profile(row)
        fragility = policy_fragility_pressure(row)

        long_term = (
            0.26 * float(row["intergenerational_responsibility"])
            + 0.20 * float(row["learning_capacity"])
            + 0.18 * float(row["robustness"])
            + 0.16 * float(row["equity"])
            + 0.12 * float(row["legitimacy"])
            + 0.08 * float(row["adaptability"])
        )

        if profile >= 0.72:
            policy_class = "Strong futures-oriented policy profile"
        elif fragility >= 0.55:
            policy_class = "High policy fragility pressure"
        else:
            policy_class = "Contested policy profile"

        rows.append({
            "policy_id": row["policy_id"],
            "policy_name": row["policy_name"],
            "policy_domain": row["policy_domain"],
            "policy_futures_profile_score": round(profile, 4),
            "policy_fragility_pressure_score": round(fragility, 4),
            "long_term_responsibility_score": round(long_term, 4),
            "policy_class": policy_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["policy_futures_profile_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.18 * float(row["economic_volatility"])
            + 0.16 * float(row["technological_disruption"])
            + 0.18 * float(row["climate_stress"])
            + 0.12 * float(row["demographic_pressure"])
            + 0.16 * float(row["geopolitical_instability"])
            + 0.10 * (1.0 - float(row["public_trust"]))
            + 0.06 * (1.0 - float(row["institutional_capacity"]))
            + 0.04 * (1.0 - float(row["fiscal_space"]))
        )

        governance_opportunity = (
            0.24 * float(row["public_trust"])
            + 0.24 * float(row["institutional_capacity"])
            + 0.18 * float(row["fiscal_space"])
            + 0.12 * (1.0 - float(row["economic_volatility"]))
            + 0.10 * (1.0 - float(row["geopolitical_instability"]))
            + 0.12 * (1.0 - float(row["climate_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "policy_stress_pressure_score": round(stress, 4),
            "governance_opportunity_score": round(governance_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["policy_stress_pressure_score"]), reverse=True)
    return rows


def score_capacity(capacity_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in capacity_rows:
        score = (
            0.18 * float(row["detection_capacity"])
            + 0.18 * float(row["learning_capacity"])
            + 0.16 * float(row["coordination_quality"])
            + 0.12 * float(row["budget_alignment"])
            + 0.12 * float(row["implementation_capacity"])
            + 0.10 * float(row["public_participation"])
            + 0.08 * float(row["data_infrastructure"])
            + 0.06 * float(row["accountability_capacity"])
        )

        rows.append({
            "capacity_id": row["capacity_id"],
            "institution_name": row["institution_name"],
            "institution_type": row["institution_type"],
            "anticipatory_governance_capacity_score": round(score, 4),
            "capacity_gap_score": round(1.0 - score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["anticipatory_governance_capacity_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.18 * float(row["probability"])
            + 0.20 * float(row["severity"])
            + 0.14 * float(row["detection_difficulty"])
            + 0.16 * float(row["governance_gap"])
            + 0.12 * float(row["equity_exposure"])
            + 0.12 * float(row["implementation_exposure"])
            + 0.08 * (1.0 - float(row["mitigation_capacity"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "policy_id": row["policy_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "policy_risk_priority_score": round(priority, 4),
            "mitigation_capacity": float(row["mitigation_capacity"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["policy_risk_priority_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        robustness = float(row["robustness"])
        adaptability = float(row["adaptability"])
        coordination = float(row["coordination"])
        legitimacy = float(row["legitimacy"])
        equity = float(row["equity"])
        implementation = float(row["implementation_capacity"])
        learning = float(row["learning_capacity"])
        viability = float(row["initial_viability"])
        legitimacy_state = legitimacy
        equity_state = equity
        adaptive_learning = learning
        horizon = int(row["time_horizon"])

        viability_values: list[float] = []
        legitimacy_values: list[float] = []
        equity_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.17 if t % 8 == 0 else 0.06

                response_gain = (
                    0.22 * robustness
                    + 0.24 * adaptability
                    + 0.20 * coordination
                    + 0.16 * legitimacy
                    + 0.12 * equity
                    + 0.06 * learning
                )

                implementation_drag = 0.10 * (1.0 - implementation)
                trust_drag = 0.06 * (1.0 - legitimacy_state)
                inequity_drag = 0.06 * (1.0 - equity_state)

                adaptive_learning = clamp(
                    adaptive_learning
                    + 0.04 * learning
                    + 0.03 * adaptability
                    + 0.02 * coordination
                    - 0.04 * disruption,
                    0.0,
                    1.4,
                )

                legitimacy_state = clamp(
                    legitimacy_state
                    + 0.04 * legitimacy
                    + 0.03 * equity
                    + 0.02 * coordination
                    - 0.04 * disruption
                    - 0.02 * (1.0 - implementation),
                    0.0,
                    1.4,
                )

                equity_state = clamp(
                    equity_state
                    + 0.04 * equity
                    + 0.02 * coordination
                    + 0.02 * learning
                    - 0.03 * disruption,
                    0.0,
                    1.4,
                )

                viability = clamp(
                    viability
                    - disruption
                    + response_gain / 4.0
                    + 0.04 * adaptive_learning
                    - implementation_drag
                    - trust_drag
                    - inequity_drag,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            legitimacy_values.append(legitimacy_state)
            equity_values.append(equity_state)
            learning_values.append(adaptive_learning)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "policy_id": row["policy_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "policy_viability": round(viability, 4),
                "legitimacy_score": round(legitimacy_state, 4),
                "equity_score": round(equity_state, 4),
                "adaptive_learning_score": round(adaptive_learning, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "policy_id": row["policy_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_policy_viability": round(viability_values[-1], 4),
            "mean_policy_viability": round(mean(viability_values), 4),
            "final_legitimacy_score": round(legitimacy_values[-1], 4),
            "final_equity_score": round(equity_values[-1], 4),
            "final_adaptive_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_policy_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        score = (
            0.12 * float(row["horizon_scanning"])
            + 0.14 * float(row["scenario_planning"])
            + 0.16 * float(row["adaptive_policy_design"])
            + 0.14 * float(row["public_participation"])
            + 0.12 * float(row["budget_alignment"])
            + 0.12 * float(row["evaluation_capacity"])
            + 0.10 * float(row["interagency_coordination"])
            + 0.06 * float(row["equity_analysis"])
            + 0.04 * float(row["implementation_support"])
        )

        operational = (
            0.18 * float(row["budget_alignment"])
            + 0.18 * float(row["implementation_support"])
            + 0.16 * float(row["evaluation_capacity"])
            + 0.14 * float(row["interagency_coordination"])
            + 0.12 * float(row["adaptive_policy_design"])
            + 0.10 * float(row["horizon_scanning"])
            + 0.06 * float(row["scenario_planning"])
            + 0.06 * float(row["equity_analysis"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "foresight_capacity_strategy_score": round(score, 4),
            "operational_governance_strategy_score": round(operational, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["foresight_capacity_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    policies: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    capacity: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Policy Option Scores",
        "",
    ]

    for row in policies:
        lines.append(
            f"- **{row['policy_name']}**: futures profile {row['policy_futures_profile_score']}; "
            f"fragility pressure {row['policy_fragility_pressure_score']}; class: {row['policy_class']}."
        )

    lines.extend(["", "## Scenario Stress Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: stress pressure {row['policy_stress_pressure_score']}; "
            f"governance opportunity {row['governance_opportunity_score']}."
        )

    lines.extend(["", "## Institutional Capacity Scores", ""])
    for row in capacity:
        lines.append(
            f"- **{row['institution_name']}**: anticipatory capacity {row['anticipatory_governance_capacity_score']}; "
            f"capacity gap {row['capacity_gap_score']}."
        )

    lines.extend(["", "## Policy Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['policy_risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Adaptive Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_policy_viability']}; "
            f"final legitimacy {row['final_legitimacy_score']}; final equity {row['final_equity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: foresight capacity strategy {row['foresight_capacity_strategy_score']}; "
            f"operational governance strategy {row['operational_governance_strategy_score']}."
        )

    avg_policy = mean(float(row["policy_futures_profile_score"]) for row in policies)
    avg_capacity = mean(float(row["anticipatory_governance_capacity_score"]) for row in capacity)
    avg_risk = mean(float(row["policy_risk_priority_score"]) for row in risks)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Policy options: {len(policies)}.",
        f"- Scenario profiles: {len(scenarios)}.",
        f"- Institutional capacity records: {len(capacity)}.",
        f"- Policy risk records: {len(risks)}.",
        f"- Average policy futures profile score: {round(avg_policy, 4)}.",
        f"- Average anticipatory governance capacity score: {round(avg_capacity, 4)}.",
        f"- Average policy risk priority score: {round(avg_risk, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats futures thinking in public policy as an applied governance capability. It compares robustness, equity, adaptability, coordination, legitimacy, implementation capacity, learning capacity, intergenerational responsibility, institutional capacity, political feasibility, risk pressure, and adaptive pathway performance.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "public_policy_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    policies_raw = read_csv(DATA / "policy_options.csv")
    scenarios_raw = read_csv(DATA / "scenario_profiles.csv")
    capacity_raw = read_csv(DATA / "institutional_capacity.csv")
    risks_raw = read_csv(DATA / "policy_risk_register.csv")
    pathways_raw = read_csv(DATA / "adaptive_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(policies_raw, scenarios_raw, capacity_raw, risks_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    policies = score_policies(policies_raw)
    scenarios = score_scenarios(scenarios_raw)
    capacity = score_capacity(capacity_raw)
    risks = score_risks(risks_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "policy_option_scores.csv", policies)
    write_csv(OUTPUTS / "scenario_profile_scores.csv", scenarios)
    write_csv(OUTPUTS / "institutional_capacity_scores.csv", capacity)
    write_csv(OUTPUTS / "policy_risk_scores.csv", risks)
    write_csv(OUTPUTS / "adaptive_policy_pathways.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_policy_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, policies, scenarios, capacity, risks, pathway_summary, strategies)

    print(f"Public policy futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
