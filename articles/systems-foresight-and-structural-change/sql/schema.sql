-- Systems Foresight and Structural Change schema.
-- SQLite compatible.

DROP VIEW IF EXISTS monitoring_trigger_scores;
DROP VIEW IF EXISTS signal_pressure_scores;
DROP VIEW IF EXISTS leverage_point_scores;
DROP VIEW IF EXISTS feedback_loop_priority_scores;
DROP VIEW IF EXISTS structural_pressure_scores;

DROP TABLE IF EXISTS monitoring_triggers;
DROP TABLE IF EXISTS strategy_pathways;
DROP TABLE IF EXISTS signals_pressure;
DROP TABLE IF EXISTS leverage_points;
DROP TABLE IF EXISTS feedback_loops;
DROP TABLE IF EXISTS system_domains;

CREATE TABLE system_domains (
    system_id TEXT PRIMARY KEY,
    system_domain TEXT NOT NULL,
    domain_type TEXT,
    system_stress REAL,
    adaptive_capacity REAL,
    public_trust REAL,
    interdependence REAL,
    distributional_vulnerability REAL,
    institutional_fragmentation REAL,
    structural_lock_in REAL,
    description TEXT
);

CREATE TABLE feedback_loops (
    loop_id TEXT PRIMARY KEY,
    system_id TEXT,
    loop_name TEXT NOT NULL,
    loop_type TEXT,
    loop_polarity TEXT,
    feedback_strength REAL,
    delay_risk REAL,
    visibility REAL,
    institutional_control REAL,
    description TEXT,
    FOREIGN KEY(system_id) REFERENCES system_domains(system_id)
);

CREATE TABLE leverage_points (
    leverage_id TEXT PRIMARY KEY,
    system_id TEXT,
    intervention TEXT NOT NULL,
    intervention_level TEXT,
    intervention_depth REAL,
    system_reach REAL,
    political_feasibility REAL,
    legitimacy_quality REAL,
    equity_quality REAL,
    implementation_readiness REAL,
    description TEXT,
    FOREIGN KEY(system_id) REFERENCES system_domains(system_id)
);

CREATE TABLE signals_pressure (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT,
    signal_name TEXT NOT NULL,
    signal_type TEXT,
    novelty REAL,
    structural_relevance REAL,
    urgency REAL,
    visibility REAL,
    affected_voice REAL,
    interpretation TEXT,
    FOREIGN KEY(system_id) REFERENCES system_domains(system_id)
);

CREATE TABLE strategy_pathways (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT,
    stress_reduction REAL,
    capacity_gain REAL,
    trust_gain REAL,
    vulnerability_reduction REAL,
    structural_depth REAL,
    implementation_complexity REAL,
    governance_dependency REAL,
    description TEXT
);

CREATE TABLE monitoring_triggers (
    trigger_id TEXT PRIMARY KEY,
    system_id TEXT,
    indicator_name TEXT,
    baseline REAL,
    threshold_value REAL,
    review_frequency TEXT,
    trigger_rule TEXT,
    decision_response TEXT,
    FOREIGN KEY(system_id) REFERENCES system_domains(system_id)
);

CREATE VIEW structural_pressure_scores AS
SELECT
    system_id,
    system_domain,
    domain_type,
    ROUND(
      0.22 * system_stress +
      0.16 * (1 - adaptive_capacity) +
      0.14 * (1 - public_trust) +
      0.16 * interdependence +
      0.14 * distributional_vulnerability +
      0.09 * institutional_fragmentation +
      0.09 * structural_lock_in,
      4
    ) AS structural_pressure_score
FROM system_domains;

CREATE VIEW feedback_loop_priority_scores AS
SELECT
    loop_id,
    system_id,
    loop_name,
    loop_type,
    loop_polarity,
    ROUND(
      feedback_strength *
      (0.40 * delay_risk + 0.30 * (1 - visibility) + 0.30 * (1 - institutional_control)),
      4
    ) AS feedback_priority_score
FROM feedback_loops;

CREATE VIEW leverage_point_scores AS
SELECT
    leverage_id,
    system_id,
    intervention,
    intervention_level,
    ROUND(
      intervention_depth *
      system_reach *
      political_feasibility *
      legitimacy_quality *
      equity_quality *
      implementation_readiness,
      4
    ) AS leverage_score
FROM leverage_points;

CREATE VIEW signal_pressure_scores AS
SELECT
    signal_id,
    system_id,
    signal_name,
    signal_type,
    ROUND(
      0.15 * novelty +
      0.30 * structural_relevance +
      0.25 * urgency +
      0.15 * visibility +
      0.15 * affected_voice,
      4
    ) AS signal_priority_score
FROM signals_pressure;

CREATE VIEW monitoring_trigger_scores AS
SELECT
    trigger_id,
    system_id,
    indicator_name,
    baseline,
    threshold_value,
    ROUND(ABS(threshold_value - baseline), 4) AS monitoring_gap,
    review_frequency,
    trigger_rule,
    decision_response
FROM monitoring_triggers;
