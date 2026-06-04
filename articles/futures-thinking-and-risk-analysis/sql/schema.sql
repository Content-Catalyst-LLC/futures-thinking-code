-- Futures Thinking and Risk Analysis schema.
-- SQLite compatible.

DROP VIEW IF EXISTS risk_governance_capacity_scores;
DROP VIEW IF EXISTS risk_indicator_priority_scores;
DROP VIEW IF EXISTS strategy_robustness_scores;
DROP VIEW IF EXISTS risk_scenario_scores;
DROP VIEW IF EXISTS risk_profile_scores;

DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS governance_records;
DROP TABLE IF EXISTS risk_indicators;
DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS risk_scenarios;
DROP TABLE IF EXISTS risk_profiles;

CREATE TABLE risk_profiles (
    profile_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    probability_confidence REAL,
    structural_uncertainty REAL,
    interdependence REAL,
    vulnerability REAL,
    resilience_capacity REAL,
    governance_capacity REAL,
    signal_visibility REAL,
    tail_risk_severity REAL,
    distributional_harm REAL,
    adaptive_capacity REAL,
    description TEXT
);

CREATE TABLE risk_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    model_uncertainty REAL,
    data_uncertainty REAL,
    nonstationarity REAL,
    cascade_potential REAL,
    tail_risk_pressure REAL,
    exposure_pressure REAL,
    vulnerability_pressure REAL,
    governance_stress REAL,
    legitimacy_stress REAL,
    early_warning_gap REAL,
    description TEXT
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    baseline_performance REAL,
    technology_disruption_performance REAL,
    climate_stress_performance REAL,
    geopolitical_fragmentation_performance REAL,
    financial_contagion_performance REAL,
    institutional_breakdown_performance REAL,
    systemic_cascade_performance REAL,
    monitoring_capacity REAL,
    adaptability REAL,
    implementation_capacity REAL,
    public_legitimacy REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES risk_profiles(profile_id)
);

CREATE TABLE risk_indicators (
    indicator_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    indicator_name TEXT,
    indicator_domain TEXT,
    signal_strength REAL,
    visibility_gap REAL,
    lead_time REAL,
    systemic_relevance REAL,
    cascade_potential REAL,
    tail_severity REAL,
    preparedness_gap REAL,
    distributional_harm REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES risk_scenarios(scenario_id)
);

CREATE TABLE governance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    record_type TEXT,
    monitoring_capacity REAL,
    scenario_refresh_capacity REAL,
    cross_sector_coordination REAL,
    public_legitimacy REAL,
    learning_capacity REAL,
    flexible_finance REAL,
    accountability_capacity REAL,
    distributional_review_capacity REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES risk_profiles(profile_id)
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    initial_preparedness REAL,
    monitoring_capacity REAL,
    trigger_sensitivity REAL,
    learning_capacity REAL,
    governance_capacity REAL,
    resilience_capacity REAL,
    vulnerability_pressure REAL,
    cascade_pressure REAL,
    tail_pressure REAL,
    public_legitimacy REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES risk_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES risk_scenarios(scenario_id)
);

CREATE VIEW risk_profile_scores AS
SELECT
    profile_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * (1 - probability_confidence) +
      0.16 * structural_uncertainty +
      0.14 * interdependence +
      0.15 * vulnerability -
      0.11 * resilience_capacity -
      0.10 * governance_capacity -
      0.08 * signal_visibility +
      0.12 * tail_risk_severity +
      0.10 * distributional_harm -
      0.02 * adaptive_capacity,
      4
    ) AS futures_risk_profile_score,
    ROUND(
      0.18 * (1 - resilience_capacity) +
      0.18 * (1 - governance_capacity) +
      0.15 * (1 - signal_visibility) +
      0.15 * structural_uncertainty +
      0.12 * vulnerability +
      0.10 * tail_risk_severity +
      0.08 * distributional_harm +
      0.04 * (1 - adaptive_capacity),
      4
    ) AS preparedness_gap_score
FROM risk_profiles;

CREATE VIEW risk_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.12 * model_uncertainty +
      0.09 * data_uncertainty +
      0.13 * nonstationarity +
      0.15 * cascade_potential +
      0.12 * tail_risk_pressure +
      0.10 * exposure_pressure +
      0.10 * vulnerability_pressure +
      0.08 * governance_stress +
      0.06 * legitimacy_stress +
      0.05 * early_warning_gap,
      4
    ) AS systemic_risk_stress_score
FROM risk_scenarios;

CREATE VIEW strategy_robustness_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      (baseline_performance + technology_disruption_performance + climate_stress_performance + geopolitical_fragmentation_performance + financial_contagion_performance + institutional_breakdown_performance + systemic_cascade_performance) / 7.0,
      4
    ) AS mean_performance,
    ROUND(
      MIN(
        baseline_performance,
        technology_disruption_performance,
        climate_stress_performance,
        geopolitical_fragmentation_performance,
        financial_contagion_performance,
        institutional_breakdown_performance,
        systemic_cascade_performance
      ),
      4
    ) AS worst_case,
    ROUND(
      0.30 * monitoring_capacity +
      0.30 * adaptability +
      0.20 * implementation_capacity +
      0.20 * public_legitimacy,
      4
    ) AS governance_quality,
    ROUND(
      0.42 * MIN(
        baseline_performance,
        technology_disruption_performance,
        climate_stress_performance,
        geopolitical_fragmentation_performance,
        financial_contagion_performance,
        institutional_breakdown_performance,
        systemic_cascade_performance
      ) +
      0.28 * ((baseline_performance + technology_disruption_performance + climate_stress_performance + geopolitical_fragmentation_performance + financial_contagion_performance + institutional_breakdown_performance + systemic_cascade_performance) / 7.0) +
      0.10 * (0.30 * monitoring_capacity + 0.30 * adaptability + 0.20 * implementation_capacity + 0.20 * public_legitimacy),
      4
    ) AS robustness_without_regret_adjustment
FROM strategy_options;

CREATE VIEW risk_indicator_priority_scores AS
SELECT
    indicator_id,
    scenario_id,
    indicator_name,
    indicator_domain,
    ROUND(
      0.13 * signal_strength +
      0.11 * visibility_gap +
      0.09 * (1 - lead_time) +
      0.15 * systemic_relevance +
      0.16 * cascade_potential +
      0.15 * tail_severity +
      0.11 * preparedness_gap +
      0.10 * distributional_harm,
      4
    ) AS risk_indicator_priority_score,
    preparedness_gap,
    distributional_harm
FROM risk_indicators;

CREATE VIEW risk_governance_capacity_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    record_type,
    ROUND(
      0.15 * monitoring_capacity +
      0.14 * scenario_refresh_capacity +
      0.14 * cross_sector_coordination +
      0.13 * public_legitimacy +
      0.14 * learning_capacity +
      0.10 * flexible_finance +
      0.10 * accountability_capacity +
      0.10 * distributional_review_capacity,
      4
    ) AS risk_governance_capacity_score,
    ROUND(
      0.16 * (1 - public_legitimacy) +
      0.15 * (1 - accountability_capacity) +
      0.14 * (1 - distributional_review_capacity) +
      0.13 * (1 - cross_sector_coordination) +
      0.12 * (1 - monitoring_capacity) +
      0.11 * (1 - scenario_refresh_capacity) +
      0.10 * (1 - learning_capacity) +
      0.09 * (1 - flexible_finance),
      4
    ) AS legitimacy_gap_score
FROM governance_records;
