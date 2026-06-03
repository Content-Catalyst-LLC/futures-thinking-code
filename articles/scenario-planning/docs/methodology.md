# Methodology

This companion repository treats scenario planning as a reproducible analytical workflow.

## Core Analytical Tasks

1. Score drivers and critical uncertainties.
2. Prioritize signals for scenario monitoring.
3. Score assumption vulnerability.
4. Evaluate strategies across scenarios.
5. Compute robustness, regret, and volatility.
6. Generate scenario planning reports and reusable outputs.

## Core Equations

### Driver Criticality

`criticality = uncertainty × impact × velocity`

### Signal Watch Score

`watch_score = 0.35 × uncertainty + 0.40 × impact + 0.25 × novelty`

### Assumption Vulnerability

`vulnerability = exposure × (1 - confidence) × (1 + (1 - reversibility))`

### Strategy Robustness

`robustness = 0.45 × worst_case + 0.30 × mean_performance + 0.15 × adaptability + 0.10 × equity_sensitivity - 0.15 × volatility - 0.05 × implementation_difficulty`

### Regret

`regret = best_strategy_performance_in_scenario - selected_strategy_performance`

## Interpretation

The workflow does not predict which scenario will occur. It helps evaluate strategy under multiple plausible futures and identify assumptions, signals, and vulnerabilities that deserve monitoring.
