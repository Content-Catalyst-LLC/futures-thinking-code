# Data Dictionary

## focal_changes.csv

Central changes used as Futures Wheel prompts.

## consequence_nodes.csv

Consequence-node register.

- `consequence_order`: Distance from the focal change. Zero is the focal node.
- `likelihood`: Plausibility of the consequence.
- `severity`: Consequence magnitude if it occurs.
- `uncertainty`: Degree of uncertainty around the consequence.
- `distributional_burden`: Degree to which burden falls unevenly on exposed groups.
- `actionability`: Degree to which institutions can act on the consequence.
- `affected_groups`: Groups likely to experience the consequence.

## consequence_edges.csv

Directed relationships among consequence nodes.

## actors.csv

Actor register for Impact Mapping.

## impact_pathways.csv

Goal-actor-impact-deliverable chains.

## interventions.csv

Candidate deliverables or interventions linked to impact pathways.

## monitoring_indicators.csv

Indicator register for adaptive review.

## distributional_audit.csv

Power and burden-shifting audit for consequence nodes.
