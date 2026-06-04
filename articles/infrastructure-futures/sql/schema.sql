-- Infrastructure Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS infrastructure_governance_capacity_scores;
DROP VIEW IF EXISTS infrastructure_risk_priority_scores;
DROP VIEW IF EXISTS infrastructure_strategy_scores;
DROP VIEW IF EXISTS infrastructure_scenario_scores;
DROP VIEW IF EXISTS infrastructure_profile_scores;

DROP TABLE IF EXISTS infrastructure_cascade_pathways;
DROP TABLE IF EXISTS infrastructure_governance_records;
DROP TABLE IF EXISTS infrastructure_risk_indicators;
DROP TABLE IF EXISTS infrastructure_strategy_options;
DROP TABLE IF EXISTS infrastructure_scenarios;
DROP TABLE IF EXISTS infrastructure_system_profiles;

CREATE TABLE infrastructure_system_profiles (
    profile_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT,
    centralization REAL,
    redundancy REAL,
    digital_dependence REAL,
    climate_exposure REAL,
    coordination_quality REAL,
    public_finance_capacity REAL,
    maintenance_integrity REAL,
    equity_of_access REAL,
    geopolitical_dependency REAL,
    description TEXT
);

CREATE TABLE infrastructure_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    physical_load REAL,
    climate_pressure REAL,
    digital_control_risk REAL,
    finance_pressure REAL,
    maintenance_backlog_pressure REAL,
    governance_fragmentation REAL,
    geopolitical_chokepoint_pressure REAL,
    access_inequality_pressure REAL,
    description TEXT
);

CREATE TABLE infrastructure_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    redundancy_gain REAL,
    maintenance_gain REAL,
    climate_adaptation_gain REAL,
    digital_accountability_gain REAL,
    governance_gain REAL,
    finance_capacity_gain REAL,
    equity_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES infrastructure_system_profiles(profile_id)
);

CREATE TABLE infrastructure_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES infrastructure_scenarios(scenario_id)
);

CREATE TABLE infrastructure_governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    coordination REAL,
    public_finance REAL,
    maintenance_capacity REAL,
    digital_accountability REAL,
    climate_governance REAL,
    procurement_integrity REAL,
    equity_safeguards REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES infrastructure_system_profiles(profile_id)
);

CREATE TABLE infrastructure_cascade_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    centralization REAL,
    redundancy REAL,
    digital_dependence REAL,
    climate_exposure REAL,
    coordination_quality REAL,
    public_finance_capacity REAL,
    maintenance_integrity REAL,
    equity_of_access REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES infrastructure_system_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES infrastructure_scenarios(scenario_id)
);

CREATE VIEW infrastructure_profile_scores AS
SELECT
    profile_id,
    system_name,
    system_type,
    ROUND(
      0.14 * (1 - centralization) +
      0.18 * redundancy -
      0.12 * digital_dependence -
      0.16 * climate_exposure +
      0.16 * coordination_quality +
      0.12 * public_finance_capacity +
      0.12 * maintenance_integrity +
      0.10 * equity_of_access -
      0.08 * geopolitical_dependency,
      4
    ) AS infrastructure_viability_score,
    ROUND(
      0.14 * centralization +
      0.14 * (1 - redundancy) +
      0.12 * digital_dependence +
      0.17 * climate_exposure +
      0.13 * (1 - coordination_quality) +
      0.11 * (1 - public_finance_capacity) +
      0.10 * (1 - maintenance_integrity) +
      0.08 * (1 - equity_of_access) +
      0.11 * geopolitical_dependency,
      4
    ) AS infrastructure_fragility_score
FROM infrastructure_system_profiles;

CREATE VIEW infrastructure_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.15 * physical_load +
      0.16 * climate_pressure +
      0.13 * digital_control_risk +
      0.13 * finance_pressure +
      0.14 * maintenance_backlog_pressure +
      0.12 * governance_fragmentation +
      0.09 * geopolitical_chokepoint_pressure +
      0.08 * access_inequality_pressure,
      4
    ) AS infrastructure_stress_score,
    ROUND(
      0.16 * (1 - governance_fragmentation) +
      0.16 * (1 - maintenance_backlog_pressure) +
      0.14 * (1 - climate_pressure) +
      0.12 * (1 - finance_pressure) +
      0.12 * (1 - physical_load) +
      0.10 * (1 - digital_control_risk) +
      0.10 * (1 - access_inequality_pressure) +
      0.10 * (1 - geopolitical_chokepoint_pressure),
      4
    ) AS infrastructure_transformation_opportunity_score
FROM infrastructure_scenarios;

CREATE VIEW infrastructure_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * redundancy_gain +
      0.16 * maintenance_gain +
      0.14 * climate_adaptation_gain +
      0.12 * digital_accountability_gain +
      0.14 * governance_gain +
      0.12 * finance_capacity_gain +
      0.12 * equity_gain +
      0.04 * implementation_capacity,
      4
    ) AS infrastructure_strategy_value_score,
    ROUND(
      0.24 * implementation_capacity +
      0.16 * governance_gain +
      0.14 * finance_capacity_gain +
      0.14 * maintenance_gain +
      0.12 * redundancy_gain +
      0.10 * climate_adaptation_gain +
      0.06 * equity_gain +
      0.04 * digital_accountability_gain,
      4
    ) AS implementation_readiness_score
FROM infrastructure_strategy_options;

CREATE VIEW infrastructure_risk_priority_scores AS
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
    ) AS infrastructure_risk_priority_score,
    distributional_harm,
    preparedness
FROM infrastructure_risk_indicators;

CREATE VIEW infrastructure_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.16 * coordination +
      0.16 * public_finance +
      0.16 * maintenance_capacity +
      0.14 * digital_accountability +
      0.14 * climate_governance +
      0.12 * procurement_integrity +
      0.12 * equity_safeguards,
      4
    ) AS infrastructure_governance_capacity_score,
    ROUND(
      0.16 * (1 - coordination) +
      0.16 * (1 - equity_safeguards) +
      0.14 * (1 - public_finance) +
      0.14 * (1 - maintenance_capacity) +
      0.14 * (1 - digital_accountability) +
      0.13 * (1 - climate_governance) +
      0.13 * (1 - procurement_integrity),
      4
    ) AS legitimacy_gap_score
FROM infrastructure_governance_records;
