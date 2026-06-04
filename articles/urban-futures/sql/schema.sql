-- Urban Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS urban_governance_capacity_scores;
DROP VIEW IF EXISTS urban_risk_priority_scores;
DROP VIEW IF EXISTS urban_strategy_scores;
DROP VIEW IF EXISTS urban_scenario_scores;
DROP VIEW IF EXISTS urban_profile_scores;

DROP TABLE IF EXISTS urban_stress_pathways;
DROP TABLE IF EXISTS urban_governance_records;
DROP TABLE IF EXISTS urban_risk_indicators;
DROP TABLE IF EXISTS urban_strategy_options;
DROP TABLE IF EXISTS urban_scenarios;
DROP TABLE IF EXISTS urban_system_profiles;

CREATE TABLE urban_system_profiles (
    profile_id TEXT PRIMARY KEY,
    city_future_name TEXT NOT NULL,
    city_type TEXT,
    infrastructure_strength REAL,
    governance_capacity REAL,
    housing_affordability REAL,
    climate_exposure REAL,
    inequality REAL,
    digital_integration REAL,
    public_finance_capacity REAL,
    social_cohesion REAL,
    maintenance_backlog REAL,
    description TEXT
);

CREATE TABLE urban_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    infrastructure_stress REAL,
    housing_pressure REAL,
    climate_pressure REAL,
    fiscal_pressure REAL,
    digital_dependency REAL,
    migration_pressure REAL,
    governance_fragmentation REAL,
    social_fragmentation REAL,
    description TEXT
);

CREATE TABLE urban_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    infrastructure_gain REAL,
    housing_stability_gain REAL,
    climate_resilience_gain REAL,
    governance_gain REAL,
    finance_gain REAL,
    digital_accountability_gain REAL,
    social_cohesion_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES urban_system_profiles(profile_id)
);

CREATE TABLE urban_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES urban_scenarios(scenario_id)
);

CREATE TABLE urban_governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    coordination REAL,
    participation REAL,
    public_finance REAL,
    maintenance_capacity REAL,
    digital_accountability REAL,
    housing_governance REAL,
    climate_governance REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES urban_system_profiles(profile_id)
);

CREATE TABLE urban_stress_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    infrastructure REAL,
    governance REAL,
    housing_stability REAL,
    public_finance REAL,
    social_cohesion REAL,
    climate_exposure REAL,
    digital_dependency REAL,
    maintenance_backlog REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES urban_system_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES urban_scenarios(scenario_id)
);

CREATE VIEW urban_profile_scores AS
SELECT
    profile_id,
    city_future_name,
    city_type,
    ROUND(
      0.17 * infrastructure_strength +
      0.16 * governance_capacity +
      0.14 * housing_affordability -
      0.14 * climate_exposure -
      0.14 * inequality +
      0.09 * digital_integration +
      0.12 * public_finance_capacity +
      0.14 * social_cohesion -
      0.08 * maintenance_backlog,
      4
    ) AS urban_viability_score,
    ROUND(
      0.15 * climate_exposure +
      0.15 * inequality +
      0.14 * maintenance_backlog +
      0.13 * (1 - infrastructure_strength) +
      0.13 * (1 - governance_capacity) +
      0.12 * (1 - housing_affordability) +
      0.10 * (1 - public_finance_capacity) +
      0.10 * (1 - social_cohesion) +
      0.08 * digital_integration,
      4
    ) AS urban_fragility_score
FROM urban_system_profiles;

CREATE VIEW urban_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.15 * infrastructure_stress +
      0.16 * housing_pressure +
      0.15 * climate_pressure +
      0.12 * fiscal_pressure +
      0.10 * digital_dependency +
      0.10 * migration_pressure +
      0.12 * governance_fragmentation +
      0.10 * social_fragmentation,
      4
    ) AS urban_stress_score,
    ROUND(
      0.18 * (1 - governance_fragmentation) +
      0.16 * (1 - fiscal_pressure) +
      0.14 * (1 - infrastructure_stress) +
      0.14 * (1 - housing_pressure) +
      0.12 * (1 - climate_pressure) +
      0.10 * (1 - social_fragmentation) +
      0.08 * (1 - migration_pressure) +
      0.08 * (1 - digital_dependency),
      4
    ) AS urban_transformation_opportunity_score
FROM urban_scenarios;

CREATE VIEW urban_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * infrastructure_gain +
      0.16 * housing_stability_gain +
      0.14 * climate_resilience_gain +
      0.14 * governance_gain +
      0.12 * finance_gain +
      0.10 * digital_accountability_gain +
      0.14 * social_cohesion_gain +
      0.04 * implementation_capacity,
      4
    ) AS urban_strategy_value_score,
    ROUND(
      0.24 * implementation_capacity +
      0.16 * governance_gain +
      0.14 * finance_gain +
      0.14 * infrastructure_gain +
      0.12 * housing_stability_gain +
      0.10 * climate_resilience_gain +
      0.06 * social_cohesion_gain +
      0.04 * digital_accountability_gain,
      4
    ) AS implementation_readiness_score
FROM urban_strategy_options;

CREATE VIEW urban_risk_priority_scores AS
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
    ) AS urban_risk_priority_score,
    distributional_harm,
    preparedness
FROM urban_risk_indicators;

CREATE VIEW urban_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.16 * coordination +
      0.14 * participation +
      0.14 * public_finance +
      0.14 * maintenance_capacity +
      0.12 * digital_accountability +
      0.15 * housing_governance +
      0.15 * climate_governance,
      4
    ) AS urban_governance_capacity_score,
    ROUND(
      0.16 * (1 - participation) +
      0.16 * (1 - coordination) +
      0.14 * (1 - housing_governance) +
      0.14 * (1 - climate_governance) +
      0.14 * (1 - public_finance) +
      0.12 * (1 - maintenance_capacity) +
      0.14 * (1 - digital_accountability),
      4
    ) AS legitimacy_gap_score
FROM urban_governance_records;
