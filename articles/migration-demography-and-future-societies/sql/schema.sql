-- Migration, Demography, and Future Societies schema.
-- SQLite compatible.

DROP VIEW IF EXISTS care_urban_capacity_scores;
DROP VIEW IF EXISTS demographic_risk_priority_scores;
DROP VIEW IF EXISTS demographic_strategy_scores;
DROP VIEW IF EXISTS migration_demography_scenario_scores;
DROP VIEW IF EXISTS demographic_profile_scores;

DROP TABLE IF EXISTS adaptive_demographic_pathways;
DROP TABLE IF EXISTS care_urban_records;
DROP TABLE IF EXISTS demographic_risk_indicators;
DROP TABLE IF EXISTS demographic_strategy_options;
DROP TABLE IF EXISTS migration_demography_scenarios;
DROP TABLE IF EXISTS demographic_profiles;

CREATE TABLE demographic_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    population_base INTEGER,
    birth_rate REAL,
    death_rate REAL,
    net_migration_rate REAL,
    aging_pressure REAL,
    youth_opportunity_gap REAL,
    migration_pressure REAL,
    care_capacity REAL,
    housing_pressure REAL,
    labor_adaptation REAL,
    climate_mobility_exposure REAL,
    social_cohesion REAL,
    gender_equity REAL,
    public_health_capacity REAL,
    description TEXT
);

CREATE TABLE migration_demography_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    aging_shock REAL,
    youth_employment_shock REAL,
    housing_shock REAL,
    care_shock REAL,
    climate_mobility_shock REAL,
    border_restriction_pressure REAL,
    labor_shortage_pressure REAL,
    public_health_shock REAL,
    social_cohesion_stress REAL,
    rights_protection_gap REAL,
    description TEXT
);

CREATE TABLE demographic_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    care_investment_gain REAL,
    housing_affordability_gain REAL,
    youth_opportunity_gain REAL,
    legal_mobility_gain REAL,
    labor_protection_gain REAL,
    climate_adaptation_gain REAL,
    reproductive_health_gain REAL,
    gender_equity_gain REAL,
    public_health_gain REAL,
    social_cohesion_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES demographic_profiles(profile_id)
);

CREATE TABLE demographic_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES migration_demography_scenarios(scenario_id)
);

CREATE TABLE care_urban_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    care_workforce_capacity REAL,
    unpaid_care_burden REAL,
    eldercare_demand REAL,
    childcare_demand REAL,
    affordable_housing_supply REAL,
    urban_service_capacity REAL,
    integration_capacity REAL,
    public_health_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES demographic_profiles(profile_id)
);

CREATE TABLE adaptive_demographic_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    population_base INTEGER,
    birth_rate REAL,
    death_rate REAL,
    net_migration_rate REAL,
    aging_pressure REAL,
    youth_opportunity_gap REAL,
    care_capacity REAL,
    housing_pressure REAL,
    labor_adaptation REAL,
    climate_mobility_exposure REAL,
    social_cohesion REAL,
    initial_adaptive_capacity REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES demographic_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES migration_demography_scenarios(scenario_id)
);

CREATE VIEW demographic_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.13 * aging_pressure +
      0.13 * youth_opportunity_gap +
      0.12 * migration_pressure +
      0.13 * (1 - care_capacity) +
      0.12 * housing_pressure +
      0.10 * (1 - labor_adaptation) +
      0.11 * climate_mobility_exposure +
      0.08 * (1 - social_cohesion) +
      0.05 * (1 - gender_equity) +
      0.03 * (1 - public_health_capacity),
      4
    ) AS demographic_stress_score,
    ROUND(
      0.18 * care_capacity +
      0.16 * labor_adaptation +
      0.16 * social_cohesion +
      0.13 * gender_equity +
      0.13 * public_health_capacity +
      0.10 * (1 - housing_pressure) +
      0.08 * (1 - youth_opportunity_gap) +
      0.06 * (1 - climate_mobility_exposure),
      4
    ) AS adaptive_capacity_score
FROM demographic_profiles;

CREATE VIEW migration_demography_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * aging_shock +
      0.12 * youth_employment_shock +
      0.12 * housing_shock +
      0.12 * care_shock +
      0.13 * climate_mobility_shock +
      0.10 * border_restriction_pressure +
      0.09 * labor_shortage_pressure +
      0.08 * public_health_shock +
      0.07 * social_cohesion_stress +
      0.05 * rights_protection_gap,
      4
    ) AS demographic_pressure_score
FROM migration_demography_scenarios;

CREATE VIEW demographic_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * care_investment_gain +
      0.12 * housing_affordability_gain +
      0.12 * youth_opportunity_gain +
      0.12 * legal_mobility_gain +
      0.11 * labor_protection_gain +
      0.10 * climate_adaptation_gain +
      0.09 * reproductive_health_gain +
      0.08 * gender_equity_gain +
      0.07 * public_health_gain +
      0.04 * social_cohesion_gain +
      0.02 * implementation_capacity,
      4
    ) AS demographic_strategy_value_score
FROM demographic_strategy_options;

CREATE VIEW demographic_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.18 * severity +
      0.15 * cascade_potential +
      0.10 * visibility_gap +
      0.13 * recovery_difficulty +
      0.20 * distributional_harm +
      0.10 * (1 - preparedness),
      4
    ) AS demographic_risk_priority_score,
    distributional_harm,
    preparedness
FROM demographic_risk_indicators;

CREATE VIEW care_urban_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    ROUND(
      0.28 * eldercare_demand +
      0.20 * childcare_demand +
      0.20 * unpaid_care_burden +
      0.14 * (1 - care_workforce_capacity) +
      0.10 * (1 - public_health_capacity) +
      0.08 * (1 - integration_capacity),
      4
    ) AS care_stress_score,
    ROUND(
      0.24 * affordable_housing_supply +
      0.20 * urban_service_capacity +
      0.18 * integration_capacity +
      0.16 * public_health_capacity +
      0.14 * care_workforce_capacity +
      0.08 * (1 - unpaid_care_burden),
      4
    ) AS urban_absorption_capacity_score
FROM care_urban_records;
