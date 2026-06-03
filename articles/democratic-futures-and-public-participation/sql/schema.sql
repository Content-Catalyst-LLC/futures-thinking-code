-- Democratic Futures and Public Participation schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS future_scenario_scores;
DROP VIEW IF EXISTS decision_uptake_scores;
DROP VIEW IF EXISTS representation_quality_scores;
DROP VIEW IF EXISTS participation_model_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS democratic_pathways;
DROP TABLE IF EXISTS future_scenarios;
DROP TABLE IF EXISTS decision_uptake_register;
DROP TABLE IF EXISTS representation_profiles;
DROP TABLE IF EXISTS participation_models;

CREATE TABLE participation_models (
    model_id TEXT PRIMARY KEY,
    participation_model TEXT NOT NULL,
    participation_type TEXT,
    inclusion REAL,
    deliberative_quality REAL,
    representation REAL,
    institutional_uptake REAL,
    accountability REAL,
    justice_safeguards REAL,
    public_learning REAL,
    decision_influence REAL,
    accessibility REAL,
    community_authority REAL,
    description TEXT
);

CREATE TABLE representation_profiles (
    representation_id TEXT PRIMARY KEY,
    model_id TEXT,
    group_name TEXT NOT NULL,
    affectedness REAL,
    representation_quality REAL,
    barrier_reduction REAL,
    compensation REAL,
    decision_access REAL,
    trust_condition REAL,
    knowledge_recognition REAL,
    description TEXT,
    FOREIGN KEY(model_id) REFERENCES participation_models(model_id)
);

CREATE TABLE decision_uptake_register (
    uptake_id TEXT PRIMARY KEY,
    model_id TEXT,
    decision_area TEXT,
    response_duty REAL,
    budget_connection REAL,
    policy_influence REAL,
    regulatory_influence REAL,
    implementation_tracking REAL,
    public_reporting REAL,
    remedy_access REAL,
    description TEXT,
    FOREIGN KEY(model_id) REFERENCES participation_models(model_id)
);

CREATE TABLE future_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    public_trust REAL,
    participation_quality REAL,
    institutional_responsiveness REAL,
    inequality_pressure REAL,
    platform_power REAL,
    climate_stress REAL,
    democratic_polarization REAL,
    civic_capacity REAL,
    description TEXT
);

CREATE TABLE democratic_pathways (
    pathway_id TEXT PRIMARY KEY,
    model_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    inclusion REAL,
    deliberation REAL,
    representation REAL,
    uptake REAL,
    accountability REAL,
    justice REAL,
    learning REAL,
    authority REAL,
    initial_trust REAL,
    time_horizon INTEGER,
    FOREIGN KEY(model_id) REFERENCES participation_models(model_id),
    FOREIGN KEY(scenario_id) REFERENCES future_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    inclusion_design REAL,
    deliberative_design REAL,
    representation_quality REAL,
    response_duty REAL,
    budget_link REAL,
    accountability_tracking REAL,
    justice_safeguards REAL,
    remedy_access REAL,
    public_learning REAL,
    description TEXT
);

CREATE VIEW participation_model_scores AS
SELECT
    model_id,
    participation_model,
    participation_type,
    ROUND(
      0.11 * inclusion +
      0.12 * deliberative_quality +
      0.11 * representation +
      0.14 * institutional_uptake +
      0.12 * accountability +
      0.12 * justice_safeguards +
      0.08 * public_learning +
      0.10 * decision_influence +
      0.05 * accessibility +
      0.05 * community_authority,
      4
    ) AS democratic_futures_capacity_score,
    ROUND(
      0.18 * (1 - institutional_uptake) +
      0.16 * (1 - decision_influence) +
      0.14 * (1 - accountability) +
      0.14 * (1 - community_authority) +
      0.12 * (1 - justice_safeguards) +
      0.10 * (1 - representation) +
      0.08 * (1 - deliberative_quality) +
      0.08 * (1 - inclusion),
      4
    ) AS tokenism_risk_score
FROM participation_models;

CREATE VIEW representation_quality_scores AS
SELECT
    representation_id,
    model_id,
    group_name,
    ROUND(
      0.20 * affectedness +
      0.20 * representation_quality +
      0.16 * barrier_reduction +
      0.12 * compensation +
      0.14 * decision_access +
      0.08 * trust_condition +
      0.10 * knowledge_recognition,
      4
    ) AS representation_quality_score,
    decision_access,
    knowledge_recognition
FROM representation_profiles;

CREATE VIEW decision_uptake_scores AS
SELECT
    uptake_id,
    model_id,
    decision_area,
    ROUND(
      0.18 * response_duty +
      0.16 * budget_connection +
      0.16 * policy_influence +
      0.14 * regulatory_influence +
      0.14 * implementation_tracking +
      0.12 * public_reporting +
      0.10 * remedy_access,
      4
    ) AS decision_uptake_score,
    budget_connection,
    remedy_access
FROM decision_uptake_register;

CREATE VIEW future_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * (1 - public_trust) +
      0.14 * (1 - participation_quality) +
      0.14 * (1 - institutional_responsiveness) +
      0.14 * inequality_pressure +
      0.12 * platform_power +
      0.12 * climate_stress +
      0.12 * democratic_polarization +
      0.06 * (1 - civic_capacity),
      4
    ) AS democratic_stress_pressure_score,
    ROUND(
      0.20 * public_trust +
      0.20 * participation_quality +
      0.18 * institutional_responsiveness +
      0.16 * civic_capacity +
      0.10 * (1 - democratic_polarization) +
      0.08 * (1 - inequality_pressure) +
      0.08 * (1 - platform_power),
      4
    ) AS democratic_futures_opportunity_score
FROM future_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * inclusion_design +
      0.12 * deliberative_design +
      0.12 * representation_quality +
      0.14 * response_duty +
      0.12 * budget_link +
      0.12 * accountability_tracking +
      0.12 * justice_safeguards +
      0.08 * remedy_access +
      0.06 * public_learning,
      4
    ) AS democratic_futures_strategy_score,
    ROUND(
      0.18 * response_duty +
      0.18 * budget_link +
      0.16 * accountability_tracking +
      0.14 * remedy_access +
      0.12 * justice_safeguards +
      0.10 * representation_quality +
      0.08 * deliberative_design +
      0.04 * public_learning,
      4
    ) AS decision_influence_strategy_score
FROM strategy_options;
