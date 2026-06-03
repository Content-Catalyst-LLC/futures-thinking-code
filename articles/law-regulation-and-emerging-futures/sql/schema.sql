-- Law, Regulation, and Emerging Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS regulatory_scenario_scores;
DROP VIEW IF EXISTS sandbox_safeguard_scores;
DROP VIEW IF EXISTS rights_remedy_scores;
DROP VIEW IF EXISTS emerging_risk_scores;
DROP VIEW IF EXISTS regulatory_model_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS adaptive_regulatory_pathways;
DROP TABLE IF EXISTS regulatory_scenarios;
DROP TABLE IF EXISTS sandbox_governance;
DROP TABLE IF EXISTS rights_remedy_register;
DROP TABLE IF EXISTS emerging_risk_register;
DROP TABLE IF EXISTS regulatory_models;

CREATE TABLE regulatory_models (
    model_id TEXT PRIMARY KEY,
    regulatory_model TEXT NOT NULL,
    model_type TEXT,
    foresight_capacity REAL,
    monitoring_capacity REAL,
    enforcement_capacity REAL,
    rights_protection REAL,
    public_participation REAL,
    revision_authority REAL,
    regulatory_learning REAL,
    capture_resistance REAL,
    legal_certainty REAL,
    remedy_access REAL,
    description TEXT
);

CREATE TABLE emerging_risk_register (
    risk_id TEXT PRIMARY KEY,
    model_id TEXT,
    risk_name TEXT NOT NULL,
    risk_domain TEXT,
    change_velocity REAL,
    harm_severity REAL,
    uncertainty REAL,
    irreversibility REAL,
    distributional_exposure REAL,
    regulatory_gap REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(model_id) REFERENCES regulatory_models(model_id)
);

CREATE TABLE rights_remedy_register (
    remedy_id TEXT PRIMARY KEY,
    model_id TEXT,
    rights_domain TEXT,
    notice REAL,
    explanation REAL,
    appeal REAL,
    audit_access REAL,
    public_enforcement REAL,
    collective_remedy REAL,
    compensation REAL,
    accessibility REAL,
    description TEXT,
    FOREIGN KEY(model_id) REFERENCES regulatory_models(model_id)
);

CREATE TABLE sandbox_governance (
    sandbox_id TEXT PRIMARY KEY,
    model_id TEXT,
    sandbox_name TEXT,
    public_interest_test REAL,
    eligibility_transparency REAL,
    rights_nonwaiver REAL,
    participant_consent REAL,
    independent_evaluation REAL,
    exit_conditions REAL,
    public_reporting REAL,
    capture_control REAL,
    description TEXT,
    FOREIGN KEY(model_id) REFERENCES regulatory_models(model_id)
);

CREATE TABLE regulatory_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    technology_acceleration REAL,
    climate_stress REAL,
    public_trust REAL,
    institutional_capacity REAL,
    capture_pressure REAL,
    rights_risk REAL,
    international_fragmentation REAL,
    learning_capacity REAL,
    description TEXT
);

CREATE TABLE adaptive_regulatory_pathways (
    pathway_id TEXT PRIMARY KEY,
    model_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    foresight REAL,
    monitoring REAL,
    enforcement REAL,
    rights REAL,
    participation REAL,
    revision REAL,
    learning REAL,
    capture_resistance REAL,
    initial_trust REAL,
    time_horizon INTEGER,
    FOREIGN KEY(model_id) REFERENCES regulatory_models(model_id),
    FOREIGN KEY(scenario_id) REFERENCES regulatory_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    foresight_capacity REAL,
    monitoring_design REAL,
    rights_safeguards REAL,
    public_participation REAL,
    revision_triggers REAL,
    enforcement_capacity REAL,
    remedy_access REAL,
    capture_resistance REAL,
    legal_certainty REAL,
    description TEXT
);

