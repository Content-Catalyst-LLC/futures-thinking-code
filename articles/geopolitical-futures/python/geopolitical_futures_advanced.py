#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Advanced dependencies are missing.")
    print("Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-advanced.txt")
    print(f"Original error: {exc}")
    sys.exit(0)

profiles = pd.read_csv(DATA / "geopolitical_futures_profiles.csv")
profiles["geopolitical_stability_score"] = (
    0.11*(1-profiles["power_concentration"]) + 0.10*profiles["interdependence"] +
    0.16*profiles["institutional_coordination"] - 0.12*profiles["technological_competition"] -
    0.12*profiles["climate_stress"] - 0.11*profiles["economic_vulnerability"] +
    0.12*profiles["domestic_resilience"] + 0.11*profiles["information_integrity"] +
    0.08*profiles["resource_security"] + 0.07*profiles["crisis_communication"]
)
profiles["cascade_risk_score"] = (
    0.12*profiles["power_concentration"] + 0.13*profiles["technological_competition"] +
    0.14*profiles["climate_stress"] + 0.13*profiles["economic_vulnerability"] +
    0.11*(1-profiles["institutional_coordination"]) + 0.10*(1-profiles["domestic_resilience"]) +
    0.10*(1-profiles["information_integrity"]) + 0.09*(1-profiles["resource_security"]) +
    0.08*(1-profiles["crisis_communication"])
)
profiles.to_csv(OUT / "advanced_geopolitical_profile_scores.csv", index=False)

ranked = profiles.sort_values("geopolitical_stability_score")
plt.figure(figsize=(10, 6))
plt.barh(ranked["future_name"], ranked["geopolitical_stability_score"])
plt.xlabel("Geopolitical Stability Score")
plt.title("Geopolitical Futures Stability Scores")
plt.tight_layout()
plt.savefig(OUT / "geopolitical_stability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(profiles["geopolitical_stability_score"], profiles["cascade_risk_score"])
for _, row in profiles.iterrows():
    plt.text(row["geopolitical_stability_score"], row["cascade_risk_score"], row["future_name"], fontsize=7)
plt.xlabel("Geopolitical Stability")
plt.ylabel("Cascade Risk")
plt.title("Geopolitical Stability vs Cascade Risk")
plt.tight_layout()
plt.savefig(OUT / "geopolitical_stability_vs_cascade_risk.png", dpi=150)
plt.close()

print("Advanced geopolitical futures workflow complete.")
