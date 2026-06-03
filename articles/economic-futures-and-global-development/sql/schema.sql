-- Economic Futures and Global Development schema.
-- SQLite compatible.

DROP VIEW IF EXISTS institutional_capacity_scores;
DROP VIEW IF EXISTS shock_priority_scores;
DROP VIEW IF EXISTS policy_portfolio_scores;
DROP VIEW IF EXISTS economic_scenario_scores;
DROP VIEW IF EXISTS development_future_scores;

DROP TABLE IF EXISTS development_pathways;
DROP TABLE IF EXISTS institutional_capacity;
DROP TABLE IF EXISTS shocks_and_stressors;
DROP TABLE IF EXISTS policy_portfolios;
DROP TABLE IF EXISTS economic_scenarios;
DROP TABLE IF EXISTS development_futures;

CREATE TABLE development_futures (
    future_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    growth REAL,
    inequality REAL,
    ecological_stress REAL,
    institutional_capacity REAL,
    resilience REAL,
    fiscal_space REAL,
    labor_inclusion REAL,
    public_investment REAL,
    technology_diffusion REAL,
    trade_resilience REAL,
    democratic_legitimacy REAL,
    description TEXT
);

CREATE TABLE economic_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    global_growth REAL,
    financial_volatility REAL,
    climate_pressure REAL,
    technology_acceleration REAL,
    trade_fragmentation REAL,
    debt_stress REAL,
    energy_transition_speed REAL,
    public_trust REAL,
    coordination_capacity REAL,
    description TEXT
);

CREATE TABLE policy_portfolios (
    policy_id TEXT PRIMARY KEY,
    policy_name TEXT,
    policy_type TEXT,
    productive_capability REAL,
    distributional_inclusion REAL,
    ecological_viability REAL,
    resilience_capacity REAL,
    fiscal_sustainability REAL,
    labor_protection REAL,
    implementation_capacity REAL,
    global_coordination_need REAL,
    democratic_legitimacy REAL,
    description TEXT
);

CREATE TABLE shocks_and_stressors (
    shock_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    shock_name TEXT,
    shock_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    systemic_reach REAL,
    distributional_exposure REAL,
    recovery_difficulty REAL,
    policy_preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES economic_scenarios(scenario_id)
);

CREATE TABLE institutional_capacity (
    institution_id TEXT PRIMARY KEY,
    future_id TEXT,
    institution_name TEXT,
    institution_domain TEXT,
    administrative_capacity REAL,
    coordination_capacity REAL,
    public_trust REAL,
    regulatory_quality REAL,
    tax_capacity REAL,
    learning_capacity REAL,
    participation_quality REAL,
    description TEXT,
    FOREIGN KEY(future_id) REFERENCES development_futures(future_id)
);

CREATE TABLE development_pathways (
    pathway_id TEXT PRIMARY KEY,
    future_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    growth REAL,
    institutional_capacity REAL,
    adaptation REAL,
    resilience REAL,
    fiscal_space REAL,
    labor_inclusion REAL,
    public_investment REAL,
    ecological_stress REAL,
    inequality REAL,
    initial_development REAL,
    time_horizon INTEGER,
    FOREIGN KEY(future_id) REFERENCES development_futures(future_id),
    FOREIGN KEY(scenario_id) REFERENCES economic_scenarios(scenario_id)
);

CREATE VIEW development_future_scores AS
SELECT
    future_id,
    future_name,
    future_type,
    ROUND(
      0.14 * growth -
      0.12 * inequality -
      0.14 * ecological_stress +
      0.13 * institutional_capacity +
      0.12 * resilience +
      0.08 * fiscal_space +
      0.08 * labor_inclusion +
      0.08 * public_investment +
      0.06 * technology_diffusion +
      0.03 * trade_resilience +
      0.02 * democratic_legitimacy,
      4
    ) AS development_quality_score,
    ROUND(
      0.16 * inequality +
      0.16 * ecological_stress +
      0.13 * (1 - institutional_capacity) +
      0.13 * (1 - resilience) +
      0.12 * (1 - fiscal_space) +
      0.10 * (1 - labor_inclusion) +
      0.08 * (1 - public_investment) +
      0.06 * (1 - trade_resilience) +
      0.06 * (1 - democratic_legitimacy),
      4
    ) AS development_fragility_score
FROM development_futures;

CREATE VIEW economic_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * financial_volatility +
      0.16 * climate_pressure +
      0.14 * trade_fragmentation +
      0.14 * debt_stress +
      0.12 * (1 - public_trust) +
      0.12 * (1 - coordination_capacity) +
      0.08 * (1 - global_growth) +
      0.08 * (1 - energy_transition_speed),
      4
    ) AS economic_future_stress_score,
    ROUND(
      0.18 * global_growth +
      0.16 * technology_acceleration +
      0.16 * energy_transition_speed +
      0.16 * coordination_capacity +
      0.14 * public_trust +
      0.10 * (1 - debt_stress) +
      0.10 * (1 - trade_fragmentation),
      4
    ) AS development_opportunity_score
FROM economic_scenarios;

CREATE VIEW policy_portfolio_scores AS
SELECT
    policy_id,
    policy_name,
    policy_type,
    ROUND(
      0.15 * productive_capability +
      0.14 * distributional_inclusion +
      0.14 * ecological_viability +
      0.14 * resilience_capacity +
      0.11 * fiscal_sustainability +
      0.10 * labor_protection +
      0.10 * implementation_capacity +
      0.06 * democratic_legitimacy +
      0.06 * (1 - global_coordination_need),
      4
    ) AS development_strategy_strength_score,
    ROUND(
      0.24 * (1 - implementation_capacity) +
      0.18 * global_coordination_need +
      0.16 * (1 - fiscal_sustainability) +
      0.14 * (1 - democratic_legitimacy) +
      0.12 * (1 - resilience_capacity) +
      0.08 * (1 - distributional_inclusion) +
      0.08 * (1 - ecological_viability),
      4
    ) AS implementation_risk_score
FROM policy_portfolios;

CREATE VIEW shock_priority_scores AS
SELECT
    shock_id,
    scenario_id,
    shock_name,
    shock_domain,
    ROUND(
      0.18 * probability_proxy +
      0.20 * severity +
      0.18 * systemic_reach +
      0.17 * distributional_exposure +
      0.15 * recovery_difficulty +
      0.12 * (1 - policy_preparedness),
      4
    ) AS development_shock_priority_score,
    policy_preparedness
FROM shocks_and_stressors;

CREATE VIEW institutional_capacity_scores AS
SELECT
    institution_id,
    future_id,
    institution_name,
    institution_domain,
    ROUND(
      0.18 * administrative_capacity +
      0.18 * coordination_capacity +
      0.14 * public_trust +
      0.14 * regulatory_quality +
      0.14 * tax_capacity +
      0.12 * learning_capacity +
      0.10 * participation_quality,
      4
    ) AS institutional_capacity_score,
    ROUND(
      0.18 * (1 - administrative_capacity) +
      0.18 * (1 - coordination_capacity) +
      0.16 * (1 - public_trust) +
      0.14 * (1 - tax_capacity) +
      0.12 * (1 - regulatory_quality) +
      0.12 * (1 - learning_capacity) +
      0.10 * (1 - participation_quality),
      4
    ) AS institutional_fragility_score
FROM institutional_capacity;
