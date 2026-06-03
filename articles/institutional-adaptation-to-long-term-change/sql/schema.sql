-- Institutional Adaptation to Long-Term Change schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS adaptation_scenario_scores;
DROP VIEW IF EXISTS feedback_capacity_scores;
DROP VIEW IF EXISTS adaptation_risk_scores;
DROP VIEW IF EXISTS institutional_profile_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS adaptation_scenarios;
DROP TABLE IF EXISTS feedback_indicators;
DROP TABLE IF EXISTS adaptation_risk_register;
DROP TABLE IF EXISTS institutional_profiles;

CREATE TABLE institutional_profiles (
    institution_id TEXT PRIMARY KEY,
    institution_name TEXT NOT NULL,
    institution_type TEXT,
    learning_capacity REAL,
    structural_flexibility REAL,
    coordination_capacity REAL,
    legitimacy REAL,
    feedback_sensitivity REAL,
    resource_mobility REAL,
    shock_responsiveness REAL,
    rigidity REAL,
    intergenerational_responsibility REAL,
    description TEXT
);

CREATE TABLE adaptation_risk_register (
    risk_id TEXT PRIMARY KEY,
    institution_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    governance_gap REAL,
    legitimacy_exposure REAL,
    implementation_exposure REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(institution_id) REFERENCES institutional_profiles(institution_id)
);

CREATE TABLE feedback_indicators (
    feedback_id TEXT PRIMARY KEY,
    institution_id TEXT,
    feedback_dimension TEXT,
    signal_detection REAL,
    interpretation_capacity REAL,
    evaluation_quality REAL,
    memory_retention REAL,
    revision_authority REAL,
    community_feedback REAL,
    public_reporting REAL,
    description TEXT,
    FOREIGN KEY(institution_id) REFERENCES institutional_profiles(institution_id)
);

CREATE TABLE adaptation_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    environmental_pressure REAL,
    technological_change REAL,
    demographic_pressure REAL,
    fiscal_constraint REAL,
    public_trust REAL,
    coordination_demand REAL,
    crisis_frequency REAL,
    description TEXT
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    institution_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    learning REAL,
    flexibility REAL,
    coordination REAL,
    legitimacy REAL,
    feedback REAL,
    resources REAL,
    rigidity REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(institution_id) REFERENCES institutional_profiles(institution_id),
    FOREIGN KEY(scenario_id) REFERENCES adaptation_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    learning_systems REAL,
    adaptive_legal_design REAL,
    cross_agency_coordination REAL,
    participatory_governance REAL,
    long_term_budgeting REAL,
    feedback_infrastructure REAL,
    accountability_safeguards REAL,
    resource_mobility REAL,
    power_analysis REAL,
    description TEXT
);

CREATE VIEW institutional_profile_scores AS
SELECT
    institution_id,
    institution_name,
    institution_type,
    ROUND(
      0.18 * learning_capacity +
      0.16 * structural_flexibility +
      0.16 * coordination_capacity +
      0.14 * legitimacy +
      0.14 * feedback_sensitivity +
      0.10 * resource_mobility +
      0.08 * shock_responsiveness -
      0.10 * rigidity +
      0.04 * intergenerational_responsibility,
      4
    ) AS adaptive_profile_score,
    ROUND(
      0.20 * rigidity +
      0.16 * (1 - learning_capacity) +
      0.16 * (1 - structural_flexibility) +
      0.14 * (1 - coordination_capacity) +
      0.12 * (1 - legitimacy) +
      0.12 * (1 - feedback_sensitivity) +
      0.10 * (1 - resource_mobility),
      4
    ) AS fragility_pressure_score
FROM institutional_profiles;

CREATE VIEW adaptation_risk_scores AS
SELECT
    risk_id,
    institution_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.20 * severity +
      0.14 * detection_difficulty +
      0.16 * governance_gap +
      0.12 * legitimacy_exposure +
      0.12 * implementation_exposure +
      0.08 * (1 - mitigation_capacity),
      4
    ) AS adaptation_risk_priority_score,
    mitigation_capacity
FROM adaptation_risk_register;

CREATE VIEW feedback_capacity_scores AS
SELECT
    feedback_id,
    institution_id,
    feedback_dimension,
    ROUND(
      0.18 * signal_detection +
      0.16 * interpretation_capacity +
      0.16 * evaluation_quality +
      0.14 * memory_retention +
      0.14 * revision_authority +
      0.12 * community_feedback +
      0.10 * public_reporting,
      4
    ) AS feedback_capacity_score
FROM feedback_indicators;

CREATE VIEW adaptation_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * environmental_pressure +
      0.18 * technological_change +
      0.14 * demographic_pressure +
      0.14 * fiscal_constraint +
      0.12 * (1 - public_trust) +
      0.12 * coordination_demand +
      0.12 * crisis_frequency,
      4
    ) AS institutional_stress_pressure_score,
    ROUND(
      0.24 * public_trust +
      0.22 * (1 - fiscal_constraint) +
      0.18 * (1 - crisis_frequency) +
      0.14 * (1 - environmental_pressure) +
      0.12 * (1 - technological_change) +
      0.10 * coordination_demand,
      4
    ) AS adaptation_opportunity_score
FROM adaptation_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * learning_systems +
      0.14 * adaptive_legal_design +
      0.14 * cross_agency_coordination +
      0.14 * participatory_governance +
      0.12 * long_term_budgeting +
      0.12 * feedback_infrastructure +
      0.10 * accountability_safeguards +
      0.05 * resource_mobility +
      0.03 * power_analysis,
      4
    ) AS institutional_adaptation_strategy_score,
    ROUND(
      0.18 * participatory_governance +
      0.16 * accountability_safeguards +
      0.14 * power_analysis +
      0.12 * feedback_infrastructure +
      0.12 * learning_systems +
      0.10 * cross_agency_coordination +
      0.10 * long_term_budgeting +
      0.08 * adaptive_legal_design,
      4
    ) AS legitimacy_and_accountability_strategy_score
FROM strategy_options;
