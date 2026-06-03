#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; OUTPUTS=ROOT/"outputs"; OUTPUTS.mkdir(exist_ok=True)
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Advanced dependencies are missing.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r requirements-advanced.txt")
    print(f"Original error: {exc}")
    sys.exit(0)
config=json.loads((ROOT/"article_config.json").read_text(encoding="utf-8"))
drivers=pd.read_csv(DATA/"drivers.csv"); scenarios=pd.read_csv(DATA/"scenarios.csv"); assumptions=pd.read_csv(DATA/"assumptions.csv"); runs=pd.read_csv(DATA/"workflow_runs.csv")
drivers["data_quality_score"]=0.25*drivers["completeness"]+0.25*drivers["validity"]+0.25*drivers["freshness"]+0.25*drivers["source_traceability"]
drivers["driver_priority_score"]=drivers["impact"]*drivers["uncertainty"]
scenarios["linked_driver_count"]=scenarios["linked_drivers"].apply(lambda x: len(str(x).split(";")))
scenarios["review_status_score"]=scenarios["review_status"].apply(lambda x: 1.0 if x=="reviewed" else 0.65)
scenarios["scenario_traceability_score"]=0.35*(scenarios["linked_driver_count"]/5).clip(upper=1)+0.30*(scenarios["assumption_count"]/6).clip(upper=1)+0.25*(scenarios["evidence_note_count"]/10).clip(upper=1)+0.10*scenarios["review_status_score"]
assumptions["assumption_fragility_score"]=0.35*(1-assumptions["confidence"])+0.35*assumptions["fragility"]+0.30*assumptions["strategic_impact"]
runs["workflow_integrity_score"]=(runs["generated_outputs"]/runs["expected_outputs"].clip(lower=1)).clip(upper=1)
drivers.to_csv(OUTPUTS/"advanced_driver_data_quality_scores.csv",index=False); scenarios.to_csv(OUTPUTS/"advanced_scenario_traceability_scores.csv",index=False); assumptions.to_csv(OUTPUTS/"advanced_assumption_fragility_scores.csv",index=False); runs.to_csv(OUTPUTS/"advanced_workflow_integrity_scores.csv",index=False)
for df, label, value, outfile in [(drivers,"driver_name","data_quality_score","driver_data_quality_scores.png"),(scenarios,"scenario_name","scenario_traceability_score","scenario_traceability_scores.png"),(assumptions,"assumption_name","assumption_fragility_score","assumption_fragility_scores.png"),(runs,"workflow_name","workflow_integrity_score","workflow_integrity_scores.png")]:
    ranked=df.sort_values(value); plt.figure(figsize=(10,6)); plt.barh(ranked[label],ranked[value]); plt.xlabel(value.replace("_"," ").title()); plt.tight_layout(); plt.savefig(OUTPUTS/outfile,dpi=150); plt.close()
print(f"Advanced workflow complete for: {config['title']}"); print(f"Outputs written to: {OUTPUTS}")