CREATE VIEW regulatory_model_scores AS
SELECT
    model_id,
    regulatory_model,
    model_type,
    ROUND(
      0.13 * foresight_capacity +
      0.12 * monitoring_capacity +
      0.12 * enforcement_capacity +
      0.14 * rights_protection +
      0.10 * public_participation +
      0.12 * revision_authority +
      0.10 * regulatory_learning +
      0.08 * capture_resistance +
      0.05 * legal_certainty +
      0.04 * remedy_access,
      4
    ) AS future_ready_regulatory_capacity_score,
    ROUND(
      0.16 * (1 - foresight_capacity) +
      0.14 * (1 - monitoring_capacity) +
      0.14 * (1 - revision_authority) +
      0.12 * (1 - regulatory_learning) +
      0.12 * (1 - enforcement_capacity) +
      0.10 * (1 - rights_protection) +
      0.08 * (1 - public_participation) +
      0.08 * (1 - capture_resistance) +
      0.06 * (1 - remedy_access),
      4
    ) AS regulatory_lag_pressure_score
FROM regulatory_models;

CREATE VIEW emerging_risk_scores AS
SELECT
    risk_id,
    model_id,
    risk_name,
    risk_domain,
    ROUND(
      0.16 * change_velocity +
      0.18 * harm_severity +
      0.13 * uncertainty +
      0.15 * irreversibility +
      0.15 * distributional_exposure +
      0.15 * regulatory_gap +
      0.08 * (1 - mitigation_capacity),
      4
    ) AS emerging_regulatory_risk_score,
    mitigation_capacity
FROM emerging_risk_register;

CREATE VIEW rights_remedy_scores AS
SELECT
    remedy_id,
    model_id,
    rights_domain,
    ROUND(
      0.14 * notice +
      0.14 * explanation +
      0.15 * appeal +
      0.15 * audit_access +
      0.14 * public_enforcement +
      0.12 * collective_remedy +
      0.08 * compensation +
      0.08 * accessibility,
      4
    ) AS rights_remedy_strength_score,
    appeal,
    audit_access,
    accessibility
FROM rights_remedy_register;

CREATE VIEW sandbox_safeguard_scores AS
SELECT
    sandbox_id,
    model_id,
    sandbox_name,
    ROUND(
      0.14 * public_interest_test +
      0.12 * eligibility_transparency +
      0.16 * rights_nonwaiver +
      0.12 * participant_consent +
      0.14 * independent_evaluation +
      0.12 * exit_conditions +
      0.10 * public_reporting +
      0.10 * capture_control,
      4
    ) AS sandbox_safeguard_score,
    ROUND(
      1 - (
        0.25 * capture_control +
        0.20 * public_reporting +
        0.20 * independent_evaluation +
        0.20 * eligibility_transparency +
        0.15 * public_interest_test
      ),
      4
    ) AS sandbox_capture_risk_score
FROM sandbox_governance;

CREATE VIEW regulatory_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * technology_acceleration +
      0.16 * climate_stress +
      0.14 * (1 - public_trust) +
      0.12 * (1 - institutional_capacity) +
      0.14 * capture_pressure +
      0.14 * rights_risk +
      0.08 * international_fragmentation +
      0.06 * (1 - learning_capacity),
      4
    ) AS regulatory_future_stress_score,
    ROUND(
      0.22 * institutional_capacity +
      0.20 * learning_capacity +
      0.18 * public_trust +
      0.12 * (1 - capture_pressure) +
      0.12 * (1 - rights_risk) +
      0.08 * (1 - international_fragmentation) +
      0.08 * (1 - climate_stress),
      4
    ) AS future_ready_regulatory_opportunity_score
FROM regulatory_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * foresight_capacity +
      0.12 * monitoring_design +
      0.14 * rights_safeguards +
      0.11 * public_participation +
      0.13 * revision_triggers +
      0.12 * enforcement_capacity +
      0.10 * remedy_access +
      0.10 * capture_resistance +
      0.05 * legal_certainty,
      4
    ) AS future_ready_regulatory_strategy_score,
    ROUND(
      0.18 * rights_safeguards +
      0.16 * remedy_access +
      0.16 * enforcement_capacity +
      0.14 * capture_resistance +
      0.12 * public_participation +
      0.10 * monitoring_design +
      0.08 * revision_triggers +
      0.06 * legal_certainty,
      4
    ) AS rights_accountability_strategy_score
FROM strategy_options;
