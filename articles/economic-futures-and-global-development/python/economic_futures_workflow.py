#!/usr/bin/env python3
"""
Standard-library workflow for Economic Futures and Global Development.

Outputs:
- development_future_scores.csv
- economic_scenario_scores.csv
- policy_portfolio_scores.csv
- shock_priority_scores.csv
- institutional_capacity_scores.csv
- development_pathways.csv
- development_pathway_summary.csv
- economic_futures_report.md
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


def development_quality(row: dict[str, str]) -> float:
    return (
        0.14 * float(row["growth"])
        - 0.12 * float(row["inequality"])
        - 0.14 * float(row["ecological_stress"])
        + 0.13 * float(row["institutional_capacity"])
        + 0.12 * float(row["resilience"])
        + 0.08 * float(row["fiscal_space"])
        + 0.08 * float(row["labor_inclusion"])
        + 0.08 * float(row["public_investment"])
        + 0.06 * float(row["technology_diffusion"])
        + 0.03 * float(row["trade_resilience"])
        + 0.02 * float(row["democratic_legitimacy"])
    )


def development_fragility(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["inequality"])
        + 0.16 * float(row["ecological_stress"])
        + 0.13 * (1.0 - float(row["institutional_capacity"]))
        + 0.13 * (1.0 - float(row["resilience"]))
        + 0.12 * (1.0 - float(row["fiscal_space"]))
        + 0.10 * (1.0 - float(row["labor_inclusion"]))
        + 0.08 * (1.0 - float(row["public_investment"]))
        + 0.06 * (1.0 - float(row["trade_resilience"]))
        + 0.06 * (1.0 - float(row["democratic_legitimacy"]))
    )


def validate_records(
    futures: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    policies: list[dict[str, str]],
    shocks: list[dict[str, str]],
    institutions: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    future_ids = {row["future_id"] for row in futures}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in shocks:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Shock {row['shock_id']} references missing scenario {row['scenario_id']}.")

    for row in institutions:
        if row["future_id"] not in future_ids:
            errors.append(f"Institution {row['institution_id']} references missing future {row['future_id']}.")

    for row in pathways:
        if row["future_id"] not in future_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing future {row['future_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("development_futures", futures, ["growth", "inequality", "ecological_stress", "institutional_capacity", "resilience", "fiscal_space", "labor_inclusion", "public_investment", "technology_diffusion", "trade_resilience", "democratic_legitimacy"]),
        ("economic_scenarios", scenarios, ["global_growth", "financial_volatility", "climate_pressure", "technology_acceleration", "trade_fragmentation", "debt_stress", "energy_transition_speed", "public_trust", "coordination_capacity"]),
        ("policy_portfolios", policies, ["productive_capability", "distributional_inclusion", "ecological_viability", "resilience_capacity", "fiscal_sustainability", "labor_protection", "implementation_capacity", "global_coordination_need", "democratic_legitimacy"]),
        ("shocks_and_stressors", shocks, ["probability_proxy", "severity", "systemic_reach", "distributional_exposure", "recovery_difficulty", "policy_preparedness"]),
        ("institutional_capacity", institutions, ["administrative_capacity", "coordination_capacity", "public_trust", "regulatory_quality", "tax_capacity", "learning_capacity", "participation_quality"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("future_id") or row.get("scenario_id") or row.get("policy_id") or row.get("shock_id") or row.get("institution_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_development_futures(futures: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in futures:
        quality = development_quality(row)
        fragility = development_fragility(row)

        if quality >= 0.35 and fragility < 0.48:
            future_class = "Broad-based resilient development profile"
        elif fragility >= 0.62:
            future_class = "High development fragility"
        else:
            future_class = "Mixed or transitional development profile"

        rows.append({
            "future_id": row["future_id"],
            "future_name": row["future_name"],
            "future_type": row["future_type"],
            "development_quality_score": round(quality, 4),
            "development_fragility_score": round(fragility, 4),
            "future_class": future_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["development_quality_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        stress = (
            0.16 * float(row["financial_volatility"])
            + 0.16 * float(row["climate_pressure"])
            + 0.14 * float(row["trade_fragmentation"])
            + 0.14 * float(row["debt_stress"])
            + 0.12 * (1.0 - float(row["public_trust"]))
            + 0.12 * (1.0 - float(row["coordination_capacity"]))
            + 0.08 * (1.0 - float(row["global_growth"]))
            + 0.08 * (1.0 - float(row["energy_transition_speed"]))
        )

        opportunity = (
            0.18 * float(row["global_growth"])
            + 0.16 * float(row["technology_acceleration"])
            + 0.16 * float(row["energy_transition_speed"])
            + 0.16 * float(row["coordination_capacity"])
            + 0.14 * float(row["public_trust"])
            + 0.10 * (1.0 - float(row["debt_stress"]))
            + 0.10 * (1.0 - float(row["trade_fragmentation"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "economic_future_stress_score": round(stress, 4),
            "development_opportunity_score": round(opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["development_opportunity_score"]), reverse=True)
    return rows


def score_policies(policies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in policies:
        strength = (
            0.15 * float(row["productive_capability"])
            + 0.14 * float(row["distributional_inclusion"])
            + 0.14 * float(row["ecological_viability"])
            + 0.14 * float(row["resilience_capacity"])
            + 0.11 * float(row["fiscal_sustainability"])
            + 0.10 * float(row["labor_protection"])
            + 0.10 * float(row["implementation_capacity"])
            + 0.06 * float(row["democratic_legitimacy"])
            + 0.06 * (1.0 - float(row["global_coordination_need"]))
        )

        implementation_risk = (
            0.24 * (1.0 - float(row["implementation_capacity"]))
            + 0.18 * float(row["global_coordination_need"])
            + 0.16 * (1.0 - float(row["fiscal_sustainability"]))
            + 0.14 * (1.0 - float(row["democratic_legitimacy"]))
            + 0.12 * (1.0 - float(row["resilience_capacity"]))
            + 0.08 * (1.0 - float(row["distributional_inclusion"]))
            + 0.08 * (1.0 - float(row["ecological_viability"]))
        )

        rows.append({
            "policy_id": row["policy_id"],
            "policy_name": row["policy_name"],
            "policy_type": row["policy_type"],
            "development_strategy_strength_score": round(strength, 4),
            "implementation_risk_score": round(implementation_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["development_strategy_strength_score"]), reverse=True)
    return rows


def score_shocks(shocks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in shocks:
        priority = (
            0.18 * float(row["probability_proxy"])
            + 0.20 * float(row["severity"])
            + 0.18 * float(row["systemic_reach"])
            + 0.17 * float(row["distributional_exposure"])
            + 0.15 * float(row["recovery_difficulty"])
            + 0.12 * (1.0 - float(row["policy_preparedness"]))
        )

        rows.append({
            "shock_id": row["shock_id"],
            "scenario_id": row["scenario_id"],
            "shock_name": row["shock_name"],
            "shock_domain": row["shock_domain"],
            "development_shock_priority_score": round(priority, 4),
            "policy_preparedness": float(row["policy_preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["development_shock_priority_score"]), reverse=True)
    return rows


def score_institutions(institutions: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in institutions:
        capacity = (
            0.18 * float(row["administrative_capacity"])
            + 0.18 * float(row["coordination_capacity"])
            + 0.14 * float(row["public_trust"])
            + 0.14 * float(row["regulatory_quality"])
            + 0.14 * float(row["tax_capacity"])
            + 0.12 * float(row["learning_capacity"])
            + 0.10 * float(row["participation_quality"])
        )

        fragility = (
            0.18 * (1.0 - float(row["administrative_capacity"]))
            + 0.18 * (1.0 - float(row["coordination_capacity"]))
            + 0.16 * (1.0 - float(row["public_trust"]))
            + 0.14 * (1.0 - float(row["tax_capacity"]))
            + 0.12 * (1.0 - float(row["regulatory_quality"]))
            + 0.12 * (1.0 - float(row["learning_capacity"]))
            + 0.10 * (1.0 - float(row["participation_quality"]))
        )

        rows.append({
            "institution_id": row["institution_id"],
            "future_id": row["future_id"],
            "institution_name": row["institution_name"],
            "institution_domain": row["institution_domain"],
            "institutional_capacity_score": round(capacity, 4),
            "institutional_fragility_score": round(fragility, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["institutional_capacity_score"]), reverse=True)
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        growth = float(row["growth"])
        institutional = float(row["institutional_capacity"])
        adaptation = float(row["adaptation"])
        resilience = float(row["resilience"])
        fiscal_space = float(row["fiscal_space"])
        labor = float(row["labor_inclusion"])
        public_investment = float(row["public_investment"])
        ecological_stress = float(row["ecological_stress"])
        inequality = float(row["inequality"])
        development = float(row["initial_development"])
        horizon = int(row["time_horizon"])

        fragility = (
            0.22 * inequality
            + 0.20 * ecological_stress
            + 0.18 * (1.0 - resilience)
            + 0.16 * (1.0 - institutional)
            + 0.14 * (1.0 - fiscal_space)
            + 0.10 * (1.0 - labor)
        )
        public_capacity = 0.34 * institutional + 0.20 * fiscal_space + 0.18 * adaptation + 0.14 * labor + 0.14 * public_investment
        fiscal_stress = 1.0 - fiscal_space

        development_values: list[float] = []
        fragility_values: list[float] = []
        public_capacity_values: list[float] = []
        fiscal_stress_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                periodic_shock = 0.20 if t % 8 == 0 else 0.08

                ecological_pressure = 0.04 * ecological_stress
                inequality_drag = 0.04 * inequality
                institutional_response = 0.22 * institutional + 0.20 * adaptation + 0.18 * resilience
                fiscal_response = 0.14 * fiscal_space + 0.12 * labor + 0.10 * public_investment

                fragility = clamp(
                    fragility
                    + 0.05 * periodic_shock
                    + ecological_pressure
                    + inequality_drag
                    - 0.04 * resilience
                    - 0.04 * institutional
                    - 0.03 * fiscal_space
                    - 0.02 * public_investment,
                    0.0,
                    1.4,
                )

                public_capacity = clamp(
                    public_capacity
                    + 0.04 * institutional
                    + 0.03 * fiscal_space
                    + 0.03 * adaptation
                    + 0.03 * public_investment
                    + 0.02 * labor
                    - 0.04 * periodic_shock
                    - 0.03 * fragility,
                    0.0,
                    1.5,
                )

                fiscal_stress = clamp(
                    fiscal_stress
                    + 0.05 * periodic_shock
                    + 0.04 * fragility
                    + 0.03 * ecological_stress
                    - 0.04 * fiscal_space
                    - 0.03 * institutional,
                    0.0,
                    1.4,
                )

                development = clamp(
                    development
                    + growth
                    + institutional_response / 8.0
                    + fiscal_response / 8.0
                    + 0.04 * public_capacity
                    - periodic_shock
                    - 0.05 * fragility
                    - 0.03 * fiscal_stress,
                    0.0,
                    1.8,
                )

            development_values.append(development)
            fragility_values.append(fragility)
            public_capacity_values.append(public_capacity)
            fiscal_stress_values.append(fiscal_stress)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "future_id": row["future_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "development_viability": round(development, 4),
                "development_fragility": round(fragility, 4),
                "public_capacity": round(public_capacity, 4),
                "fiscal_stress": round(fiscal_stress, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "future_id": row["future_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_development_viability": round(development_values[-1], 4),
            "mean_development_viability": round(mean(development_values), 4),
            "mean_development_fragility": round(mean(fragility_values), 4),
            "final_public_capacity": round(public_capacity_values[-1], 4),
            "mean_fiscal_stress": round(mean(fiscal_stress_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_development_viability"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    future_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    policy_scores: list[dict[str, Any]],
    shock_scores: list[dict[str, Any]],
    institution_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Development Future Scores",
        "",
    ]

    for row in future_scores:
        lines.append(
            f"- **{row['future_name']}**: development quality {row['development_quality_score']}; "
            f"fragility {row['development_fragility_score']}; class: {row['future_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: opportunity {row['development_opportunity_score']}; "
            f"stress {row['economic_future_stress_score']}."
        )

    lines.extend(["", "## Policy Portfolio Scores", ""])
    for row in policy_scores:
        lines.append(
            f"- **{row['policy_name']}**: strength {row['development_strategy_strength_score']}; "
            f"implementation risk {row['implementation_risk_score']}."
        )

    lines.extend(["", "## Development Shock Priority Scores", ""])
    for row in shock_scores:
        lines.append(
            f"- **{row['shock_name']}**: priority {row['development_shock_priority_score']}; "
            f"preparedness {row['policy_preparedness']}."
        )

    lines.extend(["", "## Institutional Capacity Scores", ""])
    for row in institution_scores:
        lines.append(
            f"- **{row['institution_name']}**: capacity {row['institutional_capacity_score']}; "
            f"fragility {row['institutional_fragility_score']}."
        )

    lines.extend(["", "## Development Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final viability {row['final_development_viability']}; "
            f"mean fragility {row['mean_development_fragility']}; final public capacity {row['final_public_capacity']}."
        )

    avg_quality = mean(float(row["development_quality_score"]) for row in future_scores)
    avg_fragility = mean(float(row["development_fragility_score"]) for row in future_scores)
    avg_pathway = mean(float(row["final_development_viability"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Development futures: {len(future_scores)}.",
        f"- Economic scenarios: {len(scenario_scores)}.",
        f"- Policy portfolios: {len(policy_scores)}.",
        f"- Shock records: {len(shock_scores)}.",
        f"- Institutional records: {len(institution_scores)}.",
        f"- Average development quality score: {round(avg_quality, 4)}.",
        f"- Average development fragility score: {round(avg_fragility, 4)}.",
        f"- Average final development viability: {round(avg_pathway, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats economic futures and global development as a multidimensional system where growth, distribution, ecological stress, institutions, fiscal space, labor inclusion, public investment, resilience, technology diffusion, trade position, and democratic legitimacy interact over time.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "economic_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    futures_raw = read_csv(DATA / "development_futures.csv")
    scenarios_raw = read_csv(DATA / "economic_scenarios.csv")
    policies_raw = read_csv(DATA / "policy_portfolios.csv")
    shocks_raw = read_csv(DATA / "shocks_and_stressors.csv")
    institutions_raw = read_csv(DATA / "institutional_capacity.csv")
    pathways_raw = read_csv(DATA / "development_pathways.csv")

    errors = validate_records(futures_raw, scenarios_raw, policies_raw, shocks_raw, institutions_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    future_scores = score_development_futures(futures_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    policy_scores = score_policies(policies_raw)
    shock_scores = score_shocks(shocks_raw)
    institution_scores = score_institutions(institutions_raw)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "development_future_scores.csv", future_scores)
    write_csv(OUTPUTS / "economic_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "policy_portfolio_scores.csv", policy_scores)
    write_csv(OUTPUTS / "shock_priority_scores.csv", shock_scores)
    write_csv(OUTPUTS / "institutional_capacity_scores.csv", institution_scores)
    write_csv(OUTPUTS / "development_pathways.csv", trajectories)
    write_csv(OUTPUTS / "development_pathway_summary.csv", pathway_summary)

    write_report(config, future_scores, scenario_scores, policy_scores, shock_scores, institution_scores, pathway_summary)

    print(f"Economic futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
