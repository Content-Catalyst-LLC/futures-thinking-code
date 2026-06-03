-- Biotechnology Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS biotechnology_scenario_scores;
DROP VIEW IF EXISTS biotechnology_justice_scores;
DROP VIEW IF EXISTS biotechnology_risk_scores;
DROP VIEW IF EXISTS biotechnology_capability_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS biotechnology_scenarios;
DROP TABLE IF EXISTS justice_indicators;
DROP TABLE IF EXISTS biotechnology_risk_register;
DROP TABLE IF EXISTS biotechnology_capabilities;

CREATE TABLE biotechnology_capabilities (
    capability_id TEXT PRIMARY KEY,
    capability_name TEXT NOT NULL,
    domain TEXT,
    scientific_maturity REAL,
    manufacturing_capacity REAL,
    governance_readiness REAL,
    public_legitimacy REAL,
    equity_access REAL,
    ecological_uncertainty REAL,
    dual_use_risk REAL,
    community_consent REAL,
    description TEXT
);

CREATE TABLE biotechnology_risk_register (
    risk_id TEXT PRIMARY KEY,
    capability_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    governance_gap REAL,
    ecological_exposure REAL,
    dual_use_relevance REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(capability_id) REFERENCES biotechnology_capabilities(capability_id)
);

CREATE TABLE justice_indicators (
    justice_id TEXT PRIMARY KEY,
    capability_id TEXT,
    justice_dimension TEXT,
    equitable_access REAL,
    affected_voice REAL,
    consent_strength REAL,
    benefit_sharing REAL,
    repair_capacity REAL,
    harm_concentration REAL,
    community_governance REAL,
    description TEXT,
    FOREIGN KEY(capability_id) REFERENCES biotechnology_capabilities(capability_id)
);

CREATE TABLE biotechnology_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    scientific_maturity REAL,
    governance_readiness REAL,
    ecological_uncertainty REAL,
    dual_use_risk REAL,
    public_legitimacy REAL,
    equity_access REAL,
    manufacturing_capacity REAL,
    community_consent REAL,
    description TEXT
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    pathway_name TEXT,
    science REAL,
    governance REAL,
    legitimacy REAL,
    equity REAL,
    manufacturing REAL,
    ecological_uncertainty REAL,
    dual_use_risk REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(scenario_id) REFERENCES biotechnology_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    governance_strength REAL,
    equity_access REAL,
    community_consent REAL,
    biosafety_capacity REAL,
    biosecurity_capacity REAL,
    open_science REAL,
    public_manufacturing REAL,
    ecological_monitoring REAL,
    benefit_sharing REAL,
    description TEXT
);

CREATE VIEW biotechnology_capability_scores AS
SELECT
    capability_id,
    capability_name,
    domain,
    ROUND(
      0.16 * scientific_maturity +
      0.18 * governance_readiness +
      0.16 * public_legitimacy +
      0.16 * equity_access +
      0.12 * manufacturing_capacity +
      0.12 * community_consent +
      0.05 * (1 - ecological_uncertainty) +
      0.05 * (1 - dual_use_risk),
      4
    ) AS responsible_biotechnology_capacity_score,
    ROUND(
      0.22 * dual_use_risk +
      0.20 * ecological_uncertainty +
      0.18 * (1 - governance_readiness) +
      0.16 * (1 - public_legitimacy) +
      0.14 * (1 - community_consent) +
      0.10 * (1 - equity_access),
      4
    ) AS biological_risk_pressure_score
FROM biotechnology_capabilities;

CREATE VIEW biotechnology_risk_scores AS
SELECT
    risk_id,
    capability_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.22 * severity +
      0.16 * detection_difficulty +
      0.16 * governance_gap +
      0.12 * ecological_exposure +
      0.10 * dual_use_relevance +
      0.06 * (1 - mitigation_capacity),
      4
    ) AS risk_priority_score,
    mitigation_capacity
FROM biotechnology_risk_register;

CREATE VIEW biotechnology_justice_scores AS
SELECT
    justice_id,
    capability_id,
    justice_dimension,
    ROUND(
      0.20 * equitable_access +
      0.16 * affected_voice +
      0.16 * consent_strength +
      0.16 * benefit_sharing +
      0.14 * repair_capacity +
      0.10 * community_governance +
      0.08 * (1 - harm_concentration),
      4
    ) AS biotechnology_justice_score,
    ROUND(
      0.32 * harm_concentration +
      0.18 * (1 - equitable_access) +
      0.16 * (1 - affected_voice) +
      0.14 * (1 - consent_strength) +
      0.12 * (1 - repair_capacity) +
      0.08 * (1 - community_governance),
      4
    ) AS harm_concentration_score
FROM justice_indicators;

CREATE VIEW biotechnology_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * scientific_maturity +
      0.18 * governance_readiness +
      0.16 * public_legitimacy +
      0.16 * equity_access +
      0.12 * manufacturing_capacity +
      0.12 * community_consent +
      0.05 * (1 - ecological_uncertainty) +
      0.05 * (1 - dual_use_risk),
      4
    ) AS responsible_biotechnology_capacity_score,
    ROUND(
      0.22 * dual_use_risk +
      0.20 * ecological_uncertainty +
      0.18 * (1 - governance_readiness) +
      0.16 * (1 - public_legitimacy) +
      0.14 * (1 - community_consent) +
      0.10 * (1 - equity_access),
      4
    ) AS biological_risk_pressure_score
FROM biotechnology_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * governance_strength +
      0.14 * equity_access +
      0.14 * community_consent +
      0.12 * biosafety_capacity +
      0.12 * biosecurity_capacity +
      0.10 * open_science +
      0.08 * public_manufacturing +
      0.08 * ecological_monitoring +
      0.06 * benefit_sharing,
      4
    ) AS public_interest_biotechnology_score,
    ROUND(
      0.18 * equity_access +
      0.18 * community_consent +
      0.16 * benefit_sharing +
      0.14 * governance_strength +
      0.12 * public_manufacturing +
      0.10 * open_science +
      0.08 * ecological_monitoring +
      0.04 * biosafety_capacity,
      4
    ) AS justice_governance_score
FROM strategy_options;
