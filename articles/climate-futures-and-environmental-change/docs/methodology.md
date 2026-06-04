# Methodology

This companion repository treats climate futures and environmental change as a multidimensional system involving emissions, adaptation, ecological stress, governance coordination, social vulnerability, technology deployment, transition speed, justice, residual loss, feedback pressure, and institutional capacity.

## Core Analytical Tasks

1. Validate climate profiles, scenarios, mitigation/adaptation strategies, risk indicators, governance records, and climate pathways.
2. Score climate readiness and climate fragility.
3. Score scenarios for climate stress and transition opportunity.
4. Score mitigation/adaptation strategies for total climate strategy value and implementation readiness.
5. Score risk indicators for systemic climate risk priority.
6. Score governance records for climate governance capacity and legitimacy gap.
7. Simulate climate stress, social vulnerability, and adaptive capacity under divergent pathway assumptions.
8. Export reproducible tables and a report.

## Core Equations

### Climate Readiness

`readiness = -0.16 × emissions_intensity + 0.15 × adaptation_capacity - 0.15 × ecosystem_stress + 0.14 × governance_coordination - 0.12 × social_vulnerability + 0.10 × technology_deployment + 0.14 × transition_speed + 0.12 × justice_capacity - 0.10 × residual_loss`

### Climate Fragility

`fragility = 0.16 × emissions_intensity + 0.15 × ecosystem_stress + 0.14 × social_vulnerability + 0.13 × residual_loss + 0.12 × (1 - adaptation_capacity) + 0.12 × (1 - governance_coordination) + 0.10 × (1 - transition_speed) + 0.08 × (1 - justice_capacity)`

### Risk Priority

`priority = 0.14 × probability_proxy + 0.18 × severity + 0.17 × irreversibility + 0.16 × systemic_reach + 0.12 × visibility_gap + 0.15 × distributional_harm + 0.08 × (1 - preparedness)`

## Interpretation

Scores are not predictions. They are structured prompts for comparing climate futures, testing transition pathways, surfacing systemic risk, and assessing whether institutions can act responsibly under deep uncertainty, unequal exposure, and irreversible environmental risk.
