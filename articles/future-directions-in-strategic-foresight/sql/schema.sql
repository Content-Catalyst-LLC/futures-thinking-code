-- Future Directions in Strategic Foresight schema.
-- SQLite compatible.

DROP VIEW IF EXISTS foresight_signal_priority_scores;
DROP VIEW IF EXISTS foresight_risk_priority_scores;
DROP VIEW IF EXISTS foresight_strategy_scores;
DROP VIEW IF EXISTS foresight_system_scenario_scores;
DROP VIEW IF EXISTS foresight_capability_scores;

DROP TABLE IF EXISTS adaptive_strategy_pathways;
DROP TABLE IF EXISTS foresight_signal_records;
DROP TABLE IF EXISTS foresight_risk_indicators;
DROP TABLE IF EXISTS foresight_strategy_options;
DROP TABLE IF EXISTS foresight_system_scenarios;
DROP TABLE IF EXISTS foresight_capability_profiles;

CREATE TABLE foresight_capability_profiles (
    institution_id TEXT PRIMARY KEY,
    institution_type TEXT NOT NULL,
    sector TEXT,
    signal_detection REAL,
    scenario_capability REAL,
    learning_capacity REAL,
    governance_integration REAL,
    adaptive_flexibility REAL,
    participatory_legitimacy REAL,
    ethical_accountability REAL,
    data_infrastructure REAL,
    ai_readiness REAL,
    public_legitimacy REAL,
    description TEXT
);

CREATE TABLE foresight_system_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    signal_velocity REAL,
    uncertainty_load REAL,
    data_quality REAL,
    ai_dependence REAL,
    governance_authority REAL,
    participatory_depth REAL,
    ethical_risk REAL,
    institutional_learning REAL,
    coordination_complexity REAL,
    description TEXT
);

CREATE TABLE foresight_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    institution_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    signal_pipeline_gain REAL,
    scenario_update_gain REAL,
    governance_integration_gain REAL,
    data_system_gain REAL,
    participatory_legitimacy_gain REAL,
    ethical_accountability_gain REAL,
    adaptive_strategy_gain REAL,
    ai_audit_gain REAL,
    learning_capacity_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(institution_id) REFERENCES foresight_capability_profiles(institution_id)
);

CREATE TABLE foresight_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    visibility_gap REAL,
    governance_gap REAL,
    legitimacy_gap REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES foresight_system_scenarios(scenario_id)
);

CREATE TABLE foresight_signal_records (
    signal_id TEXT PRIMARY KEY,
    domain TEXT,
    signal_name TEXT,
    signal_strength REAL,
    signal_velocity REAL,
    novelty REAL,
    relevance REAL,
    source_quality REAL,
    interpretive_confidence REAL,
    uncertainty REAL,
    description TEXT
);

CREATE TABLE adaptive_strategy_pathways (
    pathway_id TEXT PRIMARY KEY,
    institution_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    signal_detection REAL,
    scenario_capability REAL,
    learning_capacity REAL,
    governance_integration REAL,
    adaptive_flexibility REAL,
    participatory_legitimacy REAL,
    ethical_accountability REAL,
    data_infrastructure REAL,
    time_horizon INTEGER,
    FOREIGN KEY(institution_id) REFERENCES foresight_capability_profiles(institution_id),
    FOREIGN KEY(scenario_id) REFERENCES foresight_system_scenarios(scenario_id)
);

CREATE VIEW foresight_capability_scores AS
SELECT
    institution_id,
    institution_type,
    sector,
    ROUND(
      0.16 * signal_detection +
      0.16 * scenario_capability +
      0.14 * learning_capacity +
      0.14 * governance_integration +
      0.12 * adaptive_flexibility +
      0.10 * participatory_legitimacy +
      0.10 * ethical_accountability +
      0.08 * data_infrastructure,
      4
    ) AS foresight_capability_score,
    ROUND(
      0.35 * signal_detection +
      0.35 * scenario_capability +
      0.30 * data_infrastructure,
      4
    ) AS technical_capability_score,
    ROUND(
      0.45 * governance_integration +
      0.30 * adaptive_flexibility +
      0.25 * learning_capacity,
      4
    ) AS governance_capability_score,
    ROUND(
      0.40 * participatory_legitimacy +
      0.35 * ethical_accountability +
      0.25 * public_legitimacy,
      4
    ) AS legitimacy_capability_score
FROM foresight_capability_profiles;

CREATE VIEW foresight_system_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * signal_velocity +
      0.16 * uncertainty_load +
      0.10 * (1 - data_quality) +
      0.10 * ai_dependence +
      0.16 * (1 - governance_authority) +
      0.10 * (1 - participatory_depth) +
      0.12 * ethical_risk +
      0.08 * (1 - institutional_learning) +
      0.06 * coordination_complexity,
      4
    ) AS foresight_system_risk_score
FROM foresight_system_scenarios;

CREATE VIEW foresight_strategy_scores AS
SELECT
    strategy_id,
    institution_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.11 * signal_pipeline_gain +
      0.12 * scenario_update_gain +
      0.14 * governance_integration_gain +
      0.10 * data_system_gain +
      0.11 * participatory_legitimacy_gain +
      0.11 * ethical_accountability_gain +
      0.12 * adaptive_strategy_gain +
      0.07 * ai_audit_gain +
      0.08 * learning_capacity_gain +
      0.02 * implementation_capacity +
      0.02 * public_legitimacy_gain,
      4
    ) AS foresight_capability_gain_score
FROM foresight_strategy_options;

CREATE VIEW foresight_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.17 * severity +
      0.12 * irreversibility +
      0.12 * visibility_gap +
      0.18 * governance_gap +
      0.17 * legitimacy_gap +
      0.10 * (1 - preparedness),
      4
    ) AS foresight_risk_priority_score
FROM foresight_risk_indicators;

CREATE VIEW foresight_signal_priority_scores AS
SELECT
    signal_id,
    domain,
    signal_name,
    ROUND(
      0.16 * signal_strength +
      0.14 * signal_velocity +
      0.10 * novelty +
      0.20 * relevance +
      0.14 * source_quality +
      0.14 * interpretive_confidence +
      0.12 * uncertainty,
      4
    ) AS strategic_attention_score,
    ROUND(uncertainty * (1 - interpretive_confidence), 4) AS ambiguity_score
FROM foresight_signal_records;
