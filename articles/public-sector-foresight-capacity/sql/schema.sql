-- Public-Sector Foresight Capacity schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS scenario_cycle_scores;
DROP VIEW IF EXISTS decision_uptake_scores;
DROP VIEW IF EXISTS scanning_signal_scores;
DROP VIEW IF EXISTS foresight_capacity_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS scenario_cycle_profiles;
DROP TABLE IF EXISTS decision_uptake_register;
DROP TABLE IF EXISTS scanning_signals;
DROP TABLE IF EXISTS foresight_capacity_profiles;

CREATE TABLE foresight_capacity_profiles (
    capacity_id TEXT PRIMARY KEY,
    foresight_model TEXT NOT NULL,
    institution_type TEXT,
    scanning_capacity REAL,
    scenario_capacity REAL,
    decision_uptake REAL,
    participation_capacity REAL,
    budget_connection REAL,
    evaluation_capacity REAL,
    institutional_learning REAL,
    implementation_authority REAL,
    knowledge_infrastructure REAL,
    legitimacy REAL,
    description TEXT
);

CREATE TABLE scanning_signals (
    signal_id TEXT PRIMARY KEY,
    signal_name TEXT NOT NULL,
    domain TEXT,
    signal_strength REAL,
    novelty REAL,
    uncertainty REAL,
    policy_relevance REAL,
    equity_relevance REAL,
    detection_difficulty REAL,
    response_readiness REAL,
    description TEXT
);

CREATE TABLE decision_uptake_register (
    uptake_id TEXT PRIMARY KEY,
    capacity_id TEXT,
    decision_area TEXT,
    uptake_strength REAL,
    budget_influence REAL,
    regulatory_influence REAL,
    procurement_influence REAL,
    implementation_influence REAL,
    evaluation_influence REAL,
    participation_influence REAL,
    description TEXT,
    FOREIGN KEY(capacity_id) REFERENCES foresight_capacity_profiles(capacity_id)
);

CREATE TABLE scenario_cycle_profiles (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    technology_disruption REAL,
    climate_stress REAL,
    fiscal_pressure REAL,
    public_trust REAL,
    institutional_capacity REAL,
    participation_quality REAL,
    review_frequency REAL,
    implementation_pressure REAL,
    description TEXT
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    capacity_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    scanning REAL,
    scenarios REAL,
    participation REAL,
    budget REAL,
    evaluation REAL,
    learning REAL,
    authority REAL,
    legitimacy REAL,
    initial_capacity REAL,
    time_horizon INTEGER,
    FOREIGN KEY(capacity_id) REFERENCES foresight_capacity_profiles(capacity_id),
    FOREIGN KEY(scenario_id) REFERENCES scenario_cycle_profiles(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    foresight_mandate REAL,
    horizon_scanning REAL,
    scenario_cycles REAL,
    decision_pathways REAL,
    participatory_foresight REAL,
    budget_alignment REAL,
    evaluation_capacity REAL,
    knowledge_infrastructure REAL,
    implementation_authority REAL,
    description TEXT
);

CREATE VIEW foresight_capacity_scores AS
SELECT
    capacity_id,
    foresight_model,
    institution_type,
    ROUND(
      0.12 * scanning_capacity +
      0.12 * scenario_capacity +
      0.14 * decision_uptake +
      0.12 * participation_capacity +
      0.12 * budget_connection +
      0.10 * evaluation_capacity +
      0.10 * institutional_learning +
      0.10 * implementation_authority +
      0.05 * knowledge_infrastructure +
      0.03 * legitimacy,
      4
    ) AS foresight_capacity_score,
    ROUND(
      0.16 * (1 - decision_uptake) +
      0.14 * (1 - budget_connection) +
      0.14 * (1 - implementation_authority) +
      0.12 * (1 - scanning_capacity) +
      0.12 * (1 - scenario_capacity) +
      0.10 * (1 - participation_capacity) +
      0.10 * (1 - evaluation_capacity) +
      0.08 * (1 - institutional_learning) +
      0.04 * (1 - knowledge_infrastructure),
      4
    ) AS capacity_gap_score
FROM foresight_capacity_profiles;

CREATE VIEW scanning_signal_scores AS
SELECT
    signal_id,
    signal_name,
    domain,
    ROUND(
      0.16 * signal_strength +
      0.12 * novelty +
      0.12 * uncertainty +
      0.18 * policy_relevance +
      0.16 * equity_relevance +
      0.12 * detection_difficulty +
      0.14 * (1 - response_readiness),
      4
    ) AS scanning_signal_priority_score,
    ROUND(1 - response_readiness, 4) AS response_gap_score
FROM scanning_signals;

CREATE VIEW decision_uptake_scores AS
SELECT
    uptake_id,
    capacity_id,
    decision_area,
    ROUND(
      0.20 * uptake_strength +
      0.18 * budget_influence +
      0.14 * regulatory_influence +
      0.12 * procurement_influence +
      0.14 * implementation_influence +
      0.12 * evaluation_influence +
      0.10 * participation_influence,
      4
    ) AS decision_uptake_score,
    budget_influence,
    implementation_influence
FROM decision_uptake_register;

CREATE VIEW scenario_cycle_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * technology_disruption +
      0.18 * climate_stress +
      0.14 * fiscal_pressure +
      0.12 * (1 - public_trust) +
      0.12 * (1 - institutional_capacity) +
      0.10 * (1 - participation_quality) +
      0.08 * (1 - review_frequency) +
      0.10 * implementation_pressure,
      4
    ) AS foresight_stress_pressure_score,
    ROUND(
      0.22 * institutional_capacity +
      0.20 * participation_quality +
      0.18 * public_trust +
      0.14 * review_frequency +
      0.10 * (1 - fiscal_pressure) +
      0.08 * (1 - technology_disruption) +
      0.08 * (1 - climate_stress),
      4
    ) AS foresight_opportunity_score
FROM scenario_cycle_profiles;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * foresight_mandate +
      0.12 * horizon_scanning +
      0.13 * scenario_cycles +
      0.13 * decision_pathways +
      0.12 * participatory_foresight +
      0.12 * budget_alignment +
      0.10 * evaluation_capacity +
      0.08 * knowledge_infrastructure +
      0.08 * implementation_authority,
      4
    ) AS foresight_capacity_strategy_score,
    ROUND(
      0.18 * implementation_authority +
      0.18 * budget_alignment +
      0.14 * decision_pathways +
      0.12 * evaluation_capacity +
      0.10 * foresight_mandate +
      0.10 * scenario_cycles +
      0.09 * horizon_scanning +
      0.09 * knowledge_infrastructure,
      4
    ) AS implementation_authority_strategy_score
FROM strategy_options;
