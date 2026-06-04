#!/usr/bin/env python3
"""
Standard-library workflow for Ethics of Futures Thinking.

Outputs:
- ethical_futures_profile_scores.csv
- ethical_scenario_scores.csv
- ethical_strategy_scores.csv
- ethical_risk_priority_scores.csv
- stakeholder_distribution_scores.csv
- intergenerational_ethics_trajectories.csv
- intergenerational_ethics_summary.csv
- ethics_of_futures_thinking_report.md
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev
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


def ethical_profile_score(row: dict[str, str]) -> float:
    return (
        0.13 * float(row["intergenerational_responsibility"])
        + 0.12 * float(row["inclusion"])
        + 0.12 * float(row["accountability"])
        + 0.12 * float(row["risk_equity"])
        + 0.10 * float(row["transparency"])
        + 0.10 * float(row["contestability"])
        + 0.10 * float(row["precaution"])
        + 0.08 * float(row["adaptive_learning"])
        + 0.08 * float(row["epistemic_pluralism"])
        + 0.05 * float(row["public_legitimacy"])
    )


def validate_records(
    profiles: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    strategies: list[dict[str, str]],
    risks: list[dict[str, str]],
    distributions: list[dict[str, str]],
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

    for row in distributions:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Distribution record {row['record_id']} references missing scenario {row['scenario_id']}.")

    for row in pathways:
        if row["scenario_id"] not in scenario_ids:
            errors.append(f"Pathway {row['pathway_id']} references missing scenario {row['scenario_id']}.")

    numeric_specs = [
        ("profiles", profiles, ["intergenerational_responsibility", "inclusion", "accountability", "risk_equity", "transparency", "contestability", "precaution", "adaptive_learning", "epistemic_pluralism", "public_legitimacy"]),
        ("scenarios", scenarios, ["technocratic_opacity", "participation_depth", "intergenerational_weight", "risk_inequality", "corporate_capture_pressure", "security_drift", "climate_justice_alignment", "ai_opacity", "accountability_strength", "adaptive_learning_capacity"]),
        ("strategies", strategies, ["value_transparency_gain", "participation_gain", "distributional_justice_gain", "intergenerational_review_gain", "epistemic_pluralism_gain", "precaution_gain", "accountability_gain", "contestability_gain", "adaptive_learning_gain", "implementation_capacity", "public_legitimacy_gain"]),
        ("risks", risks, ["probability_proxy", "severity", "irreversibility", "visibility_gap", "distributional_harm", "rights_risk", "preparedness"]),
        ("distributions", distributions, ["benefit", "risk", "voice_weight", "moral_weight", "exposure", "protection"]),
        ("pathways", pathways, ["present_benefit", "future_benefit", "present_risk", "future_risk", "discount_weight", "inequality_penalty", "participation_quality", "accountability_strength", "precaution_strength", "adaptive_learning_capacity"]),
    ]

    for dataset_name, rows, fields in numeric_specs:
        for row in rows:
            row_id = row.get("profile_id") or row.get("scenario_id") or row.get("strategy_id") or row.get("risk_id") or row.get("record_id") or row.get("pathway_id") or "unknown"
            for field in fields:
                value = float(row[field])
                if not 0.0 <= value <= 1.0:
                    errors.append(f"{dataset_name} record {row_id} field {field} outside 0-1 range.")

    return errors


def score_profiles(profiles: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in profiles:
        score = ethical_profile_score(row)
        gap = 1.0 - score

        if score >= 0.70:
            profile_class = "Stronger ethical futures capacity"
        elif score >= 0.55:
            profile_class = "Moderate ethical futures capacity"
        else:
            profile_class = "Weak ethical futures capacity"

        rows.append({
            "profile_id": row["profile_id"],
            "institution_type": row["institution_type"],
            "profile_family": row["profile_family"],
            "ethical_futures_profile_score": round(score, 4),
            "ethical_capacity_gap": round(gap, 4),
            "profile_class": profile_class,
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["ethical_futures_profile_score"]), reverse=True)
    return rows


def score_scenarios(scenarios: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in scenarios:
        failure_risk = (
            0.14 * float(row["technocratic_opacity"])
            + 0.14 * float(row["risk_inequality"])
            + 0.12 * float(row["corporate_capture_pressure"])
            + 0.12 * float(row["security_drift"])
            + 0.12 * float(row["ai_opacity"])
            + 0.10 * (1.0 - float(row["participation_depth"]))
            + 0.10 * (1.0 - float(row["intergenerational_weight"]))
            + 0.08 * (1.0 - float(row["accountability_strength"]))
            + 0.04 * (1.0 - float(row["climate_justice_alignment"]))
            + 0.04 * (1.0 - float(row["adaptive_learning_capacity"]))
        )

        ethical_opportunity = (
            0.15 * float(row["participation_depth"])
            + 0.14 * float(row["intergenerational_weight"])
            + 0.14 * float(row["climate_justice_alignment"])
            + 0.14 * float(row["accountability_strength"])
            + 0.11 * float(row["adaptive_learning_capacity"])
            + 0.09 * (1.0 - float(row["risk_inequality"]))
            + 0.08 * (1.0 - float(row["technocratic_opacity"]))
            + 0.06 * (1.0 - float(row["ai_opacity"]))
            + 0.05 * (1.0 - float(row["corporate_capture_pressure"]))
            + 0.04 * (1.0 - float(row["security_drift"]))
        )

        rows.append({
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "scenario_family": row["scenario_family"],
            "ethical_failure_risk_score": round(failure_risk, 4),
            "ethical_opportunity_score": round(ethical_opportunity, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["ethical_failure_risk_score"]), reverse=True)
    return rows


def score_strategies(strategies: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in strategies:
        value = (
            0.11 * float(row["value_transparency_gain"])
            + 0.13 * float(row["participation_gain"])
            + 0.13 * float(row["distributional_justice_gain"])
            + 0.12 * float(row["intergenerational_review_gain"])
            + 0.10 * float(row["epistemic_pluralism_gain"])
            + 0.09 * float(row["precaution_gain"])
            + 0.11 * float(row["accountability_gain"])
            + 0.10 * float(row["contestability_gain"])
            + 0.07 * float(row["adaptive_learning_gain"])
            + 0.02 * float(row["implementation_capacity"])
            + 0.02 * float(row["public_legitimacy_gain"])
        )

        readiness = (
            0.20 * float(row["implementation_capacity"])
            + 0.16 * float(row["public_legitimacy_gain"])
            + 0.14 * float(row["accountability_gain"])
            + 0.12 * float(row["participation_gain"])
            + 0.10 * float(row["contestability_gain"])
            + 0.08 * float(row["value_transparency_gain"])
            + 0.07 * float(row["adaptive_learning_gain"])
            + 0.05 * float(row["precaution_gain"])
            + 0.04 * float(row["distributional_justice_gain"])
            + 0.04 * float(row["epistemic_pluralism_gain"])
        )

        rows.append({
            "strategy_id": row["strategy_id"],
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "ethical_strategy_value_score": round(value, 4),
            "implementation_readiness_score": round(readiness, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["ethical_strategy_value_score"]), reverse=True)
    return rows


def score_risks(risks: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in risks:
        priority = (
            0.14 * float(row["probability_proxy"])
            + 0.17 * float(row["severity"])
            + 0.15 * float(row["irreversibility"])
            + 0.10 * float(row["visibility_gap"])
            + 0.20 * float(row["distributional_harm"])
            + 0.14 * float(row["rights_risk"])
            + 0.10 * (1.0 - float(row["preparedness"]))
        )

        rows.append({
            "risk_id": row["risk_id"],
            "scenario_id": row["scenario_id"],
            "risk_name": row["risk_name"],
            "risk_domain": row["risk_domain"],
            "ethical_risk_priority_score": round(priority, 4),
            "distributional_harm": float(row["distributional_harm"]),
            "rights_risk": float(row["rights_risk"]),
            "preparedness": float(row["preparedness"]),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["ethical_risk_priority_score"]), reverse=True)
    return rows


def score_distributions(distributions: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in distributions:
        benefit = float(row["benefit"])
        risk = float(row["risk"])
        voice = float(row["voice_weight"])
        moral = float(row["moral_weight"])
        exposure = float(row["exposure"])
        protection = float(row["protection"])

        net_welfare = benefit - risk
        justice_adjusted = benefit - risk - 0.35 * exposure + 0.25 * protection + 0.20 * moral + 0.10 * voice
        vulnerability_gap = max(0.0, exposure - protection)

        rows.append({
            "record_id": row["record_id"],
            "scenario_id": row["scenario_id"],
            "group_name": row["group_name"],
            "time_period": row["time_period"],
            "benefit": benefit,
            "risk": risk,
            "net_welfare": round(net_welfare, 4),
            "justice_adjusted_score": round(justice_adjusted, 4),
            "vulnerability_gap": round(vulnerability_gap, 4),
            "description": row["description"],
        })

    rows.sort(key=lambda item: float(item["justice_adjusted_score"]))
    return rows


def simulate_pathways(pathways: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    trajectory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for row in pathways:
        present_benefit = float(row["present_benefit"])
        future_benefit = float(row["future_benefit"])
        present_risk = float(row["present_risk"])
        future_risk = float(row["future_risk"])
        discount = float(row["discount_weight"])
        inequality_penalty = float(row["inequality_penalty"])
        participation = float(row["participation_quality"])
        accountability = float(row["accountability_strength"])
        precaution = float(row["precaution_strength"])
        learning = float(row["adaptive_learning_capacity"])
        horizon = int(row["time_horizon"])

        legitimacy = (
            0.30 * participation
            + 0.28 * accountability
            + 0.18 * precaution
            + 0.14 * learning
            + 0.10 * discount
        )

        justice_score = (
            0.25 * present_benefit
            + 0.25 * future_benefit * discount
            - 0.20 * present_risk
            - 0.20 * future_risk
            - 0.10 * inequality_penalty
            + 0.10 * legitimacy
        )

        present_values: list[float] = []
        future_values: list[float] = []
        risk_values: list[float] = []
        legitimacy_values: list[float] = []
        justice_values: list[float] = []

        for t in range(1, horizon + 1):
            if t > 1:
                short_term_pressure = 0.008 if t % 6 == 0 else 0.0
                model_error = 0.006 if t % 9 == 0 else 0.0
                crisis_pressure = 0.010 if t % 13 == 0 else 0.0

                present_benefit = clamp(
                    present_benefit
                    + 0.012
                    + short_term_pressure
                    - 0.006 * participation
                    - 0.004 * precaution,
                    0.0,
                    1.8,
                )

                future_benefit = clamp(
                    future_benefit
                    + 0.012 * discount
                    + 0.010 * learning
                    + 0.006 * accountability
                    - 0.008 * short_term_pressure
                    - 0.006 * model_error,
                    0.0,
                    1.8,
                )

                present_risk = clamp(
                    present_risk
                    + 0.006 * inequality_penalty
                    + 0.006 * model_error
                    - 0.006 * accountability
                    - 0.005 * precaution,
                    0.0,
                    1.8,
                )

                future_risk = clamp(
                    future_risk
                    + 0.010 * inequality_penalty
                    + 0.008 * crisis_pressure
                    + 0.006 * model_error
                    - 0.010 * precaution
                    - 0.008 * learning
                    - 0.006 * accountability,
                    0.0,
                    1.8,
                )

                legitimacy = clamp(
                    legitimacy
                    + 0.008 * participation
                    + 0.008 * accountability
                    + 0.006 * learning
                    - 0.008 * inequality_penalty
                    - 0.005 * present_risk,
                    0.0,
                    1.8,
                )

                justice_score = clamp(
                    0.25 * present_benefit
                    + 0.25 * future_benefit * discount
                    - 0.20 * present_risk
                    - 0.20 * future_risk
                    - 0.10 * inequality_penalty
                    + 0.10 * legitimacy,
                    -1.0,
                    1.8,
                )

            present_values.append(present_benefit)
            future_values.append(future_benefit)
            risk_values.append((present_risk + future_risk) / 2.0)
            legitimacy_values.append(legitimacy)
            justice_values.append(justice_score)

            trajectory_rows.append({
                "pathway_id": row["pathway_id"],
                "scenario_id": row["scenario_id"],
                "pathway_name": row["pathway_name"],
                "time_step": t,
                "present_benefit": round(present_benefit, 4),
                "future_benefit": round(future_benefit, 4),
                "present_risk": round(present_risk, 4),
                "future_risk": round(future_risk, 4),
                "legitimacy": round(legitimacy, 4),
                "justice_adjusted_score": round(justice_score, 4),
            })

        summary_rows.append({
            "pathway_id": row["pathway_id"],
            "scenario_id": row["scenario_id"],
            "pathway_name": row["pathway_name"],
            "final_present_benefit": round(present_values[-1], 4),
            "final_future_benefit": round(future_values[-1], 4),
            "mean_risk": round(mean(risk_values), 4),
            "final_legitimacy": round(legitimacy_values[-1], 4),
            "final_justice_adjusted_score": round(justice_values[-1], 4),
            "mean_justice_adjusted_score": round(mean(justice_values), 4),
        })

    summary_rows.sort(key=lambda item: float(item["final_justice_adjusted_score"]), reverse=True)
    return trajectory_rows, summary_rows


def distribution_summary(distribution_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[float]] = {}
    for row in distribution_scores:
        grouped.setdefault(row["scenario_id"], []).append(float(row["justice_adjusted_score"]))

    rows: list[dict[str, Any]] = []
    for scenario_id, values in grouped.items():
        rows.append({
            "scenario_id": scenario_id,
            "mean_justice_adjusted_score": round(mean(values), 4),
            "justice_score_dispersion": round(pstdev(values), 4),
            "lowest_group_score": round(min(values), 4),
            "highest_group_score": round(max(values), 4),
        })

    rows.sort(key=lambda item: float(item["mean_justice_adjusted_score"]), reverse=True)
    return rows


def write_report(
    config: dict[str, Any],
    profile_scores: list[dict[str, Any]],
    scenario_scores: list[dict[str, Any]],
    strategy_scores: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    distribution_scores: list[dict[str, Any]],
    dist_summary: list[dict[str, Any]],
    pathway_summary: list[dict[str, Any]],
) -> None:
    lines = [
        f"# Research Workflow Report: {config['title']}",
        "",
        config["focus"],
        "",
        "## Ethical Futures Profile Scores",
        "",
    ]

    for row in profile_scores:
        lines.append(
            f"- **{row['institution_type']}**: profile {row['ethical_futures_profile_score']}; "
            f"capacity gap {row['ethical_capacity_gap']}; class: {row['profile_class']}."
        )

    lines.extend(["", "## Scenario Scores", ""])
    for row in scenario_scores:
        lines.append(
            f"- **{row['scenario_name']}**: ethical failure risk {row['ethical_failure_risk_score']}; "
            f"ethical opportunity {row['ethical_opportunity_score']}."
        )

    lines.extend(["", "## Strategy Scores", ""])
    for row in strategy_scores:
        lines.append(
            f"- **{row['strategy_name']}**: strategy value {row['ethical_strategy_value_score']}; "
            f"implementation readiness {row['implementation_readiness_score']}."
        )

    lines.extend(["", "## Ethical Risk Priority Scores", ""])
    for row in risk_scores:
        lines.append(
            f"- **{row['risk_name']}**: priority {row['ethical_risk_priority_score']}; "
            f"distributional harm {row['distributional_harm']}; rights risk {row['rights_risk']}."
        )

    lines.extend(["", "## Stakeholder Distribution Diagnostics", ""])
    for row in dist_summary:
        lines.append(
            f"- **{row['scenario_id']}**: mean justice-adjusted score {row['mean_justice_adjusted_score']}; "
            f"dispersion {row['justice_score_dispersion']}; lowest group score {row['lowest_group_score']}."
        )

    lines.extend(["", "## Intergenerational Ethics Summary", ""])
    for row in pathway_summary:
        lines.append(
            f"- **{row['pathway_name']}**: final justice-adjusted score {row['final_justice_adjusted_score']}; "
            f"final legitimacy {row['final_legitimacy']}; mean risk {row['mean_risk']}."
        )

    avg_profile = mean(float(row["ethical_futures_profile_score"]) for row in profile_scores)
    avg_risk = mean(float(row["ethical_risk_priority_score"]) for row in risk_scores)
    avg_strategy = mean(float(row["ethical_strategy_value_score"]) for row in strategy_scores)

    lines.extend([
        "",
        "## Summary Diagnostics",
        "",
        f"- Ethical futures profiles: {len(profile_scores)}.",
        f"- Ethical scenarios: {len(scenario_scores)}.",
        f"- Strategy options: {len(strategy_scores)}.",
        f"- Risk indicators: {len(risk_scores)}.",
        f"- Stakeholder distribution records: {len(distribution_scores)}.",
        f"- Average ethical futures profile score: {round(avg_profile, 4)}.",
        f"- Average ethical risk priority score: {round(avg_risk, 4)}.",
        f"- Average ethical strategy value score: {round(avg_strategy, 4)}.",
        "",
        "## Interpretation",
        "",
        "This workflow treats the ethics of futures thinking as an institutional and distributional system shaped by power, participation, intergenerational responsibility, risk equity, transparency, contestability, precaution, epistemic pluralism, and adaptive learning.",
        "",
        f"Repository URL: {config['repository_url']}",
    ])

    (OUTPUTS / "ethics_of_futures_thinking_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()

    profiles_raw = read_csv(DATA / "ethical_futures_profiles.csv")
    scenarios_raw = read_csv(DATA / "ethical_futures_scenarios.csv")
    strategies_raw = read_csv(DATA / "ethical_strategy_options.csv")
    risks_raw = read_csv(DATA / "ethical_risk_indicators.csv")
    distributions_raw = read_csv(DATA / "stakeholder_distribution_paths.csv")
    pathways_raw = read_csv(DATA / "intergenerational_ethics_pathways.csv")

    errors = validate_records(profiles_raw, scenarios_raw, strategies_raw, risks_raw, distributions_raw, pathways_raw)
    if errors:
        for error in errors:
            print(f"VALIDATION ERROR: {error}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")

    profile_scores = score_profiles(profiles_raw)
    scenario_scores = score_scenarios(scenarios_raw)
    strategy_scores = score_strategies(strategies_raw)
    risk_scores = score_risks(risks_raw)
    distribution_scores = score_distributions(distributions_raw)
    dist_summary = distribution_summary(distribution_scores)
    trajectories, pathway_summary = simulate_pathways(pathways_raw)

    write_csv(OUTPUTS / "ethical_futures_profile_scores.csv", profile_scores)
    write_csv(OUTPUTS / "ethical_scenario_scores.csv", scenario_scores)
    write_csv(OUTPUTS / "ethical_strategy_scores.csv", strategy_scores)
    write_csv(OUTPUTS / "ethical_risk_priority_scores.csv", risk_scores)
    write_csv(OUTPUTS / "stakeholder_distribution_scores.csv", distribution_scores)
    write_csv(OUTPUTS / "stakeholder_distribution_summary.csv", dist_summary)
    write_csv(OUTPUTS / "intergenerational_ethics_trajectories.csv", trajectories)
    write_csv(OUTPUTS / "intergenerational_ethics_summary.csv", pathway_summary)

    write_report(
        config,
        profile_scores,
        scenario_scores,
        strategy_scores,
        risk_scores,
        distribution_scores,
        dist_summary,
        pathway_summary,
    )

    print(f"Ethics of futures thinking workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")


if __name__ == "__main__":
    main()
