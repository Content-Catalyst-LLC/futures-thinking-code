-- Societal Transformation and Long-Term Change schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS equity_justice_scores;
DROP VIEW IF EXISTS system_pressure_scores;
DROP VIEW IF EXISTS transformation_scenario_scores;
DROP VIEW IF EXISTS weak_signal_priority_scores;
DROP VIEW IF EXISTS transformation_driver_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS equity_indicators;
DROP TABLE IF EXISTS system_pressure_indicators;
DROP TABLE IF EXISTS transformation_scenarios;
DROP TABLE IF EXISTS weak_signals;
DROP TABLE IF EXISTS transformation_drivers;

CREATE TABLE transformation_drivers (
    driver_id TEXT PRIMARY KEY,
    driver_name TEXT NOT NULL,
    driver_domain TEXT,
    transformative_intensity REAL,
    uncertainty REAL,
    system_reach REAL,
    feedback_strength REAL,
    threshold_proximity REAL,
    governance_relevance REAL,
    equity_relevance REAL,
    description TEXT
);

CREATE TABLE weak_signals (
    signal_id TEXT PRIMARY KEY,
    driver_id TEXT,
    signal_name TEXT,
    signal_type TEXT,
    novelty REAL,
    relevance REAL,
    urgency REAL,
    evidence_quality REAL,
    affected_voice REAL,
    source_traceability REAL,
    interpretation TEXT,
    FOREIGN KEY(driver_id) REFERENCES transformation_drivers(driver_id)
);

CREATE TABLE transformation_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    technology_intensity REAL,
    institutional_adaptability REAL,
    ecological_stress REAL,
    social_cohesion REAL,
    economic_restructuring REAL,
    equity_protection REAL,
    public_legitimacy REAL,
    time_horizon TEXT,
    description TEXT
);

CREATE TABLE system_pressure_indicators (
    indicator_id TEXT PRIMARY KEY,
    indicator_name TEXT,
    domain TEXT,
    baseline REAL,
    current_value REAL,
    threshold_value REAL,
    trend_direction TEXT,
    review_frequency TEXT,
    owner TEXT,
    interpretation TEXT
);

CREATE TABLE equity_indicators (
    equity_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    equity_dimension TEXT,
    exposure REAL,
    voice REAL,
    protection REAL,
    repair REAL,
    burden_concentration REAL,
    agency REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES transformation_scenarios(scenario_id)
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    pathway_name TEXT,
    technology REAL,
    institution REAL,
    ecology REAL,
    economic_restructuring REAL,
    public_legitimacy REAL,
    equity_protection REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(scenario_id) REFERENCES transformation_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    adaptation_depth REAL,
    transformation_depth REAL,
    equity_commitment REAL,
    public_investment REAL,
    institutional_learning REAL,
    participation_strength REAL,
    ecological_responsibility REAL,
    description TEXT
);

CREATE VIEW transformation_driver_scores AS
SELECT
    driver_id,
    driver_name,
    driver_domain,
    ROUND(
      0.18 * transformative_intensity +
      0.14 * uncertainty +
      0.16 * system_reach +
      0.14 * feedback_strength +
      0.14 * threshold_proximity +
      0.12 * governance_relevance +
      0.12 * equity_relevance,
      4
    ) AS driver_transformation_priority
FROM transformation_drivers;

CREATE VIEW weak_signal_priority_scores AS
SELECT
    signal_id,
    driver_id,
    signal_name,
    signal_type,
    ROUND(
      0.14 * novelty +
      0.24 * relevance +
      0.20 * urgency +
      0.14 * evidence_quality +
      0.16 * affected_voice +
      0.12 * source_traceability,
      4
    ) AS signal_priority_score,
    interpretation
FROM weak_signals;

CREATE VIEW transformation_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * technology_intensity +
      0.18 * economic_restructuring +
      0.18 * ecological_stress +
      0.16 * institutional_adaptability +
      0.14 * social_cohesion +
      0.08 * equity_protection +
      0.08 * public_legitimacy,
      4
    ) AS transformation_depth_score,
    ROUND(
      0.22 * institutional_adaptability +
      0.22 * equity_protection +
      0.20 * public_legitimacy +
      0.18 * social_cohesion +
      0.10 * (1 - ecological_stress) +
      0.08 * economic_restructuring,
      4
    ) AS just_transformation_capacity_score,
    ROUND(
      0.26 * ecological_stress +
      0.22 * (1 - institutional_adaptability) +
      0.20 * (1 - social_cohesion) +
      0.18 * (1 - public_legitimacy) +
      0.14 * (1 - equity_protection),
      4
    ) AS fragility_score
FROM transformation_scenarios;

CREATE VIEW system_pressure_scores AS
SELECT
    indicator_id,
    indicator_name,
    domain,
    baseline,
    current_value,
    threshold_value,
    ROUND(current_value - threshold_value, 4) AS threshold_gap,
    CASE WHEN current_value >= threshold_value THEN 1 ELSE 0 END AS threshold_breached,
    ROUND(
      0.35 * current_value +
      0.30 * CASE WHEN current_value >= threshold_value THEN 1 ELSE 0 END +
      0.20 * MAX(0, current_value - threshold_value) +
      0.15 *
        CASE review_frequency
          WHEN 'monthly' THEN 1.00
          WHEN 'quarterly' THEN 0.88
          WHEN 'semiannual' THEN 0.68
          WHEN 'annual' THEN 0.48
          ELSE 0.50
        END,
      4
    ) AS pressure_score,
    owner,
    interpretation
FROM system_pressure_indicators;

CREATE VIEW equity_justice_scores AS
SELECT
    equity_id,
    scenario_id,
    equity_dimension,
    ROUND(
      0.20 * voice +
      0.22 * protection +
      0.22 * repair +
      0.18 * agency +
      0.18 * (1 - burden_concentration),
      4
    ) AS justice_capacity_score,
    ROUND(
      0.30 * exposure +
      0.30 * burden_concentration +
      0.16 * (1 - voice) +
      0.12 * (1 - protection) +
      0.12 * (1 - agency),
      4
    ) AS harm_concentration_score
FROM equity_indicators;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.14 * adaptation_depth +
      0.16 * transformation_depth +
      0.18 * equity_commitment +
      0.16 * public_investment +
      0.14 * institutional_learning +
      0.12 * participation_strength +
      0.10 * ecological_responsibility,
      4
    ) AS public_interest_transformation_score,
    ROUND(
      0.18 * adaptation_depth +
      0.14 * transformation_depth +
      0.14 * equity_commitment +
      0.16 * public_investment +
      0.18 * institutional_learning +
      0.10 * participation_strength +
      0.10 * ecological_responsibility,
      4
    ) AS institutional_viability_score
FROM strategy_options;
