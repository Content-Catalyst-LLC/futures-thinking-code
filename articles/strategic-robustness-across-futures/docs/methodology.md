# Methodology

This companion repository treats strategic robustness as a structured comparison of strategy performance across plausible futures.

## Core Analytical Tasks

1. Define scenarios.
2. Define strategies.
3. Calculate multi-criteria performance across scenario-strategy combinations.
4. Rank strategies by worst-case viability, mean viability, threshold failures, and regret.
5. Diagnose vulnerability conditions.
6. Score adaptive triggers.
7. Score assumption fragility.
8. Export reproducible tables and reports.

## Core Equations

### Effectiveness

`effectiveness = baseline_effectiveness - 0.22 × disruption + 0.26 × shock_absorption - 0.08 × ecological_stress`

### Feasibility

`feasibility = implementation_capacity + 0.18 × fiscal_capacity - 0.30 × implementation_complexity`

### Legitimacy

`legitimacy = 0.40 × public_trust + 0.25 × legitimacy_design + 0.20 × equity_quality + 0.15 × adaptability`

### Equity

`equity = equity_quality - 0.30 × distributional_pressure + 0.15 × legitimacy_design`

### Adaptability

`adaptability_score = 0.70 × adaptability + 0.30 × implementation_capacity`

### Transformability

`transformability_score = 0.70 × transformability + 0.30 × legitimacy_design`

### Viability

`viability = weighted sum of criteria scores`

### Robustness

`robustness = minimum viability across scenarios`

### Regret

`regret = best scenario viability - strategy viability`

### Assumption Failure Risk

`failure_risk = 0.45 × (1 - confidence) + 0.55 × fragility`

## Interpretation

Scores are not predictions. They are structured comparisons designed to reveal fragile assumptions, vulnerable strategies, low-regret options, adaptive triggers, and candidate robust pathways.
