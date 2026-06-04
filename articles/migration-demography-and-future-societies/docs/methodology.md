# Methodology

This companion repository treats migration, demography, and future societies as dynamic systems shaped by age structure, fertility, mortality, migration, care capacity, housing pressure, labor adaptation, climate mobility exposure, gender equity, public health, social cohesion, and adaptive demographic governance.

## Core Analytical Tasks

1. Validate demographic profiles, scenarios, strategies, risk indicators, care/urban records, and adaptive pathways.
2. Score demographic profiles for stress and adaptive capacity.
3. Score scenarios for demographic pressure and humane-governance opportunity.
4. Score strategy options for demographic value and implementation readiness.
5. Score risk indicators for demographic-risk priority.
6. Score care and urban records for care stress and urban absorption capacity.
7. Simulate population, care stress, mobility pressure, demographic stress, and adaptive capacity over time.
8. Export reproducible tables and a report.

## Core Equations

### Population Balance

`P(t+1) = P(t) + births - deaths + net_migration`

### Demographic Stress

`stress = 0.13 × aging_pressure + 0.13 × youth_opportunity_gap + 0.12 × migration_pressure + 0.13 × (1 - care_capacity) + 0.12 × housing_pressure + 0.10 × (1 - labor_adaptation) + 0.11 × climate_mobility_exposure + 0.08 × (1 - social_cohesion) + 0.05 × (1 - gender_equity) + 0.03 × (1 - public_health_capacity)`

### Adaptive Capacity

`capacity = 0.18 × care_capacity + 0.16 × labor_adaptation + 0.16 × social_cohesion + 0.13 × gender_equity + 0.13 × public_health_capacity + 0.10 × (1 - housing_pressure) + 0.08 × (1 - youth_opportunity_gap) + 0.06 × (1 - climate_mobility_exposure)`

### Care Stress

`care_stress = eldercare_demand + childcare_demand + unpaid_care_burden - care_workforce_capacity - public_health_capacity`

## Interpretation

Scores are not predictions. They are structured prompts for comparing demographic futures, surfacing care and housing vulnerabilities, testing rights-based mobility strategies, and assessing whether institutions can govern population change without coercion, xenophobia, ageism, or abandonment.
