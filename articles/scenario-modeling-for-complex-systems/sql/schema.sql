-- Scenario Modeling for Complex Systems schema.
-- SQLite compatible.

DROP VIEW IF EXISTS monitoring_trigger_scores;
DROP VIEW IF EXISTS driver_priority_scores;
DROP VIEW IF EXISTS strategy_implementation_risk;
DROP VIEW IF EXISTS scenario_stress_profiles;
DROP VIEW IF EXISTS scenario_quality_scores;

DROP TABLE IF EXISTS monitoring_indicators;
DROP TABLE IF EXISTS driver_register;
DROP TABLE IF EXISTS strategy_portfolio;
DROP TABLE IF EXISTS scenario_assumptions;

CREATE TABLE scenario_assumptions (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    growth_rate REAL,
    shock_level REAL,
    adaptation_gain REAL,
    feedback_strength REAL,
    learning_gain REAL,
    governance_capacity REAL,
    public_trust REAL,
    distributional_pressure REAL,
    description TEXT
);

CREATE TABLE strategy_portfolio (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT,
    baseline_boost REAL,
    shock_absorption REAL,
    adaptation_boost REAL,
    equity_weight REAL,
    implementation_complexity REAL,
    governance_dependency REAL,
    description TEXT
);

CREATE TABLE driver_register (
    driver_id TEXT PRIMARY KEY,
    driver_name TEXT NOT NULL,
    domain TEXT,
    impact_level REAL,
    uncertainty_level REAL,
    interaction_strength REAL,
    time_sensitivity REAL,
    monitoring_need REAL,
    description TEXT
);

CREATE TABLE monitoring_indicators (
    indicator_id TEXT PRIMARY KEY,
    driver_id TEXT,
    indicator_name TEXT,
    baseline REAL,
    target_or_threshold REAL,
    review_frequency TEXT,
    trigger_rule TEXT,
    decision_response TEXT,
    FOREIGN KEY(driver_id) REFERENCES driver_register(driver_id)
);

CREATE VIEW scenario_quality_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.20 * growth_rate +
      0.20 * adaptation_gain +
      0.20 * learning_gain +
      0.20 * governance_capacity +
      0.20 * public_trust,
      4
    ) AS adaptive_quality_score
FROM scenario_assumptions;

CREATE VIEW scenario_stress_profiles AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.35 * shock_level +
      0.25 * feedback_strength +
      0.25 * distributional_pressure +
      0.15 * (1 - governance_capacity),
      4
    ) AS stress_profile_score
FROM scenario_assumptions;

CREATE VIEW strategy_implementation_risk AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.40 * implementation_complexity +
      0.30 * governance_dependency +
      0.30 * (1 - equity_weight),
      4
    ) AS implementation_risk_score
FROM strategy_portfolio;

CREATE VIEW driver_priority_scores AS
SELECT
    driver_id,
    driver_name,
    domain,
    ROUND(
      0.25 * impact_level +
      0.25 * uncertainty_level +
      0.20 * interaction_strength +
      0.15 * time_sensitivity +
      0.15 * monitoring_need,
      4
    ) AS driver_priority_score
FROM driver_register;

CREATE VIEW monitoring_trigger_scores AS
SELECT
    indicator_id,
    driver_id,
    indicator_name,
    baseline,
    target_or_threshold,
    ROUND(ABS(target_or_threshold - baseline), 4) AS monitoring_gap,
    review_frequency,
    trigger_rule,
    decision_response
FROM monitoring_indicators;
