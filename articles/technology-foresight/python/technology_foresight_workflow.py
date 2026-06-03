#!/usr/bin/env python3
from __future__ import annotations
import csv, json
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
        writer.writeheader(); writer.writerows(rows)

def clamp(value: float, low: float = 0.0, high: float = 2.0) -> float:
    return max(low, min(high, value))

def classify_priority(score: float) -> str:
    if score >= 0.72: return "High-priority foresight concern"
    if score >= 0.62: return "Moderate-priority foresight concern"
    return "Monitor"

def score_technologies(rows):
    out=[]
    for r in rows:
        m,c,s,i,g,l,e,d,imp = [float(r[k]) for k in ["maturity","capability_growth","institutional_support","infrastructure_readiness","governance_readiness","social_legitimacy","ecological_pressure","distributional_risk","strategic_importance"]]
        enabling = 0.16*m + 0.18*c + 0.16*s + 0.16*i + 0.14*g + 0.12*l + 0.08*(1-e)
        risk = 0.25*d + 0.20*e + 0.20*(1-g) + 0.15*(1-l) + 0.20*imp
        priority = 0.55*risk + 0.45*enabling
        out.append({**r,"enabling_score":round(enabling,4),"risk_score":round(risk,4),"foresight_priority_score":round(priority,4),"priority_class":classify_priority(priority)})
    return sorted(out, key=lambda x: float(x["foresight_priority_score"]), reverse=True)

def score_signals(rows):
    out=[]
    for r in rows:
        score = 0.14*float(r["novelty"]) + 0.24*float(r["relevance"]) + 0.20*float(r["urgency"]) + 0.14*float(r["evidence_quality"]) + 0.12*float(r["affected_voice"]) + 0.16*float(r["governance_relevance"])
        out.append({**r,"signal_priority_score":round(score,4)})
    return sorted(out, key=lambda x: float(x["signal_priority_score"]), reverse=True)

def score_governance(rows):
    out=[]
    for r in rows:
        readiness = 0.22*float(r["regulatory_capacity"]) + 0.20*float(r["standards_maturity"]) + 0.22*float(r["accountability_infrastructure"]) + 0.18*float(r["public_participation"]) + 0.18*float(r["enforcement_feasibility"])
        out.append({**r,"governance_readiness_score":round(readiness,4),"governance_gap_score":round(1-readiness,4)})
    return sorted(out, key=lambda x: float(x["governance_gap_score"]), reverse=True)

def score_risks(rows):
    out=[]
    for r in rows:
        score = 0.25*float(r["burden_concentration"]) + 0.22*float(r["exposure"]) + 0.22*float(r["worker_displacement"]) + 0.21*float(r["community_vulnerability"]) + 0.10*(1-float(r["mitigation_capacity"]))
        out.append({**r,"distributional_risk_score":round(score,4)})
    return sorted(out, key=lambda x: float(x["distributional_risk_score"]), reverse=True)

def simulate_pathways(rows):
    trajectories=[]; summaries=[]
    for r in rows:
        state=float(r["initial_state"]); horizon=int(r["time_horizon"]); values=[]
        for t in range(1,horizon+1):
            if t>1:
                enabling = 0.22*float(r["capability"]) + 0.20*float(r["institutional_support"]) + 0.18*float(r["governance_readiness"]) + 0.16*float(r["public_legitimacy"])
                friction = 0.18*float(r["constraint_pressure"]) + 0.16*float(r["distributional_risk"]) + 0.10*(1-float(r["governance_readiness"]))
                shock = 0.03 if t % 9 != 0 else 0.10
                penalty = 0.04 if float(r["public_legitimacy"]) < 0.45 and t > 12 else 0.0
                state = clamp(state + enabling/4 - friction/4 - shock/5 - penalty)
            values.append(state)
            trajectories.append({"pathway_id":r["pathway_id"],"technology_id":r["technology_id"],"pathway_name":r["pathway_name"],"time_step":t,"trajectory_strength":round(state,4)})
        summaries.append({"pathway_id":r["pathway_id"],"technology_id":r["technology_id"],"pathway_name":r["pathway_name"],"final_trajectory_strength":round(values[-1],4),"mean_trajectory_strength":round(mean(values),4),"minimum_trajectory_strength":round(min(values),4),"maximum_trajectory_strength":round(max(values),4)})
    return trajectories, sorted(summaries, key=lambda x: float(x["final_trajectory_strength"]), reverse=True)

