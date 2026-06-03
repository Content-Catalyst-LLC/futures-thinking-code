-- Futures Thinking in Business Strategy schema.
-- SQLite compatible.

DROP VIEW IF EXISTS capability_priority_scores;
DROP VIEW IF EXISTS strategic_option_scores;
DROP VIEW IF EXISTS strategy_profile_scores;

DROP TABLE IF EXISTS dynamic_capability_pathways;
DROP TABLE IF EXISTS early_warning_indicators;
DROP TABLE IF EXISTS capability_register;
DROP TABLE IF EXISTS strategic_options;
DROP TABLE IF EXISTS future_scenarios;
DROP TABLE IF EXISTS strategy_profiles;

CREATE TABLE strategy_profiles (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT,
    innovation_capacity REAL,
    uncertainty_exposure REAL,
    resilience REAL,
    strategic_flexibility REAL,
    organizational_alignment REAL,
    sensing_capability REAL,
    capital_flexibility REAL,
    legitimacy_trust REAL,
    transition_readiness REAL,
    description TEXT
);

CREATE TABLE future_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    market_growth REAL,
    technology_acceleration REAL,
    regulatory_pressure REAL,
    climate_stress REAL,
    supply_chain_stability REAL,
    capital_availability REAL,
    labor_availability REAL,
    consumer_trust_pressure REAL,
    geopolitical_fragmentation REAL,
    description TEXT
);

CREATE TABLE strategic_options (
    option_id TEXT PRIMARY KEY,
    strategy_id TEXT,
    option_name TEXT,
    option_type TEXT,
    learning_value REAL,
    upside_potential REAL,
    cost_to_maintain REAL,
    reversibility REAL,
    scalability REAL,
    strategic_fit REAL,
    signal_sensitivity REAL,
    description TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE capability_register (
    capability_id TEXT PRIMARY KEY,
    strategy_id TEXT,
    capability_name TEXT,
    capability_type TEXT,
    current_strength REAL,
    future_importance REAL,
    development_difficulty REAL,
    coordination_requirement REAL,
    investment_need REAL,
    learning_rate REAL,
    description TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE early_warning_indicators (
    indicator_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    indicator_name TEXT,
    indicator_domain TEXT,
    baseline_value REAL,
    current_signal_strength REAL,
    strategic_relevance REAL,
    lead_time REAL,
    monitoring_difficulty REAL,
    trigger_threshold REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES future_scenarios(scenario_id)
);

CREATE TABLE dynamic_capability_pathways (
    pathway_id TEXT PRIMARY KEY,
    strategy_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    sensing REAL,
    innovation REAL,
    resilience REAL,
    flexibility REAL,
    alignment REAL,
    capital_flexibility REAL,
    trust REAL,
    transition_readiness REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(strategy_id) REFERENCES strategy_profiles(strategy_id),
    FOREIGN KEY(scenario_id) REFERENCES future_scenarios(scenario_id)
);

CREATE VIEW strategy_profile_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.14 * innovation_capacity -
      0.10 * uncertainty_exposure +
      0.15 * resilience +
      0.14 * strategic_flexibility +
      0.10 * organizational_alignment +
      0.12 * sensing_capability +
      0.08 * capital_flexibility +
      0.09 * legitimacy_trust +
      0.08 * transition_readiness,
      4
    ) AS business_futures_readiness_score,
    ROUND(
      0.18 * uncertainty_exposure +
      0.14 * (1 - resilience) +
      0.14 * (1 - strategic_flexibility) +
      0.13 * (1 - sensing_capability) +
      0.11 * (1 - capital_flexibility) +
      0.10 * (1 - organizational_alignment) +
      0.10 * (1 - legitimacy_trust) +
      0.10 * (1 - transition_readiness),
      4
    ) AS strategic_fragility_score
FROM strategy_profiles;

CREATE VIEW strategic_option_scores AS
SELECT
    option_id,
    strategy_id,
    option_name,
    option_type,
    ROUND(
      0.22 * learning_value +
      0.20 * upside_potential +
      0.15 * reversibility +
      0.15 * scalability +
      0.14 * strategic_fit +
      0.14 * signal_sensitivity -
      0.20 * cost_to_maintain,
      4
    ) AS net_strategic_option_value,
    ROUND(
      0.18 * learning_value +
      0.18 * strategic_fit +
      0.16 * signal_sensitivity +
      0.14 * reversibility +
      0.14 * scalability +
      0.12 * upside_potential +
      0.08 * (1 - cost_to_maintain),
      4
    ) AS option_quality_score
FROM strategic_options;

CREATE VIEW capability_priority_scores AS
SELECT
    capability_id,
    strategy_id,
    capability_name,
    capability_type,
    ROUND(
      CASE
        WHEN future_importance - current_strength > 0 THEN future_importance - current_strength
        ELSE 0
      END,
      4
    ) AS future_capability_gap,
    ROUND(
      0.34 * future_importance +
      0.20 * development_difficulty +
      0.18 * coordination_requirement +
      0.14 * investment_need +
      0.14 * (1 - current_strength),
      4
    ) AS capability_investment_priority
FROM capability_register;
