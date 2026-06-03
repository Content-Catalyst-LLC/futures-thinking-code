# Methodology

This companion repository treats biotechnology futures as a systems-governance problem involving scientific capability, manufacturing, public legitimacy, ecological uncertainty, dual-use risk, equity, and community consent.

## Core Analytical Tasks

1. Validate capability, risk, justice, scenario, pathway, and strategy records.
2. Score biotechnology capabilities by responsible readiness.
3. Score risks by biological risk pressure and mitigation gaps.
4. Score justice capacity and harm concentration.
5. Score scenarios by responsible biotechnology capacity, biological risk pressure, and justice profile.
6. Simulate biotechnology pathway viability, biological risk pressure, and access capacity over time.
7. Score strategy options for public-interest biotechnology governance.
8. Export reproducible tables and a report.

## Core Equations

### Responsible Biotechnology Capacity

`capacity = 0.16 × science + 0.18 × governance + 0.16 × legitimacy + 0.16 × equity + 0.12 × manufacturing + 0.12 × consent + 0.05 × (1 - ecological_uncertainty) + 0.05 × (1 - dual_use_risk)`

### Biological Risk Pressure

`risk = 0.22 × dual_use_risk + 0.20 × ecological_uncertainty + 0.18 × (1 - governance) + 0.16 × (1 - legitimacy) + 0.14 × (1 - consent) + 0.10 × (1 - equity)`

### Justice Profile

`justice = 0.28 × equity + 0.24 × consent + 0.20 × legitimacy + 0.16 × governance + 0.12 × (1 - biological_risk_pressure)`

### Risk Priority

`risk_priority = 0.18 × probability + 0.22 × severity + 0.16 × detection_difficulty + 0.16 × governance_gap + 0.12 × ecological_exposure + 0.10 × dual_use_relevance + 0.06 × (1 - mitigation_capacity)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing biotechnology pathways, surfacing governance gaps, identifying biological risk pressure, and evaluating whether biotechnology futures are aligned with public health, ecological responsibility, and justice.
