#!/usr/bin/env python3
from __future__ import annotations

import csv, json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
CONFIG = ROOT / "article_config.json"
OUTPUTS.mkdir(exist_ok=True)

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]

def classify_traceability(score: float) -> str:
    if score >= 0.80: return "Strong traceability"
    if score >= 0.65: return "Moderate traceability"
    return "Weak traceability"

def validate(drivers, signals, scenarios, assumptions, evaluations, lineage):
    errors=[]
    driver_ids={r["driver_id"] for r in drivers}
    scenario_ids={r["scenario_id"] for r in scenarios}
    for r in drivers:
        for field in ["driver_id","driver_name","impact","uncertainty"]:
            if not r.get(field): errors.append(f"Driver missing {field}: {r}")
        for field in ["impact","uncertainty","source_traceability","freshness","completeness","validity"]:
            v=float(r[field])
            if not 0 <= v <= 1: errors.append(f"Driver {r['driver_id']} field {field} outside 0-1 range")
    for r in signals:
        if r["driver_id"] not in driver_ids: errors.append(f"Signal {r['signal_id']} references missing driver {r['driver_id']}")
    for r in scenarios:
        for did in split_ids(r["linked_drivers"]):
            if did not in driver_ids: errors.append(f"Scenario {r['scenario_id']} references missing driver {did}")
    for r in assumptions:
        if r["scenario_id"] not in scenario_ids: errors.append(f"Assumption {r['assumption_id']} references missing scenario {r['scenario_id']}")
    for r in evaluations:
        if r["scenario_id"] not in scenario_ids: errors.append(f"Evaluation {r['evaluation_id']} references missing scenario {r['scenario_id']}")
    for r in lineage:
        if not r["source_object_id"] or not r["target_object_id"]: errors.append(f"Lineage edge {r['edge_id']} missing source or target")
    return errors

def score_drivers(rows):
    out=[]
    for r in rows:
        impact=float(r["impact"]); uncertainty=float(r["uncertainty"])
        quality=0.25*float(r["completeness"])+0.25*float(r["validity"])+0.25*float(r["freshness"])+0.25*float(r["source_traceability"])
        out.append({**r,"data_quality_score":round(quality,4),"driver_priority_score":round(impact*uncertainty,4)})
    return sorted(out,key=lambda x:(float(x["data_quality_score"]),float(x["driver_priority_score"])),reverse=True)

def score_signals(rows):
    out=[]
    for r in rows:
        quality=0.25*float(r["evidence_quality"])+0.25*float(r["source_traceability"])+0.20*float(r["relevance"])+0.15*float(r["urgency"])+0.15*float(r["affected_voice"])
        priority=0.16*float(r["novelty"])+0.24*float(r["relevance"])+0.22*float(r["urgency"])+0.18*float(r["evidence_quality"])+0.10*float(r["affected_voice"])+0.10*float(r["source_traceability"])
        out.append({**r,"data_quality_score":round(quality,4),"warning_priority_score":round(priority,4)})
    return sorted(out,key=lambda x:float(x["warning_priority_score"]),reverse=True)

def score_scenarios(rows):
    out=[]
    for r in rows:
        dcount=len(split_ids(r["linked_drivers"])); acount=int(r["assumption_count"]); ecount=int(r["evidence_note_count"])
        review=1.0 if r["review_status"]=="reviewed" else 0.65
        trace=0.35*min(dcount/5,1)+0.30*min(acount/6,1)+0.25*min(ecount/10,1)+0.10*review
        out.append({**r,"linked_driver_count":dcount,"scenario_traceability_score":round(trace,4),"traceability_class":classify_traceability(trace)})
    return sorted(out,key=lambda x:float(x["scenario_traceability_score"]),reverse=True)

def score_assumptions(rows):
    out=[]
    for r in rows:
        score=0.35*(1-float(r["confidence"]))+0.35*float(r["fragility"])+0.30*float(r["strategic_impact"])
        out.append({**r,"assumption_fragility_score":round(score,4)})
    return sorted(out,key=lambda x:float(x["assumption_fragility_score"]),reverse=True)

def score_evals(rows):
    out=[]
    for r in rows:
        score=0.25*float(r["effectiveness"])+0.20*float(r["feasibility"])+0.20*float(r["equity"])+0.20*float(r["legitimacy"])+0.15*float(r["adaptability"])
        out.append({**r,"strategy_viability_score":round(score,4)})
    return sorted(out,key=lambda x:float(x["strategy_viability_score"]),reverse=True)

