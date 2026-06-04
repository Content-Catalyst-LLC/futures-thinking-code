-- Global Governance Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS institutional_capacity_scores;
DROP VIEW IF EXISTS governance_risk_priority_scores;
DROP VIEW IF EXISTS governance_strategy_scores;
DROP VIEW IF EXISTS governance_scenario_scores;
DROP VIEW IF EXISTS governance_profile_scores;

DROP TABLE IF EXISTS adaptive_governance_pathways;
DROP TABLE IF EXISTS institutional_records;
DROP TABLE IF EXISTS governance_risk_indicators;
DROP TABLE IF EXISTS governance_strategy_options;
DROP TABLE IF EXISTS governance_scenarios;
DROP TABLE IF EXISTS governance_profiles;

CREATE TABLE governance_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    institutional_capacity REAL,
    legitimacy REAL,
    legal_authority REAL,
    finance_capacity REAL,
    collective_action REAL,
    technology_governance REAL,
    planetary_risk_coordination REAL,
    adaptive_learning REAL,
    public_accountability REAL,
    representation_equity REAL,
    description TEXT
);

CREATE TABLE governance_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    climate_stress REAL,
    health_stress REAL,
    finance_stress REAL,
    technology_stress REAL,
    migration_stress REAL,
    security_stress REAL,
    legitimacy_stress REAL,
    institutional_fragmentation REAL,
    private_power_pressure REAL,
    civil_society_constraint REAL,
    description TEXT
);

CREATE TABLE governance_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    representation_gain REAL,
    finance_gain REAL,
    legal_accountability_gain REAL,
    climate_governance_gain REAL,
    health_governance_gain REAL,
    technology_governance_gain REAL,
    migration_protection_gain REAL,
    security_coordination_gain REAL,
    civil_society_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES governance_profiles(profile_id)
);

CREATE TABLE governance_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    cascade_potential REAL,
    visibility_gap REAL,
    recovery_difficulty REAL,
    distributional_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES governance_scenarios(scenario_id)
);

CREATE TABLE institutional_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    diplomatic_capacity REAL,
    monitoring_capacity REAL,
    finance_capacity REAL,
    legal_accountability REAL,
    scientific_capacity REAL,
    implementation_capacity REAL,
    public_accountability REAL,
    civil_society_space REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES governance_profiles(profile_id)
);

CREATE TABLE adaptive_governance_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    initial_governance_capacity REAL,
    institutional_capacity REAL,
    legitimacy REAL,
    legal_authority REAL,
    finance_capacity REAL,
    collective_action REAL,
    technology_governance REAL,
    planetary_coordination REAL,
    adaptive_learning REAL,
    public_accountability REAL,
    system_stress REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES governance_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES governance_scenarios(scenario_id)
);

CREATE VIEW governance_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.14 * institutional_capacity +
      0.16 * legitimacy +
      0.12 * legal_authority +
      0.11 * finance_capacity +
      0.13 * collective_action +
      0.10 * technology_governance +
      0.10 * planetary_risk_coordination +
      0.08 * adaptive_learning +
      0.08 * public_accountability +
      0.08 * representation_equity,
      4
    ) AS governance_capacity_score,
    ROUND(
      0.18 * (1 - legitimacy) +
      0.14 * (1 - representation_equity) +
      0.13 * (1 - public_accountability) +
      0.12 * (1 - legal_authority) +
      0.11 * (1 - collective_action) +
      0.10 * (1 - finance_capacity) +
      0.08 * (1 - institutional_capacity) +
      0.07 * (1 - technology_governance) +
      0.04 * (1 - planetary_risk_coordination) +
      0.03 * (1 - adaptive_learning),
      4
    ) AS legitimacy_gap_score
FROM governance_profiles;

CREATE VIEW governance_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * climate_stress +
      0.10 * health_stress +
      0.10 * finance_stress +
      0.11 * technology_stress +
      0.08 * migration_stress +
      0.10 * security_stress +
      0.13 * legitimacy_stress +
      0.12 * institutional_fragmentation +
      0.09 * private_power_pressure +
      0.05 * civil_society_constraint,
      4
    ) AS global_governance_stress_score
FROM governance_scenarios;

CREATE VIEW governance_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * representation_gain +
      0.12 * finance_gain +
      0.12 * legal_accountability_gain +
      0.11 * climate_governance_gain +
      0.09 * health_governance_gain +
      0.10 * technology_governance_gain +
      0.08 * migration_protection_gain +
      0.08 * security_coordination_gain +
      0.08 * civil_society_gain +
      0.04 * implementation_capacity +
      0.05 * public_legitimacy_gain,
      4
    ) AS governance_strategy_value_score
FROM governance_strategy_options;

CREATE VIEW governance_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.18 * severity +
      0.17 * cascade_potential +
      0.12 * visibility_gap +
      0.14 * recovery_difficulty +
      0.17 * distributional_harm +
      0.08 * (1 - preparedness),
      4
    ) AS governance_risk_priority_score,
    distributional_harm,
    preparedness
FROM governance_risk_indicators;

CREATE VIEW institutional_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.14 * diplomatic_capacity +
      0.13 * monitoring_capacity +
      0.13 * finance_capacity +
      0.13 * legal_accountability +
      0.13 * scientific_capacity +
      0.12 * implementation_capacity +
      0.12 * public_accountability +
      0.10 * civil_society_space,
      4
    ) AS institutional_capacity_score
FROM institutional_records;
