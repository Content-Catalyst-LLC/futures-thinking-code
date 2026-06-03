#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for the history of futures thinking.
Gracefully exits if dependencies are missing.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

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

config = json.loads((ROOT / "article_config.json").read_text(encoding="utf-8"))

traditions = pd.read_csv(DATA / "historical_traditions.csv")
institutions = pd.read_csv(DATA / "institutional_developments.csv")
methods = pd.read_csv(DATA / "method_genealogy.csv")
risks = pd.read_csv(DATA / "historical_risks.csv")

traditions["reflective_foresight_score"] = (
    0.25 * traditions["methodological_discipline"] +
    0.25 * traditions["participatory_depth"] +
    0.25 * traditions["ethical_reflection"] +
    0.25 * traditions["systems_orientation"]
)

traditions["power_risk_score"] = (
    traditions["institutional_power"] *
    (1 - traditions["participatory_depth"]) *
    (1 - traditions["ethical_reflection"])
)

institutions["institutional_balance_score"] = (
    0.50 * institutions["method_influence"] +
    0.50 * institutions["public_accountability"]
)

methods["method_risk_score"] = (
    methods["technocratic_risk"] *
    (1 - methods["participatory_potential"]) *
    (1 - methods["ethical_sensitivity"])
)

methods["reflective_method_score"] = (
    0.34 * methods["participatory_potential"] +
    0.33 * methods["ethical_sensitivity"] +
    0.33 * (1 - methods["technocratic_risk"])
)

priority_weight = {"high": 1.20, "medium": 1.00, "low": 0.80}
risks["weighted_risk_priority"] = risks["severity"] * risks["mitigation_priority"].map(priority_weight).fillna(1.0)

traditions = traditions.sort_values("reflective_foresight_score", ascending=False)
power_risk = traditions.sort_values("power_risk_score", ascending=False)
methods = methods.sort_values("reflective_method_score", ascending=False)
risks = risks.sort_values("weighted_risk_priority", ascending=False)

traditions.to_csv(OUTPUTS / "advanced_historical_tradition_scores.csv", index=False)
institutions.to_csv(OUTPUTS / "advanced_institutional_development_scores.csv", index=False)
methods.to_csv(OUTPUTS / "advanced_method_genealogy_scores.csv", index=False)
risks.to_csv(OUTPUTS / "advanced_historical_risk_priorities.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(traditions["tradition"], traditions["reflective_foresight_score"])
plt.xlabel("Reflective foresight score")
plt.title(f"Historical Traditions — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "historical_traditions_reflective_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(power_risk["tradition"], power_risk["power_risk_score"])
plt.xlabel("Power risk score")
plt.title("Power Risk by Historical Tradition")
plt.tight_layout()
plt.savefig(OUTPUTS / "historical_traditions_power_risk.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(methods["method"], methods["reflective_method_score"])
plt.xlabel("Reflective method score")
plt.title("Method Genealogy: Reflective Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "method_genealogy_reflective_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(risks["risk_name"], risks["weighted_risk_priority"])
plt.xlabel("Weighted risk priority")
plt.title("Historical Futures Thinking Risks")
plt.tight_layout()
plt.savefig(OUTPUTS / "historical_risk_priorities.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
