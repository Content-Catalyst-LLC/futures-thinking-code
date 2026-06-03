# Methodology

This companion repository treats supply chain futures as a multidimensional system involving cost efficiency, supplier diversification, inventory buffers, visibility, labor accountability, climate adaptation, digital traceability, circularity, regulatory readiness, recovery capacity, and public value.

## Core Analytical Tasks

1. Validate supply chain profiles, scenarios, strategies, chokepoints, procurement/circularity records, and disruption pathways.
2. Score supply chain resilience and fragility.
3. Score future scenarios for disruption pressure and adaptation opportunity.
4. Score resilience strategies for resilience gain and implementation risk.
5. Score chokepoints for systemic risk priority.
6. Score procurement/circularity records for public-interest supply governance.
7. Simulate supply chain viability, disruption exposure, and recovery under repeated shocks.
8. Export reproducible tables and a report.

## Core Equations

### Resilience Score

`resilience = 0.10 × cost_efficiency + 0.16 × supplier_diversification + 0.14 × inventory_buffer + 0.14 × supply_visibility + 0.12 × labor_accountability + 0.13 × climate_adaptation + 0.09 × digital_traceability + 0.06 × circularity + 0.04 × regulatory_readiness + 0.02 × recovery_capacity`

### Fragility Score

`fragility = 0.16 × (1 - supplier_diversification) + 0.16 × (1 - inventory_buffer) + 0.14 × (1 - supply_visibility) + 0.14 × (1 - climate_adaptation) + 0.12 × (1 - labor_accountability) + 0.10 × (1 - recovery_capacity) + 0.08 × (1 - regulatory_readiness) + 0.06 × (1 - digital_traceability) + 0.04 × (1 - circularity)`

### Chokepoint Priority

`priority = 0.18 × dependency_concentration + 0.17 × substitution_difficulty + 0.16 × disruption_probability + 0.18 × systemic_reach + 0.17 × recovery_difficulty + 0.14 × visibility_gap`

## Interpretation

Scores are not predictions. They are structured prompts for comparing supply chain futures, surfacing hidden dependencies, evaluating resilience strategies, and testing whether supply systems remain viable under uncertainty.
