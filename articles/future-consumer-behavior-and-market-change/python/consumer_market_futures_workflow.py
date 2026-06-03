#!/usr/bin/env python3
"""
Standard-library workflow for Future Consumer Behavior and Market Change.

Outputs:
- consumer_future_profile_scores.csv
- market_scenario_scores.csv
- consumer_strategy_option_scores.csv
- vulnerability_priority_scores.csv
- regulatory_market_scores.csv
- adoption_pathways.csv
- adoption_pathway_summary.csv
- consumer_market_futures_report.md
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


def consumer_future_health(row: dict[str, str]) -> float:
    return (
        0.14 * float(row["affordability"])
        + 0.16 * float(row["trust"])
        + 0.10 * float(row["sustainability_demand"])
        + 0.16 * float(row["access_inclusion"])
        + 0.10 * (1.0 - float(row["price_sensitivity"]))
        + 0.12 * (1.0 - float(row["behavioral_friction"]))
        + 0.06 * float(row["digital_dependence"])
        + 0.06 * float(row["regulatory_pressure"])
        + 0.06 * float(row["privacy_confidence"])
        + 0.04 * float(row["local_resilience"])
    )


def market_fragility(row: dict[str, str]) -> float:
    return (
        0.16 * float(row["price_sensitivity"])
        + 0.16 * float(row["behavioral_friction"])
        + 0.14 * (1.0 - float(row["trust"]))
        + 0.12 * (1.0 - float(row["access_inclusion"]))
        + 0.10 * (1.0 - float(row["affordability"]))
        + 0.10 * float(row["digital_dependence"])
        + 0.08 * (1.0 - float(row["privacy_confidence"]))
        + 0.08 * (1.0 - float(row["local_resilience"]))
        + 0.06 * float(row["regulatory_pressure"])
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    options: list[dict[str, str]],
    vulnerabilities: list[dict[str, str]],
    regulations: list[dict[str, str]],
    pathways: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    profile_ids = {row["profile_id"] for row in profiles}
    scenario_ids = {row["scenario_id"] for row in scenarios}

    for row in options:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Option {row['option_id']} references missing profile {row['profile_id']}.")

    for row in vulnerabilities:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Vulnerability indicator {row['indicator_id']} references missing profile {row['profile_id']}.")

    for row in regulations:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Regulatory record {row['record_id']} references missing scenario {row['scenario_id']}.")

    for row in pathways:
        if row["profile_id"] not in profile_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing profile {row['profile_id']}.")
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["affordability", "trust", "digital_dependence", "sustainability_demand", "access_inclusion", "price_sensitivity", "behavioral_friction", "regulatory_pressure", "privacy_confidence", "local_resilience"]),
        ("scenarios", scenarios, ["cost_pressure", "trust_pressure", "technology_acceleration", "platform_concentration", "privacy_regulation", "sustainability_pressure", "access_gap", "consumer_protection_strength"]),
        ("options", options, ["affordability_support", "trust_building", "privacy_protection", "access_inclusion", "sustainability_credibility", "behavioral_integrity", "implementation_capacity", "market_scalability"]),
        ("vulnerabilities", vulnerabilities, ["budget_pressure", "information_asymmetry", "digital_exclusion", "behavioral_manipulation", "lack_of_alternatives", "remedy_access", "consumer_protection"]),
        ("regulations", regulations, ["privacy_rules", "pricing_transparency", "subscription_fairness", "accessibility_enforcement", "green_claims_enforcement", "platform_accountability", "consumer_remedy_strength"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("option_id") or row.get("indicator_id") or row.get("record_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in profiles:
        health = consumer_future_health(row)
        fragility = market_fragility(row)

        if health >= 0.62 and fragility < 0.56:
            profile_class = "More inclusive and trust-supporting consumer future"
        elif fragility >= 0.68:
            profile_class = "High consumer vulnerability or market fragility"
        else:
            profile_class = "Mixed or transitional consumer future"

        rows.append({
            "profile_id": row["profile_id"],
            "consumer_future_name": row["consumer_future_name"],
            "consumer_future_type": row["consumer_future_type"],
            "consumer_future_health_score": round(health, 4),
            "market_fragility_score": round(fragility, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["consumer_future_health_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in scenarios:
        transition_pressure = (
            0.16 * float(row["cost_pressure"])
            + 0.16 * float(row["trust_pressure"])
            + 0.14 * float(row["technology_acceleration"])
            + 0.14 * float(row["platform_concentration"])
            + 0.12 * float(row["sustainability_pressure"])
            + 0.10 * float(row["access_gap"])
            + 0.10 * float(row["privacy_regulation"])
            + 0.08 * (1.0 - float(row["consumer_protection_strength"]))
        )

        protection_opportunity = (
            0.22 * float(row["consumer_protection_strength"])
            + 0.18 * float(row["privacy_regulation"])
            + 0.14 * float(row["sustainability_pressure"])
            + 0.12 * (1.0 - float(row["access_gap"]))
            + 0.10 * (1.0 - float(row["trust_pressure"]))
            + 0.10 * (1.0 - float(row["cost_pressure"]))
            + 0.08 * (1.0 - float(row["platform_concentration"]))
            + 0.06 * float(row["technology_acceleration"])
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "market_transition_pressure_score": round(transition_pressure, 4),
            "consumer_protection_opportunity_score": round(protection_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["consumer_protection_opportunity_score"]), reverse=True)
    return rows


def score_options(options: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in options:
        strength = (
            0.16 * float(row["affordability_support"])
            + 0.16 * float(row["trust_building"])
            + 0.14 * float(row["privacy_protection"])
            + 0.14 * float(row["access_inclusion"])
            + 0.14 * float(row["sustainability_credibility"])
            + 0.14 * float(row["behavioral_integrity"])
            + 0.06 * float(row["implementation_capacity"])
            + 0.06 * float(row["market_scalability"])
        )

        implementation_risk = (
            0.25 * (1.0 - float(row["implementation_capacity"]))
            + 0.15 * (1.0 - float(row["market_scalability"]))
            + 0.12 * (1.0 - float(row["trust_building"]))
            + 0.12 * (1.0 - float(row["behavioral_integrity"]))
            + 0.10 * (1.0 - float(row["privacy_protection"]))
            + 0.10 * (1.0 - float(row["access_inclusion"]))
            + 0.08 * (1.0 - float(row["affordability_support"]))
            + 0.08 * (1.0 - float(row["sustainability_credibility"]))
        )

        rows.append({
            "option_id": row["option_id"],
            "profile_id": row["profile_id"],
            "option_name": row["option_name"],
            "option_type": row["option_type"],
            "consumer_support_strategy_score": round(strength, 4),
            "implementation_risk_score": round(implementation_risk, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["consumer_support_strategy_score"]), reverse=True)
    return rows


def score_vulnerabilities(vulnerabilities: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in vulnerabilities:
        priority = (
            0.18 * float(row["budget_pressure"])
            + 0.16 * float(row["information_asymmetry"])
            + 0.14 * float(row["digital_exclusion"])
            + 0.18 * float(row["behavioral_manipulation"])
            + 0.14 * float(row["lack_of_alternatives"])
            + 0.10 * (1.0 - float(row["remedy_access"]))
            + 0.10 * (1.0 - float(row["consumer_protection"]))
        )

        rows.append({
            "indicator_id": row["indicator_id"],
            "profile_id": row["profile_id"],
            "indicator_name": row["indicator_name"],
            "indicator_domain": row["indicator_domain"],
            "consumer_vulnerability_priority_score": round(priority, 4),
            "remedy_access": float(row["remedy_access"]),
            "consumer_protection": float(row["consumer_protection"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["consumer_vulnerability_priority_score"]), reverse=True)
    return rows


def score_regulatory_records(regulations: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in regulations:
        strength = (
            0.16 * float(row["privacy_rules"])
            + 0.14 * float(row["pricing_transparency"])
            + 0.14 * float(row["subscription_fairness"])
            + 0.14 * float(row["accessibility_enforcement"])
            + 0.14 * float(row["green_claims_enforcement"])
            + 0.14 * float(row["platform_accountability"])
            + 0.14 * float(row["consumer_remedy_strength"])
        )

        rows.append({
            "record_id": row["record_id"],
            "scenario_id": row["scenario_id"],
            "regulatory_domain": row["regulatory_domain"],
            "public_interest_market_governance_score": round(strength, 4),
            "consumer_remedy_strength": float(row["consumer_remedy_strength"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["public_interest_market_governance_score"]), reverse=True)
    return rows


def simulate_adoption(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        affordability = float(row["affordability"])
        trust = float(row["trust"])
        access_index = float(row["access_index"])
        platform_visibility = float(row["platform_visibility"])
        sustainability = float(row["sustainability_demand"])
        social = float(row["social_influence"])
        friction = float(row["behavioral_friction"])
        price_sensitivity = float(row["price_sensitivity"])
        adoption = float(row["initial_adoption"])
        horizon = int(row["time_horizon"])

        vulnerability = (
            0.24 * (1.0 - affordability)
            + 0.20 * friction
            + 0.18 * price_sensitivity
            + 0.16 * (1.0 - access_index)
            + 0.12 * (1.0 - trust)
            + 0.10 * platform_visibility
        )

        adoption_values: list[float] = []
        trust_values: list[float] = []
        vulnerability_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                pressure_event = 0.16 if t % 8 == 0 else 0.05

                enabling_force = (
                    0.20 * affordability
                    + 0.20 * trust
                    + 0.18 * access_index
                    + 0.16 * platform_visibility
                    + 0.14 * sustainability
                    + 0.12 * social
                )

                barrier_force = (
                    0.22 * friction
                    + 0.20 * price_sensitivity
                    + 0.18 * (1.0 - affordability)
                    + 0.14 * (1.0 - access_index)
                    + 0.14 * (1.0 - trust)
                    + 0.12 * pressure_event
                )

                trust = clamp(
                    trust
                    + 0.03 * access_index
                    + 0.03 * affordability
                    + 0.02 * sustainability
                    - 0.04 * friction
                    - 0.03 * pressure_event,
                    0.0,
                    1.2,
                )

                vulnerability = clamp(
                    vulnerability
                    + 0.05 * pressure_event
                    + 0.03 * price_sensitivity
                    + 0.03 * friction
                    - 0.03 * access_index
                    - 0.03 * trust,
                    0.0,
                    1.4,
                )

                diffusion = 0.18 * adoption * (1.0 - adoption)
                adoption = clamp(
                    adoption
                    + diffusion
                    + 0.06 * enabling_force
                    - 0.05 * barrier_force
                    - 0.03 * vulnerability,
                    0.0,
                    1.0,
                )

            adoption_values.append(adoption)
            trust_values.append(trust)
            vulnerability_values.append(vulnerability)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "profile_id": row["profile_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "adoption": round(adoption, 4),
                "trust": round(trust, 4),
                "consumer_vulnerability": round(vulnerability, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_adoption": round(adoption_values[-1], 4),
            "mean_adoption": round(mean(adoption_values), 4),
            "final_trust": round(trust_values[-1], 4),
            "mean_vulnerability": round(mean(vulnerability_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_adoption"]), reverse=True)
    return trajectory_rows, summary_rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    option_scores: list[dict[str, Any]],
    vulnerability_scores: list[dict[str, Any]],
    regulatory_scores: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Consumer Future Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['consumer_future_name']}**: health {row['consumer_future_health_score']}; "
            f"fragility {row['market_fragility_score']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Market Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: transition pressure {row['market_transition_pressure_score']}; "
            f"protection opportunity {row['consumer_protection_opportunity_score']}."
        )

    lines.extend(["", "## Consumer Strategy Option Scores", ""])
    for row in option_scores:
        lines.append(
            f"- **{row['option_name']}**: support score {row['consumer_support_strategy_score']}; "
            f"implementation risk {row['implementation_risk_score']}."
        )

    lines.extend(["", "## Consumer Vulnerability Priority Scores", ""])
    for row in vulnerability_scores:
        lines.append(
            f"- **{row['indicator_name']}**: vulnerability priority {row['consumer_vulnerability_priority_score']}; "
            f"remedy access {row['remedy_access']}."
        )

    lines.extend(["", "## Regulatory Market Governance Scores", ""])
    for row in regulatory_scores:
        lines.append(
            f"- **{row['regulatory_domain']}**: governance score {row['public_interest_market_governance_score']}; "
            f"remedy strength {row['consumer_remedy_strength']}."
        )

    lines.extend(["", "## Adoption Pathway Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final adoption {row['final_adoption']}; "
            f"final trust {row['final_trust']}; mean vulnerability {row['mean_vulnerability']}."
        )

    avg_health = mean(float(row["consumer_future_health_score"]) for row in profile_scores)
    avg_fragility = mean(float(row["market_fragility_score"]) for row in profile_scores)
    avg_adoption = mean(float(row["final_adoption"]) for row in pathway_summary)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Consumer future profiles: {len(profile_scores)}.",
        f"- Market scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(option_scores)}.",
        f"- Vulnerability indicators: {len(vulnerability_scores)}.",
        f"- Regulatory records: {len(regulatory_scores)}.",
        f"- Average consumer future health score: {round(avg_health, 4)}.",
        f"- Average market fragility score: {round(avg_fragility, 4)}.",
        f"- Average final adoption: {round(avg_adoption, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats consumer futures as systems shaped by affordability trust digital mediation sustainability access inclusion behavioral friction regulation vulnerability and market power.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "consumer_market_futures_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "consumer_future_profiles.csv")
    scenarios_raw = read_csv(DATA / "market_scenarios.csv")
    options_raw = read_csv(DATA / "consumer_strategy_options.csv")
    vulnerabilities_raw = read_csv(DATA / "vulnerability_indicators.csv")
    regulations_raw = read_csv(DATA / "regulatory_market_records.csv")
    pathways_raw = read_csv(DATA / "adoption_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, options_raw, vulnerabilities_raw, regulations_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    option_scores = score_options(options_raw)
    vulnerability_scores = score_vulnerabilities(vulnerabilities_raw)
    regulatory_scores = score_regulatory_records(regulations_raw)
    trajectories, pathway_summary = simulate_adoption(pathways_raw)

    write_csv(OUTPUTS / "consumer_future_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "market_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "consumer_strategy_option_scores.csv", option_scores)
    write_csv(OUTPUTS / "vulnerability_priority_scores.csv", vulnerability_scores)
    write_csv(OUTPUTS / "regulatory_market_scores.csv", regulatory_scores)
    write_csv(OUTPUTS / "adoption_pathways.csv", trajectories)
    write_csv(OUTPUTS / "adoption_pathway_summary.csv", pathway_summary)

    write_report(config, profile_scores, scenario_scores, option_scores, vulnerability_scores, regulatory_scores, pathway_summary)

    print(f"Consumer market futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
