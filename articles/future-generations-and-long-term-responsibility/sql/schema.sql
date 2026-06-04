-- Future Generations and Long-Term Responsibility schema.
-- SQLite compatible.

DROP VIEW IF EXISTS inheritance_record_scores;
DROP VIEW IF EXISTS long_term_risk_priority_scores;
DROP VIEW IF EXISTS intergenerational_strategy_scores;
DROP VIEW IF EXISTS future_generation_scenario_scores;
DROP VIEW IF EXISTS intergenerational_profile_scores;

DROP TABLE IF EXISTS adaptive_long_term_pathways;
DROP TABLE IF EXISTS inheritance_records;
DROP TABLE IF EXISTS long_term_risk_indicators;
DROP TABLE IF EXISTS intergenerational_strategy_options;
DROP TABLE IF EXISTS future_generation_scenarios;
DROP TABLE IF EXISTS intergenerational_responsibility_profiles;

CREATE TABLE intergenerational_responsibility_profiles (
    profile_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    climate_burden REAL,
    debt_without_assets REAL,
    infrastructure_decay REAL,
    ecological_damage REAL,
    institutional_capacity REAL,
    technological_lock_in REAL,
    adaptive_capacity REAL,
    future_representation REAL,
    reparative_continuity REAL,
    public_legitimacy REAL,
    description TEXT
);

CREATE TABLE future_generation_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    short_term_pressure REAL,
    climate_delay REAL,
    ecological_threshold_risk REAL,
    debt_transfer REAL,
    maintenance_deferral REAL,
    technology_lock_in REAL,
    institutional_fragility REAL,
    future_representation_gap REAL,
    reparative_gap REAL,
    adaptive_learning_capacity REAL,
    description TEXT
);

CREATE TABLE intergenerational_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    future_generation_review_gain REAL,
    climate_budgeting_gain REAL,
    maintenance_accounting_gain REAL,
    ecological_restoration_gain REAL,
    public_investment_gain REAL,
    youth_participation_gain REAL,
    technology_accountability_gain REAL,
    reparative_finance_gain REAL,
    adaptive_governance_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES intergenerational_responsibility_profiles(profile_id)
);

CREATE TABLE long_term_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    future_generation_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES future_generation_scenarios(scenario_id)
);

CREATE TABLE inheritance_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    inherited_burden REAL,
    future_freedom REAL,
    institutional_capacity REAL,
    ecological_damage REAL,
    adaptive_capacity REAL,
    future_representation REAL,
    reparative_continuity REAL,
    public_legitimacy REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES intergenerational_responsibility_profiles(profile_id)
);

CREATE TABLE adaptive_long_term_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    inherited_burden REAL,
    future_freedom REAL,
    institutional_capacity REAL,
    ecological_damage REAL,
    adaptive_capacity REAL,
    future_representation REAL,
    reparative_continuity REAL,
    public_legitimacy REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES intergenerational_responsibility_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES future_generation_scenarios(scenario_id)
);

CREATE VIEW intergenerational_profile_scores AS
SELECT
    profile_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * climate_burden +
      0.14 * debt_without_assets +
      0.16 * infrastructure_decay +
      0.18 * ecological_damage +
      0.14 * technological_lock_in +
      0.10 * (1 - institutional_capacity) +
      0.06 * (1 - adaptive_capacity) +
      0.04 * (1 - future_representation),
      4
    ) AS inherited_burden_score,
    ROUND(
      0.20 * institutional_capacity +
      0.20 * adaptive_capacity +
      0.16 * future_representation +
      0.14 * (1 - technological_lock_in) +
      0.12 * (1 - infrastructure_decay) +
      0.10 * (1 - ecological_damage) +
      0.05 * (1 - climate_burden) +
      0.03 * (1 - debt_without_assets),
      4
    ) AS future_freedom_score
FROM intergenerational_responsibility_profiles;

CREATE VIEW future_generation_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.13 * short_term_pressure +
      0.14 * climate_delay +
      0.14 * ecological_threshold_risk +
      0.11 * debt_transfer +
      0.12 * maintenance_deferral +
      0.11 * technology_lock_in +
      0.11 * institutional_fragility +
      0.07 * future_representation_gap +
      0.05 * reparative_gap +
      0.02 * (1 - adaptive_learning_capacity),
      4
    ) AS long_term_risk_score
FROM future_generation_scenarios;

CREATE VIEW intergenerational_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * future_generation_review_gain +
      0.13 * climate_budgeting_gain +
      0.12 * maintenance_accounting_gain +
      0.12 * ecological_restoration_gain +
      0.11 * public_investment_gain +
      0.10 * youth_participation_gain +
      0.10 * technology_accountability_gain +
      0.09 * reparative_finance_gain +
      0.07 * adaptive_governance_gain +
      0.02 * implementation_capacity +
      0.01 * public_legitimacy_gain,
      4
    ) AS intergenerational_strategy_value_score
FROM intergenerational_strategy_options;

CREATE VIEW long_term_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.16 * severity +
      0.15 * irreversibility +
      0.10 * visibility_gap +
      0.18 * distributional_harm +
      0.18 * future_generation_harm +
      0.09 * (1 - preparedness),
      4
    ) AS long_term_risk_priority_score
FROM long_term_risk_indicators;

CREATE VIEW inheritance_record_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    inherited_burden,
    future_freedom,
    ROUND(
      0.18 * future_freedom +
      0.18 * institutional_capacity +
      0.18 * adaptive_capacity +
      0.14 * future_representation +
      0.12 * reparative_continuity +
      0.10 * public_legitimacy -
      0.06 * inherited_burden -
      0.04 * ecological_damage,
      4
    ) AS stewardship_capacity_score
FROM inheritance_records;
