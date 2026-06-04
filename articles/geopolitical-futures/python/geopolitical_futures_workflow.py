#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows):
    if not rows:
        return
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def clamp(x, lo=0.0, hi=2.2):
    return max(lo, min(hi, x))

def stability(r):
    return (
        0.11 * (1 - float(r["power_concentration"])) +
        0.10 * float(r["interdependence"]) +
        0.16 * float(r["institutional_coordination"]) -
        0.12 * float(r["technological_competition"]) -
        0.12 * float(r["climate_stress"]) -
        0.11 * float(r["economic_vulnerability"]) +
        0.12 * float(r["domestic_resilience"]) +
        0.11 * float(r["information_integrity"]) +
        0.08 * float(r["resource_security"]) +
        0.07 * float(r["crisis_communication"])
    )

def cascade(r):
    return (
        0.12 * float(r["power_concentration"]) +
        0.13 * float(r["technological_competition"]) +
        0.14 * float(r["climate_stress"]) +
        0.13 * float(r["economic_vulnerability"]) +
        0.11 * (1 - float(r["institutional_coordination"])) +
        0.10 * (1 - float(r["domestic_resilience"])) +
        0.10 * (1 - float(r["information_integrity"])) +
        0.09 * (1 - float(r["resource_security"])) +
        0.08 * (1 - float(r["crisis_communication"]))
    )

def validate():
    profiles = read_csv("geopolitical_futures_profiles.csv")
    scenarios = read_csv("geopolitical_scenarios.csv")
    strategies = read_csv("geopolitical_strategy_options.csv")
    risks = read_csv("geopolitical_risk_indicators.csv")
    governance = read_csv("geopolitical_governance_records.csv")
    paths = read_csv("strategic_interaction_pathways.csv")

    profile_ids = {r["profile_id"] for r in profiles}
    scenario_ids = {r["scenario_id"] for r in scenarios}

    errors = []
    for r in strategies:
        if r["profile_id"] not in profile_ids:
            errors.append(f"Missing profile for strategy {r['strategy_id']}")
    for r in risks:
        if r["scenario_id"] not in scenario_ids:
            errors.append(f"Missing scenario for risk {r['risk_id']}")
    for r in governance:
        if r["profile_id"] not in profile_ids:
            errors.append(f"Missing profile for governance {r['record_id']}")
    for r in paths:
        if r["profile_id"] not in profile_ids:
            errors.append(f"Missing profile for pathway {r['pathway_id']}")
        if r["scenario_id"] not in scenario_ids:
            errors.append(f"Missing scenario for pathway {r['pathway_id']}")

    if errors:
        for e in errors:
            print("VALIDATION ERROR:", e)
        raise SystemExit(1)

    return profiles, scenarios, strategies, risks, governance, paths

def score_profiles(rows):
    out = []
    for r in rows:
        s = stability(r)
        c = cascade(r)
        label = "Stronger geopolitical resilience" if s >= 0.22 and c < 0.50 else "High cascade risk" if c >= 0.65 else "Mixed or transitional geopolitical pathway"
        out.append({
            "profile_id": r["profile_id"],
            "future_name": r["future_name"],
            "geopolitical_stability_score": round(s, 4),
            "cascade_risk_score": round(c, 4),
            "profile_class": label,
            "description": r["description"],
        })
    return sorted(out, key=lambda x: x["geopolitical_stability_score"], reverse=True)

def score_scenarios(rows):
    out = []
    for r in rows:
        stress = (
            0.13 * float(r["military_tension"]) +
            0.12 * float(r["economic_fragmentation"]) +
            0.12 * float(r["technology_rivalry"]) +
            0.13 * float(r["climate_security_pressure"]) +
            0.12 * float(r["institutional_weakness"]) +
            0.10 * float(r["information_disorder"]) +
            0.10 * float(r["supply_chain_stress"]) +
            0.07 * float(r["migration_pressure"]) +
            0.06 * float(r["energy_resource_stress"]) +
            0.05 * float(r["crisis_communication_gap"])
        )
        out.append({
            "scenario_id": r["scenario_id"],
            "scenario_name": r["scenario_name"],
            "geopolitical_stress_score": round(stress, 4),
            "description": r["description"],
        })
    return sorted(out, key=lambda x: x["geopolitical_stress_score"], reverse=True)

