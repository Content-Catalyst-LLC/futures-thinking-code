# Methodology

This companion repository treats food, water, and land-use futures as coupled social-ecological systems involving production, water security, soil health, biodiversity, governance, climate exposure, market vulnerability, justice, livelihoods, and adaptive capacity.

## Core Analytical Tasks

1. Validate profiles, scenarios, strategies, risk indicators, governance records, and pathways.
2. Score food-water-land resilience and fragility.
3. Score scenarios for resource stress and transformation opportunity.
4. Score strategies for resource-systems value and implementation readiness.
5. Score risk indicators for systemic resource risk priority.
6. Score governance records for resource governance capacity and legitimacy gap.
7. Simulate resource resilience, stress, and adaptive capacity under repeated shocks.
8. Export reproducible tables and a report.

## Core Equations

### Food-Water-Land Resilience

`resilience = 0.13 × production_capacity + 0.16 × water_security + 0.15 × soil_health + 0.14 × biodiversity_integrity + 0.14 × governance_capacity - 0.12 × climate_exposure - 0.08 × market_vulnerability + 0.14 × justice_capacity + 0.12 × livelihood_resilience`

### Food-Water-Land Fragility

`fragility = 0.16 × climate_exposure + 0.14 × market_vulnerability + 0.14 × (1 - water_security) + 0.13 × (1 - soil_health) + 0.12 × (1 - biodiversity_integrity) + 0.12 × (1 - governance_capacity) + 0.10 × (1 - justice_capacity) + 0.06 × (1 - livelihood_resilience) + 0.03 × (1 - production_capacity)`

### Risk Priority

`priority = 0.14 × probability_proxy + 0.18 × severity + 0.17 × cascade_potential + 0.12 × visibility_gap + 0.14 × recovery_difficulty + 0.17 × distributional_harm + 0.08 × (1 - preparedness)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing resource futures, surfacing risk, testing strategies, and assessing whether systems remain regenerative, just, resilient, and governable under uncertainty.
