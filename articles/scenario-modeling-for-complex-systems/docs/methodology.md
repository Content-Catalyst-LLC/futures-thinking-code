# Methodology

This companion repository treats scenario modeling as structured exploration across alternative system assumptions.

## Core Analytical Tasks

1. Define scenario assumptions.
2. Define strategy portfolios.
3. Simulate system-state pathways across scenario-strategy combinations.
4. Evaluate robustness using worst-case viability.
5. Evaluate regret compared with best strategy performance in each scenario.
6. Score drivers by impact, uncertainty, interaction, time sensitivity, and monitoring need.
7. Score monitoring indicators and link them to decision triggers.
8. Export reproducible tables and reports.

## Core Equations

### System State

`state[t] = state[t-1] + growth - absorbed_shock - stress_feedback + adaptive_capacity[t]`

### Stress Feedback

`stress_feedback = feedback_strength × max(0, 1 - state[t-1])`

### Adaptive Capacity

`adaptive_capacity[t] = min(cap, adaptive_capacity[t-1] + learning_gain × stress + strategy_adaptation_boost)`

### Viability Score

`viability = 0.35 × final_state + 0.30 × min_state + 0.20 × mean_state + 0.15 × final_adaptive_capacity`

### Robustness

`robustness = min(viability across scenarios)`

### Regret

`regret[strategy, scenario] = best_viability_in_scenario - strategy_viability_in_scenario`

### Driver Priority

`driver_priority = 0.25 × impact + 0.25 × uncertainty + 0.20 × interaction + 0.15 × time_sensitivity + 0.15 × monitoring_need`

## Interpretation

The workflow does not predict the future. It compares how strategies behave under alternative assumptions and identifies which strategies are robust, fragile, adaptive, or high-regret across multiple plausible futures.
