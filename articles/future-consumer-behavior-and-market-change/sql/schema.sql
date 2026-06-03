-- Future Consumer Behavior and Market Change schema.
-- SQLite compatible.

DROP VIEW IF EXISTS regulatory_market_scores;
DROP VIEW IF EXISTS vulnerability_priority_scores;
DROP VIEW IF EXISTS consumer_strategy_option_scores;
DROP VIEW IF EXISTS market_scenario_scores;
DROP VIEW IF EXISTS consumer_future_profile_scores;

DROP TABLE IF EXISTS adoption_pathways;
DROP TABLE IF EXISTS regulatory_market_records;
DROP TABLE IF EXISTS vulnerability_indicators;
DROP TABLE IF EXISTS consumer_strategy_options;
DROP TABLE IF EXISTS market_scenarios;
DROP TABLE IF EXISTS consumer_future_profiles;

CREATE TABLE consumer_future_profiles (
    profile_id TEXT PRIMARY KEY,
    consumer_future_name TEXT NOT NULL,
    consumer_future_type TEXT,
    affordability REAL,
    trust REAL,
    digital_dependence REAL,
    sustainability_demand REAL,
    access_inclusion REAL,
    price_sensitivity REAL,
    behavioral_friction REAL,
    regulatory_pressure REAL,
    privacy_confidence REAL,
    local_resilience REAL,
    description TEXT
);

CREATE TABLE market_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    cost_pressure REAL,
    trust_pressure REAL,
    technology_acceleration REAL,
    platform_concentration REAL,
    privacy_regulation REAL,
    sustainability_pressure REAL,
    access_gap REAL,
    consumer_protection_strength REAL,
    description TEXT
);

CREATE TABLE consumer_strategy_options (
    option_id TEXT PRIMARY KEY,
    profile_id TEXT,
    option_name TEXT,
    option_type TEXT,
    affordability_support REAL,
    trust_building REAL,
    privacy_protection REAL,
    access_inclusion REAL,
    sustainability_credibility REAL,
    behavioral_integrity REAL,
    implementation_capacity REAL,
    market_scalability REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES consumer_future_profiles(profile_id)
);

CREATE TABLE vulnerability_indicators (
    indicator_id TEXT PRIMARY KEY,
    profile_id TEXT,
    indicator_name TEXT,
    indicator_domain TEXT,
    budget_pressure REAL,
    information_asymmetry REAL,
    digital_exclusion REAL,
    behavioral_manipulation REAL,
    lack_of_alternatives REAL,
    remedy_access REAL,
    consumer_protection REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES consumer_future_profiles(profile_id)
);

CREATE TABLE regulatory_market_records (
    record_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    regulatory_domain TEXT,
    privacy_rules REAL,
    pricing_transparency REAL,
    subscription_fairness REAL,
    accessibility_enforcement REAL,
    green_claims_enforcement REAL,
    platform_accountability REAL,
    consumer_remedy_strength REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES market_scenarios(scenario_id)
);

CREATE TABLE adoption_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    affordability REAL,
    trust REAL,
    access_index REAL,
    platform_visibility REAL,
    sustainability_demand REAL,
    social_influence REAL,
    behavioral_friction REAL,
    price_sensitivity REAL,
    initial_adoption REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES consumer_future_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES market_scenarios(scenario_id)
);

CREATE VIEW consumer_future_profile_scores AS
SELECT
    profile_id,
    consumer_future_name,
    consumer_future_type,
    ROUND(
      0.14 * affordability +
      0.16 * trust +
      0.10 * sustainability_demand +
      0.16 * access_inclusion +
      0.10 * (1 - price_sensitivity) +
      0.12 * (1 - behavioral_friction) +
      0.06 * digital_dependence +
      0.06 * regulatory_pressure +
      0.06 * privacy_confidence +
      0.04 * local_resilience,
      4
    ) AS consumer_future_health_score,
    ROUND(
      0.16 * price_sensitivity +
      0.16 * behavioral_friction +
      0.14 * (1 - trust) +
      0.12 * (1 - access_inclusion) +
      0.10 * (1 - affordability) +
      0.10 * digital_dependence +
      0.08 * (1 - privacy_confidence) +
      0.08 * (1 - local_resilience) +
      0.06 * regulatory_pressure,
      4
    ) AS market_fragility_score
FROM consumer_future_profiles;

CREATE VIEW market_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * cost_pressure +
      0.16 * trust_pressure +
      0.14 * technology_acceleration +
      0.14 * platform_concentration +
      0.12 * sustainability_pressure +
      0.10 * access_gap +
      0.10 * privacy_regulation +
      0.08 * (1 - consumer_protection_strength),
      4
    ) AS market_transition_pressure_score,
    ROUND(
      0.22 * consumer_protection_strength +
      0.18 * privacy_regulation +
      0.14 * sustainability_pressure +
      0.12 * (1 - access_gap) +
      0.10 * (1 - trust_pressure) +
      0.10 * (1 - cost_pressure) +
      0.08 * (1 - platform_concentration) +
      0.06 * technology_acceleration,
      4
    ) AS consumer_protection_opportunity_score
FROM market_scenarios;

CREATE VIEW consumer_strategy_option_scores AS
SELECT
    option_id,
    profile_id,
    option_name,
    option_type,
    ROUND(
      0.16 * affordability_support +
      0.16 * trust_building +
      0.14 * privacy_protection +
      0.14 * access_inclusion +
      0.14 * sustainability_credibility +
      0.14 * behavioral_integrity +
      0.06 * implementation_capacity +
      0.06 * market_scalability,
      4
    ) AS consumer_support_strategy_score,
    ROUND(
      0.25 * (1 - implementation_capacity) +
      0.15 * (1 - market_scalability) +
      0.12 * (1 - trust_building) +
      0.12 * (1 - behavioral_integrity) +
      0.10 * (1 - privacy_protection) +
      0.10 * (1 - access_inclusion) +
      0.08 * (1 - affordability_support) +
      0.08 * (1 - sustainability_credibility),
      4
    ) AS implementation_risk_score
FROM consumer_strategy_options;

CREATE VIEW vulnerability_priority_scores AS
SELECT
    indicator_id,
    profile_id,
    indicator_name,
    indicator_domain,
    ROUND(
      0.18 * budget_pressure +
      0.16 * information_asymmetry +
      0.14 * digital_exclusion +
      0.18 * behavioral_manipulation +
      0.14 * lack_of_alternatives +
      0.10 * (1 - remedy_access) +
      0.10 * (1 - consumer_protection),
      4
    ) AS consumer_vulnerability_priority_score,
    remedy_access,
    consumer_protection
FROM vulnerability_indicators;

CREATE VIEW regulatory_market_scores AS
SELECT
    record_id,
    scenario_id,
    regulatory_domain,
    ROUND(
      0.16 * privacy_rules +
      0.14 * pricing_transparency +
      0.14 * subscription_fairness +
      0.14 * accessibility_enforcement +
      0.14 * green_claims_enforcement +
      0.14 * platform_accountability +
      0.14 * consumer_remedy_strength,
      4
    ) AS public_interest_market_governance_score,
    consumer_remedy_strength
FROM regulatory_market_records;
