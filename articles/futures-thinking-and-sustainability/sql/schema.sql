-- Futures Thinking and Sustainability schema.
-- SQLite compatible.

DROP VIEW IF EXISTS governance_capacity_scores;
DROP VIEW IF EXISTS sustainability_risk_priority_scores;
DROP VIEW IF EXISTS transition_strategy_scores;
DROP VIEW IF EXISTS sustainability_scenario_scores;
DROP VIEW IF EXISTS sustainability_profile_scores;

DROP TABLE IF EXISTS transition_pathways;
DROP TABLE IF EXISTS governance_capacity_records;
DROP TABLE IF EXISTS sustainability_risk_indicators;
DROP TABLE IF EXISTS transition_strategies;
DROP TABLE IF EXISTS sustainability_scenarios;
DROP TABLE IF EXISTS sustainability_future_profiles;

CREATE TABLE sustainability_future_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    ecological_integrity REAL,
    social_equity REAL,
    adaptive_capacity REAL,
    technological_responsibility REAL,
    governance_coordination REAL,
    public_finance_capacity REAL,
    resilience_capacity REAL,
    justice_legitimacy REAL,
    degradation_pressure REAL,
    description TEXT
);

CREATE TABLE sustainability_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    climate_stress REAL,
    biodiversity_pressure REAL,
    resource_constraint REAL,
    inequality_pressure REAL,
    technology_change REAL,
    governance_fragmentation REAL,
    public_finance_stress REAL,
    transition_momentum REAL,
    description TEXT
);

CREATE TABLE transition_strategies (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    ecological_gain REAL,
    equity_gain REAL,
    adaptive_capacity_gain REAL,
    governance_gain REAL,
    finance_gain REAL,
    resilience_gain REAL,
    justice_gain REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES sustainability_future_profiles(profile_id)
);

CREATE TABLE sustainability_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    systemic_reach REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES sustainability_scenarios(scenario_id)
);

CREATE TABLE governance_capacity_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    participation REAL,
    accountability REAL,
    coordination REAL,
    monitoring_capacity REAL,
    adaptive_learning REAL,
    public_investment REAL,
    justice_safeguards REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES sustainability_future_profiles(profile_id)
);

CREATE TABLE transition_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    ecology REAL,
    governance REAL,
    adaptation REAL,
    public_finance REAL,
    resilience REAL,
    justice REAL,
    degradation_pressure REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES sustainability_future_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES sustainability_scenarios(scenario_id)
);

CREATE VIEW sustainability_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.17 * ecological_integrity +
      0.15 * social_equity +
      0.14 * adaptive_capacity +
      0.10 * technological_responsibility +
      0.14 * governance_coordination +
      0.10 * public_finance_capacity +
      0.10 * resilience_capacity +
      0.10 * justice_legitimacy -
      0.08 * degradation_pressure,
      4
    ) AS sustainability_viability_score,
    ROUND(
      0.16 * degradation_pressure +
      0.15 * (1 - ecological_integrity) +
      0.14 * (1 - social_equity) +
      0.13 * (1 - governance_coordination) +
      0.12 * (1 - adaptive_capacity) +
      0.11 * (1 - public_finance_capacity) +
      0.10 * (1 - resilience_capacity) +
      0.09 * (1 - justice_legitimacy),
      4
    ) AS sustainability_fragility_score
FROM sustainability_future_profiles;

CREATE VIEW sustainability_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.17 * climate_stress +
      0.15 * biodiversity_pressure +
      0.13 * resource_constraint +
      0.15 * inequality_pressure +
      0.12 * governance_fragmentation +
      0.12 * public_finance_stress +
      0.08 * (1 - transition_momentum) +
      0.08 * technology_change,
      4
    ) AS sustainability_stress_score,
    ROUND(
      0.20 * transition_momentum +
      0.14 * technology_change +
      0.12 * (1 - governance_fragmentation) +
      0.12 * (1 - public_finance_stress) +
      0.12 * (1 - inequality_pressure) +
      0.10 * (1 - climate_stress) +
      0.10 * (1 - biodiversity_pressure) +
      0.10 * (1 - resource_constraint),
      4
    ) AS transition_opportunity_score
FROM sustainability_scenarios;

CREATE VIEW transition_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * ecological_gain +
      0.16 * equity_gain +
      0.14 * adaptive_capacity_gain +
      0.14 * governance_gain +
      0.12 * finance_gain +
      0.12 * resilience_gain +
      0.12 * justice_gain +
      0.04 * implementation_capacity,
      4
    ) AS sustainability_gain_score,
    ROUND(
      0.24 * implementation_capacity +
      0.14 * governance_gain +
      0.14 * finance_gain +
      0.14 * adaptive_capacity_gain +
      0.12 * resilience_gain +
      0.10 * justice_gain +
      0.08 * ecological_gain +
      0.04 * equity_gain,
      4
    ) AS implementation_readiness_score
FROM transition_strategies;

CREATE VIEW sustainability_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.18 * severity +
      0.17 * irreversibility +
      0.16 * systemic_reach +
      0.12 * visibility_gap +
      0.15 * distributional_harm +
      0.08 * (1 - preparedness),
      4
    ) AS sustainability_risk_priority_score,
    distributional_harm,
    preparedness
FROM sustainability_risk_indicators;

CREATE VIEW governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.14 * participation +
      0.14 * accountability +
      0.16 * coordination +
      0.14 * monitoring_capacity +
      0.16 * adaptive_learning +
      0.12 * public_investment +
      0.14 * justice_safeguards,
      4
    ) AS governance_capacity_score,
    ROUND(
      0.18 * (1 - participation) +
      0.18 * (1 - accountability) +
      0.16 * (1 - justice_safeguards) +
      0.14 * (1 - coordination) +
      0.12 * (1 - adaptive_learning) +
      0.12 * (1 - public_investment) +
      0.10 * (1 - monitoring_capacity),
      4
    ) AS legitimacy_gap_score
FROM governance_capacity_records;
