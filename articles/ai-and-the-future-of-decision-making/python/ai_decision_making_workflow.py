#!/usr/bin/env python3
"""
Standard-library workflow for AI and the Future of Decision-Making.

Outputs:
- decision_system_profile_scores.csv
- governance_readiness_scores.csv
- risk_priority_scores.csv
- equity_harm_scores.csv
- hybrid_decision_performance.csv
- hybrid_decision_summary.csv
- strategy_option_scores.csv
- ai_decision_making_report.md
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


def validate_records(
    systems: list[dict[str, str]],
    governance: list[dict[str, str]],
    risks: list[dict[str, str]],
    equity: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    system_ids = {row["system_id"] for row in systems}

    for dataset_name, rows in [
        ("governance_controls", governance),
        ("risk_indicators", risks),
        ("equity_harm_indicators", equity),
        ("pathway_parameters", pathways),
    ]:
        for row in rows:
            if row["system_id"] not in system_ids:
                errors.append(f"{dataset_name} record references missing system {row['system_id']}.")

    numeric_specs = [
        ("decision_system_profiles", systems, ["human_judgment", "machine_inference", "coordination_quality", "transparency", "uncertainty_management", "accountability", "contestability", "equity_protection", "automation_intensity"]),
        ("governance_controls", governance, ["documentation", "auditability", "explainability", "human_oversight", "appeal_rights", "monitoring_strength", "enforcement_capacity"]),
        ("risk_indicators", risks, ["probability", "severity", "detection_difficulty", "governance_gap", "affected_population_exposure", "mitigation_capacity"]),
        ("equity_harm_indicators", equity, ["error_burden", "exposure", "vulnerability", "contestability", "voice", "protection", "repair_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("system_id") or row.get("risk_id") or row.get("equity_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def classify_system(governance_profile: float, risk_profile: float) -> str:
    if governance_profile >= 0.78:
        return "High-governance decision system"
    if risk_profile >= 0.55:
        return "High-risk decision system"
    return "Moderate-governance decision system"


def score_decision_systems(systems: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in systems:
        human = float(row["human_judgment"])
        machine = float(row["machine_inference"])
        coordination = float(row["coordination_quality"])
        transparency = float(row["transparency"])
        uncertainty = float(row["uncertainty_management"])
        accountability = float(row["accountability"])
        contestability = float(row["contestability"])
        equity = float(row["equity_protection"])
        automation = float(row["automation_intensity"])

        profile = (
            0.16 * human
            + 0.16 * machine
            + 0.16 * coordination
            + 0.12 * transparency
            + 0.12 * uncertainty
            + 0.12 * accountability
            + 0.08 * contestability
            + 0.08 * equity
        )

        governance_profile = (
            0.22 * transparency
            + 0.24 * accountability
            + 0.24 * contestability
            + 0.18 * uncertainty
            + 0.12 * equity
        )

        risk_profile = (
            0.26 * automation
            + 0.20 * (1.0 - accountability)
            + 0.20 * (1.0 - contestability)
            + 0.18 * (1.0 - transparency)
            + 0.16 * (1.0 - equity)
        )

        rows.append({
            "system_id": row["system_id"],
            "system_type": row["system_type"],
            "decision_domain": row["decision_domain"],
            "decision_system_profile_score": round(profile, 4),
            "governance_profile_score": round(governance_profile, 4),
            "risk_profile_score": round(risk_profile, 4),
            "system_class": classify_system(governance_profile, risk_profile),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["decision_system_profile_score"]), reverse=True)
    return rows


def score_governance(controls: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in controls:
        documentation = float(row["documentation"])
        auditability = float(row["auditability"])
        explainability = float(row["explainability"])
        oversight = float(row["human_oversight"])
        appeals = float(row["appeal_rights"])
        monitoring = float(row["monitoring_strength"])
        enforcement = float(row["enforcement_capacity"])

        readiness = (
            0.16 * documentation
            + 0.16 * auditability
            + 0.14 * explainability
            + 0.16 * oversight
            + 0.14 * appeals
            + 0.12 * monitoring
            + 0.12 * enforcement
        )

        rows.append({
            "control_id": row["control_id"],
            "system_id": row["system_id"],
            "control_name": row["control_name"],
            "control_type": row["control_type"],
            "governance_readiness_score": round(readiness, 4),
            "governance_gap_score": round(1.0 - readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["governance_gap_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        probability = float(row["probability"])
        severity = float(row["severity"])
        detection = float(row["detection_difficulty"])
        governance_gap = float(row["governance_gap"])
        exposure = float(row["affected_population_exposure"])
        mitigation = float(row["mitigation_capacity"])

        priority = (
            0.22 * probability
            + 0.24 * severity
            + 0.18 * detection
            + 0.18 * governance_gap
            + 0.12 * exposure
            + 0.06 * (1.0 - mitigation)
        )

        rows.append({
            "risk_id": row["risk_id"],
            "system_id": row["system_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "risk_priority_score": round(priority, 4),
            "mitigation_capacity": mitigation,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["risk_priority_score"]), reverse=True)
    return rows


def score_equity(equity_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in equity_rows:
        error = float(row["error_burden"])
        exposure = float(row["exposure"])
        vulnerability = float(row["vulnerability"])
        contestability = float(row["contestability"])
        voice = float(row["voice"])
        protection = float(row["protection"])
        repair = float(row["repair_capacity"])

        justice = (
            0.18 * contestability
            + 0.18 * voice
            + 0.20 * protection
            + 0.18 * repair
            + 0.14 * (1.0 - error)
            + 0.12 * (1.0 - vulnerability)
        )

        harm = (
            0.25 * error
            + 0.22 * exposure
            + 0.22 * vulnerability
            + 0.16 * (1.0 - contestability)
            + 0.15 * (1.0 - repair)
        )

        rows.append({
            "equity_id": row["equity_id"],
            "system_id": row["system_id"],
            "equity_dimension": row["equity_dimension"],
            "justice_capacity_score": round(justice, 4),
            "harm_risk_score": round(harm, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["harm_risk_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        human = float(row["human"])
        machine = float(row["machine"])
        coordination = float(row["coordination"])
        governance = float(row["governance"])
        contestability = float(row["contestability"])
        decision_quality = float(row["initial_decision_quality"])
        uncertainty_pressure = 0.20
        harm_risk = 0.20
        horizon = int(row["time_horizon"])

        quality_values: list[float] = []
        uncertainty_values: list[float] = []
        harm_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                regime_shift = 0.16 if t % 9 == 0 else 0.06
                governance_buffer = 0.10 * governance + 0.08 * contestability

                performance_gain = (
                    0.22 * human
                    + 0.24 * machine
                    + 0.26 * coordination
                    + 0.16 * governance
                    + 0.12 * contestability
                )

                automation_fragility = 0.10 * machine * (1.0 - governance) * (1.0 - contestability)

                uncertainty_pressure = clamp(
                    uncertainty_pressure * 0.88 + regime_shift + automation_fragility,
                    0.0,
                    1.5,
                )

                harm_risk = max(
                    0.0,
                    min(
                        1.0,
                        0.35 * (1.0 - governance)
                        + 0.35 * (1.0 - contestability)
                        + 0.20 * automation_fragility
                        + 0.10 * regime_shift,
                    ),
                )

                decision_quality = clamp(
                    decision_quality - regime_shift - automation_fragility + performance_gain / 4 + governance_buffer / 3,
                    0.0,
                    1.8,
                )

            quality_values.append(decision_quality)
            uncertainty_values.append(uncertainty_pressure)
            harm_values.append(harm_risk)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "system_id": row["system_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "decision_quality": round(decision_quality, 4),
                "uncertainty_pressure": round(uncertainty_pressure, 4),
                "harm_risk": round(harm_risk, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "system_id": row["system_id"],
            "pathway_name": row["pathway_name"],
            "final_decision_quality": round(quality_values[-1], 4),
            "mean_decision_quality": round(mean(quality_values), 4),
            "max_uncertainty_pressure": round(max(uncertainty_values), 4),
            "mean_harm_risk": round(mean(harm_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_decision_quality"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        human = float(row["human_authority"])
        machine = float(row["machine_capability"])
        coordination = float(row["coordination_design"])
        transparency = float(row["transparency"])
        accountability = float(row["accountability"])
        contestability = float(row["contestability"])
        equity = float(row["equity_protection"])
        stress_testing = float(row["uncertainty_stress_testing"])

        public_interest = (
            0.12 * human
            + 0.12 * machine
            + 0.16 * coordination
            + 0.12 * transparency
            + 0.16 * accountability
            + 0.14 * contestability
            + 0.10 * equity
            + 0.08 * stress_testing
        )

        governance_strength = (
            0.16 * transparency
            + 0.20 * accountability
            + 0.18 * contestability
            + 0.16 * equity
            + 0.16 * stress_testing
            + 0.14 * coordination
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "public_interest_decision_score": round(public_interest, 4),
            "governance_strength_score": round(governance_strength, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_decision_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    systems: list[dict[str, Any]],
    governance: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    equity: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Decision-System Profile Scores",
        "",
    ]

    for row in systems:
        lines.append(
            f"- **{row['system_type']}**: profile {row['decision_system_profile_score']}; "
            f"governance {row['governance_profile_score']}; risk {row['risk_profile_score']}; class: {row['system_class']}."
        )

    lines.extend(["", "## Governance Readiness and Gaps", ""])
    for row in governance:
        lines.append(
            f"- **{row['control_name']}**: readiness {row['governance_readiness_score']}; "
            f"gap {row['governance_gap_score']}."
        )

    lines.extend(["", "## Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Equity Harm and Justice Scores", ""])
    for row in equity:
        lines.append(
            f"- **{row['equity_dimension']}**: harm risk {row['harm_risk_score']}; "
            f"justice capacity {row['justice_capacity_score']}."
        )

    lines.extend(["", "## Hybrid Decision Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final decision quality {row['final_decision_quality']}; "
            f"max uncertainty pressure {row['max_uncertainty_pressure']}; mean harm risk {row['mean_harm_risk']}."
        )

    lines.extend(["", "## Strategy Option Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: public-interest decision score {row['public_interest_decision_score']}; "
            f"governance strength {row['governance_strength_score']}."
        )

    avg_profile = mean(float(row["decision_system_profile_score"]) for row in systems)
    avg_governance_gap = mean(float(row["governance_gap_score"]) for row in governance)
    avg_harm = mean(float(row["harm_risk_score"]) for row in equity)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Decision systems: {len(systems)}.",
        f"- Governance controls: {len(governance)}.",
        f"- Risk indicators: {len(risks)}.",
        f"- Equity indicators: {len(equity)}.",
        f"- Average decision-system profile score: {round(avg_profile, 4)}.",
        f"- Average governance gap score: {round(avg_governance_gap, 4)}.",
        f"- Average equity harm risk score: {round(avg_harm, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats AI decision-making as a socio-technical system. It compares human judgment, machine inference, coordination, transparency, uncertainty management, accountability, contestability, equity protection, and harm risk. Scores are designed to support review and institutional learning rather than replace judgment.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "ai_decision_making_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    systems_raw = read_csv(DATA / "decision_system_profiles.csv")
    governance_raw = read_csv(DATA / "governance_controls.csv")
    risks_raw = read_csv(DATA / "risk_indicators.csv")
    equity_raw = read_csv(DATA / "equity_harm_indicators.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(systems_raw, governance_raw, risks_raw, equity_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    systems = score_decision_systems(systems_raw)
    governance = score_governance(governance_raw)
    risks = score_risks(risks_raw)
    equity = score_equity(equity_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "decision_system_profile_scores.csv", systems)
    write_csv(OUTPUTS / "governance_readiness_scores.csv", governance)
    write_csv(OUTPUTS / "risk_priority_scores.csv", risks)
    write_csv(OUTPUTS / "equity_harm_scores.csv", equity)
    write_csv(OUTPUTS / "hybrid_decision_performance.csv", trajectories)
    write_csv(OUTPUTS / "hybrid_decision_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, systems, governance, risks, equity, pathway_summary, strategies)

    print(f"AI decision-making workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
