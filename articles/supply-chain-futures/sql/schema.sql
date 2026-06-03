-- Supply Chain Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS procurement_circularity_scores;
DROP VIEW IF EXISTS chokepoint_priority_scores;
DROP VIEW IF EXISTS resilience_strategy_scores;
DROP VIEW IF EXISTS supply_chain_scenario_scores;
DROP VIEW IF EXISTS supply_chain_profile_scores;

DROP TABLE IF EXISTS disruption_pathways;
DROP TABLE IF EXISTS procurement_circularity_records;
DROP TABLE IF EXISTS chokepoint_risk_register;
DROP TABLE IF EXISTS resilience_strategies;
DROP TABLE IF EXISTS supply_chain_scenarios;
DROP TABLE IF EXISTS supply_chain_profiles;

CREATE TABLE supply_chain_profiles (
    profile_id TEXT PRIMARY KEY,
    supply_chain_name TEXT NOT NULL,
    supply_chain_type TEXT,
    cost_efficiency REAL,
    supplier_diversification REAL,
    inventory_buffer REAL,
    supply_visibility REAL,
    labor_accountability REAL,
    climate_adaptation REAL,
    digital_traceability REAL,
    circularity REAL,
    regulatory_readiness REAL,
    recovery_capacity REAL,
    description TEXT
);

CREATE TABLE supply_chain_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    trade_fragmentation REAL,
    climate_disruption REAL,
    technology_acceleration REAL,
    critical_minerals_pressure REAL,
    labor_stress REAL,
    transport_chokepoint_pressure REAL,
    regulatory_pressure REAL,
    demand_volatility REAL,
    description TEXT
);

CREATE TABLE resilience_strategies (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    supplier_diversification_gain REAL,
    buffer_gain REAL,
    visibility_gain REAL,
    labor_accountability_gain REAL,
    climate_adaptation_gain REAL,
    circularity_gain REAL,
    implementation_capacity REAL,
    cost_burden REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES supply_chain_profiles(profile_id)
);

CREATE TABLE chokepoint_risk_register (
    chokepoint_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    chokepoint_name TEXT,
    chokepoint_type TEXT,
    dependency_concentration REAL,
    substitution_difficulty REAL,
    disruption_probability REAL,
    systemic_reach REAL,
    recovery_difficulty REAL,
    visibility_gap REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES supply_chain_scenarios(scenario_id)
);

CREATE TABLE procurement_circularity_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    public_value REAL,
    resilience_support REAL,
    labor_standard_strength REAL,
    environmental_performance REAL,
    traceability_quality REAL,
    circular_material_capacity REAL,
    implementation_readiness REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES supply_chain_profiles(profile_id)
);

CREATE TABLE disruption_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    cost_efficiency REAL,
    diversification REAL,
    buffer REAL,
    visibility REAL,
    labor_accountability REAL,
    climate_adaptation REAL,
    traceability REAL,
    recovery_capacity REAL,
    initial_viability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES supply_chain_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES supply_chain_scenarios(scenario_id)
);

CREATE VIEW supply_chain_profile_scores AS
SELECT
    profile_id,
    supply_chain_name,
    supply_chain_type,
    ROUND(
      0.10 * cost_efficiency +
      0.16 * supplier_diversification +
      0.14 * inventory_buffer +
      0.14 * supply_visibility +
      0.12 * labor_accountability +
      0.13 * climate_adaptation +
      0.09 * digital_traceability +
      0.06 * circularity +
      0.04 * regulatory_readiness +
      0.02 * recovery_capacity,
      4
    ) AS supply_chain_resilience_score,
    ROUND(
      0.16 * (1 - supplier_diversification) +
      0.16 * (1 - inventory_buffer) +
      0.14 * (1 - supply_visibility) +
      0.14 * (1 - climate_adaptation) +
      0.12 * (1 - labor_accountability) +
      0.10 * (1 - recovery_capacity) +
      0.08 * (1 - regulatory_readiness) +
      0.06 * (1 - digital_traceability) +
      0.04 * (1 - circularity),
      4
    ) AS supply_chain_fragility_score
FROM supply_chain_profiles;

CREATE VIEW supply_chain_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.16 * trade_fragmentation +
      0.18 * climate_disruption +
      0.14 * critical_minerals_pressure +
      0.12 * labor_stress +
      0.14 * transport_chokepoint_pressure +
      0.10 * regulatory_pressure +
      0.10 * demand_volatility +
      0.06 * technology_acceleration,
      4
    ) AS disruption_pressure_score,
    ROUND(
      0.16 * technology_acceleration +
      0.16 * regulatory_pressure +
      0.14 * climate_disruption +
      0.14 * critical_minerals_pressure +
      0.12 * demand_volatility +
      0.10 * trade_fragmentation +
      0.10 * labor_stress +
      0.08 * transport_chokepoint_pressure,
      4
    ) AS adaptation_opportunity_score
FROM supply_chain_scenarios;

CREATE VIEW resilience_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.18 * supplier_diversification_gain +
      0.16 * buffer_gain +
      0.16 * visibility_gain +
      0.14 * labor_accountability_gain +
      0.16 * climate_adaptation_gain +
      0.10 * circularity_gain +
      0.10 * implementation_capacity -
      0.10 * cost_burden,
      4
    ) AS resilience_gain_score,
    ROUND(
      0.28 * (1 - implementation_capacity) +
      0.18 * cost_burden +
      0.10 * (1 - supplier_diversification_gain) +
      0.10 * (1 - buffer_gain) +
      0.10 * (1 - visibility_gain) +
      0.10 * (1 - labor_accountability_gain) +
      0.08 * (1 - climate_adaptation_gain) +
      0.06 * (1 - circularity_gain),
      4
    ) AS implementation_risk_score
FROM resilience_strategies;

CREATE VIEW chokepoint_priority_scores AS
SELECT
    chokepoint_id,
    scenario_id,
    chokepoint_name,
    chokepoint_type,
    ROUND(
      0.18 * dependency_concentration +
      0.17 * substitution_difficulty +
      0.16 * disruption_probability +
      0.18 * systemic_reach +
      0.17 * recovery_difficulty +
      0.14 * visibility_gap,
      4
    ) AS chokepoint_priority_score,
    visibility_gap
FROM chokepoint_risk_register;

CREATE VIEW procurement_circularity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.18 * public_value +
      0.18 * resilience_support +
      0.14 * labor_standard_strength +
      0.14 * environmental_performance +
      0.14 * traceability_quality +
      0.12 * circular_material_capacity +
      0.10 * implementation_readiness,
      4
    ) AS public_interest_supply_governance_score,
    implementation_readiness
FROM procurement_circularity_records;
