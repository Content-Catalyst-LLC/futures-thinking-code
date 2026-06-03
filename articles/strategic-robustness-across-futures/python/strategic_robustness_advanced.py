#!/usr/bin/env python3
"""
Advanced pandas/numpy/matplotlib workflow for Strategic Robustness Across Futures.
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

scenarios = pd.read_csv(DATA / "scenarios.csv")
strategies = pd.read_csv(DATA / "strategies.csv")
criteria = pd.read_csv(DATA / "performance_criteria.csv")
triggers = pd.read_csv(DATA / "adaptive_triggers.csv")
vulnerabilities = pd.read_csv(DATA / "vulnerability_conditions.csv")
assumptions = pd.read_csv(DATA / "assumption_register.csv")

weights = dict(zip(criteria["criterion_name"], criteria["weight"]))

performance_rows = []

for _, scenario in scenarios.iterrows():
    for _, strategy in strategies.iterrows():
        effectiveness = (
            strategy["baseline_effectiveness"]
            - 0.22 * scenario["disruption_level"]
            + 0.26 * strategy["shock_absorption"]
            - 0.08 * scenario["ecological_stress"]
            - 0.05 * scenario["technology_volatility"] * (1 - strategy["adaptability"])
        )

        feasibility = (
            scenario["implementation_capacity"]
            + 0.18 * scenario["fiscal_capacity"]
            - 0.30 * strategy["implementation_complexity"]
            - 0.05 * scenario["disruption_level"]
        )

        legitimacy = (
            0.40 * scenario["public_trust"]
            + 0.25 * strategy["legitimacy_design"]
            + 0.20 * strategy["equity_quality"]
            + 0.15 * strategy["adaptability"]
            - 0.05 * scenario["distributional_pressure"]
        )

        equity = (
            strategy["equity_quality"]
            - 0.30 * scenario["distributional_pressure"]
            + 0.15 * strategy["legitimacy_design"]
            + 0.10 * strategy["transformability"]
        )

        adaptability_score = (
            0.70 * strategy["adaptability"]
            + 0.30 * scenario["implementation_capacity"]
            - 0.05 * scenario["technology_volatility"] * (1 - strategy["shock_absorption"])
        )

        transformability_score = (
            0.70 * strategy["transformability"]
            + 0.30 * strategy["legitimacy_design"]
            - 0.06 * strategy["implementation_complexity"]
        )

        metrics = {
            "effectiveness": max(0, min(1, effectiveness)),
            "feasibility": max(0, min(1, feasibility)),
            "legitimacy": max(0, min(1, legitimacy)),
            "equity": max(0, min(1, equity)),
            "adaptability": max(0, min(1, adaptability_score)),
            "transformability": max(0, min(1, transformability_score)),
        }

        viability = sum(weights[name] * metrics[name] for name in weights)

        performance_rows.append({
            "scenario_id": scenario["scenario_id"],
            "scenario_name": scenario["scenario_name"],
            "scenario_family": scenario["scenario_family"],
            "strategy_id": strategy["strategy_id"],
            "strategy_name": strategy["strategy_name"],
            "strategy_type": strategy["strategy_type"],
            "effectiveness": metrics["effectiveness"],
            "feasibility": metrics["feasibility"],
            "legitimacy": metrics["legitimacy"],
            "equity": metrics["equity"],
            "adaptability_score": metrics["adaptability"],
            "transformability_score": metrics["transformability"],
            "viability_score": max(0, min(1, viability))
        })

performance = pd.DataFrame(performance_rows)

robustness = (
    performance
    .groupby(["strategy_id", "strategy_name", "strategy_type"])
    .agg(
        worst_case_viability=("viability_score", "min"),
        mean_viability=("viability_score", "mean"),
        best_case_viability=("viability_score", "max"),
        viability_range=("viability_score", lambda x: x.max() - x.min()),
        threshold_failures=("viability_score", lambda x: (x < 0.50).sum()),
        low_legitimacy_cases=("legitimacy", lambda x: (x < 0.50).sum()),
        low_equity_cases=("equity", lambda x: (x < 0.50).sum())
    )
    .reset_index()
    .sort_values(["worst_case_viability", "mean_viability"], ascending=False)
)

performance["best_scenario_viability"] = (
    performance.groupby("scenario_id")["viability_score"].transform("max")
)
performance["regret"] = performance["best_scenario_viability"] - performance["viability_score"]

regret_summary = (
    performance
    .groupby(["strategy_id", "strategy_name"])
    .agg(
        max_regret=("regret", "max"),
        mean_regret=("regret", "mean")
    )
    .reset_index()
    .sort_values(["max_regret", "mean_regret"])
)

frequency = {"monthly": 1.00, "quarterly": 0.88, "semiannual": 0.68, "annual": 0.48}
triggers["monitoring_gap"] = (triggers["threshold_value"] - triggers["baseline"]).abs()
triggers["review_weight"] = triggers["review_frequency"].map(frequency).fillna(0.50)
triggers["trigger_priority_score"] = (
    0.45 * triggers["monitoring_gap"]
    + 0.35 * triggers["threshold_value"]
    + 0.20 * triggers["review_weight"]
)

vulnerabilities["vulnerability_priority_score"] = (
    0.50 * vulnerabilities["severity"]
    + 0.25 * (1 - vulnerabilities["detectability"])
    + 0.25 * (1 - vulnerabilities["mitigation_capacity"])
)

assumptions["assumption_failure_risk"] = (
    0.45 * (1 - assumptions["confidence"])
    + 0.55 * assumptions["fragility"]
)

performance.to_csv(OUTPUTS / "advanced_scenario_strategy_performance.csv", index=False)
robustness.to_csv(OUTPUTS / "advanced_strategy_robustness_scores.csv", index=False)
performance.sort_values("regret", ascending=False).to_csv(OUTPUTS / "advanced_scenario_strategy_regret.csv", index=False)
regret_summary.to_csv(OUTPUTS / "advanced_strategy_regret_summary.csv", index=False)
triggers.sort_values("trigger_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_adaptive_trigger_scores.csv", index=False)
vulnerabilities.sort_values("vulnerability_priority_score", ascending=False).to_csv(OUTPUTS / "advanced_vulnerability_scores.csv", index=False)
assumptions.sort_values("assumption_failure_risk", ascending=False).to_csv(OUTPUTS / "advanced_assumption_fragility_scores.csv", index=False)

plt.figure(figsize=(10, 6))
ranked = robustness.sort_values("worst_case_viability")
plt.barh(ranked["strategy_name"], ranked["worst_case_viability"])
plt.xlabel("Worst-Case Viability")
plt.title(f"Worst-Case Strategy Viability — {config['short_title']}")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_robustness_scores.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
ranked_regret = regret_summary.sort_values("max_regret", ascending=True)
plt.barh(ranked_regret["strategy_name"], ranked_regret["max_regret"])
plt.xlabel("Maximum Regret")
plt.title("Maximum Regret by Strategy")
plt.tight_layout()
plt.savefig(OUTPUTS / "strategy_regret_scores.png", dpi=150)
plt.close()

pivot = performance.pivot(index="strategy_name", columns="scenario_name", values="viability_score")
plt.figure(figsize=(10, 6))
plt.imshow(pivot.values, aspect="auto")
plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
plt.yticks(range(len(pivot.index)), pivot.index)
plt.colorbar(label="Viability Score")
plt.title("Scenario-Strategy Viability Matrix")
plt.tight_layout()
plt.savefig(OUTPUTS / "scenario_strategy_viability_matrix.png", dpi=150)
plt.close()

print(f"Advanced workflow complete for: {config['title']}")
print(f"Outputs written to: {OUTPUTS}")
