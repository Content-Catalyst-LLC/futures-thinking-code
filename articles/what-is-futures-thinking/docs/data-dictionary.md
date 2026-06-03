# Data Dictionary

## scenarios.csv

- `scenario_id`: Short scenario identifier.
- `scenario_name`: Scenario name.
- `summary`: Short scenario description.
- `plausibility`: Plausibility score from 0 to 1.
- `time_horizon_years`: Approximate futures horizon.
- `system_stress`: Stress score from 0 to 1.

## strategies.csv

- `strategy_id`: Strategy identifier.
- `strategy_name`: Strategy label.
- `strategy_type`: Analytical type.
- `description`: Strategy summary.
- `adaptability`: Ability to adjust across futures.
- `implementation_difficulty`: Difficulty of implementation.
- `equity_sensitivity`: Sensitivity to distributional and legitimacy concerns.

## strategy_performance.csv

- `strategy_id`: Strategy identifier.
- `scenario_id`: Scenario identifier.
- `performance`: Scenario-specific performance score.
- `confidence`: Confidence in the assessment.
- `notes`: Interpretation notes.

## drivers.csv

- `driver_id`: Driver identifier.
- `domain`: Driver domain.
- `driver_name`: Driver label.
- `uncertainty`: Uncertainty score.
- `impact`: Impact score.
- `velocity`: Speed of change.
- `description`: Driver interpretation.

## signals.csv

- `signal_id`: Signal identifier.
- `domain`: Signal domain.
- `signal`: Signal description.
- `uncertainty`: Uncertainty score.
- `impact`: Impact score.
- `novelty`: Novelty score.
- `source_type`: Synthetic source category.
- `monitoring_priority`: Qualitative priority.

## assumptions.csv

- `assumption_id`: Assumption identifier.
- `assumption_text`: Assumption statement.
- `domain`: Domain.
- `confidence`: Current confidence in the assumption.
- `exposure`: Strategic exposure if wrong.
- `reversibility`: Ease of reversal if assumption fails.
- `monitoring_signal`: Signal to monitor.

## forecast_observations.csv

- `metric`: Forecasted metric.
- `period`: Time period.
- `observed_value`: Observed synthetic value.
- `forecast_value`: Forecast synthetic value.
- `domain`: Domain.
