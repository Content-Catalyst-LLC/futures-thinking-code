# Methodology

This companion repository treats uncertainty matrices and driver mapping as a structured foresight workflow.

## Core Analytical Tasks

1. Score drivers by impact, uncertainty, urgency, interaction strength, distributional burden, monitoring feasibility, evidence strength, and controllability.
2. Classify drivers into matrix quadrants.
3. Score outgoing and incoming cross-impact.
4. Identify scenario-axis candidates.
5. Score signal priorities.
6. Score monitoring priorities and assumption fragility.
7. Export reproducible tables and reports.

## Core Equations

### Driver Priority

`priority = 0.22 × impact + 0.20 × uncertainty + 0.14 × urgency + 0.14 × interaction + 0.12 × burden + 0.08 × monitoring + 0.06 × evidence + 0.04 × (1 - controllability)`

### Matrix Classification

- High impact / high uncertainty: critical uncertainty.
- High impact / low uncertainty: baseline structural driver.
- Low impact / high uncertainty: watchlist uncertainty.
- Low impact / low uncertainty: lower-priority factor.

### Cross-Impact

`cross_impact = outgoing_influence + incoming_influence`

### Axis Suitability

`axis_suitability = impact × uncertainty × interaction_strength × monitoring_feasibility × evidence_strength`

### Signal Priority

`signal_priority = 0.15 × novelty + 0.30 × relevance + 0.25 × urgency + 0.15 × evidence_quality + 0.15 × affected_voice`

### Monitoring Priority

`monitoring_priority = 0.35 × uncertainty + 0.25 × monitoring_feasibility + 0.20 × urgency + 0.20 × distributional_burden`

## Interpretation

Scores are structured prompts, not objective truths. Driver mapping should be revised through evidence, stakeholder knowledge, assumption testing, and monitoring.
