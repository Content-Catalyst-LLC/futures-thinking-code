-- AI and the Future of Decision-Making schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS equity_harm_scores;
DROP VIEW IF EXISTS risk_priority_scores;
DROP VIEW IF EXISTS governance_readiness_scores;
DROP VIEW IF EXISTS decision_system_profile_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS uncertainty_scenarios;
DROP TABLE IF EXISTS equity_harm_indicators;
DROP TABLE IF EXISTS risk_indicators;
DROP TABLE IF EXISTS governance_controls;
DROP TABLE IF EXISTS decision_system_profiles;

CREATE TABLE decision_system_profiles (
    system_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    decision_domain TEXT,
    human_judgment REAL,
    machine_inference REAL,
    coordination_quality REAL,
    transparency REAL,
    uncertainty_management REAL,
    accountability REAL,
    contestability REAL,
    equity_protection REAL,
    automation_intensity REAL,
    description TEXT
);

CREATE TABLE governance_controls (
    control_id TEXT PRIMARY KEY,
    system_id TEXT,
    control_name TEXT,
    control_type TEXT,
    documentation REAL,
    auditability REAL,
    explainability REAL,
    human_oversight REAL,
    appeal_rights REAL,
    monitoring_strength REAL,
    enforcement_capacity REAL,
    description TEXT,
    FOREIGN KEY(system_id) REFERENCES decision_system_profiles(system_id)
);

CREATE TABLE risk_indicators (
    risk_id TEXT PRIMARY KEY,
    system_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    governance_gap REAL,
    affected_population_exposure REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(system_id) REFERENCES decision_system_profiles(system_id)
);

CREATE TABLE equity_harm_indicators (
    equity_id TEXT PRIMARY KEY,
    system_id TEXT,
    equity_dimension TEXT,
    error_burden REAL,
    exposure REAL,
    vulnerability REAL,
    contestability REAL,
    voice REAL,
    protection REAL,
    repair_capacity REAL,
    description TEXT,
    FOREIGN KEY(system_id) REFERENCES decision_system_profiles(system_id)
);

CREATE TABLE uncertainty_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    environment_stability REAL,
    distribution_shift REAL,
    adversarial_pressure REAL,
    public_trust REAL,
    regulatory_strength REAL,
    institutional_capacity REAL,
    description TEXT
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    system_id TEXT,
    pathway_name TEXT,
    human REAL,
    machine REAL,
    coordination REAL,
    governance REAL,
    contestability REAL,
    initial_decision_quality REAL,
    time_horizon INTEGER,
    FOREIGN KEY(system_id) REFERENCES decision_system_profiles(system_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    human_authority REAL,
    machine_capability REAL,
    coordination_design REAL,
    transparency REAL,
    accountability REAL,
    contestability REAL,
    equity_protection REAL,
    uncertainty_stress_testing REAL,
    description TEXT
);

CREATE VIEW decision_system_profile_scores AS
SELECT
    system_id,
    system_type,
    decision_domain,
    ROUND(
      0.16 * human_judgment +
      0.16 * machine_inference +
      0.16 * coordination_quality +
      0.12 * transparency +
      0.12 * uncertainty_management +
      0.12 * accountability +
      0.08 * contestability +
      0.08 * equity_protection,
      4
    ) AS decision_system_profile_score,
    ROUND(
      0.22 * transparency +
      0.24 * accountability +
      0.24 * contestability +
      0.18 * uncertainty_management +
      0.12 * equity_protection,
      4
    ) AS governance_profile_score,
    ROUND(
      0.26 * automation_intensity +
      0.20 * (1 - accountability) +
      0.20 * (1 - contestability) +
      0.18 * (1 - transparency) +
      0.16 * (1 - equity_protection),
      4
    ) AS risk_profile_score
FROM decision_system_profiles;

CREATE VIEW governance_readiness_scores AS
SELECT
    control_id,
    system_id,
    control_name,
    control_type,
    ROUND(
      0.16 * documentation +
      0.16 * auditability +
      0.14 * explainability +
      0.16 * human_oversight +
      0.14 * appeal_rights +
      0.12 * monitoring_strength +
      0.12 * enforcement_capacity,
      4
    ) AS governance_readiness_score,
    ROUND(
      1 - (
        0.16 * documentation +
        0.16 * auditability +
        0.14 * explainability +
        0.16 * human_oversight +
        0.14 * appeal_rights +
        0.12 * monitoring_strength +
        0.12 * enforcement_capacity
      ),
      4
    ) AS governance_gap_score
FROM governance_controls;

CREATE VIEW risk_priority_scores AS
SELECT
    risk_id,
    system_id,
    risk_name,
    risk_type,
    ROUND(
      0.22 * probability +
      0.24 * severity +
      0.18 * detection_difficulty +
      0.18 * governance_gap +
      0.12 * affected_population_exposure +
      0.06 * (1 - mitigation_capacity),
      4
    ) AS risk_priority_score,
    mitigation_capacity
FROM risk_indicators;

CREATE VIEW equity_harm_scores AS
SELECT
    equity_id,
    system_id,
    equity_dimension,
    ROUND(
      0.18 * contestability +
      0.18 * voice +
      0.20 * protection +
      0.18 * repair_capacity +
      0.14 * (1 - error_burden) +
      0.12 * (1 - vulnerability),
      4
    ) AS justice_capacity_score,
    ROUND(
      0.25 * error_burden +
      0.22 * exposure +
      0.22 * vulnerability +
      0.16 * (1 - contestability) +
      0.15 * (1 - repair_capacity),
      4
    ) AS harm_risk_score
FROM equity_harm_indicators;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * human_authority +
      0.12 * machine_capability +
      0.16 * coordination_design +
      0.12 * transparency +
      0.16 * accountability +
      0.14 * contestability +
      0.10 * equity_protection +
      0.08 * uncertainty_stress_testing,
      4
    ) AS public_interest_decision_score,
    ROUND(
      0.16 * transparency +
      0.20 * accountability +
      0.18 * contestability +
      0.16 * equity_protection +
      0.16 * uncertainty_stress_testing +
      0.14 * coordination_design,
      4
    ) AS governance_strength_score
FROM strategy_options;
