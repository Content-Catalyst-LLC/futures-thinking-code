#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]; DATA = ROOT / "data"; OUTPUTS = ROOT / "outputs"; OUTPUTS.mkdir(exist_ok=True)
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Advanced dependencies are missing.")
    print("Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-advanced.txt")
    print(f"Original error: {exc}")
    sys.exit(0)
config=json.loads((ROOT/"article_config.json").read_text())
tech=pd.read_csv(DATA/"technology_profiles.csv")
controls=pd.read_csv(DATA/"governance_controls.csv")
risks=pd.read_csv(DATA/"distributional_risks.csv")
tech["enabling_score"]=0.16*tech.maturity+0.18*tech.capability_growth+0.16*tech.institutional_support+0.16*tech.infrastructure_readiness+0.14*tech.governance_readiness+0.12*tech.social_legitimacy+0.08*(1-tech.ecological_pressure)
tech["risk_score"]=0.25*tech.distributional_risk+0.20*tech.ecological_pressure+0.20*(1-tech.governance_readiness)+0.15*(1-tech.social_legitimacy)+0.20*tech.strategic_importance
tech["foresight_priority_score"]=0.55*tech.risk_score+0.45*tech.enabling_score
controls["governance_readiness_score"]=0.22*controls.regulatory_capacity+0.20*controls.standards_maturity+0.22*controls.accountability_infrastructure+0.18*controls.public_participation+0.18*controls.enforcement_feasibility
controls["governance_gap_score"]=1-controls.governance_readiness_score
risks["distributional_risk_score"]=0.25*risks.burden_concentration+0.22*risks.exposure+0.22*risks.worker_displacement+0.21*risks.community_vulnerability+0.10*(1-risks.mitigation_capacity)
tech.sort_values("foresight_priority_score", ascending=False).to_csv(OUTPUTS/"advanced_technology_foresight_profiles.csv", index=False)
controls.sort_values("governance_gap_score", ascending=False).to_csv(OUTPUTS/"advanced_governance_readiness_scores.csv", index=False)
risks.sort_values("distributional_risk_score", ascending=False).to_csv(OUTPUTS/"advanced_distributional_risk_scores.csv", index=False)
for df, label, field, filename in [(tech,"technology_name","foresight_priority_score","technology_foresight_priority_scores.png"),(controls,"control_name","governance_gap_score","governance_gap_scores.png"),(risks,"risk_name","distributional_risk_score","distributional_risk_scores.png")]:
    ranked=df.sort_values(field)
    plt.figure(figsize=(10,6)); plt.barh(ranked[label], ranked[field]); plt.xlabel(field.replace("_"," ").title()); plt.tight_layout(); plt.savefig(OUTPUTS/filename, dpi=150); plt.close()
print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