def score_strategies(rows):
    fields = [
        "diplomacy_gain", "crisis_communication_gain", "institutional_gain",
        "supply_chain_resilience_gain", "technology_governance_gain", "climate_security_gain",
        "energy_resource_gain", "information_integrity_gain", "domestic_resilience_gain",
        "regional_cooperation_gain", "implementation_capacity"
    ]
    weights = [0.12,0.14,0.14,0.10,0.10,0.10,0.08,0.08,0.08,0.05,0.01]
    out = []
    for r in rows:
        value = sum(w * float(r[f]) for w, f in zip(weights, fields))
        out.append({
            "strategy_id": r["strategy_id"],
            "profile_id": r["profile_id"],
            "strategy_name": r["strategy_name"],
            "geopolitical_strategy_value_score": round(value, 4),
            "description": r["description"],
        })
    return sorted(out, key=lambda x: x["geopolitical_strategy_value_score"], reverse=True)

def score_risks(rows):
    out = []
    for r in rows:
        priority = (
            0.14 * float(r["probability_proxy"]) +
            0.18 * float(r["severity"]) +
            0.17 * float(r["cascade_potential"]) +
            0.12 * float(r["visibility_gap"]) +
            0.14 * float(r["recovery_difficulty"]) +
            0.17 * float(r["distributional_harm"]) +
            0.08 * (1 - float(r["preparedness"]))
        )
        out.append({
            "risk_id": r["risk_id"],
            "scenario_id": r["scenario_id"],
            "risk_name": r["risk_name"],
            "geopolitical_risk_priority_score": round(priority, 4),
            "description": r["description"],
        })
    return sorted(out, key=lambda x: x["geopolitical_risk_priority_score"], reverse=True)

def score_governance(rows):
    fields = [
        "diplomatic_capacity", "crisis_communication", "institutional_legitimacy",
        "regional_coordination", "technology_accountability", "climate_security_coordination",
        "information_integrity_capacity", "domestic_resilience_capacity"
    ]
    weights = [0.14,0.16,0.16,0.12,0.10,0.10,0.11,0.11]
    out = []
    for r in rows:
        value = sum(w * float(r[f]) for w, f in zip(weights, fields))
        out.append({
            "record_id": r["record_id"],
            "profile_id": r["profile_id"],
            "record_name": r["record_name"],
            "geopolitical_governance_capacity_score": round(value, 4),
            "description": r["description"],
        })
    return sorted(out, key=lambda x: x["geopolitical_governance_capacity_score"], reverse=True)

