# Methodology

This companion repository treats economic futures and global development as a multidimensional system involving growth, distribution, ecological viability, institutional capacity, resilience, fiscal space, labor inclusion, public investment, technology diffusion, trade resilience, and democratic legitimacy.

## Core Analytical Tasks

1. Validate development futures, scenarios, policy portfolios, shocks, institutions, and pathways.
2. Score development quality and development fragility.
3. Score policy portfolios for development strategy strength and implementation risk.
4. Score shock priority across probability proxy, severity, systemic reach, distributional exposure, recovery difficulty, and preparedness.
5. Score institutional capacity and institutional fragility.
6. Simulate development pathways under repeated stress.
7. Export reproducible tables and a report.

## Core Equations

### Development Quality

`quality = 0.14 × growth - 0.12 × inequality - 0.14 × ecological_stress + 0.13 × institutional_capacity + 0.12 × resilience + 0.08 × fiscal_space + 0.08 × labor_inclusion + 0.08 × public_investment + 0.06 × technology_diffusion + 0.03 × trade_resilience + 0.02 × democratic_legitimacy`

### Development Fragility

`fragility = 0.16 × inequality + 0.16 × ecological_stress + 0.13 × (1 - institutional_capacity) + 0.13 × (1 - resilience) + 0.12 × (1 - fiscal_space) + 0.10 × (1 - labor_inclusion) + 0.08 × (1 - public_investment) + 0.06 × (1 - trade_resilience) + 0.06 × (1 - democratic_legitimacy)`

### Policy Portfolio Strength

`strength = 0.15 × productive_capability + 0.14 × distributional_inclusion + 0.14 × ecological_viability + 0.14 × resilience_capacity + 0.11 × fiscal_sustainability + 0.10 × labor_protection + 0.10 × implementation_capacity + 0.06 × democratic_legitimacy + 0.06 × (1 - global_coordination_need)`

### Shock Priority

`priority = 0.18 × probability_proxy + 0.20 × severity + 0.18 × systemic_reach + 0.17 × distributional_exposure + 0.15 × recovery_difficulty + 0.12 × (1 - policy_preparedness)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing development futures, surfacing fragility, identifying investment priorities, and testing whether development pathways remain viable under uncertainty.
