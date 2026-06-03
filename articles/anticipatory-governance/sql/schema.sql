-- Anticipatory Governance schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS scenario_profile_scores;
DROP VIEW IF EXISTS emerging_risk_scores;
DROP VIEW IF EXISTS weak_signal_scores;
DROP VIEW IF EXISTS governance_profile_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS scenario_profiles;
DROP TABLE IF EXISTS emerging_risk_register;
DROP TABLE IF EXISTS weak_signal_register;
DROP TABLE IF EXISTS governance_profiles;

CREATE TABLE governance_profiles (
    governance_id TEXT PRIMARY KEY,
    governance_strategy TEXT NOT NULL,
    governance_type TEXT,
    detection_capacity REAL,
    interpretation_capacity REAL,
    scenario_capacity REAL,
    preparedness_capacity REAL,
    legitimacy REAL,
    coordination_capacity REAL,
    adaptive_authority REAL,
    equity_safeguards REAL,
    learning_capacity REAL,
    implementation_connection REAL,
    description TEXT
);

CREATE TABLE weak_signal_register (
    signal_id TEXT PRIMARY KEY,
    signal_name TEXT NOT NULL,
    domain TEXT,
    signal_strength REAL,
    novelty REAL,
    uncertainty REAL,
    system_relevance REAL,
    justice_relevance REAL,
    detection_difficulty REAL,
    response_readiness REAL,
    description TEXT
);

CREATE TABLE emerging_risk_register (
    risk_id TEXT PRIMARY KEY,
    governance_id TEXT,
    risk_name TEXT NOT NULL,
    risk_domain TEXT,
    probability REAL,
    severity REAL,
    uncertainty REAL,
    detection_difficulty REAL,
    justice_exposure REAL,
    governance_gap REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(governance_id) REFERENCES governance_profiles(governance_id)
);

CREATE TABLE scenario_profiles (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    technology_acceleration REAL,
    climate_stress REAL,
    public_trust REAL,
    geopolitical_volatility REAL,
    fiscal_pressure REAL,
    institutional_capacity REAL,
    participation_quality REAL,
    crisis_frequency REAL,
    description TEXT
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    governance_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    detection REAL,
    interpretation REAL,
    preparedness REAL,
    legitimacy REAL,
    coordination REAL,
    adaptive_authority REAL,
    equity REAL,
    learning REAL,
    initial_capacity REAL,
    time_horizon INTEGER,
    FOREIGN KEY(governance_id) REFERENCES governance_profiles(governance_id),
    FOREIGN KEY(scenario_id) REFERENCES scenario_profiles(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    horizon_scanning REAL,
    scenario_planning REAL,
    early_warning REAL,
    adaptive_regulation REAL,
    public_participation REAL,
    budget_alignment REAL,
    evaluation_capacity REAL,
    equity_safeguards REAL,
    implementation_authority REAL,
    description TEXT
);

CREATE VIEW governance_profile_scores AS
SELECT
    governance_id,
    governance_strategy,
    governance_type,
    ROUND(
      0.12 * detection_capacity +
      0.12 * interpretation_capacity +
      0.12 * scenario_capacity +
      0.12 * preparedness_capacity +
      0.12 * legitimacy +
      0.10 * coordination_capacity +
      0.10 * adaptive_authority +
      0.08 * equity_safeguards +
      0.07 * learning_capacity +
      0.05 * implementation_connection,
      4
    ) AS anticipatory_capacity_score,
    ROUND(
      0.16 * (1 - detection_capacity) +
      0.14 * (1 - preparedness_capacity) +
      0.14 * (1 - adaptive_authority) +
      0.14 * (1 - coordination_capacity) +
      0.14 * (1 - legitimacy) +
      0.12 * (1 - equity_safeguards) +
      0.08 * (1 - learning_capacity) +
      0.08 * (1 - implementation_connection),
      4
    ) AS anticipatory_fragility_pressure_score
FROM governance_profiles;

CREATE VIEW weak_signal_scores AS
SELECT
    signal_id,
    signal_name,
    domain,
    ROUND(
      0.16 * signal_strength +
      0.14 * novelty +
      0.12 * uncertainty +
      0.18 * system_relevance +
      0.16 * justice_relevance +
      0.12 * detection_difficulty +
      0.12 * (1 - response_readiness),
      4
    ) AS weak_signal_priority_score,
    ROUND(1 - response_readiness, 4) AS response_gap_score
FROM weak_signal_register;

CREATE VIEW emerging_risk_scores AS
SELECT
    risk_id,
    governance_id,
    risk_name,
    risk_domain,
    ROUND(
      0.16 * probability +
      0.18 * severity +
      0.14 * uncertainty +
      0.14 * detection_difficulty +
      0.14 * justice_exposure +
      0.14 * governance_gap +
      0.10 * (1 - mitigation_capacity),
      4
    ) AS emerging_risk_priority_score,
    mitigation_capacity
FROM emerging_risk_register;

CREATE VIEW scenario_profile_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * technology_acceleration +
      0.18 * climate_stress +
      0.14 * (1 - public_trust) +
      0.14 * geopolitical_volatility +
      0.12 * fiscal_pressure +
      0.10 * (1 - institutional_capacity) +
      0.08 * (1 - participation_quality) +
      0.08 * crisis_frequency,
      4
    ) AS future_stress_pressure_score,
    ROUND(
      0.22 * institutional_capacity +
      0.22 * participation_quality +
      0.20 * public_trust +
      0.12 * (1 - fiscal_pressure) +
      0.10 * (1 - crisis_frequency) +
      0.08 * (1 - geopolitical_volatility) +
      0.06 * (1 - climate_stress),
      4
    ) AS democratic_anticipatory_opportunity_score
FROM scenario_profiles;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * horizon_scanning +
      0.12 * scenario_planning +
      0.14 * early_warning +
      0.14 * adaptive_regulation +
      0.14 * public_participation +
      0.12 * budget_alignment +
      0.10 * evaluation_capacity +
      0.08 * equity_safeguards +
      0.04 * implementation_authority,
      4
    ) AS anticipatory_governance_strategy_score,
    ROUND(
      0.18 * implementation_authority +
      0.16 * budget_alignment +
      0.14 * early_warning +
      0.14 * adaptive_regulation +
      0.12 * evaluation_capacity +
      0.10 * horizon_scanning +
      0.08 * scenario_planning +
      0.08 * public_participation,
      4
    ) AS operational_authority_strategy_score
FROM strategy_options;
