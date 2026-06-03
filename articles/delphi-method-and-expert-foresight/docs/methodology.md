# Methodology

This companion repository treats Delphi as structured expert judgment under uncertainty.

## Core Analytical Tasks

1. Audit panel composition and expertise diversity.
2. Track expert judgments across rounds.
3. Compute consensus, dispersion, stability, and uncertainty metrics.
4. Identify stable disagreement and high-uncertainty issues.
5. Score issue priorities.
6. Link qualitative rationales to decision implications.
7. Translate Delphi outputs into policy, scenario, monitoring, and research uses.

## Core Equations

### Priority Score

`priority = 0.25 × likelihood + 0.30 × impact + 0.20 × urgency + 0.15 × governance_relevance + 0.10 × monitoring_need`

### Uncertainty Range

`uncertainty_range = high_estimate - low_estimate`

### Round Dispersion

`dispersion = upper_quartile - lower_quartile`

### Stability

`stability_shift = abs(median_round_t - median_round_t_minus_1)`

### Expert Judgment Profile

`judgment_profile = 0.25 × likelihood + 0.35 × impact + 0.25 × urgency + 0.15 × feasibility`

### Panel Diversity Score

`diversity_score = mean(formal_expert, practice_expert, community_expert, ethics_expert) × panel_weight × (1 - blind_spot_risk)`

## Interpretation

The workflow does not treat expert consensus as truth. It makes expert judgment, disagreement, uncertainty, and decision translation more transparent.
