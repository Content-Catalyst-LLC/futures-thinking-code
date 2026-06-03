# Methodology

This companion repository turns future-category reasoning into a reproducible workflow.

## Core Analytical Tasks

1. Classify candidate futures across plausibility, probability, and preference.
2. Identify futures that are probable but not preferable.
3. Identify futures that are preferable but not yet probable.
4. Rank strategic priority across future categories.
5. Evaluate strategy fit across probable, plausible, and preferable futures.
6. Track category shifts over time.

## Core Equations

### Plausibility Score

`plausibility = 0.40 × driver_support + 0.35 × pathway_coherence + 0.25 × constraint_fit`

### Probability Score

`probability = 0.70 × current_trend_strength + 0.30 × driver_support`

### Preference Score

`preference = 0.30 × justice + 0.25 × sustainability + 0.25 × resilience + 0.20 × legitimacy`

### Strategic Priority

`priority = 0.35 × plausibility + 0.25 × probability + 0.40 × preference`

### Strategy Category Fit

`fit = 0.20 × probable_fit + 0.30 × plausible_fit + 0.30 × preferable_fit + 0.20 × adaptive_capacity - 0.05 × implementation_difficulty + 0.05 × equity_sensitivity`

## Interpretation

The workflow does not automate judgment. It helps teams make category distinctions explicit so they can discuss evidence, values, uncertainty, and strategy more carefully.
