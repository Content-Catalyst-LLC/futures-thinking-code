# Data Dictionary

## drivers.csv

Core driver register for futures intelligence. Key fields include impact, uncertainty, traceability, freshness, completeness, validity, and review status.

## signals.csv

Signal register linked to drivers, including source traceability, evidence quality, affected voice, and interpretation.

## scenarios.csv

Scenario repository records with version, time horizon, linked drivers, assumption count, evidence notes, review status, and narrative summary.

## assumptions.csv

Assumption register linked to scenarios and indicators with confidence, fragility, strategic impact, and revision rules.

## strategy_evaluations.csv

Scenario-strategy test records with effectiveness, feasibility, equity, legitimacy, adaptability, reviewer, and notes.

## lineage_edges.csv

Dependency graph linking drivers, signals, assumptions, scenarios, evaluations, and reports.

## workflow_runs.csv

Workflow integrity records for reproducible execution.

## validation_rules.csv

Human-readable validation rules for the companion workflow.
