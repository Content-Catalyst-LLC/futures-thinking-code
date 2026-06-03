-- Futures Thinking in Public Policy schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS policy_risk_scores;
DROP VIEW IF EXISTS institutional_capacity_scores;
DROP VIEW IF EXISTS scenario_profile_scores;
DROP VIEW IF EXISTS policy_option_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS policy_risk_register;
DROP TABLE IF EXISTS institutional_capacity;
DROP TABLE IF EXISTS scenario_profiles;
DROP TABLE IF EXISTS policy_options;

CREATE TABLE policy_options (
    policy_id TEXT PRIMARY KEY,
    policy_name TEXT NOT NULL,
    policy_domain TEXT,
    robustness REAL,
    equity REAL,
    adaptability REAL,
    coordination REAL,
    legitimacy REAL,
    implementation_capacity REAL,
    political_feasibility REAL,
    learning_capacity REAL,
    intergenerational_responsibility REAL,
    description TEXT
);

CREATE TABLE scenario_profiles (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    economic_volatility REAL,
    technological_disruption REAL,
    climate_stress REAL,
    demographic_pressure REAL,
    geopolitical_instability REAL,
    public_trust REAL,
    institutional_capacity REAL,
    fiscal_space REAL,
    description TEXT
);

CREATE TABLE institutional_capacity (
    capacity_id TEXT PRIMARY KEY,
    institution_name TEXT,
    institution_type TEXT,
    detection_capacity REAL,
    learning_capacity REAL,
    coordination_quality REAL,
    budget_alignment REAL,
    implementation_capacity REAL,
    public_participation REAL,
    data_infrastructure REAL,
    accountability_capacity REAL,
    description TEXT
);

CREATE TABLE policy_risk_register (
    risk_id TEXT PRIMARY KEY,
    policy_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    governance_gap REAL,
    equity_exposure REAL,
    implementation_exposure REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(policy_id) REFERENCES policy_options(policy_id)
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    policy_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    robustness REAL,
    adaptability REAL,
    coordination REAL,
    legitimacy REAL,
    equity REAL,
    implementation_capacity REAL,
    learning_capacity REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(policy_id) REFERENCES policy_options(policy_id),
    FOREIGN KEY(scenario_id) REFERENCES scenario_profiles(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    horizon_scanning REAL,
    scenario_planning REAL,
    adaptive_policy_design REAL,
    public_participation REAL,
    budget_alignment REAL,
    evaluation_capacity REAL,
    interagency_coordination REAL,
    equity_analysis REAL,
    implementation_support REAL,
    description TEXT
);

CREATE VIEW policy_option_scores AS
SELECT
    policy_id,
    policy_name,
    policy_domain,
    ROUND(
      0.20 * robustness +
      0.16 * equity +
      0.18 * adaptability +
      0.14 * coordination +
      0.14 * legitimacy +
      0.08 * implementation_capacity +
      0.06 * learning_capacity +
      0.04 * intergenerational_responsibility,
      4
    ) AS policy_futures_profile_score,
    ROUND(
      0.20 * (1 - robustness) +
      0.18 * (1 - adaptability) +
      0.16 * (1 - coordination) +
      0.14 * (1 - legitimacy) +
      0.12 * (1 - equity) +
      0.10 * (1 - learning_capacity) +
      0.10 * (1 - implementation_capacity),
      4
    ) AS policy_fragility_pressure_score
FROM policy_options;

CREATE VIEW scenario_profile_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * economic_volatility +
      0.16 * technological_disruption +
      0.18 * climate_stress +
      0.12 * demographic_pressure +
      0.16 * geopolitical_instability +
      0.10 * (1 - public_trust) +
      0.06 * (1 - institutional_capacity) +
      0.04 * (1 - fiscal_space),
      4
    ) AS policy_stress_pressure_score,
    ROUND(
      0.24 * public_trust +
      0.24 * institutional_capacity +
      0.18 * fiscal_space +
      0.12 * (1 - economic_volatility) +
      0.10 * (1 - geopolitical_instability) +
      0.12 * (1 - climate_stress),
      4
    ) AS governance_opportunity_score
FROM scenario_profiles;

CREATE VIEW institutional_capacity_scores AS
SELECT
    capacity_id,
    institution_name,
    institution_type,
    ROUND(
      0.18 * detection_capacity +
      0.18 * learning_capacity +
      0.16 * coordination_quality +
      0.12 * budget_alignment +
      0.12 * implementation_capacity +
      0.10 * public_participation +
      0.08 * data_infrastructure +
      0.06 * accountability_capacity,
      4
    ) AS anticipatory_governance_capacity_score
FROM institutional_capacity;

CREATE VIEW policy_risk_scores AS
SELECT
    risk_id,
    policy_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.20 * severity +
      0.14 * detection_difficulty +
      0.16 * governance_gap +
      0.12 * equity_exposure +
      0.12 * implementation_exposure +
      0.08 * (1 - mitigation_capacity),
      4
    ) AS policy_risk_priority_score,
    mitigation_capacity
FROM policy_risk_register;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * horizon_scanning +
      0.14 * scenario_planning +
      0.16 * adaptive_policy_design +
      0.14 * public_participation +
      0.12 * budget_alignment +
      0.12 * evaluation_capacity +
      0.10 * interagency_coordination +
      0.06 * equity_analysis +
      0.04 * implementation_support,
      4
    ) AS foresight_capacity_strategy_score,
    ROUND(
      0.18 * budget_alignment +
      0.18 * implementation_support +
      0.16 * evaluation_capacity +
      0.14 * interagency_coordination +
      0.12 * adaptive_policy_design +
      0.10 * horizon_scanning +
      0.06 * scenario_planning +
      0.06 * equity_analysis,
      4
    ) AS operational_governance_strategy_score
FROM strategy_options;
