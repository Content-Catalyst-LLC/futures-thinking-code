-- Colonial Futures and Contested Imagination schema.
-- SQLite compatible.

DROP VIEW IF EXISTS extraction_voice_scores;
DROP VIEW IF EXISTS coloniality_risk_priority_scores;
DROP VIEW IF EXISTS reparative_strategy_scores;
DROP VIEW IF EXISTS colonial_future_scenario_scores;
DROP VIEW IF EXISTS colonial_future_profile_scores;

DROP TABLE IF EXISTS adaptive_colonial_future_pathways;
DROP TABLE IF EXISTS extraction_voice_records;
DROP TABLE IF EXISTS coloniality_risk_indicators;
DROP TABLE IF EXISTS reparative_strategy_options;
DROP TABLE IF EXISTS colonial_future_scenarios;
DROP TABLE IF EXISTS colonial_future_profiles;

CREATE TABLE colonial_future_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    agenda_setting_power REAL,
    consent_quality REAL,
    land_exposure REAL,
    external_control REAL,
    epistemic_justice REAL,
    local_benefit REAL,
    ecological_harm REAL,
    reparative_capacity REAL,
    sovereignty_recognition REAL,
    data_sovereignty REAL,
    labor_protection REAL,
    description TEXT
);

CREATE TABLE colonial_future_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    extraction_pressure REAL,
    external_control_pressure REAL,
    consent_gap REAL,
    land_risk REAL,
    knowledge_erasure REAL,
    data_extraction REAL,
    security_drift REAL,
    ecological_harm REAL,
    reparative_opening REAL,
    community_voice REAL,
    description TEXT
);

CREATE TABLE reparative_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    land_return_gain REAL,
    consent_quality_gain REAL,
    community_ownership_gain REAL,
    epistemic_justice_gain REAL,
    data_sovereignty_gain REAL,
    labor_rights_gain REAL,
    ecological_restoration_gain REAL,
    reparative_finance_gain REAL,
    accountability_gain REAL,
    implementation_capacity REAL,
    legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES colonial_future_profiles(profile_id)
);

CREATE TABLE coloniality_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    rights_risk REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES colonial_future_scenarios(scenario_id)
);

CREATE TABLE extraction_voice_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    extraction_burden REAL,
    community_voice REAL,
    external_control REAL,
    ecological_harm REAL,
    local_benefit REAL,
    reparative_capacity REAL,
    consent_quality REAL,
    sovereignty_recognition REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES colonial_future_profiles(profile_id)
);

CREATE TABLE adaptive_colonial_future_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    extraction_burden REAL,
    community_voice REAL,
    external_control REAL,
    ecological_harm REAL,
    local_benefit REAL,
    reparative_capacity REAL,
    consent_quality REAL,
    sovereignty_recognition REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES colonial_future_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES colonial_future_scenarios(scenario_id)
);

CREATE VIEW colonial_future_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.12 * agenda_setting_power +
      0.12 * (1 - consent_quality) +
      0.12 * land_exposure +
      0.12 * external_control +
      0.11 * (1 - epistemic_justice) +
      0.10 * (1 - local_benefit) +
      0.10 * ecological_harm +
      0.09 * (1 - reparative_capacity) +
      0.07 * (1 - sovereignty_recognition) +
      0.03 * (1 - data_sovereignty) +
      0.02 * (1 - labor_protection),
      4
    ) AS coloniality_risk_score,
    ROUND(
      0.16 * consent_quality +
      0.15 * epistemic_justice +
      0.14 * local_benefit +
      0.16 * reparative_capacity +
      0.14 * sovereignty_recognition +
      0.08 * data_sovereignty +
      0.07 * labor_protection +
      0.05 * (1 - external_control) +
      0.03 * (1 - land_exposure) +
      0.02 * (1 - ecological_harm),
      4
    ) AS reparative_future_score
FROM colonial_future_profiles;

CREATE VIEW colonial_future_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.14 * extraction_pressure +
      0.14 * external_control_pressure +
      0.13 * consent_gap +
      0.12 * land_risk +
      0.12 * knowledge_erasure +
      0.10 * data_extraction +
      0.09 * security_drift +
      0.08 * ecological_harm +
      0.05 * (1 - reparative_opening) +
      0.03 * (1 - community_voice),
      4
    ) AS colonial_pressure_score
FROM colonial_future_scenarios;

CREATE VIEW reparative_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * land_return_gain +
      0.13 * consent_quality_gain +
      0.12 * community_ownership_gain +
      0.12 * epistemic_justice_gain +
      0.10 * data_sovereignty_gain +
      0.10 * labor_rights_gain +
      0.10 * ecological_restoration_gain +
      0.09 * reparative_finance_gain +
      0.07 * accountability_gain +
      0.02 * implementation_capacity +
      0.02 * legitimacy_gain,
      4
    ) AS reparative_strategy_value_score
FROM reparative_strategy_options;

CREATE VIEW coloniality_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.17 * severity +
      0.15 * irreversibility +
      0.10 * visibility_gap +
      0.20 * distributional_harm +
      0.14 * rights_risk +
      0.10 * (1 - preparedness),
      4
    ) AS coloniality_risk_priority_score
FROM coloniality_risk_indicators;

CREATE VIEW extraction_voice_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    extraction_burden,
    ROUND(
      0.18 * community_voice +
      0.16 * local_benefit +
      0.16 * reparative_capacity +
      0.16 * consent_quality +
      0.14 * sovereignty_recognition -
      0.08 * extraction_burden -
      0.07 * external_control -
      0.05 * ecological_harm,
      4
    ) AS future_making_legitimacy_score,
    ROUND(
      CASE
        WHEN extraction_burden + external_control + ecological_harm - local_benefit - reparative_capacity - consent_quality > 0
        THEN extraction_burden + external_control + ecological_harm - local_benefit - reparative_capacity - consent_quality
        ELSE 0
      END,
      4
    ) AS reparative_gap_score
FROM extraction_voice_records;
