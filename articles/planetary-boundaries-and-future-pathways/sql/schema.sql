-- Planetary Boundaries and Future Pathways schema.
-- SQLite compatible.

DROP VIEW IF EXISTS planetary_governance_capacity_scores;
DROP VIEW IF EXISTS planetary_risk_priority_scores;
DROP VIEW IF EXISTS pathway_strategy_scores;
DROP VIEW IF EXISTS boundary_scenario_scores;
DROP VIEW IF EXISTS planetary_pathway_scores;

DROP TABLE IF EXISTS planetary_pathway_simulations;
DROP TABLE IF EXISTS planetary_governance_records;
DROP TABLE IF EXISTS planetary_risk_indicators;
DROP TABLE IF EXISTS pathway_strategy_options;
DROP TABLE IF EXISTS boundary_scenarios;
DROP TABLE IF EXISTS planetary_pathway_profiles;

CREATE TABLE planetary_pathway_profiles (
    pathway_id TEXT PRIMARY KEY,
    pathway_name TEXT NOT NULL,
    pathway_type TEXT,
    climate_pressure REAL,
    biosphere_pressure REAL,
    land_pressure REAL,
    freshwater_pressure REAL,
    nutrient_pressure REAL,
    ocean_pressure REAL,
    aerosol_pressure REAL,
    novel_entity_pressure REAL,
    social_foundation_security REAL,
    governance_capacity REAL,
    justice_capacity REAL,
    technology_dependence REAL,
    regeneration_capacity REAL,
    description TEXT
);

CREATE TABLE boundary_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    climate_stress REAL,
    biosphere_stress REAL,
    land_stress REAL,
    freshwater_stress REAL,
    nutrient_stress REAL,
    ocean_stress REAL,
    aerosol_stress REAL,
    novel_entity_stress REAL,
    social_stress REAL,
    governance_fragmentation REAL,
    description TEXT
);

CREATE TABLE pathway_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    climate_reduction REAL,
    biosphere_recovery REAL,
    land_restoration REAL,
    water_security REAL,
    nutrient_circularity REAL,
    novel_entity_control REAL,
    social_foundation_gain REAL,
    governance_gain REAL,
    justice_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(pathway_id) REFERENCES planetary_pathway_profiles(pathway_id)
);

CREATE TABLE planetary_risk_indicators (
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
    FOREIGN KEY(scenario_id) REFERENCES boundary_scenarios(scenario_id)
);

CREATE TABLE planetary_governance_records (
    record_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    record_name TEXT,
    record_type TEXT,
    monitoring_capacity REAL,
    policy_coordination REAL,
    public_finance REAL,
    participation REAL,
    justice_safeguards REAL,
    international_cooperation REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(pathway_id) REFERENCES planetary_pathway_profiles(pathway_id)
);

CREATE TABLE planetary_pathway_simulations (
    simulation_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    scenario_id TEXT,
    simulation_name TEXT,
    boundary_pressure REAL,
    social_foundations REAL,
    governance REAL,
    justice REAL,
    technology_dependence REAL,
    regeneration REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(pathway_id) REFERENCES planetary_pathway_profiles(pathway_id),
    FOREIGN KEY(scenario_id) REFERENCES boundary_scenarios(scenario_id)
);

CREATE VIEW planetary_pathway_scores AS
SELECT
    pathway_id,
    pathway_name,
    pathway_type,
    ROUND(
      0.16 * climate_pressure +
      0.16 * biosphere_pressure +
      0.12 * land_pressure +
      0.12 * freshwater_pressure +
      0.10 * nutrient_pressure +
      0.10 * ocean_pressure +
      0.08 * aerosol_pressure +
      0.10 * novel_entity_pressure +
      0.06 * technology_dependence,
      4
    ) AS total_boundary_pressure_score,
    ROUND(
      0.22 * social_foundation_security +
      0.20 * governance_capacity +
      0.20 * justice_capacity +
      0.14 * regeneration_capacity -
      0.20 * (
        0.16 * climate_pressure +
        0.16 * biosphere_pressure +
        0.12 * land_pressure +
        0.12 * freshwater_pressure +
        0.10 * nutrient_pressure +
        0.10 * ocean_pressure +
        0.08 * aerosol_pressure +
        0.10 * novel_entity_pressure +
        0.06 * technology_dependence
      ) +
      0.04 * (1 - technology_dependence),
      4
    ) AS safe_and_just_pathway_score
FROM planetary_pathway_profiles;

CREATE VIEW boundary_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * climate_stress +
      0.16 * biosphere_stress +
      0.12 * land_stress +
      0.12 * freshwater_stress +
      0.10 * nutrient_stress +
      0.10 * ocean_stress +
      0.08 * aerosol_stress +
      0.10 * novel_entity_stress +
      0.08 * social_stress +
      0.08 * governance_fragmentation,
      4
    ) AS planetary_stress_score,
    ROUND(
      0.16 * (1 - climate_stress) +
      0.16 * (1 - biosphere_stress) +
      0.12 * (1 - freshwater_stress) +
      0.12 * (1 - land_stress) +
      0.10 * (1 - nutrient_stress) +
      0.10 * (1 - novel_entity_stress) +
      0.10 * (1 - social_stress) +
      0.10 * (1 - governance_fragmentation) +
      0.04 * (1 - ocean_stress) +
      0.02 * (1 - aerosol_stress),
      4
    ) AS transformation_opportunity_score
FROM boundary_scenarios;

CREATE VIEW pathway_strategy_scores AS
SELECT
    strategy_id,
    pathway_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.14 * climate_reduction +
      0.14 * biosphere_recovery +
      0.11 * land_restoration +
      0.11 * water_security +
      0.09 * nutrient_circularity +
      0.09 * novel_entity_control +
      0.12 * social_foundation_gain +
      0.10 * governance_gain +
      0.08 * justice_gain +
      0.02 * implementation_capacity,
      4
    ) AS pathway_strategy_value_score,
    ROUND(
      0.24 * implementation_capacity +
      0.17 * governance_gain +
      0.15 * justice_gain +
      0.13 * social_foundation_gain +
      0.10 * climate_reduction +
      0.08 * biosphere_recovery +
      0.06 * water_security +
      0.04 * land_restoration +
      0.03 * novel_entity_control,
      4
    ) AS implementation_readiness_score
FROM pathway_strategy_options;

CREATE VIEW planetary_risk_priority_scores AS
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
    ) AS planetary_risk_priority_score,
    distributional_harm,
    preparedness
FROM planetary_risk_indicators;

CREATE VIEW planetary_governance_capacity_scores AS
SELECT
    record_id,
    pathway_id,
    record_name,
    record_type,
    ROUND(
      0.16 * monitoring_capacity +
      0.17 * policy_coordination +
      0.15 * public_finance +
      0.14 * participation +
      0.15 * justice_safeguards +
      0.12 * international_cooperation +
      0.11 * implementation_capacity,
      4
    ) AS planetary_governance_capacity_score,
    ROUND(
      0.18 * (1 - participation) +
      0.17 * (1 - justice_safeguards) +
      0.15 * (1 - policy_coordination) +
      0.14 * (1 - public_finance) +
      0.13 * (1 - monitoring_capacity) +
      0.12 * (1 - implementation_capacity) +
      0.11 * (1 - international_cooperation),
      4
    ) AS legitimacy_gap_score
FROM planetary_governance_records;
