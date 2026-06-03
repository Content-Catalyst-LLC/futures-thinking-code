# Methodology

This companion repository treats early warning systems and futures intelligence as a structured monitoring, interpretation, and response workflow.

## Core Analytical Tasks

1. Score signals by novelty, relevance, urgency, evidence quality, affected voice, vulnerability, and lead-time value.
2. Evaluate indicators against thresholds.
3. Score trigger priority.
4. Score assumption-failure risk.
5. Score cross-system cascade risk.
6. Monitor scenario movement.
7. Link indicators to response protocols.
8. Export reproducible tables and reports.

## Core Equations

### Warning Score

`warning = 0.12 × novelty + 0.22 × relevance + 0.20 × urgency + 0.13 × evidence + 0.11 × affected_voice + 0.13 × vulnerability + 0.09 × lead_time`

### Threshold Gap

`threshold_gap = current_value - threshold_value`

### Trigger Priority

`trigger_priority = 0.45 × breach + 0.25 × current_value + 0.20 × positive_gap + 0.10 × review_weight`

### Assumption Failure Risk

`failure_risk = 0.45 × (1 - confidence) + 0.55 × fragility`

### Cascade Score

`cascade = influence_weight × (0.40 + 0.25 × delay_risk + 0.35 × cascade_potential)`

### Scenario Monitor Score

`scenario_score = scenario_relevance × monitoring_weight`

## Interpretation

Scores support institutional judgment. They do not replace public accountability, local knowledge, domain expertise, response capacity, or ethical reasoning.
