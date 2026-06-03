#!/usr/bin/env python3
"""
Standard-library workflow for Biotechnology Futures.

Outputs:
- biotechnology_capability_scores.csv
- biotechnology_risk_scores.csv
- biotechnology_justice_scores.csv
- biotechnology_scenario_scores.csv
- biotechnology_pathways.csv
- biotechnology_pathway_summary.csv
- strategy_option_scores.csv
- biotechnology_futures_report.md
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


def responsible_capacity(
    science: float,
    governance: float,
    legitimacy: float,
    equity: float,
    manufacturing: float,
    consent: float,
    ecology_uncertainty: float,
    dual_use: float,
) -> float:
    return (
        0.16 * science
        + 0.18 * governance
        + 0.16 * legitimacy
        + 0.16 * equity
        + 0.12 * manufacturing
        + 0.12 * consent
        + 0.05 * (1.0 - ecology_uncertainty)
        + 0.05 * (1.0 - dual_use)
    )


def biological_risk_pressure(
    dual_use: float,
    ecology_uncertainty: float,
    governance: float,
    legitimacy: float,
    consent: float,
    equity: float,
) -> float:
    return (
        0.22 * dual_use
        + 0.20 * ecology_uncertainty
        + 0.18 * (1.0 - governance)
        + 0.16 * (1.0 - legitimacy)
        + 0.14 * (1.0 - consent)
        + 0.10 * (1.0 - equity)
    )


def validate_records(
    capabilities: list[dict[str, str]],
    risks: list[dict[str, str]],
    justice: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    capability_ids = {row["capability_id"] for row in capabilities}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in risks:
        if row["capability_id"] not in capability_ids:
            errors.append(f"Risk {row['risk_id']} references missing capability {row['capability_id']}.")

    for row in justice:
        if row["capability_id"] not in capability_ids:
            errors.append(f"Justice indicator {row['justice_id']} references missing capability {row['capability_id']}.")

    for row in pathways:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    return errors


def score_capabilities(capabilities: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in capabilities:
        science = float(row["scientific_maturity"])
        manufacturing = float(row["manufacturing_capacity"])
        governance = float(row["governance_readiness"])
        legitimacy = float(row["public_legitimacy"])
        equity = float(row["equity_access"])
        ecology = float(row["ecological_uncertainty"])
        dual_use = float(row["dual_use_risk"])
        consent = float(row["community_consent"])

        capacity = responsible_capacity(science, governance, legitimacy, equity, manufacturing, consent, ecology, dual_use)
        risk = biological_risk_pressure(dual_use, ecology, governance, legitimacy, consent, equity)

        rows.append({
            "capability_id": row["capability_id"],
            "capability_name": row["capability_name"],
            "domain": row["domain"],
            "responsible_biotechnology_capacity_score": round(capacity, 4),
            "biological_risk_pressure_score": round(risk, 4),
            "scientific_maturity": science,
            "governance_readiness": governance,
            "equity_access": equity,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["responsible_biotechnology_capacity_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in risks:
        probability = float(row["probability"])
        severity = float(row["severity"])
        detection = float(row["detection_difficulty"])
        governance_gap = float(row["governance_gap"])
        ecological_exposure = float(row["ecological_exposure"])
        dual_use = float(row["dual_use_relevance"])
        mitigation = float(row["mitigation_capacity"])

        priority = (
            0.18 * probability
            + 0.22 * severity
            + 0.16 * detection
            + 0.16 * governance_gap
            + 0.12 * ecological_exposure
            + 0.10 * dual_use
            + 0.06 * (1.0 - mitigation)
        )

        rows.append({
            "risk_id": row["risk_id"],
            "capability_id": row["capability_id"],
            "risk_name": row["risk_name"],
            "risk_type": row["risk_type"],
            "risk_priority_score": round(priority, 4),
            "mitigation_capacity": mitigation,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["risk_priority_score"]), reverse=True)
    return rows


def score_justice(justice_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in justice_rows:
        access = float(row["equitable_access"])
        voice = float(row["affected_voice"])
        consent = float(row["consent_strength"])
        benefit = float(row["benefit_sharing"])
        repair = float(row["repair_capacity"])
        harm = float(row["harm_concentration"])
        governance = float(row["community_governance"])

        justice_score = (
            0.20 * access
            + 0.16 * voice
            + 0.16 * consent
            + 0.16 * benefit
            + 0.14 * repair
            + 0.10 * governance
            + 0.08 * (1.0 - harm)
        )

        harm_score = (
            0.32 * harm
            + 0.18 * (1.0 - access)
            + 0.16 * (1.0 - voice)
            + 0.14 * (1.0 - consent)
            + 0.12 * (1.0 - repair)
            + 0.08 * (1.0 - governance)
        )

        rows.append({
            "justice_id": row["justice_id"],
            "capability_id": row["capability_id"],
            "justice_dimension": row["justice_dimension"],
            "biotechnology_justice_score": round(justice_score, 4),
            "harm_concentration_score": round(harm_score, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["biotechnology_justice_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        science = float(row["scientific_maturity"])
        governance = float(row["governance_readiness"])
        ecology = float(row["ecological_uncertainty"])
        dual_use = float(row["dual_use_risk"])
        legitimacy = float(row["public_legitimacy"])
        equity = float(row["equity_access"])
        manufacturing = float(row["manufacturing_capacity"])
        consent = float(row["community_consent"])

        capacity = responsible_capacity(science, governance, legitimacy, equity, manufacturing, consent, ecology, dual_use)
        risk = biological_risk_pressure(dual_use, ecology, governance, legitimacy, consent, equity)
        justice_profile = (
            0.28 * equity
            + 0.24 * consent
            + 0.20 * legitimacy
            + 0.16 * governance
            + 0.12 * (1.0 - risk)
        )

        if justice_profile >= 0.75:
            scenario_class = "High justice and governance capacity"
        elif risk >= 0.62:
            scenario_class = "High biological risk pressure"
        else:
            scenario_class = "Contested biotechnology pathway"

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "responsible_biotechnology_capacity_score": round(capacity, 4),
            "biological_risk_pressure_score": round(risk, 4),
            "justice_profile_score": round(justice_profile, 4),
            "scenario_class": scenario_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["responsible_biotechnology_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        science = float(row["science"])
        governance = float(row["governance"])
        legitimacy = float(row["legitimacy"])
        equity = float(row["equity"])
        manufacturing = float(row["manufacturing"])
        ecology = float(row["ecological_uncertainty"])
        dual_use = float(row["dual_use_risk"])
        viability = float(row["initial_viability"])
        biological_risk = 0.30 + 0.20 * dual_use + 0.15 * ecology
        access_capacity = equity
        horizon = int(row["time_horizon"])

        viability_values: list[float] = []
        risk_values: list[float] = []
        access_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                disruption = 0.10 if t % 9 == 0 else 0.03

                innovation_force = (
                    0.24 * science
                    + 0.20 * manufacturing
                    + 0.18 * governance
                    + 0.16 * legitimacy
                    + 0.16 * equity
                )

                pressure = (
                    0.24 * dual_use
                    + 0.22 * ecology
                    + 0.18 * (1.0 - governance)
                    + 0.16 * (1.0 - legitimacy)
                    + 0.12 * (1.0 - equity)
                    + disruption
                )

                access_capacity = clamp(
                    access_capacity
                    + 0.04 * equity
                    + 0.03 * governance
                    + 0.02 * manufacturing
                    - 0.03 * (1.0 - legitimacy),
                    0.0,
                    1.4,
                )

                biological_risk = clamp(
                    biological_risk * 0.88
                    + pressure
                    - 0.08 * governance
                    - 0.05 * legitimacy,
                    0.0,
                    1.8,
                )

                viability = clamp(
                    viability
                    + innovation_force / 4.0
                    - pressure / 4.0
                    + 0.04 * access_capacity
                    - 0.03 * biological_risk,
                    0.0,
                    1.8,
                )

            viability_values.append(viability)
            risk_values.append(biological_risk)
            access_values.append(access_capacity)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "biotechnology_viability": round(viability, 4),
                "biological_risk_pressure": round(biological_risk, 4),
                "access_capacity": round(access_capacity, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_viability": round(viability_values[-1], 4),
            "mean_biological_risk": round(mean(risk_values), 4),
            "final_access_capacity": round(access_values[-1], 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in strategies:
        governance = float(row["governance_strength"])
        equity = float(row["equity_access"])
        consent = float(row["community_consent"])
        biosafety = float(row["biosafety_capacity"])
        biosecurity = float(row["biosecurity_capacity"])
        open_science = float(row["open_science"])
        public_manufacturing = float(row["public_manufacturing"])
        ecological = float(row["ecological_monitoring"])
        benefit = float(row["benefit_sharing"])

        public_interest = (
            0.16 * governance
            + 0.14 * equity
            + 0.14 * consent
            + 0.12 * biosafety
            + 0.12 * biosecurity
            + 0.10 * open_science
            + 0.08 * public_manufacturing
            + 0.08 * ecological
            + 0.06 * benefit
        )

        justice_governance = (
            0.18 * equity
            + 0.18 * consent
            + 0.16 * benefit
            + 0.14 * governance
            + 0.12 * public_manufacturing
            + 0.10 * open_science
            + 0.08 * ecological
            + 0.04 * biosafety
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "public_interest_biotechnology_score": round(public_interest, 4),
            "justice_governance_score": round(justice_governance, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_biotechnology_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    capabilities: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    justice: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Biotechnology Capability Scores",
        "",
    ]

    for row in capabilities:
        lines.append(
            f"- **{row['capability_name']}**: responsible capacity {row['responsible_biotechnology_capacity_score']}; "
            f"biological risk pressure {row['biological_risk_pressure_score']}; domain: {row['domain']}."
        )

    lines.extend(["", "## Biotechnology Risk Priorities", ""])
    for row in risks:
        lines.append(
            f"- **{row['risk_name']}**: risk priority {row['risk_priority_score']}; "
            f"mitigation capacity {row['mitigation_capacity']}."
        )

    lines.extend(["", "## Justice and Harm Scores", ""])
    for row in justice:
        lines.append(
            f"- **{row['justice_dimension']}**: justice score {row['biotechnology_justice_score']}; "
            f"harm concentration {row['harm_concentration_score']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenarios:
        lines.append(
            f"- **{row['scenario_name']}**: responsible capacity {row['responsible_biotechnology_capacity_score']}; "
            f"risk pressure {row['biological_risk_pressure_score']}; class: {row['scenario_class']}."
        )

    lines.extend(["", "## Pathway Simulation Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_viability']}; "
            f"mean biological risk {row['mean_biological_risk']}; final access capacity {row['final_access_capacity']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategies:
        lines.append(
            f"- **{row['strategy_name']}**: public-interest biotechnology score {row['public_interest_biotechnology_score']}; "
            f"justice governance score {row['justice_governance_score']}."
        )

    avg_capacity = mean(float(row["responsible_biotechnology_capacity_score"]) for row in capabilities)
    avg_risk = mean(float(row["risk_priority_score"]) for row in risks)
    avg_justice = mean(float(row["biotechnology_justice_score"]) for row in justice)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Biotechnology capabilities: {len(capabilities)}.",
        f"- Risk records: {len(risks)}.",
        f"- Justice indicators: {len(justice)}.",
        f"- Scenarios: {len(scenarios)}.",
        f"- Average responsible biotechnology capacity: {round(avg_capacity, 4)}.",
        f"- Average biotechnology risk priority: {round(avg_risk, 4)}.",
        f"- Average justice score: {round(avg_justice, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats biotechnology futures as a systems-governance challenge. It compares scientific maturity, manufacturing capacity, governance readiness, public legitimacy, equity access, ecological uncertainty, dual-use risk, community consent, biological risk pressure, and public-interest strategy options.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "biotechnology_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    capabilities_raw = read_csv(DATA / "biotechnology_capabilities.csv")
    risks_raw = read_csv(DATA / "biotechnology_risk_register.csv")
    justice_raw = read_csv(DATA / "justice_indicators.csv")
    scenarios_raw = read_csv(DATA / "biotechnology_scenarios.csv")
    pathways_raw = read_csv(DATA / "pathway_parameters.csv")
    strategies_raw = read_csv(DATA / "strategy_options.csv")

    errors = validate_records(capabilities_raw, risks_raw, justice_raw, scenarios_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    capabilities = score_capabilities(capabilities_raw)
    risks = score_risks(risks_raw)
    justice = score_justice(justice_raw)
    scenarios = score_scenarios(scenarios_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)
    strategies = score_strategies(strategies_raw)

    write_csv(OUTPUTS / "biotechnology_capability_scores.csv", capabilities)
    write_csv(OUTPUTS / "biotechnology_risk_scores.csv", risks)
    write_csv(OUTPUTS / "biotechnology_justice_scores.csv", justice)
    write_csv(OUTPUTS / "biotechnology_scenario_scores.csv", scenarios)
    write_csv(OUTPUTS / "biotechnology_pathways.csv", trajectories)
    write_csv(OUTPUTS / "biotechnology_pathway_summary.csv", pathway_summary)
    write_csv(OUTPUTS / "strategy_option_scores.csv", strategies)

    write_report(config, capabilities, risks, justice, scenarios, pathway_summary, strategies)

    print(f"Biotechnology futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
