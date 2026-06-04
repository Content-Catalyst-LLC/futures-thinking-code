-- Climate Futures and Environmental Change schema.
-- SQLite compatible.

DROP VIEW IF EXISTS climate_governance_capacity_scores;
DROP VIEW IF EXISTS climate_risk_priority_scores;
DROP VIEW IF EXISTS mitigation_adaptation_strategy_scores;
DROP VIEW IF EXISTS climate_scenario_scores;
DROP VIEW IF EXISTS climate_profile_scores;

DROP TABLE IF EXISTS climate_pathways;
DROP TABLE IF EXISTS climate_governance_records;
DROP TABLE IF EXISTS climate_risk_indicators;
DROP TABLE IF EXISTS mitigation_adaptation_strategies;
DROP TABLE IF EXISTS climate_scenarios;
DROP TABLE IF EXISTS climate_future_profiles;

CREATE TABLE climate_future_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    emissions_intensity REAL,
    adaptation_capacity REAL,
    ecosystem_stress REAL,
    governance_coordination REAL,
    social_vulnerability REAL,
    technology_deployment REAL,
    transition_speed REAL,
    justice_capacity REAL,
    residual_loss REAL,
    description TEXT
);

CREATE TABLE climate_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    emissions_pressure REAL,
    feedback_pressure REAL,
    physical_hazard_pressure REAL,
    ecological_degradation REAL,
    social_vulnerability_pressure REAL,
    transition_momentum REAL,
    governance_fragmentation REAL,
    adaptation_finance_gap REAL,
    description TEXT
);

CREATE TABLE mitigation_adaptation_strategies (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    mitigation_effect REAL,
    adaptation_gain REAL,
    vulnerability_reduction REAL,
    ecosystem_protection REAL,
    governance_gain REAL,
    finance_capacity REAL,
    justice_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES climate_future_profiles(profile_id)
);

CREATE TABLE climate_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    systemic_reach REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES climate_scenarios(scenario_id)
);

CREATE TABLE climate_governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    mitigation_governance REAL,
    adaptation_governance REAL,
    public_finance REAL,
    monitoring_capacity REAL,
    coordination REAL,
    participation REAL,
    justice_safeguards REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES climate_future_profiles(profile_id)
);

CREATE TABLE climate_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    emissions REAL,
    sink_strength REAL,
    feedback_pressure REAL,
    adaptation REAL,
    vulnerability_reduction REAL,
    governance_capacity REAL,
    justice_capacity REAL,
    initial_climate_stress REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES climate_future_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES climate_scenarios(scenario_id)
);

CREATE VIEW climate_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      -0.16 * emissions_intensity +
       0.15 * adaptation_capacity -
       0.15 * ecosystem_stress +
       0.14 * governance_coordination -
       0.12 * social_vulnerability +
       0.10 * technology_deployment +
       0.14 * transition_speed +
       0.12 * justice_capacity -
       0.10 * residual_loss,
      4
    ) AS climate_readiness_score,
    ROUND(
      0.16 * emissions_intensity +
      0.15 * ecosystem_stress +
      0.14 * social_vulnerability +
      0.13 * residual_loss +
      0.12 * (1 - adaptation_capacity) +
      0.12 * (1 - governance_coordination) +
      0.10 * (1 - transition_speed) +
      0.08 * (1 - justice_capacity),
      4
    ) AS climate_fragility_score
FROM climate_future_profiles;

CREATE VIEW climate_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.15 * emissions_pressure +
      0.15 * feedback_pressure +
      0.15 * physical_hazard_pressure +
      0.13 * ecological_degradation +
      0.14 * social_vulnerability_pressure +
      0.12 * governance_fragmentation +
      0.10 * adaptation_finance_gap +
      0.06 * (1 - transition_momentum),
      4
    ) AS climate_stress_score,
    ROUND(
      0.22 * transition_momentum +
      0.14 * (1 - emissions_pressure) +
      0.12 * (1 - governance_fragmentation) +
      0.12 * (1 - adaptation_finance_gap) +
      0.12 * (1 - social_vulnerability_pressure) +
      0.10 * (1 - ecological_degradation) +
      0.09 * (1 - feedback_pressure) +
      0.09 * (1 - physical_hazard_pressure),
      4
    ) AS transition_opportunity_score
FROM climate_scenarios;

CREATE VIEW mitigation_adaptation_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.17 * mitigation_effect +
      0.16 * adaptation_gain +
      0.15 * vulnerability_reduction +
      0.14 * ecosystem_protection +
      0.13 * governance_gain +
      0.11 * finance_capacity +
      0.10 * justice_gain +
      0.04 * implementation_capacity,
      4
    ) AS climate_strategy_value_score,
    ROUND(
      0.24 * implementation_capacity +
      0.14 * governance_gain +
      0.14 * finance_capacity +
      0.12 * adaptation_gain +
      0.12 * mitigation_effect +
      0.10 * vulnerability_reduction +
      0.08 * justice_gain +
      0.06 * ecosystem_protection,
      4
    ) AS implementation_readiness_score
FROM mitigation_adaptation_strategies;

CREATE VIEW climate_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.18 * severity +
      0.17 * irreversibility +
      0.16 * systemic_reach +
      0.12 * visibility_gap +
      0.15 * distributional_harm +
      0.08 * (1 - preparedness),
      4
    ) AS climate_risk_priority_score,
    distributional_harm,
    preparedness
FROM climate_risk_indicators;

CREATE VIEW climate_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.16 * mitigation_governance +
      0.16 * adaptation_governance +
      0.14 * public_finance +
      0.14 * monitoring_capacity +
      0.16 * coordination +
      0.10 * participation +
      0.14 * justice_safeguards,
      4
    ) AS climate_governance_capacity_score,
    ROUND(
      0.18 * (1 - participation) +
      0.18 * (1 - justice_safeguards) +
      0.14 * (1 - adaptation_governance) +
      0.14 * (1 - coordination) +
      0.12 * (1 - public_finance) +
      0.12 * (1 - mitigation_governance) +
      0.12 * (1 - monitoring_capacity),
      4
    ) AS legitimacy_gap_score
FROM climate_governance_records;