def score_lineage(rows):
    out=[]
    for r in rows:
        out.append({**r,"lineage_criticality_score":round(float(r["dependency_strength"]),4)})
    return sorted(out,key=lambda x:float(x["lineage_criticality_score"]),reverse=True)

def score_runs(rows):
    out=[]
    for r in rows:
        expected=max(float(r["expected_outputs"]),1.0); generated=float(r["generated_outputs"])
        out.append({**r,"workflow_integrity_score":round(min(generated/expected,1.0),4)})
    return sorted(out,key=lambda x:float(x["workflow_integrity_score"]),reverse=True)

def write_report(config, drivers, signals, scenarios, assumptions, evaluations, lineage, runs):
    lines=[f"# Research Workflow Report: {config['title']}","",f"Generated: {datetime.now(timezone.utc).isoformat()}","",config["focus"],"","## Summary Diagnostics",""]
    lines += [f"- Driver records: {len(drivers)}.",f"- Signal records: {len(signals)}.",f"- Scenario records: {len(scenarios)}.",f"- Assumption records: {len(assumptions)}.",f"- Strategy evaluation records: {len(evaluations)}."]
    lines += [f"- Average driver data quality: {round(mean(float(r['data_quality_score']) for r in drivers),4)}.",f"- Average scenario traceability: {round(mean(float(r['scenario_traceability_score']) for r in scenarios),4)}.",f"- Average workflow integrity: {round(mean(float(r['workflow_integrity_score']) for r in runs),4)}."]
    lines += ["","## Driver Data Quality",""]
    for r in drivers: lines.append(f"- **{r['driver_name']}**: quality {r['data_quality_score']}; priority {r['driver_priority_score']}; review {r['review_status']}.")
    lines += ["","## Scenario Traceability",""]
    for r in scenarios: lines.append(f"- **{r['scenario_name']}**: traceability {r['scenario_traceability_score']} ({r['traceability_class']}).")
    lines += ["","## Assumption Fragility",""]
    for r in assumptions: lines.append(f"- **{r['assumption_name']}**: fragility {r['assumption_fragility_score']}; revision rule: {r['revision_rule']}")
    lines += ["","## Interpretation", "", "This workflow validates records, scores quality and traceability, tracks assumption fragility, preserves lineage, checks workflow integrity, and generates reusable outputs for future foresight review cycles.", "", f"Repository URL: {config['repository_url']}"]
    (OUTPUTS/"foresight_data_systems_report.md").write_text("\n".join(lines),encoding="utf-8")

def main():
    config=json.loads(CONFIG.read_text(encoding="utf-8"))
    drivers_raw=read_csv(DATA/"drivers.csv"); signals_raw=read_csv(DATA/"signals.csv"); scenarios_raw=read_csv(DATA/"scenarios.csv")
    assumptions_raw=read_csv(DATA/"assumptions.csv"); evals_raw=read_csv(DATA/"strategy_evaluations.csv"); lineage_raw=read_csv(DATA/"lineage_edges.csv"); runs_raw=read_csv(DATA/"workflow_runs.csv")
    errors=validate(drivers_raw,signals_raw,scenarios_raw,assumptions_raw,evals_raw,lineage_raw)
    if errors:
        for e in errors: print(f"VALIDATION ERROR: {e}")
        raise SystemExit("Validation failed. Fix source data before generating outputs.")
    drivers=score_drivers(drivers_raw); signals=score_signals(signals_raw); scenarios=score_scenarios(scenarios_raw); assumptions=score_assumptions(assumptions_raw); evals=score_evals(evals_raw); lineage=score_lineage(lineage_raw); runs=score_runs(runs_raw)
    write_csv(OUTPUTS/"driver_data_quality_scores.csv",drivers); write_csv(OUTPUTS/"signal_data_quality_scores.csv",signals); write_csv(OUTPUTS/"scenario_traceability_scores.csv",scenarios); write_csv(OUTPUTS/"assumption_fragility_scores.csv",assumptions); write_csv(OUTPUTS/"strategy_evaluation_scores.csv",evals); write_csv(OUTPUTS/"lineage_dependency_scores.csv",lineage); write_csv(OUTPUTS/"workflow_integrity_scores.csv",runs)
    write_report(config,drivers,signals,scenarios,assumptions,evals,lineage,runs)
    print(f"Foresight data systems workflow complete for: {config['title']}"); print(f"Outputs written to: {OUTPUTS}")
if __name__=="__main__": main()
