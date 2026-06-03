# Data Dictionary

## signals.csv

Synthetic signal register for early warning and futures intelligence.

- `novelty`: How new or unexpected the signal is.
- `relevance`: Importance for the focal system or strategic question.
- `urgency`: Time sensitivity.
- `evidence_quality`: Reliability and usefulness of evidence.
- `affected_voice`: Degree to which affected people or frontline knowledge are represented.
- `vulnerability`: Exposure or vulnerability associated with the signal.
- `lead_time_value`: Value of early detection for protective or adaptive action.

## indicators.csv

Monitoring indicators with baselines, current values, thresholds, review frequency, owners, trigger rules, and linked response protocols.

## assumptions.csv

Fragile strategy assumptions linked to indicators and revision rules.

## scenario_monitors.csv

Scenario indicators showing which scenario pathway a signal may support.

## cross_system_interactions.csv

Directed cross-system relationships and cascade potential.

## response_protocols.csv

Defined responses that connect warning to authority, communication, accountability, and action.
