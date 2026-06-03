# Methodology

Article: Forecasting, Foresight, and Futures Studies

## Research Design

This companion directory treats futures thinking as a reproducible analytical workflow. It combines:

1. Forecast-error diagnostics.
2. Driver-priority analysis.
3. Signal-priority scoring.
4. Assumption vulnerability scoring.
5. Scenario robustness analysis.
6. Strategic regret analysis.
7. Practice-profile comparison.

## Scoring Logic

The workflows are not claiming predictive certainty. They are designed to make assumptions visible and compare strategies across plausible futures.

## Core Equations

### Driver Priority

`driver_priority = uncertainty × impact × velocity`

### Signal Watch Score

`watch_score = 0.35 × uncertainty + 0.40 × impact + 0.25 × novelty`

### Assumption Vulnerability

`vulnerability = exposure × (1 - confidence) × (1 + (1 - reversibility))`

### Strategy Robustness

`robustness = 0.45 × worst_case + 0.30 × mean_performance + 0.15 × adaptability + 0.10 × equity_sensitivity - 0.15 × volatility`

### Regret

`regret = best_strategy_performance_in_scenario - selected_strategy_performance`

## Interpretation

A high robustness score does not mean a strategy is universally best. It means the strategy performs comparatively well across multiple plausible futures while limiting downside exposure.