def score_strategies(rows):
    out=[]
    for r in rows:
        a,p,pi,g,l,e = [float(r[k]) for k in ["acceleration","precaution","public_investment","governance_strength","labor_protection","ecological_safeguard"]]
        viability = 0.16*a + 0.18*p + 0.18*pi + 0.20*g + 0.16*l + 0.12*e
        public = 0.12*a + 0.20*p + 0.20*pi + 0.22*g + 0.16*l + 0.10*e
        out.append({**r,"strategy_viability_score":round(viability,4),"public_interest_score":round(public,4)})
    return sorted(out, key=lambda x: float(x["public_interest_score"]), reverse=True)

def main():
    config=json.loads(CONFIG.read_text())
    tech=read_csv(DATA/"technology_profiles.csv"); ids={r["technology_id"] for r in tech}
    signals=read_csv(DATA/"technology_signals.csv"); controls=read_csv(DATA/"governance_controls.csv"); risks=read_csv(DATA/"distributional_risks.csv"); pathways=read_csv(DATA/"pathway_parameters.csv"); strategies=read_csv(DATA/"strategy_options.csv")
    for label, rows in [("signals",signals),("controls",controls),("risks",risks),("pathways",pathways)]:
        for r in rows:
            if r["technology_id"] not in ids: raise SystemExit(f"Validation failed: {label} references missing technology {r['technology_id']}")
    scored_tech=score_technologies(tech); scored_signals=score_signals(signals); scored_gov=score_governance(controls); scored_risks=score_risks(risks); traj, summary=simulate_pathways(pathways); scored_strategies=score_strategies(strategies)
    write_csv(OUTPUTS/"technology_foresight_profiles.csv", scored_tech); write_csv(OUTPUTS/"signal_priority_scores.csv", scored_signals); write_csv(OUTPUTS/"governance_readiness_scores.csv", scored_gov); write_csv(OUTPUTS/"distributional_risk_scores.csv", scored_risks); write_csv(OUTPUTS/"technology_pathway_trajectories.csv", traj); write_csv(OUTPUTS/"technology_pathway_summary.csv", summary); write_csv(OUTPUTS/"strategy_option_scores.csv", scored_strategies)
    lines=[f"# Research Workflow Report: {config['title']}","",config["focus"],"","## Technology Foresight Profiles"]
    for r in scored_tech: lines.append(f"- **{r['technology_name']}**: priority {r['foresight_priority_score']}; enabling {r['enabling_score']}; risk {r['risk_score']}; {r['priority_class']}.")
    lines += ["","## Highest Governance Gaps"]
    for r in scored_gov[:5]: lines.append(f"- **{r['control_name']}**: governance gap {r['governance_gap_score']}.")
    lines += ["","## Highest Distributional Risks"]
    for r in scored_risks[:5]: lines.append(f"- **{r['risk_name']}**: distributional risk {r['distributional_risk_score']}.")
    lines += ["","## Pathway Simulation Summary"]
    for r in summary: lines.append(f"- **{r['pathway_name']}**: final trajectory {r['final_trajectory_strength']}; mean {r['mean_trajectory_strength']}.")
    lines += ["","## Strategy Option Scores"]
    for r in scored_strategies: lines.append(f"- **{r['strategy_name']}**: public-interest score {r['public_interest_score']}; viability {r['strategy_viability_score']}.")
    lines += ["",f"Repository URL: {config['repository_url']}"]
    (OUTPUTS/"technology_foresight_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Technology foresight workflow complete for: {config['title']}")
    print(f"Outputs written to: {OUTPUTS}")
if __name__ == "__main__": main()
