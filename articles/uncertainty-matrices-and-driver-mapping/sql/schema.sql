-- Uncertainty Matrices and Driver Mapping schema.
-- SQLite compatible.

DROP VIEW IF EXISTS assumption_fragility_scores;
DROP VIEW IF EXISTS monitoring_priority_scores;
DROP VIEW IF EXISTS signal_priority_scores;
DROP VIEW IF EXISTS driver_cross_impact_scores;
DROP VIEW IF EXISTS driver_interaction_scores;
DROP VIEW IF EXISTS scenario_axis_candidates;
DROP VIEW IF EXISTS driver_priority_scores;

DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS monitoring_indicators;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS driver_interactions;
DROP TABLE IF EXISTS driver_register;

CREATE TABLE driver_register (
    driver_id TEXT PRIMARY KEY,
    driver_name TEXT NOT NULL,
    domain TEXT,
    driver_type TEXT,
    impact REAL,
    uncertainty REAL,
    urgency REAL,
    interaction_strength REAL,
    distributional_burden REAL,
    monitoring_feasibility REAL,
    evidence_strength REAL,
    controllability REAL,
    description TEXT
);

CREATE TABLE driver_interactions (
    interaction_id TEXT PRIMARY KEY,
    source_driver_id TEXT,
    target_driver_id TEXT,
    relationship_type TEXT,
    influence_weight REAL,
    direction TEXT,
    delay_risk REAL,
    cascade_potential REAL,
    notes TEXT,
    FOREIGN KEY(source_driver_id) REFERENCES driver_register(driver_id),
    FOREIGN KEY(target_driver_id) REFERENCES driver_register(driver_id)
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    driver_id TEXT,
    signal_name TEXT NOT NULL,
    signal_type TEXT,
    novelty REAL,
    relevance REAL,
    urgency REAL,
    evidence_quality REAL,
    affected_voice REAL,
    interpretation TEXT,
    FOREIGN KEY(driver_id) REFERENCES driver_register(driver_id)
);

CREATE TABLE monitoring_indicators (
    indicator_id TEXT PRIMARY KEY,
    driver_id TEXT,
    indicator_name TEXT,
    baseline REAL,
    threshold_value REAL,
    review_frequency TEXT,
    assumption_risk TEXT,
    trigger_rule TEXT,
    decision_response TEXT,
    FOREIGN KEY(driver_id) REFERENCES driver_register(driver_id)
);

CREATE TABLE assumption_register (
    assumption_id TEXT PRIMARY KEY,
    driver_id TEXT,
    assumption_name TEXT,
    assumption_text TEXT,
    confidence REAL,
    fragility REAL,
    monitoring_signal TEXT,
    revision_rule TEXT,
    FOREIGN KEY(driver_id) REFERENCES driver_register(driver_id)
);

CREATE VIEW driver_priority_scores AS
SELECT
    driver_id,
    driver_name,
    domain,
    driver_type,
    ROUND(
      0.22 * impact +
      0.20 * uncertainty +
      0.14 * urgency +
      0.14 * interaction_strength +
      0.12 * distributional_burden +
      0.08 * monitoring_feasibility +
      0.06 * evidence_strength +
      0.04 * (1 - controllability),
      4
    ) AS driver_priority_score,
    CASE
      WHEN impact >= 0.80 AND uncertainty >= 0.72 THEN 'Critical uncertainty'
      WHEN impact >= 0.80 AND uncertainty < 0.72 THEN 'Baseline structural driver'
      WHEN impact < 0.80 AND uncertainty >= 0.72 THEN 'Watchlist uncertainty'
      ELSE 'Lower-priority factor'
    END AS matrix_quadrant,
    ROUND(
      impact * uncertainty * interaction_strength * monitoring_feasibility * evidence_strength,
      4
    ) AS axis_suitability_score
FROM driver_register;

CREATE VIEW scenario_axis_candidates AS
SELECT
    driver_id,
    driver_name,
    domain,
    impact,
    uncertainty,
    ROUND(
      impact * uncertainty * interaction_strength * monitoring_feasibility * evidence_strength,
      4
    ) AS axis_suitability_score
FROM driver_register
WHERE impact >= 0.80 AND uncertainty >= 0.72;

CREATE VIEW driver_interaction_scores AS
SELECT
    interaction_id,
    source_driver_id,
    target_driver_id,
    relationship_type,
    ROUND(
      influence_weight * (0.45 + 0.25 * delay_risk + 0.30 * cascade_potential),
      4
    ) AS interaction_priority_score
FROM driver_interactions;

CREATE VIEW driver_cross_impact_scores AS
SELECT
    d.driver_id,
    d.driver_name,
    ROUND(COALESCE(outgoing.outgoing_influence, 0), 4) AS outgoing_influence,
    ROUND(COALESCE(incoming.incoming_influence, 0), 4) AS incoming_influence,
    ROUND(COALESCE(outgoing.outgoing_influence, 0) + COALESCE(incoming.incoming_influence, 0), 4) AS total_cross_impact
FROM driver_register d
LEFT JOIN (
    SELECT source_driver_id AS driver_id, SUM(influence_weight) AS outgoing_influence
    FROM driver_interactions
    GROUP BY source_driver_id
) outgoing ON d.driver_id = outgoing.driver_id
LEFT JOIN (
    SELECT target_driver_id AS driver_id, SUM(influence_weight) AS incoming_influence
    FROM driver_interactions
    GROUP BY target_driver_id
) incoming ON d.driver_id = incoming.driver_id;

CREATE VIEW signal_priority_scores AS
SELECT
    signal_id,
    driver_id,
    signal_name,
    signal_type,
    ROUND(
      0.15 * novelty +
      0.30 * relevance +
      0.25 * urgency +
      0.15 * evidence_quality +
      0.15 * affected_voice,
      4
    ) AS signal_priority_score
FROM signals;

CREATE VIEW monitoring_priority_scores AS
SELECT
    m.indicator_id,
    m.driver_id,
    m.indicator_name,
    m.baseline,
    m.threshold_value,
    ROUND(ABS(m.threshold_value - m.baseline), 4) AS monitoring_gap,
    m.review_frequency,
    m.assumption_risk,
    m.trigger_rule,
    m.decision_response
FROM monitoring_indicators m;

CREATE VIEW assumption_fragility_scores AS
SELECT
    assumption_id,
    driver_id,
    assumption_name,
    ROUND((1 - confidence) * 0.45 + fragility * 0.55, 4) AS assumption_failure_risk,
    monitoring_signal,
    revision_rule
FROM assumption_register;
