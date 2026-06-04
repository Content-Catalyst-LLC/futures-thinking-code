# Methodology

This companion repository treats health futures and public systems as coupled population-health, care, infrastructure, governance, and trust systems. It evaluates prevention, healthcare access, public health infrastructure, climate readiness, workforce resilience, technology governance, social protection, public trust, equity, care capacity, risk priority, and adaptive capacity.

## Core Analytical Tasks

1. Validate health system profiles, scenarios, strategies, risk indicators, governance records, and stress pathways.
2. Score public health resilience and system fragility.
3. Score scenarios for health system stress and transformation opportunity.
4. Score strategies for public system value and implementation readiness.
5. Score risk indicators for systemic health risk priority.
6. Score governance records for public health governance capacity and legitimacy gap.
7. Simulate public health resilience, system stress, and adaptive capacity under repeated shocks.
8. Export reproducible tables and a report.

## Core Equations

### Public Health Resilience

`resilience = 0.13 × prevention_capacity + 0.12 × healthcare_access + 0.15 × public_health_infrastructure + 0.10 × climate_readiness + 0.11 × workforce_resilience + 0.08 × technology_governance + 0.11 × social_protection + 0.08 × public_trust + 0.07 × equity_capacity + 0.05 × care_capacity`

### Health System Fragility

`fragility = 0.13 × (1 - prevention_capacity) + 0.12 × (1 - healthcare_access) + 0.15 × (1 - public_health_infrastructure) + 0.11 × (1 - climate_readiness) + 0.13 × (1 - workforce_resilience) + 0.08 × (1 - technology_governance) + 0.10 × (1 - social_protection) + 0.08 × (1 - public_trust) + 0.06 × (1 - equity_capacity) + 0.04 × (1 - care_capacity)`

### Risk Priority

`priority = 0.14 × probability_proxy + 0.18 × severity + 0.17 × cascade_potential + 0.12 × visibility_gap + 0.14 × recovery_difficulty + 0.17 × distributional_harm + 0.08 × (1 - preparedness)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing health futures, surfacing risk, testing strategies, and assessing whether public systems remain preventive, equitable, resilient, trusted, and governable under stress.
