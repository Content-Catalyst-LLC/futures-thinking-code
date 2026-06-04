-- Financial Futures and Systemic Risk schema.
-- SQLite compatible.

DROP VIEW IF EXISTS public_finance_climate_scores;
DROP VIEW IF EXISTS risk_indicator_priority_scores;
DROP VIEW IF EXISTS policy_option_scores;
DROP VIEW IF EXISTS financial_scenario_scores;
DROP VIEW IF EXISTS financial_profile_scores;

DROP TABLE IF EXISTS stress_pathways;
DROP TABLE IF EXISTS public_finance_climate_records;
DROP TABLE IF EXISTS risk_indicators;
DROP TABLE IF EXISTS policy_options;
DROP TABLE IF EXISTS financial_scenarios;
DROP TABLE IF EXISTS financial_system_profiles;

CREATE TABLE financial_system_profiles (
    profile_id TEXT PRIMARY KEY,
    financial_future_name TEXT NOT NULL,
    financial_future_type TEXT,
    leverage REAL,
    liquidity_resilience REAL,
    household_security REAL,
    climate_exposure REAL,
    nonbank_exposure REAL,
    digital_run_risk REAL,
    regulatory_strength REAL,
    public_finance_capacity REAL,
    consumer_protection REAL,
    productive_investment REAL,
    description TEXT
);

CREATE TABLE financial_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    rate_shock REAL,
    liquidity_shock REAL,
    asset_price_shock REAL,
    climate_shock REAL,
    digital_run_pressure REAL,
    sovereign_refinancing_pressure REAL,
    nonbank_stress REAL,
    household_default_pressure REAL,
    description TEXT
);

CREATE TABLE policy_options (
    policy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    policy_name TEXT,
    policy_type TEXT,
    capital_buffer_strength REAL,
    liquidity_support REAL,
    consumer_protection_gain REAL,
    climate_risk_governance REAL,
    nonbank_oversight REAL,
    digital_resilience REAL,
    public_finance_support REAL,
    implementation_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES financial_system_profiles(profile_id)
);

CREATE TABLE risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    contagion_potential REAL,
    opacity REAL,
    recovery_difficulty REAL,
    distributional_harm REAL,
    policy_preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES financial_scenarios(scenario_id)
);

CREATE TABLE public_finance_climate_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    tax_capacity REAL,
    debt_sustainability REAL,
    adaptation_finance REAL,
    insurance_availability REAL,
    public_investment_capacity REAL,
    household_protection REAL,
    climate_risk_disclosure REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES financial_system_profiles(profile_id)
);

CREATE TABLE stress_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    leverage REAL,
    liquidity_resilience REAL,
    household_security REAL,
    climate_exposure REAL,
    nonbank_exposure REAL,
    digital_run_risk REAL,
    regulatory_strength REAL,
    public_finance_capacity REAL,
    initial_stability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES financial_system_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES financial_scenarios(scenario_id)
);

CREATE VIEW financial_profile_scores AS
SELECT
    profile_id,
    financial_future_name,
    financial_future_type,
    ROUND(
      0.14 * liquidity_resilience +
      0.14 * household_security +
      0.14 * regulatory_strength +
      0.10 * public_finance_capacity +
      0.10 * consumer_protection +
      0.10 * productive_investment +
      0.10 * (1 - leverage) +
      0.08 * (1 - climate_exposure) +
      0.06 * (1 - nonbank_exposure) +
      0.04 * (1 - digital_run_risk),
      4
    ) AS financial_resilience_score,
    ROUND(
      0.16 * leverage +
      0.14 * (1 - liquidity_resilience) +
      0.14 * climate_exposure +
      0.13 * nonbank_exposure +
      0.13 * digital_run_risk +
      0.12 * (1 - household_security) +
      0.10 * (1 - public_finance_capacity) +
      0.08 * (1 - regulatory_strength),
      4
    ) AS systemic_risk_score
FROM financial_system_profiles;

CREATE VIEW financial_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.14 * rate_shock +
      0.16 * liquidity_shock +
      0.14 * asset_price_shock +
      0.14 * climate_shock +
      0.14 * digital_run_pressure +
      0.12 * sovereign_refinancing_pressure +
      0.10 * nonbank_stress +
      0.06 * household_default_pressure,
      4
    ) AS financial_stress_pressure_score,
    ROUND(
      0.18 * household_default_pressure +
      0.16 * sovereign_refinancing_pressure +
      0.14 * climate_shock +
      0.12 * asset_price_shock +
      0.12 * rate_shock +
      0.10 * liquidity_shock +
      0.10 * nonbank_stress +
      0.08 * digital_run_pressure,
      4
    ) AS social_financial_fragility_score
FROM financial_scenarios;

CREATE VIEW policy_option_scores AS
SELECT
    policy_id,
    profile_id,
    policy_name,
    policy_type,
    ROUND(
      0.16 * capital_buffer_strength +
      0.16 * liquidity_support +
      0.14 * consumer_protection_gain +
      0.14 * climate_risk_governance +
      0.14 * nonbank_oversight +
      0.12 * digital_resilience +
      0.10 * public_finance_support +
      0.04 * implementation_capacity,
      4
    ) AS financial_stability_gain_score,
    ROUND(
      0.28 * (1 - implementation_capacity) +
      0.12 * (1 - capital_buffer_strength) +
      0.12 * (1 - liquidity_support) +
      0.12 * (1 - consumer_protection_gain) +
      0.10 * (1 - climate_risk_governance) +
      0.10 * (1 - nonbank_oversight) +
      0.08 * (1 - digital_resilience) +
      0.08 * (1 - public_finance_support),
      4
    ) AS implementation_risk_score
FROM policy_options;

CREATE VIEW risk_indicator_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.15 * probability_proxy +
      0.18 * severity +
      0.17 * contagion_potential +
      0.14 * opacity +
      0.14 * recovery_difficulty +
      0.14 * distributional_harm +
      0.08 * (1 - policy_preparedness),
      4
    ) AS systemic_risk_priority_score,
    distributional_harm,
    policy_preparedness
FROM risk_indicators;

CREATE VIEW public_finance_climate_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.16 * tax_capacity +
      0.16 * debt_sustainability +
      0.16 * adaptation_finance +
      0.12 * insurance_availability +
      0.16 * public_investment_capacity +
      0.14 * household_protection +
      0.10 * climate_risk_disclosure,
      4
    ) AS public_finance_resilience_score,
    ROUND(
      0.18 * (1 - tax_capacity) +
      0.18 * (1 - debt_sustainability) +
      0.16 * (1 - public_investment_capacity) +
      0.14 * (1 - adaptation_finance) +
      0.12 * (1 - insurance_availability) +
      0.12 * (1 - household_protection) +
      0.10 * (1 - climate_risk_disclosure),
      4
    ) AS fiscal_climate_fragility_score
FROM public_finance_climate_records;
