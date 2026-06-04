-- Health Futures and Public Systems schema.
-- SQLite compatible.

DROP VIEW IF EXISTS health_governance_capacity_scores;
DROP VIEW IF EXISTS health_risk_priority_scores;
DROP VIEW IF EXISTS health_strategy_scores;
DROP VIEW IF EXISTS health_scenario_scores;
DROP VIEW IF EXISTS health_system_profile_scores;

DROP TABLE IF EXISTS health_stress_pathways;
DROP TABLE IF EXISTS health_governance_records;
DROP TABLE IF EXISTS health_risk_indicators;
DROP TABLE IF EXISTS health_strategy_options;
DROP TABLE IF EXISTS health_futures_scenarios;
DROP TABLE IF EXISTS health_system_profiles;

CREATE TABLE health_system_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    prevention_capacity REAL,
    healthcare_access REAL,
    public_health_infrastructure REAL,
    climate_readiness REAL,
    workforce_resilience REAL,
    technology_governance REAL,
    social_protection REAL,
    public_trust REAL,
    equity_capacity REAL,
    care_capacity REAL,
    description TEXT
);

CREATE TABLE health_futures_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    disease_burden_pressure REAL,
    climate_health_pressure REAL,
    biological_risk_pressure REAL,
    workforce_pressure REAL,
    care_pressure REAL,
    chronic_disease_pressure REAL,
    mental_health_pressure REAL,
    technology_governance_pressure REAL,
    trust_pressure REAL,
    equity_pressure REAL,
    description TEXT
);

CREATE TABLE health_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    prevention_gain REAL,
    access_gain REAL,
    public_health_gain REAL,
    climate_health_gain REAL,
    workforce_gain REAL,
    technology_governance_gain REAL,
    social_protection_gain REAL,
    trust_gain REAL,
    equity_gain REAL,
    care_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES health_system_profiles(profile_id)
);

CREATE TABLE health_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES health_futures_scenarios(scenario_id)
);

CREATE TABLE health_governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    monitoring_capacity REAL,
    public_health_finance REAL,
    workforce_capacity REAL,
    community_participation REAL,
    technology_accountability REAL,
    equity_safeguards REAL,
    emergency_coordination REAL,
    care_system_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES health_system_profiles(profile_id)
);

CREATE TABLE health_stress_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    prevention REAL,
    healthcare_access REAL,
    public_health REAL,
    climate_readiness REAL,
    workforce REAL,
    social_protection REAL,
    public_trust REAL,
    equity REAL,
    care_capacity REAL,
    initial_resilience REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES health_system_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES health_futures_scenarios(scenario_id)
);

CREATE VIEW health_system_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.13 * prevention_capacity +
      0.12 * healthcare_access +
      0.15 * public_health_infrastructure +
      0.10 * climate_readiness +
      0.11 * workforce_resilience +
      0.08 * technology_governance +
      0.11 * social_protection +
      0.08 * public_trust +
      0.07 * equity_capacity +
      0.05 * care_capacity,
      4
    ) AS public_health_resilience_score,
    ROUND(
      0.13 * (1 - prevention_capacity) +
      0.12 * (1 - healthcare_access) +
      0.15 * (1 - public_health_infrastructure) +
      0.11 * (1 - climate_readiness) +
      0.13 * (1 - workforce_resilience) +
      0.08 * (1 - technology_governance) +
      0.10 * (1 - social_protection) +
      0.08 * (1 - public_trust) +
      0.06 * (1 - equity_capacity) +
      0.04 * (1 - care_capacity),
      4
    ) AS health_system_fragility_score
FROM health_system_profiles;

CREATE VIEW health_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * disease_burden_pressure +
      0.13 * climate_health_pressure +
      0.13 * biological_risk_pressure +
      0.13 * workforce_pressure +
      0.11 * care_pressure +
      0.11 * chronic_disease_pressure +
      0.10 * mental_health_pressure +
      0.07 * technology_governance_pressure +
      0.05 * trust_pressure +
      0.05 * equity_pressure,
      4
    ) AS health_system_stress_score,
    ROUND(
      0.14 * (1 - disease_burden_pressure) +
      0.13 * (1 - workforce_pressure) +
      0.13 * (1 - climate_health_pressure) +
      0.12 * (1 - biological_risk_pressure) +
      0.12 * (1 - care_pressure) +
      0.10 * (1 - trust_pressure) +
      0.10 * (1 - equity_pressure) +
      0.08 * (1 - chronic_disease_pressure) +
      0.05 * (1 - mental_health_pressure) +
      0.03 * (1 - technology_governance_pressure),
      4
    ) AS health_transformation_opportunity_score
FROM health_futures_scenarios;

CREATE VIEW health_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * prevention_gain +
      0.12 * access_gain +
      0.14 * public_health_gain +
      0.11 * climate_health_gain +
      0.11 * workforce_gain +
      0.08 * technology_governance_gain +
      0.10 * social_protection_gain +
      0.08 * trust_gain +
      0.08 * equity_gain +
      0.04 * care_gain +
      0.01 * implementation_capacity,
      4
    ) AS health_strategy_value_score,
    ROUND(
      0.22 * implementation_capacity +
      0.14 * workforce_gain +
      0.13 * public_health_gain +
      0.12 * trust_gain +
      0.11 * equity_gain +
      0.10 * access_gain +
      0.08 * social_protection_gain +
      0.06 * prevention_gain +
      0.04 * technology_governance_gain,
      4
    ) AS implementation_readiness_score
FROM health_strategy_options;

CREATE VIEW health_risk_priority_scores AS
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
    ) AS health_risk_priority_score,
    distributional_harm,
    preparedness
FROM health_risk_indicators;

CREATE VIEW health_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.15 * monitoring_capacity +
      0.15 * public_health_finance +
      0.14 * workforce_capacity +
      0.13 * community_participation +
      0.11 * technology_accountability +
      0.13 * equity_safeguards +
      0.11 * emergency_coordination +
      0.08 * care_system_capacity,
      4
    ) AS health_governance_capacity_score,
    ROUND(
      0.17 * (1 - community_participation) +
      0.16 * (1 - equity_safeguards) +
      0.14 * (1 - public_health_finance) +
      0.13 * (1 - monitoring_capacity) +
      0.12 * (1 - workforce_capacity) +
      0.10 * (1 - technology_accountability) +
      0.10 * (1 - emergency_coordination) +
      0.08 * (1 - care_system_capacity),
      4
    ) AS legitimacy_gap_score
FROM health_governance_records;