def simulate(rows):
    trajectories, summary = [], []
    for r in rows:
        comm = float(r["communication_capacity"])
        da = float(r["domestic_pressure_a"])
        db = float(r["domestic_pressure_b"])
        inter = float(r["economic_interdependence"])
        inst = float(r["institutional_buffer"])
        tech = float(r["technology_shock_exposure"])
        clim = float(r["climate_security_exposure"])
        info = float(r["information_disorder"])
        a = float(r["initial_actor_a"])
        b = float(r["initial_actor_b"])
        horizon = int(r["time_horizon"])

        escalation = 0.20*abs(a-b) + 0.14*da + 0.14*db + 0.12*tech + 0.12*clim + 0.12*info + 0.10*(1-comm) - 0.08*inter - 0.08*inst
        resilience = 0.20*comm + 0.20*inst + 0.16*inter + 0.12*(1-da) + 0.12*(1-db) + 0.10*(1-tech) + 0.06*(1-clim) + 0.04*(1-info)
        e_vals, r_vals = [], []

        for t in range(1, horizon + 1):
            if t > 1:
                uncertainty = 0.16 if t % 8 == 0 else 0.06
                tech_shock = 0.10 * tech if t % 11 == 0 else 0.0
                clim_shock = 0.10 * clim if t % 13 == 0 else 0.0
                info_shock = 0.08 * info if t % 9 == 0 else 0.0
                action_a = 0.10 + 0.04*b + 0.03*da + 0.02*info
                action_b = 0.10 + 0.04*a + 0.03*db + 0.02*info
                restraint = 0.05*comm + 0.04*inst + 0.03*inter
                a = clamp(a + 0.22*action_a - 0.18*action_b + uncertainty + tech_shock + info_shock - restraint)
                b = clamp(b + 0.22*action_b - 0.18*action_a + uncertainty + tech_shock + info_shock - restraint)
                escalation = clamp(escalation + 0.10*uncertainty + 0.08*tech_shock + 0.08*clim_shock + 0.07*info_shock + 0.05*abs(a-b) + 0.04*da + 0.04*db - 0.06*comm - 0.05*inst - 0.03*inter, 0, 1.8)
                resilience = clamp(resilience + 0.04*comm + 0.04*inst + 0.03*inter - 0.05*escalation - 0.03*uncertainty - 0.02*tech_shock - 0.02*clim_shock - 0.02*info_shock, 0, 1.8)

            e_vals.append(escalation)
            r_vals.append(resilience)
            trajectories.append({
                "pathway_id": r["pathway_id"],
                "profile_id": r["profile_id"],
                "scenario_id": r["scenario_id"],
                "pathway_name": r["pathway_name"],
                "time_step": t,
                "actor_a_position": round(a, 4),
                "actor_b_position": round(b, 4),
                "escalation_pressure": round(escalation, 4),
                "system_resilience": round(resilience, 4),
            })

        summary.append({
            "pathway_id": r["pathway_id"],
            "pathway_name": r["pathway_name"],
            "final_escalation_pressure": round(e_vals[-1], 4),
            "mean_escalation_pressure": round(mean(e_vals), 4),
            "final_system_resilience": round(r_vals[-1], 4),
            "mean_system_resilience": round(mean(r_vals), 4),
        })
    return trajectories, sorted(summary, key=lambda x: x["final_system_resilience"], reverse=True)

def report(config, profiles, scenarios, strategies, risks, governance, summary):
    lines = [f"# Research Workflow Report: {config['title']}", "", config["focus"], ""]
    lines += ["## Profile Scores", ""]
    lines += [f"- **{r['future_name']}**: stability {r['geopolitical_stability_score']}; cascade risk {r['cascade_risk_score']}; {r['profile_class']}." for r in profiles]
    lines += ["", "## Scenario Stress", ""]
    lines += [f"- **{r['scenario_name']}**: stress {r['geopolitical_stress_score']}." for r in scenarios]
    lines += ["", "## Strategy Scores", ""]
    lines += [f"- **{r['strategy_name']}**: value {r['geopolitical_strategy_value_score']}." for r in strategies]
    lines += ["", "## Risk Priorities", ""]
    lines += [f"- **{r['risk_name']}**: priority {r['geopolitical_risk_priority_score']}." for r in risks]
    lines += ["", "## Governance Capacity", ""]
    lines += [f"- **{r['record_name']}**: capacity {r['geopolitical_governance_capacity_score']}." for r in governance]
    lines += ["", "## Strategic Interaction Summary", ""]
    lines += [f"- **{r['pathway_name']}**: final escalation {r['final_escalation_pressure']}; final resilience {r['final_system_resilience']}." for r in summary]
    lines += ["", f"Repository URL: {config['repository_url']}"]
    (OUT / "geopolitical_futures_report.md").write_text("\n".join(lines), encoding="utf-8")

def main():
    config = json.loads((ROOT / "article_config.json").read_text(encoding="utf-8"))
    profiles, scenarios, strategies, risks, governance, paths = validate()
    p_scores = score_profiles(profiles)
    s_scores = score_scenarios(scenarios)
    t_scores = score_strategies(strategies)
    r_scores = score_risks(risks)
    g_scores = score_governance(governance)
    traj, summ = simulate(paths)

    write_csv("geopolitical_profile_scores.csv", p_scores)
    write_csv("geopolitical_scenario_scores.csv", s_scores)
    write_csv("geopolitical_strategy_scores.csv", t_scores)
    write_csv("geopolitical_risk_priority_scores.csv", r_scores)
    write_csv("geopolitical_governance_capacity_scores.csv", g_scores)
    write_csv("strategic_interaction_paths.csv", traj)
    write_csv("strategic_interaction_summary.csv", summ)
    report(config, p_scores, s_scores, t_scores, r_scores, g_scores, summ)

    print(f"Geopolitical futures workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUT}")

if __name__ == "__main__":
    main()
