-- Digital Platform Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS platform_scenario_scores;
DROP VIEW IF EXISTS platform_accountability_scores;
DROP VIEW IF EXISTS platform_risk_scores;
DROP VIEW IF EXISTS platform_profile_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS platform_scenarios;
DROP TABLE IF EXISTS accountability_indicators;
DROP TABLE IF EXISTS platform_risk_register;
DROP TABLE IF EXISTS platform_profiles;

CREATE TABLE platform_profiles (
    platform_id TEXT PRIMARY KEY,
    platform_name TEXT NOT NULL,
    platform_type TEXT,
    market_role TEXT,
    network_effect_strength REAL,
    data_advantage REAL,
    gatekeeping_power REAL,
    lock_in REAL,
    interoperability REAL,
    public_accountability REAL,
    user_rights REAL,
    worker_protection REAL,
    ecological_responsibility REAL,
    digital_public_value REAL,
    description TEXT
);

CREATE TABLE platform_risk_register (
    risk_id TEXT PRIMARY KEY,
    platform_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    accountability_gap REAL,
    dependency_exposure REAL,
    public_harm_relevance REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(platform_id) REFERENCES platform_profiles(platform_id)
);

CREATE TABLE accountability_indicators (
    accountability_id TEXT PRIMARY KEY,
    platform_id TEXT,
    accountability_dimension TEXT,
    transparency REAL,
    auditability REAL,
    contestability REAL,
    enforceability REAL,
    researcher_access REAL,
    remedy_capacity REAL,
    public_participation REAL,
    description TEXT,
    FOREIGN KEY(platform_id) REFERENCES platform_profiles(platform_id)
);

CREATE TABLE platform_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    platform_power REAL,
    data_advantage REAL,
    interoperability REAL,
    worker_protection REAL,
    public_accountability REAL,
    user_rights REAL,
    ecological_responsibility REAL,
    digital_public_value REAL,
    description TEXT
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    pathway_name TEXT,
    platform_power REAL,
    data_advantage REAL,
    interoperability REAL,
    public_accountability REAL,
    user_rights REAL,
    worker_protection REAL,
    digital_public_value REAL,
    initial_public_value REAL,
    time_horizon INTEGER,
    FOREIGN KEY(scenario_id) REFERENCES platform_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    interoperability REAL,
    user_rights REAL,
    worker_protection REAL,
    public_accountability REAL,
    researcher_access REAL,
    competition_enforcement REAL,
    public_infrastructure REAL,
    ecological_standards REAL,
    remedy_capacity REAL,
    description TEXT
);

CREATE VIEW platform_profile_scores AS
SELECT
    platform_id,
    platform_name,
    platform_type,
    market_role,
    ROUND(
      0.26 * network_effect_strength +
      0.24 * data_advantage +
      0.22 * gatekeeping_power +
      0.16 * lock_in +
      0.12 * (1 - interoperability),
      4
    ) AS platform_power_score,
    ROUND(
      0.18 * interoperability +
      0.18 * public_accountability +
      0.16 * user_rights +
      0.14 * worker_protection +
      0.14 * digital_public_value +
      0.10 * ecological_responsibility +
      0.05 * (1 - (
        0.26 * network_effect_strength +
        0.24 * data_advantage +
        0.22 * gatekeeping_power +
        0.16 * lock_in +
        0.12 * (1 - interoperability)
      )) +
      0.05 * (1 - data_advantage),
      4
    ) AS public_interest_platform_capacity_score
FROM platform_profiles;

CREATE VIEW platform_risk_scores AS
SELECT
    risk_id,
    platform_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.20 * severity +
      0.16 * detection_difficulty +
      0.16 * accountability_gap +
      0.14 * dependency_exposure +
      0.10 * public_harm_relevance +
      0.06 * (1 - mitigation_capacity),
      4
    ) AS platform_risk_priority_score,
    mitigation_capacity
FROM platform_risk_register;

CREATE VIEW platform_accountability_scores AS
SELECT
    accountability_id,
    platform_id,
    accountability_dimension,
    ROUND(
      0.18 * transparency +
      0.16 * auditability +
      0.18 * contestability +
      0.18 * enforceability +
      0.10 * researcher_access +
      0.12 * remedy_capacity +
      0.08 * public_participation,
      4
    ) AS accountability_capacity_score,
    ROUND(
      1 - (
        0.18 * transparency +
        0.16 * auditability +
        0.18 * contestability +
        0.18 * enforceability +
        0.10 * researcher_access +
        0.12 * remedy_capacity +
        0.08 * public_participation
      ),
      4
    ) AS accountability_gap_score
FROM accountability_indicators;

CREATE VIEW platform_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * interoperability +
      0.18 * public_accountability +
      0.16 * user_rights +
      0.14 * worker_protection +
      0.14 * digital_public_value +
      0.10 * ecological_responsibility +
      0.05 * (1 - platform_power) +
      0.05 * (1 - data_advantage),
      4
    ) AS public_interest_platform_capacity_score,
    ROUND(
      0.24 * platform_power +
      0.20 * data_advantage +
      0.18 * (1 - interoperability) +
      0.14 * (1 - user_rights) +
      0.14 * (1 - public_accountability) +
      0.10 * (1 - worker_protection),
      4
    ) AS platform_dependency_pressure_score
FROM platform_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * interoperability +
      0.14 * user_rights +
      0.14 * worker_protection +
      0.16 * public_accountability +
      0.10 * researcher_access +
      0.10 * competition_enforcement +
      0.10 * public_infrastructure +
      0.08 * ecological_standards +
      0.02 * remedy_capacity,
      4
    ) AS public_interest_platform_strategy_score,
    ROUND(
      0.16 * public_accountability +
      0.16 * remedy_capacity +
      0.14 * user_rights +
      0.12 * worker_protection +
      0.12 * researcher_access +
      0.12 * competition_enforcement +
      0.10 * interoperability +
      0.08 * public_infrastructure,
      4
    ) AS accountability_strategy_score
FROM strategy_options;
