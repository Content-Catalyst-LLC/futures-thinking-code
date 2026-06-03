-- Early Warning Systems and Futures Intelligence schema.
-- SQLite compatible.

DROP VIEW IF EXISTS response_protocol_priorities;
DROP VIEW IF EXISTS cross_system_cascade_scores;
DROP VIEW IF EXISTS scenario_monitor_scores;
DROP VIEW IF EXISTS assumption_failure_scores;
DROP VIEW IF EXISTS threshold_trigger_scores;
DROP VIEW IF EXISTS signal_warning_scores;

DROP TABLE IF EXISTS response_protocols;
DROP TABLE IF EXISTS cross_system_interactions;
DROP TABLE IF EXISTS scenario_monitors;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS signals;

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    signal_name TEXT NOT NULL,
    domain TEXT,
    signal_type TEXT,
    novelty REAL,
    relevance REAL,
    urgency REAL,
    evidence_quality REAL,
    affected_voice REAL,
    vulnerability REAL,
    lead_time_value REAL,
    description TEXT
);

CREATE TABLE indicators (
    indicator_id TEXT PRIMARY KEY,
    domain TEXT,
    indicator_name TEXT NOT NULL,
    baseline REAL,
    current_value REAL,
    threshold_value REAL,
    review_frequency TEXT,
    warning_owner TEXT,
    trigger_rule TEXT,
    response_protocol_id TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    domain TEXT,
    assumption_name TEXT,
    assumption_text TEXT,
    confidence REAL,
    fragility REAL,
    linked_indicator TEXT,
    revision_rule TEXT
);

CREATE TABLE scenario_monitors (
    scenario_id TEXT,
    scenario_name TEXT,
    indicator_name TEXT,
    signal_direction TEXT,
    scenario_relevance REAL,
    monitoring_weight REAL,
    interpretation TEXT
);

CREATE TABLE cross_system_interactions (
    interaction_id TEXT PRIMARY KEY,
    source_domain TEXT,
    target_domain TEXT,
    relationship_type TEXT,
    influence_weight REAL,
    delay_risk REAL,
    cascade_potential REAL,
    description TEXT
);

CREATE TABLE response_protocols (
    response_protocol_id TEXT PRIMARY KEY,
    response_name TEXT,
    response_type TEXT,
    lead_agency TEXT,
    action_level TEXT,
    public_communication_required TEXT,
    accountability_review_required TEXT,
    response_description TEXT
);

CREATE VIEW signal_warning_scores AS
SELECT
    signal_id,
    signal_name,
    domain,
    signal_type,
    ROUND(
      0.12 * novelty +
      0.22 * relevance +
      0.20 * urgency +
      0.13 * evidence_quality +
      0.11 * affected_voice +
      0.13 * vulnerability +
      0.09 * lead_time_value,
      4
    ) AS warning_score,
    CASE
      WHEN (
        0.12 * novelty +
        0.22 * relevance +
        0.20 * urgency +
        0.13 * evidence_quality +
        0.11 * affected_voice +
        0.13 * vulnerability +
        0.09 * lead_time_value
      ) >= 0.82 THEN 'Escalate'
      WHEN (
        0.12 * novelty +
        0.22 * relevance +
        0.20 * urgency +
        0.13 * evidence_quality +
        0.11 * affected_voice +
        0.13 * vulnerability +
        0.09 * lead_time_value
      ) >= 0.76 THEN 'Watch closely'
      ELSE 'Monitor'
    END AS warning_level
FROM signals;

CREATE VIEW threshold_trigger_scores AS
SELECT
    indicator_id,
    domain,
    indicator_name,
    baseline,
    current_value,
    threshold_value,
    ROUND(current_value - threshold_value, 4) AS threshold_gap,
    CASE WHEN current_value >= threshold_value THEN 1 ELSE 0 END AS threshold_breached,
    review_frequency,
    warning_owner,
    ROUND(
      0.45 * CASE WHEN current_value >= threshold_value THEN 1 ELSE 0 END +
      0.25 * current_value +
      0.20 * MAX(0, current_value - threshold_value) +
      0.10 *
        CASE review_frequency
          WHEN 'monthly' THEN 1.00
          WHEN 'quarterly' THEN 0.88
          WHEN 'semiannual' THEN 0.68
          WHEN 'annual' THEN 0.48
          ELSE 0.50
        END,
      4
    ) AS trigger_priority_score,
    trigger_rule,
    response_protocol_id
FROM indicators;

CREATE VIEW assumption_failure_scores AS
SELECT
    assumption_id,
    domain,
    assumption_name,
    ROUND(0.45 * (1 - confidence) + 0.55 * fragility, 4) AS assumption_failure_risk,
    linked_indicator,
    revision_rule
FROM assumptions;

CREATE VIEW scenario_monitor_scores AS
SELECT
    scenario_id,
    scenario_name,
    indicator_name,
    signal_direction,
    ROUND(scenario_relevance * monitoring_weight, 4) AS scenario_monitor_score,
    interpretation
FROM scenario_monitors;

CREATE VIEW cross_system_cascade_scores AS
SELECT
    interaction_id,
    source_domain,
    target_domain,
    relationship_type,
    ROUND(
      influence_weight * (0.40 + 0.25 * delay_risk + 0.35 * cascade_potential),
      4
    ) AS cascade_warning_score,
    description
FROM cross_system_interactions;

CREATE VIEW response_protocol_priorities AS
SELECT
    rp.response_protocol_id,
    rp.response_name,
    rp.response_type,
    rp.lead_agency,
    rp.action_level,
    ROUND(COALESCE(tt.trigger_priority_score, 0), 4) AS linked_trigger_priority,
    ROUND(
      0.55 * COALESCE(tt.trigger_priority_score, 0) +
      0.20 *
        CASE rp.action_level
          WHEN 'escalate' THEN 1.00
          WHEN 'pause' THEN 0.96
          WHEN 'prepare' THEN 0.72
          WHEN 'watch' THEN 0.54
          ELSE 0.50
        END +
      0.15 * CASE WHEN LOWER(rp.public_communication_required) = 'yes' THEN 1 ELSE 0 END +
      0.10 * CASE WHEN LOWER(rp.accountability_review_required) = 'yes' THEN 1 ELSE 0 END,
      4
    ) AS response_priority_score,
    rp.response_description
FROM response_protocols rp
LEFT JOIN threshold_trigger_scores tt
ON rp.response_protocol_id = tt.response_protocol_id;
