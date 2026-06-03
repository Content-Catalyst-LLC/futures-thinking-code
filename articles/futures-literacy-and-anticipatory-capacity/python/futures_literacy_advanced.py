#!/usr/bin/env python3
"""
Advanced pandas/matplotlib workflow for Futures Literacy and Anticipatory Capacity.
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

profiles = pd.read_csv(DATA / "capacity_profiles.csv")
assumptions = pd.read_csv(DATA / "assumptions.csv")
signals = pd.read_csv(DATA / "signals.csv")
future_images = pd.read_csv(DATA / "future_images.csv")
learning = pd.read_csv(DATA / "learning_cycles.csv")

weights = {
    "scanning_capacity": 0.15,
    "interpretive_capacity": 0.15,
    "assumption_visibility": 0.17,
    "imagination_range": 0.13,
    "participatory_depth": 0.17,
    "learning_capacity": 0.13,
    "action_translation": 0.10,
}

profiles["anticipatory_capacity_score"] = sum(
    profiles[column] * weight for column, weight in weights.items()
)

assumptions["vulnerability_score"] = (
    assumptions["exposure"] *
    (1 - assumptions["confidence"]) *
    (1 + (1 - assumptions["reversibility"]))
)

signals["watch_score"] = (
    0.35 * signals["uncertainty"] +
    0.40 * signals["impact"] +
    0.25 * signals["novelty"]
)

future_images["future_image_risk"] = (
    future_images["assumption_risk"] *
    (1 + (future_images["participation_need"] - 0.70).clip(lower=0))
)

frequency_bonus = {
    "monthly": 0.12,
    "bimonthly": 0.10,
    "quarterly": 0.08,
    "semiannual": 0.04,
    "annual": 0.02,
}

learning["review_bonus"] = learning["signal_review_frequency"].map(frequency_bonus).fillna(0)
learning["institutional_learning_score"] = (
    0.35 * learning["learning_score"] +
    0.30 * learning["decision_linkage"] +
    0.25 * learning["public_participation_level"] +
    learning["review_bonus"]
)

profiles = profiles.sort_values("anticipatory_capacity_score", ascending=False)
assumptions = assumptions.sort_values("vulnerability_score", ascending=False)
signals = signals.sort_values("watch_score", ascending=False)
future_images = future_images.sort_values("future_image_risk", ascending=False)
learning = learning.sort_values("institutional_learning_score", ascending=False)

profiles.to_csv(OUTPUTS / "advanced_anticipatory_capacity_scores.csv", index=False)
assumptions.to_csv(OUTPUTS / "advanced_assumption_vulnerability_scores.csv", index=False)
signals.to_csv(OUTPUTS / "advanced_signal_watch_scores.csv", index=False)
future_images.to_csv(OUTPUTS / "advanced_future_image_risk_scores.csv", index=False)
learning.to_csv(OUTPUTS / "advanced_learning_cycle_scores.csv", index=False)

plt.figure(figsize=(10, 6))
plt.barh(profiles["organization_type"], profiles["anticipatory_capacity_score"])
plt.xlabel("Anticipatory capacity score")
plt.title(f"Anticipatory Capacity — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "anticipatory_capacity_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(assumptions.head(7)["assumption_id"], assumptions.head(7)["vulnerability_score"])
plt.xlabel("Vulnerability score")
plt.title("Assumption Vulnerability Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "assumption_vulnerability_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(signals.head(8)["signal_id"], signals.head(8)["watch_score"])
plt.xlabel("Watch score")
plt.title("Signal Watch Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "signal_watch_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
plt.barh(learning["cycle_name"], learning["institutional_learning_score"])
plt.xlabel("Institutional learning score")
plt.title("Learning Cycle Scores")
plt.tight_layout()
plt.savefig(OUTPUTS / "learning_cycle_scores.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
