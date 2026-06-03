-- Energy Transition Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS energy_transition_scenario_scores;
DROP VIEW IF EXISTS energy_justice_scores;
DROP VIEW IF EXISTS transition_risk_scores;
DROP VIEW IF EXISTS energy_transition_capability_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS energy_transition_scenarios;
DROP TABLE IF EXISTS justice_indicators;
DROP TABLE IF EXISTS transition_risk_register;
DROP TABLE IF EXISTS energy_transition_capabilities;

CREATE TABLE energy_transition_capabilities (
    capability_id TEXT PRIMARY KEY,
    capability_name TEXT NOT NULL,
    domain TEXT,
    clean_power_expansion REAL,
    grid_readiness REAL,
    storage_flexibility REAL,
    electrification_capacity REAL,
    fossil_phase_down REAL,
    energy_justice REAL,
    labor_transition REAL,
    material_responsibility REAL,
    climate_resilience REAL,
    description TEXT
);

CREATE TABLE transition_risk_register (
    risk_id TEXT PRIMARY KEY,
    capability_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    governance_gap REAL,
    infrastructure_exposure REAL,
    justice_relevance REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(capability_id) REFERENCES energy_transition_capabilities(capability_id)
);

CREATE TABLE justice_indicators (
    justice_id TEXT PRIMARY KEY,
    capability_id TEXT,
    justice_dimension TEXT,
    affordability REAL,
    community_voice REAL,
    worker_security REAL,
    health_benefit REAL,
    ownership_access REAL,
    repair_capacity REAL,
    harm_reduction REAL,
    description TEXT,
    FOREIGN KEY(capability_id) REFERENCES energy_transition_capabilities(capability_id)
);

CREATE TABLE energy_transition_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    clean_power_expansion REAL,
    grid_readiness REAL,
    storage_flexibility REAL,
    electrification_capacity REAL,
    fossil_phase_down REAL,
    energy_justice REAL,
    labor_transition REAL,
    material_responsibility REAL,
    climate_resilience REAL,
    description TEXT
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    pathway_name TEXT,
    clean_power REAL,
    grid REAL,
    storage REAL,
    electrification REAL,
    fossil_phase_down REAL,
    justice REAL,
    labor REAL,
    materials REAL,
    resilience REAL,
    initial_transition_capacity REAL,
    time_horizon INTEGER,
    FOREIGN KEY(scenario_id) REFERENCES energy_transition_scenarios(scenario_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    grid_investment REAL,
    clean_power_deployment REAL,
    electrification_support REAL,
    fossil_phase_down_planning REAL,
    justice_investment REAL,
    labor_protection REAL,
    material_governance REAL,
    resilience_investment REAL,
    public_finance REAL,
    description TEXT
);

CREATE VIEW energy_transition_capability_scores AS
SELECT
    capability_id,
    capability_name,
    domain,
    ROUND(
      0.14 * clean_power_expansion +
      0.14 * grid_readiness +
      0.12 * storage_flexibility +
      0.12 * electrification_capacity +
      0.12 * fossil_phase_down +
      0.12 * energy_justice +
      0.10 * labor_transition +
      0.08 * material_responsibility +
      0.06 * climate_resilience,
      4
    ) AS transition_readiness_score,
    ROUND(
      0.18 * (1 - grid_readiness) +
      0.16 * (1 - storage_flexibility) +
      0.16 * (1 - fossil_phase_down) +
      0.14 * (1 - energy_justice) +
      0.12 * (1 - labor_transition) +
      0.12 * (1 - material_responsibility) +
      0.12 * (1 - climate_resilience),
      4
    ) AS transition_risk_pressure_score
FROM energy_transition_capabilities;

CREATE VIEW transition_risk_scores AS
SELECT
    risk_id,
    capability_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.20 * severity +
      0.14 * detection_difficulty +
      0.16 * governance_gap +
      0.14 * infrastructure_exposure +
      0.12 * justice_relevance +
      0.06 * (1 - mitigation_capacity),
      4
    ) AS transition_risk_priority_score,
    mitigation_capacity
FROM transition_risk_register;

CREATE VIEW energy_justice_scores AS
SELECT
    justice_id,
    capability_id,
    justice_dimension,
    ROUND(
      0.18 * affordability +
      0.16 * community_voice +
      0.16 * worker_security +
      0.16 * health_benefit +
      0.12 * ownership_access +
      0.12 * repair_capacity +
      0.10 * harm_reduction,
      4
    ) AS energy_justice_score,
    ROUND(
      1 - (
        0.18 * affordability +
        0.16 * community_voice +
        0.16 * worker_security +
        0.16 * health_benefit +
        0.12 * ownership_access +
        0.12 * repair_capacity +
        0.10 * harm_reduction
      ),
      4
    ) AS energy_justice_gap_score
FROM justice_indicators;

CREATE VIEW energy_transition_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.14 * clean_power_expansion +
      0.14 * grid_readiness +
      0.12 * storage_flexibility +
      0.12 * electrification_capacity +
      0.12 * fossil_phase_down +
      0.12 * energy_justice +
      0.10 * labor_transition +
      0.08 * material_responsibility +
      0.06 * climate_resilience,
      4
    ) AS transition_readiness_score,
    ROUND(
      0.18 * (1 - grid_readiness) +
      0.16 * (1 - storage_flexibility) +
      0.16 * (1 - fossil_phase_down) +
      0.14 * (1 - energy_justice) +
      0.12 * (1 - labor_transition) +
      0.12 * (1 - material_responsibility) +
      0.12 * (1 - climate_resilience),
      4
    ) AS transition_risk_pressure_score
FROM energy_transition_scenarios;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.14 * grid_investment +
      0.12 * clean_power_deployment +
      0.12 * electrification_support +
      0.12 * fossil_phase_down_planning +
      0.14 * justice_investment +
      0.12 * labor_protection +
      0.10 * material_governance +
      0.08 * resilience_investment +
      0.06 * public_finance,
      4
    ) AS public_interest_transition_strategy_score,
    ROUND(
      0.18 * justice_investment +
      0.16 * labor_protection +
      0.14 * resilience_investment +
      0.14 * material_governance +
      0.12 * fossil_phase_down_planning +
      0.10 * grid_investment +
      0.08 * public_finance +
      0.08 * electrification_support,
      4
    ) AS justice_resilience_strategy_score
FROM strategy_options;
