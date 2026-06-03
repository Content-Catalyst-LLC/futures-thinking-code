#!/usr/bin/env python3
"""
Standard-library workflow for Law, Regulation, and Emerging Futures.

Outputs:
- regulatory_model_scores.csv
- emerging_risk_scores.csv
- rights_remedy_scores.csv
- sandbox_safeguard_scores.csv
- regulatory_scenario_scores.csv
- adaptive_regulatory_pathways.csv
- adaptive_regulatory_pathway_summary.csv
- strategy_option_scores.csv
- regulatory_futures_report.md
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


def regulatory_capacity(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["foresight_capacity"])
        + 0.12 * float(row["monitoring_capacity"])
        + 0.12 * float(row["enforcement_capacity"])
        + 0.14 * float(row["rights_protection"])
        + 0.10 * float(row["public_participation"])
        + 0.12 * float(row["revision_authority"])
        + 0.10 * float(row["regulatory_learning"])
        + 0.08 * float(row["capture_resistance"])
        + 0.05 * float(row["legal_certainty"])
        + 0.04 * float(row["remedy_access"])
    )


def regulatory_lag_pressure(row: dict[str, str]) -> float:
    return (
        0.16 * (1.0 - float(row["foresight_capacity"]))
        + 0.14 * (1.0 - float(row["monitoring_capacity"]))
        + 0.14 * (1.0 - float(row["revision_authority"]))
        + 0.12 * (1.0 - float(row["regulatory_learning"]))
        + 0.12 * (1.0 - float(row["enforcement_capacity"]))
        + 0.10 * (1.0 - float(row["rights_protection"]))
        + 0.08 * (1.0 - float(row["public_participation"]))
        + 0.08 * (1.0 - float(row["capture_resistance"]))
        + 0.06 * (1.0 - float(row["remedy_access"]))
    )


def validate_records(
    models: list[dict[str, str]],
    risks: list[dict[str, str]],
    rights: list[dict[str, str]],
    sandboxes: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    model_ids = {row["model_id"] for row in models}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["model_id"] not in model_ids:
            errors.append(f"Risk {row['risk_id']} references missing model {row['model_id']}.")

    for row in rights:
        if row["model_id"] not in model_ids:
            errors.append(f"Rights record {row['remedy_id']} references missing model {row['model_id']}.")

    for row in sandboxes:
        if row["model_id"] not in model_ids:
            errors.append(f"Sandbox {row['sandbox_id']} references missing model {row['model_id']}.")

    for row in pathways:
        if row["model_id"] not in model_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing model {row['model_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("models", models, ["foresight_capacity", "monitoring_capacity", "enforcement_capacity", "rights_protection", "public_participation", "revision_authority", "regulatory_learning", "capture_resistance", "legal_certainty", "remedy_access"]),
        ("risks", risks, ["change_velocity", "harm_severity", "uncertainty", "irreversibility", "distributional_exposure", "regulatory_gap", "mitigation_capacity"]),
        ("rights", rights, ["notice", "explanation", "appeal", "audit_access", "public_enforcement", "collective_remedy", "compensation", "accessibility"]),
        ("sandboxes", sandboxes, ["public_interest_test", "eligibility_transparency", "rights_nonwaiver", "participant_consent", "independent_evaluation", "exit_conditions", "public_reporting", "capture_control"]),
        ("scenarios", scenarios, ["technology_acceleration", "climate_stress", "public_trust", "institutional_capacity", "capture_pressure", "rights_risk", "international_fragmentation", "learning_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("model_id") or row.get("scenario_id") or row.get("risk_id") or row.get("remedy_id") or row.get("sandbox_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_models(models: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in models:
        capacity = regulatory_capacity(row)
        lag = regulatory_lag_pressure(row)

        if capacity >= 0.74:
            model_class = "Strong future-ready regulatory capacity"
        elif lag >= 0.55:
            model_class = "High regulatory lag or capture risk"
        else:
            model_class = "Developing regulatory futures capacity"

        rows.append({
            "model_id": row["model_id"],
            "regulatory_model": row["regulatory_model"],
            "model_type": row["model_type"],
            "future_ready_regulatory_capacity_score": round(capacity, 4),
            "regulatory_lag_pressure_score": round(lag, 4),
            "regulatory_class": model_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_ready_regulatory_capacity_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        priority = (
            0.16 * float(row["change_velocity"])
            + 0.18 * float(row["harm_severity"])
            + 0.13 * float(row["uncertainty"])
            + 0.15 * float(row["irreversibility"])
            + 0.15 * float(row["distributional_exposure"])
            + 0.15 * float(row["regulatory_gap"])
            + 0.08 * (1.0 - float(row["mitigation_capacity"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "model_id": row["model_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "emerging_regulatory_risk_score": round(priority, 4),
            "mitigation_capacity": float(row["mitigation_capacity"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["emerging_regulatory_risk_score"]), reverse=True)
    return rows


def score_rights(rights: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in rights:
        score = (
            0.14 * float(row["notice"])
            + 0.14 * float(row["explanation"])
            + 0.15 * float(row["appeal"])
            + 0.15 * float(row["audit_access"])
            + 0.14 * float(row["public_enforcement"])
            + 0.12 * float(row["collective_remedy"])
            + 0.08 * float(row["compensation"])
            + 0.08 * float(row["accessibility"])
        )

        rows.append({
            "remedy_id": row["remedy_id"],
            "model_id": row["model_id"],
            "rights_domain": row["rights_domain"],
            "rights_remedy_strength_score": round(score, 4),
            "appeal": float(row["appeal"]),
            "audit_access": float(row["audit_access"]),
            "accessibility": float(row["accessibility"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["rights_remedy_strength_score"]), reverse=True)
    return rows


def score_sandboxes(sandboxes: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in sandboxes:
        score = (
            0.14 * float(row["public_interest_test"])
            + 0.12 * float(row["eligibility_transparency"])
            + 0.16 * float(row["rights_nonwaiver"])
            + 0.12 * float(row["participant_consent"])
            + 0.14 * float(row["independent_evaluation"])
            + 0.12 * float(row["exit_conditions"])
            + 0.10 * float(row["public_reporting"])
            + 0.10 * float(row["capture_control"])
        )

        capture_risk = 1.0 - (
            0.25 * float(row["capture_control"])
            + 0.20 * float(row["public_reporting"])
            + 0.20 * float(row["independent_evaluation"])
            + 0.20 * float(row["eligibility_transparency"])
            + 0.15 * float(row["public_interest_test"])
        )

        rows.append({
            "sandbox_id": row["sandbox_id"],
            "model_id": row["model_id"],
            "sandbox_name": row["sandbox_name"],
            "sandbox_safeguard_score": round(score, 4),
            "sandbox_capture_risk_score": round(capture_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["sandbox_safeguard_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.16 * float(row["technology_acceleration"])
            + 0.16 * float(row["climate_stress"])
            + 0.14 * (1.0 - float(row["public_trust"]))
            + 0.12 * (1.0 - float(row["institutional_capacity"]))
            + 0.14 * float(row["capture_pressure"])
            + 0.14 * float(row["rights_risk"])
            + 0.08 * float(row["international_fragmentation"])
            + 0.06 * (1.0 - float(row["learning_capacity"]))
        )

        opportunity = (
            0.22 * float(row["institutional_capacity"])
            + 0.20 * float(row["learning_capacity"])
            + 0.18 * float(row["public_trust"])
            + 0.12 * (1.0 - float(row["capture_pressure"]))
            + 0.12 * (1.0 - float(row["rights_risk"]))
            + 0.08 * (1.0 - float(row["international_fragmentation"]))
            + 0.08 * (1.0 - float(row["climate_stress"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "regulatory_future_stress_score": round(stress, 4),
            "future_ready_regulatory_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_ready_regulatory_opportunity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        foresight = float(row["foresight"])
        monitoring = float(row["monitoring"])
        enforcement = float(row["enforcement"])
        rights = float(row["rights"])
        participation = float(row["participation"])
        revision = float(row["revision"])
        learning = float(row["learning"])
        capture_resistance = float(row["capture_resistance"])
        trust = float(row["initial_trust"])

        capacity = (
            0.14 * foresight
            + 0.13 * monitoring
            + 0.13 * enforcement
            + 0.15 * rights
            + 0.12 * participation
            + 0.13 * revision
            + 0.12 * learning
            + 0.08 * capture_resistance
        )
        lag = 1.0 - (0.45 * foresight + 0.35 * monitoring + 0.20 * revision)
        rights_state = rights
        learning_state = learning
        horizon = int(row["time_horizon"])

        capacity_values: list[float] = []
        lag_values: list[float] = []
        rights_values: list[float] = []
        trust_values: list[float] = []
        learning_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                change_pressure = 0.16 if t % 8 == 0 else 0.06

                anticipatory_gain = 0.24 * foresight + 0.20 * monitoring
                legal_gain = 0.22 * revision + 0.18 * enforcement
                legitimacy_gain = 0.16 * participation + 0.14 * capture_resistance
                learning_gain = 0.18 * learning_state

                lag = clamp(
                    lag
                    + 0.08 * change_pressure
                    - 0.04 * anticipatory_gain
                    - 0.03 * legal_gain
                    - 0.02 * learning_gain,
                    0.0,
                    1.4,
                )

                rights_state = clamp(
                    rights_state
                    + 0.04 * rights
                    + 0.03 * enforcement
                    + 0.02 * participation
                    - 0.04 * lag,
                    0.0,
                    1.4,
                )

                learning_state = clamp(
                    learning_state
                    + 0.04 * learning
                    + 0.03 * monitoring
                    + 0.02 * revision
                    - 0.02 * change_pressure,
                    0.0,
                    1.4,
                )

                trust = clamp(
                    trust
                    + 0.04 * rights_state
                    + 0.03 * participation
                    + 0.03 * capture_resistance
                    - 0.05 * lag,
                    0.0,
                    1.4,
                )

                capacity = clamp(
                    capacity
                    + anticipatory_gain / 7.0
                    + legal_gain / 7.0
                    + legitimacy_gain / 8.0
                    + learning_gain / 8.0
                    - 0.08 * lag
                    - 0.03 * change_pressure,
                    0.0,
                    1.8,
                )

            capacity_values.append(capacity)
            lag_values.append(lag)
            rights_values.append(rights_state)
            trust_values.append(trust)
            learning_values.append(learning_state)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "model_id": row["model_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "future_ready_regulatory_capacity": round(capacity, 4),
                "regulatory_lag_pressure": round(lag, 4),
                "rights_protection": round(rights_state, 4),
                "public_trust": round(trust, 4),
                "learning_score": round(learning_state, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "model_id": row["model_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_regulatory_capacity": round(capacity_values[-1], 4),
            "mean_regulatory_capacity": round(mean(capacity_values), 4),
            "mean_regulatory_lag_pressure": round(mean(lag_values), 4),
            "final_rights_protection": round(rights_values[-1], 4),
            "final_public_trust": round(trust_values[-1], 4),
            "final_learning_score": round(learning_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_regulatory_capacity"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        future_ready_score = (
            0.13 * float(row["foresight_capacity"])
            + 0.12 * float(row["monitoring_design"])
            + 0.14 * float(row["rights_safeguards"])
            + 0.11 * float(row["public_participation"])
            + 0.13 * float(row["revision_triggers"])
            + 0.12 * float(row["enforcement_capacity"])
            + 0.10 * float(row["remedy_access"])
            + 0.10 * float(row["capture_resistance"])
            + 0.05 * float(row["legal_certainty"])
        )

        accountability_score = (
            0.18 * float(row["rights_safeguards"])
            + 0.16 * float(row["remedy_access"])
            + 0.16 * float(row["enforcement_capacity"])
            + 0.14 * float(row["capture_resistance"])
            + 0.12 * float(row["public_participation"])
            + 0.10 * float(row["monitoring_design"])
            + 0.08 * float(row["revision_triggers"])
            + 0.06 * float(row["legal_certainty"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "future_ready_regulatory_strategy_score": round(future_ready_score, 4),
            "rights_accountability_strategy_score": round(accountability_score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["future_ready_regulatory_strategy_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    model_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    rights_scores: list[dict[str, Any]],
    sandbox_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Regulatory Model Scores",
        "",
    ]

    for row in model_scores:
        lines.append(
            f"- **{row['regulatory_model']}**: capacity {row['future_ready_regulatory_capacity_score']}; "
            f"lag pressure {row['regulatory_lag_pressure_score']}; class: {row['regulatory_class']}."
        )

    lines.extend(["", "## Emerging Regulatory Risk Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: risk score {row['emerging_regulatory_risk_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Rights and Remedy Scores", ""])
    for row in rights_scores:
        lines.append(
            f"- **{row['rights_domain']}**: rights-remedy strength {row['rights_remedy_strength_score']}; "
            f"appeal {row['appeal']}; audit access {row['audit_access']}."
        )

    lines.extend(["", "## Sandbox Safeguard Scores", ""])
    for row in sandbox_scores:
        lines.append(
            f"- **{row['sandbox_name']}**: safeguard score {row['sandbox_safeguard_score']}; "
            f"capture risk {row['sandbox_capture_risk_score']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: opportunity {row['future_ready_regulatory_opportunity_score']}; "
            f"stress {row['regulatory_future_stress_score']}."
        )

    lines.extend(["", "## Adaptive Regulatory Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final capacity {row['final_regulatory_capacity']}; "
            f"mean lag {row['mean_regulatory_lag_pressure']}; final rights {row['final_rights_protection']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: future-ready strategy {row['future_ready_regulatory_strategy_score']}; "
            f"rights accountability {row['rights_accountability_strategy_score']}."
        )

    avg_capacity = mean(float(row["future_ready_regulatory_capacity_score"]) for row in model_scores)
    avg_lag = mean(float(row["regulatory_lag_pressure_score"]) for row in model_scores)
    avg_rights = mean(float(row["rights_remedy_strength_score"]) for row in rights_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Regulatory models: {len(model_scores)}.",
        f"- Emerging risk records: {len(risk_scores)}.",
        f"- Rights-remedy records: {len(rights_scores)}.",
        f"- Sandbox records: {len(sandbox_scores)}.",
        f"- Future scenarios: {len(scenario_scores)}.",
        f"- Average future-ready regulatory capacity score: {round(avg_capacity, 4)}.",
        f"- Average regulatory lag pressure score: {round(avg_lag, 4)}.",
        f"- Average rights-remedy strength score: {round(avg_rights, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats future-ready regulation as a legal and institutional system for foresight, monitoring, enforcement, rights protection, public participation, adaptive rule design, regulatory learning, capture resistance, legal certainty, and remedy.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "regulatory_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    models_raw = read_csv(DATA / "regulatory_models.csv")
    risks_raw = read_csv(DATA / "emerging_risk_register.csv")
    rights_raw = read_csv(DATA / "rights_remedy_register.csv")
    sandboxes_raw = read_csv(DATA / "sandbox_governance.csv")
    scenarios_raw = read_csv(DATA / "regulatory_scenarios.csv")
    pathways_raw = read_csv(DATA / "adaptive_regulatory_pathways.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(models_raw, risks_raw, rights_raw, sandboxes_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    model_scores = score_models(models_raw)
    risk_scores = score_risks(risks_raw)
    rights_scores = score_rights(rights_raw)
    sandbox_scores = score_sandboxes(sandboxes_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategy_scores = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "regulatory_model_scores.csv", model_scores)
    write_csv(OUTPUTS / "emerging_risk_scores.csv", risk_scores)
    write_csv(OUTPUTS / "rights_remedy_scores.csv", rights_scores)
    write_csv(OUTPUTS / "sandbox_safeguard_scores.csv", sandbox_scores)
    write_csv(OUTPUTS / "regulatory_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "adaptive_regulatory_pathways.csv", trajectories)
    write_csv(OUTPUTS / "adaptive_regulatory_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategy_scores)

    write_report(config, model_scores, risk_scores, rights_scores, sandbox_scores, scenario_scores, pathway_summary, strategy_scores)

    print(f"Regulatory futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
