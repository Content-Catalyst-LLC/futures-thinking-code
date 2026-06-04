-- Security Futures and Hybrid Risk schema.
-- SQLite compatible.

DROP VIEW IF EXISTS infrastructure_cascade_scores;
DROP VIEW IF EXISTS hybrid_risk_priority_scores;
DROP VIEW IF EXISTS security_strategy_scores;
DROP VIEW IF EXISTS security_scenario_scores;
DROP VIEW IF EXISTS security_profile_scores;

DROP TABLE IF EXISTS adaptive_security_pathways;
DROP TABLE IF EXISTS infrastructure_dependencies;
DROP TABLE IF EXISTS security_risk_indicators;
DROP TABLE IF EXISTS security_strategy_options;
DROP TABLE IF EXISTS security_scenarios;
DROP TABLE IF EXISTS security_profiles;

CREATE TABLE security_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    future_type TEXT,
    cyber_exposure REAL,
    infrastructure_dependence REAL,
    information_vulnerability REAL,
    climate_security_stress REAL,
    resource_dependence REAL,
    institutional_coordination REAL,
    civilian_protection REAL,
    adaptive_resilience REAL,
    public_trust REAL,
    attribution_clarity REAL,
    description TEXT
);

CREATE TABLE security_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    cyber_shock REAL,
    infrastructure_shock REAL,
    information_shock REAL,
    climate_shock REAL,
    resource_shock REAL,
    migration_pressure REAL,
    security_escalation REAL,
    institutional_fragmentation REAL,
    private_infrastructure_dependency REAL,
    civilian_harm_pressure REAL,
    description TEXT
);

CREATE TABLE security_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    cyber_resilience_gain REAL,
    infrastructure_redundancy_gain REAL,
    information_integrity_gain REAL,
    climate_security_adaptation_gain REAL,
    resource_security_gain REAL,
    institutional_coordination_gain REAL,
    civilian_protection_gain REAL,
    deterrence_gain REAL,
    adaptive_learning_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES security_profiles(profile_id)
);

CREATE TABLE security_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    cascade_potential REAL,
    visibility_gap REAL,
    recovery_difficulty REAL,
    distributional_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES security_scenarios(scenario_id)
);

CREATE TABLE infrastructure_dependencies (
    dependency_id TEXT PRIMARY KEY,
    source_system TEXT,
    target_system TEXT,
    dependency_weight REAL,
    disruption_sensitivity REAL,
    recovery_capacity REAL,
    public_harm_potential REAL,
    private_operator_dependency REAL,
    description TEXT
);

CREATE TABLE adaptive_security_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    initial_resilience REAL,
    cyber_exposure REAL,
    infrastructure_dependence REAL,
    information_vulnerability REAL,
    climate_security_stress REAL,
    resource_dependence REAL,
    institutional_coordination REAL,
    civilian_protection REAL,
    adaptive_resilience REAL,
    public_trust REAL,
    system_stress REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES security_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES security_scenarios(scenario_id)
);

CREATE VIEW security_profile_scores AS
SELECT
    profile_id,
    future_name,
    future_type,
    ROUND(
      0.13 * cyber_exposure +
      0.13 * infrastructure_dependence +
      0.13 * information_vulnerability +
      0.12 * climate_security_stress +
      0.10 * resource_dependence +
      0.11 * (1 - institutional_coordination) +
      0.10 * (1 - civilian_protection) +
      0.10 * (1 - adaptive_resilience) +
      0.05 * (1 - public_trust) +
      0.03 * (1 - attribution_clarity),
      4
    ) AS hybrid_risk_score,
    ROUND(
      0.20 * institutional_coordination +
      0.22 * civilian_protection +
      0.22 * adaptive_resilience +
      0.16 * public_trust +
      0.08 * attribution_clarity +
      0.04 * (1 - cyber_exposure) +
      0.04 * (1 - information_vulnerability) +
      0.04 * (1 - infrastructure_dependence),
      4
    ) AS security_resilience_score
FROM security_profiles;

CREATE VIEW security_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.13 * cyber_shock +
      0.13 * infrastructure_shock +
      0.12 * information_shock +
      0.12 * climate_shock +
      0.10 * resource_shock +
      0.08 * migration_pressure +
      0.10 * security_escalation +
      0.09 * institutional_fragmentation +
      0.06 * private_infrastructure_dependency +
      0.07 * civilian_harm_pressure,
      4
    ) AS hybrid_security_stress_score
FROM security_scenarios;

CREATE VIEW security_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.12 * cyber_resilience_gain +
      0.12 * infrastructure_redundancy_gain +
      0.12 * information_integrity_gain +
      0.10 * climate_security_adaptation_gain +
      0.09 * resource_security_gain +
      0.12 * institutional_coordination_gain +
      0.12 * civilian_protection_gain +
      0.07 * deterrence_gain +
      0.08 * adaptive_learning_gain +
      0.03 * implementation_capacity +
      0.03 * public_legitimacy_gain,
      4
    ) AS security_strategy_value_score
FROM security_strategy_options;

CREATE VIEW hybrid_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.18 * severity +
      0.18 * cascade_potential +
      0.10 * visibility_gap +
      0.13 * recovery_difficulty +
      0.17 * distributional_harm +
      0.10 * (1 - preparedness),
      4
    ) AS hybrid_risk_priority_score,
    distributional_harm,
    preparedness
FROM security_risk_indicators;

CREATE VIEW infrastructure_cascade_scores AS
SELECT
    dependency_id,
    source_system,
    target_system,
    ROUND(
      dependency_weight *
      disruption_sensitivity *
      public_harm_potential *
      (1 - recovery_capacity),
      4
    ) AS cascade_exposure_score,
    ROUND(
      0.40 * private_operator_dependency +
      0.30 * public_harm_potential +
      0.20 * disruption_sensitivity +
      0.10 * (1 - recovery_capacity),
      4
    ) AS public_private_risk_score
FROM infrastructure_dependencies;
