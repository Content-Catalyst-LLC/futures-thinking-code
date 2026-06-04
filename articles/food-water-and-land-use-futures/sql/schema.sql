-- Food, Water, and Land-Use Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS resource_governance_capacity_scores;
DROP VIEW IF EXISTS resource_risk_priority_scores;
DROP VIEW IF EXISTS adaptation_strategy_scores;
DROP VIEW IF EXISTS resource_scenario_scores;
DROP VIEW IF EXISTS food_water_land_profile_scores;

DROP TABLE IF EXISTS resource_stress_pathways;
DROP TABLE IF EXISTS resource_governance_records;
DROP TABLE IF EXISTS resource_risk_indicators;
DROP TABLE IF EXISTS adaptation_strategy_options;
DROP TABLE IF EXISTS resource_scenarios;
DROP TABLE IF EXISTS food_water_land_profiles;

CREATE TABLE food_water_land_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    production_capacity REAL,
    water_security REAL,
    soil_health REAL,
    biodiversity_integrity REAL,
    governance_capacity REAL,
    climate_exposure REAL,
    market_vulnerability REAL,
    justice_capacity REAL,
    livelihood_resilience REAL,
    description TEXT
);

CREATE TABLE resource_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    food_pressure REAL,
    water_pressure REAL,
    land_pressure REAL,
    soil_degradation_pressure REAL,
    biodiversity_pressure REAL,
    climate_pressure REAL,
    market_pressure REAL,
    governance_fragmentation REAL,
    rights_conflict_pressure REAL,
    description TEXT
);

CREATE TABLE adaptation_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    production_gain REAL,
    water_gain REAL,
    soil_gain REAL,
    biodiversity_gain REAL,
    governance_gain REAL,
    justice_gain REAL,
    livelihood_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES food_water_land_profiles(profile_id)
);

CREATE TABLE resource_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES resource_scenarios(scenario_id)
);

CREATE TABLE resource_governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    land_rights REAL,
    water_governance REAL,
    food_security_institutions REAL,
    soil_monitoring REAL,
    biodiversity_governance REAL,
    participation REAL,
    public_finance REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES food_water_land_profiles(profile_id)
);

CREATE TABLE resource_stress_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    production REAL,
    water_security REAL,
    soil_health REAL,
    biodiversity REAL,
    governance REAL,
    justice REAL,
    livelihood_resilience REAL,
    climate_exposure REAL,
    market_vulnerability REAL,
    initial_resilience REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES food_water_land_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES resource_scenarios(scenario_id)
);

CREATE VIEW food_water_land_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.13 * production_capacity +
      0.16 * water_security +
      0.15 * soil_health +
      0.14 * biodiversity_integrity +
      0.14 * governance_capacity -
      0.12 * climate_exposure -
      0.08 * market_vulnerability +
      0.14 * justice_capacity +
      0.12 * livelihood_resilience,
      4
    ) AS food_water_land_resilience_score,
    ROUND(
      0.16 * climate_exposure +
      0.14 * market_vulnerability +
      0.14 * (1 - water_security) +
      0.13 * (1 - soil_health) +
      0.12 * (1 - biodiversity_integrity) +
      0.12 * (1 - governance_capacity) +
      0.10 * (1 - justice_capacity) +
      0.06 * (1 - livelihood_resilience) +
      0.03 * (1 - production_capacity),
      4
    ) AS food_water_land_fragility_score
FROM food_water_land_profiles;

CREATE VIEW resource_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.13 * food_pressure +
      0.15 * water_pressure +
      0.13 * land_pressure +
      0.13 * soil_degradation_pressure +
      0.12 * biodiversity_pressure +
      0.14 * climate_pressure +
      0.09 * market_pressure +
      0.06 * governance_fragmentation +
      0.05 * rights_conflict_pressure,
      4
    ) AS resource_stress_score,
    ROUND(
      0.15 * (1 - water_pressure) +
      0.15 * (1 - soil_degradation_pressure) +
      0.14 * (1 - biodiversity_pressure) +
      0.14 * (1 - governance_fragmentation) +
      0.12 * (1 - rights_conflict_pressure) +
      0.11 * (1 - food_pressure) +
      0.09 * (1 - climate_pressure) +
      0.06 * (1 - market_pressure) +
      0.04 * (1 - land_pressure),
      4
    ) AS resource_transformation_opportunity_score
FROM resource_scenarios;

CREATE VIEW adaptation_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * production_gain +
      0.16 * water_gain +
      0.16 * soil_gain +
      0.15 * biodiversity_gain +
      0.14 * governance_gain +
      0.15 * justice_gain +
      0.08 * livelihood_gain +
      0.04 * implementation_capacity,
      4
    ) AS resource_strategy_value_score,
    ROUND(
      0.24 * implementation_capacity +
      0.16 * governance_gain +
      0.14 * justice_gain +
      0.12 * water_gain +
      0.12 * soil_gain +
      0.10 * livelihood_gain +
      0.08 * production_gain +
      0.04 * biodiversity_gain,
      4
    ) AS implementation_readiness_score
FROM adaptation_strategy_options;

CREATE VIEW resource_risk_priority_scores AS
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
    ) AS resource_risk_priority_score,
    distributional_harm,
    preparedness
FROM resource_risk_indicators;

CREATE VIEW resource_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.15 * land_rights +
      0.17 * water_governance +
      0.15 * food_security_institutions +
      0.13 * soil_monitoring +
      0.14 * biodiversity_governance +
      0.14 * participation +
      0.12 * public_finance,
      4
    ) AS resource_governance_capacity_score,
    ROUND(
      0.18 * (1 - participation) +
      0.17 * (1 - land_rights) +
      0.15 * (1 - water_governance) +
      0.14 * (1 - food_security_institutions) +
      0.13 * (1 - biodiversity_governance) +
      0.12 * (1 - public_finance) +
      0.11 * (1 - soil_monitoring),
      4
    ) AS legitimacy_gap_score
FROM resource_governance_records;
