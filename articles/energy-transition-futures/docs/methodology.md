# Methodology

This companion repository treats energy transition futures as a systems-governance problem involving clean power, grids, storage, electrification, fossil phase-down, justice, labor, materials, finance, and climate resilience.

## Core Analytical Tasks

1. Validate capability, risk, justice, scenario, pathway, and strategy records.
2. Score transition capabilities by readiness and risk pressure.
3. Score transition risks by probability, severity, infrastructure exposure, justice relevance, and mitigation capacity.
4. Score energy justice capacity and justice gaps.
5. Score scenarios by transition readiness, transition risk pressure, and justice-resilience capacity.
6. Simulate transition capacity, emissions pressure, and justice-resilience scores over time.
7. Score strategy options for public-interest energy transition governance.
8. Export reproducible tables and a report.

## Core Equations

### Transition Readiness

`readiness = 0.14 × clean_power + 0.14 × grid + 0.12 × storage + 0.12 × electrification + 0.12 × fossil_phase_down + 0.12 × justice + 0.10 × labor + 0.08 × materials + 0.06 × resilience`

### Transition Risk Pressure

`risk = 0.18 × (1 - grid) + 0.16 × (1 - storage) + 0.16 × (1 - fossil_phase_down) + 0.14 × (1 - justice) + 0.12 × (1 - labor) + 0.12 × (1 - materials) + 0.12 × (1 - resilience)`

### Justice-Resilience Capacity

`justice_resilience = 0.24 × justice + 0.20 × labor + 0.18 × resilience + 0.16 × materials + 0.12 × fossil_phase_down + 0.10 × grid`

### Risk Priority

`risk_priority = 0.18 × probability + 0.20 × severity + 0.14 × detection_difficulty + 0.16 × governance_gap + 0.14 × infrastructure_exposure + 0.12 × justice_relevance + 0.06 × (1 - mitigation_capacity)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing energy transition pathways, identifying bottlenecks, surfacing justice and infrastructure risks, and testing whether transition strategies are aligned with decarbonization, reliability, affordability, material responsibility, and public legitimacy.
