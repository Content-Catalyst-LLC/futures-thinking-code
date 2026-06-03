# Methodology

This companion repository treats public-sector foresight capacity as an institutional system involving scanning, scenarios, decision uptake, participation, budget connection, evaluation, institutional learning, implementation authority, knowledge infrastructure, and legitimacy.

## Core Analytical Tasks

1. Validate capacity, signal, uptake, scenario, pathway, and strategy records.
2. Score public-sector foresight capacity and capacity gaps.
3. Score weak signals by public priority and response gap.
4. Score decision uptake across budget, regulation, procurement, implementation, evaluation, and participation.
5. Score scenario-cycle stress and foresight opportunity.
6. Simulate foresight capacity, decision uptake, legitimacy, and learning over time.
7. Score strategies for building institutionalized foresight capacity.
8. Export reproducible tables and a report.

## Core Equations

### Foresight Capacity Score

`capacity = 0.12 × scanning + 0.12 × scenarios + 0.14 × decision_uptake + 0.12 × participation + 0.12 × budget + 0.10 × evaluation + 0.10 × learning + 0.10 × authority + 0.05 × knowledge + 0.03 × legitimacy`

### Capacity Gap Score

`gap = 0.16 × (1 - decision_uptake) + 0.14 × (1 - budget) + 0.14 × (1 - authority) + 0.12 × (1 - scanning) + 0.12 × (1 - scenarios) + 0.10 × (1 - participation) + 0.10 × (1 - evaluation) + 0.08 × (1 - learning) + 0.04 × (1 - knowledge)`

### Weak Signal Priority

`priority = 0.16 × signal_strength + 0.12 × novelty + 0.12 × uncertainty + 0.18 × policy_relevance + 0.16 × equity_relevance + 0.12 × detection_difficulty + 0.14 × (1 - response_readiness)`

### Decision Uptake

`uptake = 0.20 × uptake_strength + 0.18 × budget_influence + 0.14 × regulatory_influence + 0.12 × procurement_influence + 0.14 × implementation_influence + 0.12 × evaluation_influence + 0.10 × participation_influence`

## Interpretation

Scores are not predictions. They are structured prompts for comparing public-sector foresight capacity, surfacing institutional gaps, prioritizing signals, and testing whether foresight changes decisions.
